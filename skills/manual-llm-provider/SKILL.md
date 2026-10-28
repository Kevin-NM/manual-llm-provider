---
name: manual-llm-provider
license: MIT
description: "Add or review a manual LLM provider in an existing application: users export a prompt, run it in an external chat, and import results through durable tasks and the application's existing validation and approval flow. Use for copy-paste, bring-your-own-chat, or no-API-key model workflows; not for ordinary prompt writing or operating a chat service."
---

# Manual Llm Provider

Implement a human-operated model transport without creating a second, incompatible application workflow. This skill supplies development guidance, not a running provider, hosted service, or external-chat automation.

## Locate the integration seam

Inspect the actual provider adapter, prompt builder, source/version tracking, validators, approval/write path, persistence, and resume mechanism. Reuse those components. Report missing capabilities rather than inventing a semantic reviewer or a checkpoint system.

Choose the smallest useful task unit for the product: a scene, document section, translation batch, code-generation request, or another existing unit. Do not impose a fixed number of tasks, a framework, a database, or a genre. Resolve whether the requested scope covers text generation only or also structured-output operations; expose unsupported operations explicitly.

For an existing provider implementation, preserve its configured defaults and HTTP behavior. Make the manual discriminator explicit and backward compatible. A manual model name is a self-reported label, never a verified model identity.

## Preserve these transport invariants

- Build prompts from the same effective, approved inputs as the existing provider. Freeze the exact exportable snapshot, source versions, prompt hash, and relevant task context. Keep audit provenance separate from model-facing context where the application already does so. Explain any context selection or omission; do not silently remove approved constraints to fit a limit.
- Offer separate role prompts when useful and a single-message chat export. Clearly label role guidance in the latter as user-provided instructions, without claiming actual System authority in another service.
- The manual generation transport must not enter HTTP dispatch, fallback to another provider, require a secret, record delivery, or fabricate token usage. Guard shared transport entry points, including unsupported operations, before a client is created.
- Persist tasks and submitted output server-side or in the application's durable store. Browser storage can help preserve unsent edits, but is not the authoritative task record.
- Bind a submission to its run, unit, attempt, prompt snapshot, and source revision. Save it as a candidate before validation; never directly apply pasted text to authoritative output.
- Reuse deterministic validators and, for structured requests, the existing schema/parser and output constraints. Reuse a semantic reviewer only if it exists, is available, and its use is authorized for this workflow; disclose any separate review API calls. If the requested workflow forbids all model API calls or a reviewer is unavailable, leave semantics pending human review. Separate validator evidence from the user's acceptance, and require a meaningful acceptance action.
- Only accepted output becomes authoritative input for dependent tasks. Rebuild the next prompt with accepted output and confirmed state; do not rely on external chat history. Upstream edits invalidate dependent prompts and any acceptance derived from them.
- Preserve attempts, candidates, rejected output, and old runs. A retry creates new evidence; recovery resumes existing work instead of generating duplicate work.

Read [the durable task contract](references/task-contract.md) when designing storage, transitions, dependencies, or crash recovery. Adapt it to existing project conventions rather than copying a new persistence layer wholesale.

## Implement the user interaction

Expose prepare/export, copy or download, paste or file import, validate, accept/reject, retry, and resume at the application's existing generation entry point. A separate window, panel, or CLI is a product choice. Show the unit identifier, attempt, source revision, prompt hash, validation limitations, and stale status near the action that depends on them.

Protect unsent edits during navigation and version conflicts. Retain a recoverable submitted candidate if validation is interrupted. Distinguish accepted candidates from still-pending validation evidence. Finish through the application's existing output/review path; task acceptance does not silently approve global facts, publish content, or bypass whole-result review.

Check outbound snapshots for known credentials and common sensitive fields. Do not include provider configuration or transport headers. If a secret conflicts with required input, block export with a useful explanation instead of silently rewriting facts. A redacted historical view must be labeled and cannot be exported under the original snapshot hash. Recheck at export and acceptance, including from a stale browser session. Secret detection is a safeguard, not proof that arbitrary user text contains no secrets.

## Verify and deliver

Use [the acceptance scenarios](references/acceptance.md) to select meaningful tests for the project's storage and risk. Exercise at least one complete multi-unit workflow without API credentials and one resume after a real storage/process boundary. Test HTTP providers through isolated fakes, not paid production calls.

Report the integration seam, changed files, checks actually run, unsupported operation types, and human-review limitations. Provide concise operating instructions. Do not describe a skill installation as an implementation, synthetic output as real model quality validation, or a prepared prompt as an HTTP request. Preserve the user's Git and publishing instructions.
