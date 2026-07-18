### Mode: find

Find existing rationale without letting retrieval replace its authored source.

### Input ABI

Consume `decision-query` with the question and at least one usable anchor when
available: absolute owner root, canonical decision ID, exact path, source
surface, changed path, owner, or repository. A retriever packet is optional.

### Procedure

1. Preserve the narrowest supplied anchor. Use this order:
   canonical ID or exact decision path, source or changed-path index, owner
   surface, known repository slice, then bounded free-text retrieval.
2. When both an absolute owner root and canonical ID are supplied:
   - read only the supplied root `AGENTS.md` and the exact decision-lane card
     when present
   - query the owner-declared exact-ID index, normally
     `docs/decisions/indexes/by-number.md`, and follow the matched source path
   - if the row is absent or stale, perform one bounded filename lookup under
     the owner decision home for that ID
   - do not inspect the current working directory, enumerate repositories, or
     run repository-wide search
3. For other anchors, use the owner-declared index or optional decision
   retriever first only when it is narrower than direct source lookup. Record
   its freshness and issues. Split a long query into owner, ID, path, or
   subject anchors before free-text search.
4. Treat every derived match as a locator. Read each authored decision record
   used for rationale, status, supersession, owner, or applicability.
5. Read one source record in ascending, non-overlapping windows. Start with
   lines 1 through 320; continue at 321 only when the answer requires it.
6. Classify each retained match as `exact`, `likely`, `analogy`, `stale`,
   `superseded`, or `missing`. Stop once sufficient verified matches answer the
   query.
7. When the user explicitly asks how a known decision was used, what happened
   after it, or which later failures followed, finish source identity first and
   hand that stable anchor to `aoa-session-memory-evidence-route`. Do not load
   session memory for ordinary rationale lookup.
8. If no adequate record exists, return a handoff to `record` only when an
   accepted decision is already supplied. If the source is wrong or stale,
   return a handoff to `correct`. Do not continue automatically.

### Output ABI

Return `decision-match-list` containing:

- selected mode and original query anchors
- owner repository, canonical ID, authored source path, and source status
- match class, relevance, confidence, and verified rationale summary
- derived lookup source and freshness when one was used
- actual effects (`read-only`), skipped routes, uncertainty, next route, and
  stop line

### Failure and termination

Return `blocked_missing_input` when neither a permitted owner source nor a
bounded locator is available. Never invent a decision, treat a title as
rationale, or widen to unrelated repositories after a sufficient match.
