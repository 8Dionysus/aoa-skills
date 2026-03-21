# Evaluation Snapshot
## Prompt
Tighten validation on a service boundary where downstream consumers rely on a stable response shape.
## Expected selection
use
## Why
Two modules or services interact across a meaningful boundary, and a smoke path or interface needs a stable validation contract.
## Expected object
A contract-style test or boundary assertion that captures the expected shape or behavior across the interface.
## Boundary notes
Use this skill when the interaction boundary matters to other consumers. Do not use it for purely local refactors.
## Verification hooks
The response should identify the boundary and state the contract that downstream consumers depend on.

