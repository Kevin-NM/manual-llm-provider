"""Publication validation boundaries using synthetic temporary skills."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_skill import SkillError, validate


class ValidateSkillTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.skill = Path(self.folder.name) / 'sample-skill'
        self.skill.mkdir()
        self.manifest = self.skill / 'SKILL.md'
        self.original = '---\nname: sample-skill\ndescription: "Sample skill for a synthetic publication test."\n---\n\n# 範例\n\nKeep approved facts.\n'
        self.manifest.write_text(self.original, encoding='utf-8')

    def test_valid_utf8_skill_and_reference(self):
        reference = self.skill / 'references' / 'contract.md'
        reference.parent.mkdir()
        reference.write_text('保留資料與來源。\n', encoding='utf-8')
        self.manifest.write_text(self.original + '[Contract](references/contract.md)\n', encoding='utf-8')
        self.assertEqual(validate(self.skill)['markdown_files'], 2)

    def test_missing_reference_is_not_publishable(self):
        self.manifest.write_text(self.original + '[Missing](references/missing.md)\n', encoding='utf-8')
        with self.assertRaisesRegex(SkillError, 'Missing local reference'):
            validate(self.skill)

    def test_existing_reference_cannot_escape_the_skill(self):
        (self.skill.parent / 'private.md').write_text('synthetic', encoding='utf-8')
        self.manifest.write_text(self.original + '[Private](../private.md)\n', encoding='utf-8')
        with self.assertRaisesRegex(SkillError, 'escapes'):
            validate(self.skill)

    def test_malformed_frontmatter_is_rejected(self):
        self.manifest.write_text('---\nname: [\n---\nbody', encoding='utf-8')
        with self.assertRaisesRegex(SkillError, 'YAML'):
            validate(self.skill)

    def test_ui_prompt_cannot_invoke_a_different_skill(self):
        agents = self.skill / 'agents'
        agents.mkdir()
        (agents / 'openai.yaml').write_text('interface:\n  short_description: "A descriptive test skill label for users"\n  default_prompt: "Use $wrong-name"\n', encoding='utf-8')
        with self.assertRaisesRegex(SkillError, 'must name the skill'):
            validate(self.skill)

    def test_known_secret_shape_is_rejected(self):
        self.manifest.write_text(self.original + 'ghp_' + 'synthetic' * 5, encoding='utf-8')
        with self.assertRaisesRegex(SkillError, 'Possible secret'):
            validate(self.skill)

    def test_ui_prompt_cannot_only_match_a_different_skill_prefix(self):
        agents = self.skill / 'agents'
        agents.mkdir()
        (agents / 'openai.yaml').write_text('interface:\n  short_description: "A descriptive test skill label for users"\n  default_prompt: "Use $sample-skill-extra"\n', encoding='utf-8')
        with self.assertRaisesRegex(SkillError, 'must name the skill'):
            validate(self.skill)

    def test_cli_returns_failure_for_an_incomplete_package(self):
        command = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_skill.py'
        result = subprocess.run([sys.executable, str(command), str(self.skill / 'missing')],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 1)
        self.assertIn('SKILL.md is missing', result.stderr)


if __name__ == '__main__':
    unittest.main()
