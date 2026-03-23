# Evaluation Snapshot
## Prompt
Clarify which file is authoritative because several docs overlap, and keep top-level status docs short and link-driven once canonical homes already exist.
## Expected selection
use
## Why
A repository has several docs that may overlap or conflict, contributors may not know which file to trust first, and top-level status docs should stay short when canonical homes already exist.
## Expected object
A source-of-truth decision that names the authoritative file and explains the relationship to overlapping documents.

Lightweight entrypoint docs should link outward instead of duplicating chronology or changing counters.
## Boundary notes
Use this skill when the main task is document authority or ownership and the repo already has canonical homes for detailed status or history. Do not use it for broader policy design.
## Verification hooks
The response should identify the authoritative source, explain why it should be trusted over the others, and keep top-level status docs routed outward.
