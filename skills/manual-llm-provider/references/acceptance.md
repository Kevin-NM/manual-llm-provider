# Acceptance scenarios

Adapt these cases to the application's real units, source approval policy, persistence, and risk. Synthetic fixtures establish workflow correctness; they do not establish the quality or identity of an external model.

For every implementation, verify no-key operation, prompt parity, candidate/acceptance separation, source-version guards, accepted dependencies, durable resume, and the existing final apply/review path. Select additional failure-injection cases for the persistence design. Browser-specific checks apply when a UI exists or is being added; a library or CLI can exercise its actual public interface instead. Do not create a browser UI merely to satisfy this checklist.

| Scenario | Observable evidence |
| --- | --- |
| No API credentials | Complete multiple dependent tasks, apply output through the existing path, and observe zero model-transport calls or HTTP-delivery events. Guard unsupported generation types too. |
| Same builder | Manual role prompts match the effective API prompts for the same approved inputs; combined framing, context size, hashes, and selection differences are visible. |
| Resume | Destroy and recreate the service/storage session or restart the test process; reload the same tasks, prompts, candidates, acceptances, and next unit. Browser reload alone cannot prove durable backend storage. |
| Unsent input | Navigate/reload with an unsent edit; it is restored locally or an explicit save/leave warning prevents silent loss. It is not treated as a submitted candidate. |
| Candidate isolation | Submit wrong task metadata, incompatible revisions, malformed or duplicate output. No result is auto-accepted or applied to authoritative output. Wrong-task prose with plausible formatting still needs semantic review. |
| Semantic reviewer absent | Deterministic results remain visible; unresolved semantic checks are pending human review and require an explicit decision. No fabricated reviewer result. |
| Sources change | Modify an input or approval relevant under the product's version policy. Stale import, acceptance, export, and final application are blocked or require an explicit new snapshot. |
| Dependencies change | Accept a unit and prepare the next; revise the upstream unit. Dependent prompts and derived acceptances become unusable, then rebuild from the newly accepted input. Old evidence remains. |
| Concurrent windows | Use the same expected version in competing operations. At most one conflicting mutation succeeds; the rejected user's unsent edits remain available. |
| Validation interruption | Save candidate A, then submit B and interrupt validation. Reload and resume B. A remains historical and cannot masquerade as the current candidate. |
| Preparation interruption | Accept a unit, then fail construction of the next prompt, for example on an input budget. Acceptance survives and next-task preparation can resume without duplicate acceptance. |
| Apply interruption | Fail after writing final output but before completion recording. Recover from an exact write intent; do not overwrite unrelated edits or require regenerating accepted work. |
| Coarse/reversed clock | Freeze or roll back time while appending transitions and checkpoints. Current logical state remains correct, including after restart under the chosen persistence model. |
| Corrupt history | Damage one isolated historical snapshot. Preserve it and disclose unreadability; other valid runs remain available. |
| Secret settings change | Introduce a known credential that matches previously saved content. An old browser cannot accept/export unsafe original data; redacted displays cannot be downloaded using old hashes. |
| HTTP regression | Existing provider credentials, selection, timeouts, retry policies, and ordinary output/review behavior retain their prior contract. |
| Product UI | Exercise the actual backend through the interface for copy/download, file import, validation, acceptance, reload, final application, and creating another run. Mocked DOM tests alone may miss state-contract bugs. |

Prefer the product's established test runners. Use temporary workspaces or database fixtures, synthetic input, mocked HTTP transports, and isolated browser profiles. Do not use real API keys, unpublished user content, or production storage just to produce test evidence.

Record the exact commands or test targets and actual outcomes. A format-valid skill, passing unit suite, or mocked interface is not proof that another project's implementation works. Mark unavailable checks as not run, and distinguish an unverified model label from a provider's reported completion metadata.
