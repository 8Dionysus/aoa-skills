# Evaluation Snapshot
## Prompt
Apply a bounded non-trivial change in an atm10 repository where local files, commands, and approval notes still need to be named explicitly.
## Expected selection
use
## Why
The base `aoa-change-protocol` workflow is already correct, but the local repo still needs repo-relative files, commands, and approval notes named explicitly.
## Expected object
A bounded local change note that keeps repo-relative paths, route cards, commands, recovery anchors, downstream approval, and verification explicit.
## Boundary notes
Use this overlay when the base workflow is right and only the local repo shape needs a thin adaptation.
The route should name ATM10 `AGENTS.md`, nearest nested route cards, and any owning public docs such as `docs/SOURCE_OF_TRUTH.md`, `docs/RUNBOOK.md`, or `docs/PRODUCT_EDGE_POSTURE.md`.
## Verification hooks
The response should keep the base plan shape, name repo-relative commands, preserve dry-run/report-only safety when automation is involved, and leave downstream approval explicit.
