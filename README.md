# Manual LLM Provider

A development skill for adding **resumable, auditable, copy-paste LLM workflows** to existing applications.

[繁體中文](README.zh-TW.md) · [Skill instructions](skills/manual-llm-provider/SKILL.md) · [MIT license](LICENSE)

Let users bring their own chat interface:

```text
Prepare prompt -> User runs it in an external AI chat -> Import response
-> Save and validate candidate -> User accepts or rejects -> Continue
```

The manual generation transport needs no model API key. It preserves the application's prompt builder, source revisions, validators, checkpoints, and final review path.

## What you get

This is a **skill for coding agents**: instructions and references for implementing or reviewing a manual provider. Your project supplies its runtime, storage, UI or CLI, and domain-specific validation. Installing the skill alone does not add a provider to an application.

Use it for translation batches, document sections, story scenes, structured-output jobs, or other existing generation units. It does not require a framework, database, or fixed task count. It does not automate external chat sites or verify which model a user actually used.

## Install or try it

The installable folder is [`skills/manual-llm-provider`](skills/manual-llm-provider).

In Codex, when `$skill-installer` is available, ask:

```text
Use $skill-installer to install the skill from
https://github.com/Kevin-NM/manual-llm-provider/tree/main/skills/manual-llm-provider
```

If your environment uses a managed or shared skill library, follow its installation workflow and preserve existing entries. Do not overwrite a skill with the same name. Codex's [official skill documentation](https://learn.chatgpt.com/docs/build-skills) describes installation and discovery, including repository `.agents/skills` and user `~/.agents/skills` locations.

To evaluate without installing, ask a coding agent to read `skills/manual-llm-provider/SKILL.md` and apply it to a specific development task. This does not activate a global skill or modify configuration.

`agents/openai.yaml` supplies optional Codex UI metadata. Other hosts may read the core Markdown instructions, but their installation, discovery, and invocation behavior must be checked separately.

## Example request

```text
Use $manual-llm-provider to add a manual LLM option to this existing
translation app. Reuse its prompt builder, SQLite jobs, validators,
and final review flow.

Users should copy prompts into an external chat, paste back translations,
and resume after restarting the app. Only accepted translations may feed
the next section. Keep existing HTTP providers working.

First inspect the real code and propose the smallest compatible change.
Do not publish or commit without my instruction.
```

For a review, specify the existing manual provider, its persistence mechanism, and the behaviors you want checked.

## Design principles

- **Same effective inputs:** reuse approved context and the prompt builder; record exact snapshots, hashes, and source-selection differences.
- **Explicit manual transport:** no generation API dispatch, silent fallback, fabricated token usage, or HTTP-delivery claims. Model names remain self-reported labels.
- **Candidates before application:** preserve imported output before validation; distinguish deterministic checks, semantic review, and human acceptance.
- **Accepted dependencies only:** rebuild downstream prompts from accepted results. Upstream edits invalidate dependent prompts and derived acceptances.
- **Durable progress:** retain attempts and candidates, guard competing updates, and recover interrupted validation, preparation, or final writes.
- **Existing final review:** task acceptance does not silently publish content or approve application-wide facts.

Read the [durable task contract](skills/manual-llm-provider/references/task-contract.md) for storage and recovery, and select tests from the [acceptance scenarios](skills/manual-llm-provider/references/acceptance.md).

## Repository layout

```text
skills/manual-llm-provider/
  SKILL.md
  agents/openai.yaml
  references/task-contract.md
  references/acceptance.md
scripts/validate_skill.py
tests/
requirements-dev.txt
```

## Development checks

With Python 3.10 or newer, run from the repository root:

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py
python -m unittest discover -s tests -v
```

These checks validate the skill package and its tooling. They do not execute a generated application or prove external-model quality. A synthetic translation-app planning exercise has also been used to evaluate the guidance; each adopting project still needs runtime integration tests.

## Trust and limitations

Review a skill before installing or executing its instructions. This package includes no model credentials, NGSE runtime code, real run prompts, or private story data. The design was extracted from a manual-provider implementation in NGSE and generalized for other applications.

A combined chat prompt is an ordinary user message; copied role guidance does not gain real System authority. Credential detection is a safeguard, not proof that arbitrary text is safe to export. If a separately configured semantic reviewer calls an API, that use must be authorized and disclosed; a fully API-free workflow keeps unresolved semantics pending human review.

## Contributing

Open an issue or pull request with a concrete use case or reproducible failure. Keep guidance focused on reusable integration decisions, preserve existing application behavior, and include verification appropriate to the change. Use synthetic fixtures; do not include secrets or private user content.

## License

[MIT](LICENSE), copyright © 2026 Kevin-NM. This covers this repository's contents and does not change the licensing of NGSE or an application that adopts the skill.
