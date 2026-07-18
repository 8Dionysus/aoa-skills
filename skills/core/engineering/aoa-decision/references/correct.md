### Mode: correct

Correct decision source or derived decision lookup drift without rewriting
history or treating a generated view as authority.

### Input ABI

Consume `decision-correction-target` with:

- exact owner and existing decision source or canonical ID
- observed mismatch and expected state
- affected decision indexes or retrieval consumers
- owner decision/index law
- explicit effect authority for every requested write

### Procedure

1. Read the exact authored decision and owner decision-lane law before any
   generated view or write.
2. Classify the mismatch as exactly one primary class:
   `source-content`, `source-metadata`, `semantic-supersession`,
   `generated-index-only`, or `external-cache-only`.
3. For `source-content` or `source-metadata`, make the smallest authorized
   owner-source correction. Do not widen a typo, path, or metadata repair into
   new rationale.
4. For `semantic-supersession`, preserve reviewable history through the
   owner's status and supersession vocabulary. If a genuinely new accepted
   decision also requires a new record, finish the current correction and
   return a separate `record` handoff.
5. For `generated-index-only`, leave source untouched and run only the
   owner-declared builder. If the builder or index contract is missing, return
   `blocked_missing_input` with expected parity and no manual patch proposal.
6. For `external-cache-only`, leave owner source and local indexes untouched.
   Use the declared refresh route when authorized; otherwise return the exact
   stale consumer as a handoff.
7. After a source change, rebuild declared owner indexes from source. Run the
   owner decision check and every affected source-surface check required by
   local law.
8. Compare each refreshed local consumer with the authored record. Check an
   external graph or KAG packet only as a derived consumer; never clear source
   debt by refreshing a cache.
9. Record pre-state, intended and actual effects, validation, residual drift,
   and whether rollback or supersession preserved history. In an explicit
   non-VCS owner root, use hashes or direct comparisons and do not probe or
   retry Git commands.

### Output ABI

Return `corrected-decision` with:

- disposition: `corrected`, `refreshed_derived_only`, `no_change`, or
  `blocked_missing_input`
- primary mismatch class, owner, canonical ID, source path, and expected state
- source effect, generated effect, external refresh effect, and preserved
  history posture
- owner checks, parity comparison, skipped consumers, residual risk, next
  route, and stop line

### Failure and termination

Stop before any write when the owner source, correction class, index contract,
builder, or effect authority is missing. Never hand-edit a generated index,
silently replace rationale, or claim correction while a declared consumer
remains stale.
