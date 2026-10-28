"""Validate the published skill's metadata, local references, and text boundaries.

No network calls or target-application code execution. This is not a complete
secret audit and does not validate implementations produced using the skill.
"""
import argparse
from pathlib import Path
import re
import sys

import yaml


class SkillError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise SkillError(message)


def validate(skill):
    skill = Path(skill).resolve()
    manifest = skill / 'SKILL.md'
    require(manifest.is_file(), 'SKILL.md is missing')
    text = manifest.read_text(encoding='utf-8')
    front = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    require(front is not None, 'SKILL.md must begin with YAML frontmatter')
    try:
        header = yaml.safe_load(front.group(1))
    except yaml.YAMLError as exc:
        raise SkillError('Invalid frontmatter YAML') from exc
    require(isinstance(header, dict), 'Frontmatter must be a mapping')
    name = header.get('name')
    require(isinstance(name, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)
            and len(name) <= 64, 'Invalid skill name')
    require(name == skill.name, 'Skill name must match its folder')
    description = header.get('description')
    require(isinstance(description, str) and 0 < len(description.strip()) <= 1024,
            'Description is missing or too long')
    require('<' not in description and '>' not in description, 'Description contains angle brackets')
    require(bool(text[front.end():].strip()), 'Skill body is empty')

    metadata = skill / 'agents' / 'openai.yaml'
    if metadata.is_file():
        try:
            config = yaml.safe_load(metadata.read_text(encoding='utf-8'))
        except yaml.YAMLError as exc:
            raise SkillError('Invalid agents/openai.yaml') from exc
        require(isinstance(config, dict), 'UI metadata must be a mapping')
        interface = config.get('interface')
        require(isinstance(interface, dict), 'UI interface must be a mapping')
        short = interface.get('short_description')
        require(isinstance(short, str) and 25 <= len(short) <= 64, 'UI short description must be 25-64 characters')
        default = interface.get('default_prompt')
        require(isinstance(default, str) and re.search(r'\$' + re.escape(name) + r'(?![a-z0-9-])', default),
                'UI default prompt must name the skill')

    markdown_count = 0
    for path in sorted(skill.rglob('*')):
        require(not path.is_symlink() and path.resolve().is_relative_to(skill),
                'Skill resources must stay inside the skill folder')
        if not path.is_file() or path.suffix not in {'.md', '.yaml', '.yml'}:
            continue
        content = path.read_text(encoding='utf-8')
        require('[TODO:' not in content, 'Unfinished scaffold in ' + path.name)
        require(not re.search(r'\bgh[pousr]_[A-Za-z0-9]{20,}|(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}|-----BEGIN [^-]*PRIVATE KEY-----', content),
                'Possible secret literal in ' + path.name)
        require(not re.search(r'[A-Za-z]:[\\/](?:Users|Codex)[\\/]|/Users/[^/]+/|/home/[^/]+/', content),
                'Local user path in ' + path.name)
        if path.suffix != '.md':
            continue
        markdown_count += 1
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if target.startswith(('https://', 'http://', '#', 'mailto:')):
                continue
            filename = target.split('#', 1)[0]
            referenced = (path.parent / filename).resolve()
            require(referenced.is_relative_to(skill), 'Reference escapes the skill folder')
            require(referenced.is_file(), 'Missing local reference: ' + filename)
    return {'name': name, 'markdown_files': markdown_count}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'skills' / 'manual-llm-provider')
    args = parser.parse_args(argv)
    try:
        result = validate(args.skill)
    except (SkillError, OSError, UnicodeError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        return 1
    print(f"PASS: {result['name']} (metadata and {result['markdown_files']} Markdown files)")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
