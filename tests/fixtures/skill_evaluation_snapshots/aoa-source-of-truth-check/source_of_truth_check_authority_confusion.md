# Evaluation Snapshot
## Prompt
Clarify which file is authoritative because several docs overlap and contributors do not know what to trust first.
## Expected selection
use
## Why
A repository has several docs that may overlap or conflict, contributors may not know which file to trust first, and a change touches docs, process, or operational guidance and the question is which file is authoritative.
## Expected object
A source-of-truth decision that names the authoritative file and explains the relationship to overlapping documents.
## Boundary notes
Use this skill when the main task is document authority or ownership. Do not use it for broader policy design.
## Verification hooks
The response should identify the authoritative source and explain why it should be trusted over the others.

