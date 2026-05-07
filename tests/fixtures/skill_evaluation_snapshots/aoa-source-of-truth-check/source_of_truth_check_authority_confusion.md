# Evaluation Snapshot
## Prompt
Clarify which file is authoritative because several docs overlap, and keep top-level status docs short and link-driven once canonical homes already exist.
## Expected selection
use
## Why
A repository can have docs, source manifests, generated exports, runtime receipts, and provenance notes that overlap or conflict. Contributors need to know which surface to trust first, and top-level status docs should stay short when canonical homes already exist.
## Expected object
A source-of-truth decision that names the authoritative file and explains the relationship to overlapping documents.

Lightweight entrypoint docs should link outward instead of duplicating chronology or changing counters.
## Boundary notes
Use this skill when the main task is authority or ownership across docs, source, config, generated/export, operational, status, or provenance surfaces. Do not use it for broader policy design or for a plain rebuild when the source owner is already clear.
## Verification hooks
The response should identify the authoritative source, explain why it should be trusted over weaker companions, keep generated/export surfaces subordinate, and keep top-level status docs routed outward.
