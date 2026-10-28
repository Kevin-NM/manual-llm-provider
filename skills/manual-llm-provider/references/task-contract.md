# Durable task contract

Use these semantics with the host application's existing tables, files, event log, or job system. The field names and representation are examples, not a required schema.

## Evidence and identity

| Record | Minimum useful content |
| --- | --- |
| Run | scope/tenant or workspace, run ID, manual transport marker, self-reported model label, input/source revisions, existing-output revision, prompt/validation contract version |
| Attempt | stable task/unit ID, attempt ID and ordinal, upstream accepted candidate IDs/hashes, exact role and combined prompt snapshots, snapshot hash, source projection/selection evidence |
| Submission | candidate ID, bound attempt and prompt hash, exact submitted output, content hash, durable submission time or logical sequence |
| Validation | candidate ID/hash, validator version, errors and warnings, semantic reviewer status and evidence, any unresolved review items |
| Acceptance | exact candidate ID/hash and source revisions, actor or local-author action, reviewed items/note where meaningful, accepted/rejected decision |

Scope all reads and mutations to the existing application ownership rules. IDs and hashes prevent accidental mix-ups; they do not by themselves prove authorship or resist malicious replacement of every stored record. Do not introduce a new global data store that bypasses access controls.

Define the exact hash representation. For text, a UTF-8 byte hash is practical; do not silently trim or normalize an already-hashed snapshot. For structured data, use the application's deterministic serialization or persist the exact bytes being hashed. If output normalization is intentional, keep raw and normalized hashes separately. Hash the actual combined export too, since framing can affect context size.

Immutable snapshots plus small versioned state records usually avoid repeatedly copying every prompt and candidate on each transition. Select current state by a reliable logical version or durable ordered sequence. A wall-clock timestamp plus a random suffix is not a reliable ordering scheme: coarse clocks, clock rollback, and restarts can select an older state. A process-local counter alone does not establish ordering across processes or restarts; use the storage system's concurrency guarantees.

## States and decisions

Typical lifecycle:

```text
prepared -> awaiting_external_output -> submitted -> validating
                                                -> pending_human_review
                                                -> accepted | rejected
```

The product may keep pending human review as a validation substatus instead of a separate task state. Additional `stale`, `invalidated`, `saving`, `completed`, and recoverable-error states should fit its existing job model.

`awaiting_external_output` records the user's workflow, not proof they copied anything, sent a message, or used the named model. No manual state implies HTTP delivery or remote completion. `accepted` means a specific candidate was approved for this task; it is distinct from final publication or application-wide facts.

On revised submission, clear the current acceptable-candidate pointer before validating the new candidate. Keep old candidates in history. If validation stops, show the newly saved pending submission, not the last successfully validated candidate. Recovery should validate that same saved candidate; retry starts a new attempt instead.

Reject deterministic errors before acceptance. Where semantics remain uncertain, show the actual unresolved checks and bind the user's review to the candidate and source versions; a boolean named `validated` must not conflate format checks, model review, and author acceptance.

## Sources, dependencies, and concurrency

Before preparing, importing, accepting, or applying output, check the frozen effective inputs against current sources under the host's transaction or concurrency mechanism. Use expected state/version guards for competing windows or workers. Distinguish changes to approved content, drafts, current output, and provider labels according to the product's explicit version policy; never substitute a newly edited draft silently for a frozen approved snapshot.

Dependent prompts include the full accepted context required by the existing builder, or an explicitly confirmed summary with provenance if that is already the product's design. A generated but unaccepted summary is not confirmed state. If an upstream candidate is revised, invalidate dependent prompt snapshots and derived acceptances. Rebuilding preserves their old evidence and produces a new attempt.

Pin model labels in historical runs. Decide explicitly whether changing a label affects future attempts or requires a new run; do not relabel past output. API and manual checkpoints may share storage, but compatibility checks must distinguish their source and approval requirements before reuse.

## Crash boundaries

Persist raw submissions before validation and acceptance before dependent preparation. A later input-budget failure must not erase an already accepted unit. Provide separate resume actions for pending validation and for preparing a missing next task.

Applying final output often crosses two writes: authoritative output and run completion. Prefer an existing transaction. Otherwise persist a write intent first, including intended output hash and the source/baseline revision needed to detect conflicts. On recovery, finish recording completion only if the actual output, current sources, approval state, and intent agree. A matching output hash alone does not license overwriting subsequent edits. Retry should not blindly apply output again.

Preserve corrupt evidence. If one historical run is unreadable, isolate it in the list and disclose the failure while leaving other runs accessible. An explicitly requested corrupt snapshot must fail clearly rather than being rebuilt from current settings.

## Export boundaries

Export the selected prompt/attempt and its provenance. Do not bundle unrelated run output, candidates, history, or provider configuration into a prompt download. Recheck the immutable original before export. If later credential settings make an old prompt unsafe to export, block it or create an explicitly new sanitized snapshot with its own hash and disclosed differences; never silently serve changed content under the original hash.
