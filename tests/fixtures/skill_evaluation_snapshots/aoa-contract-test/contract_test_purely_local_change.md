# Evaluation Snapshot
## Prompt
Refactor a local helper with no downstream boundary or interface change.
## Expected selection
do_not_use
## Why
The change is entirely local and does not affect a meaningful boundary, so contract-test framing is unnecessary.
## Expected object
A deflection toward an ordinary local refactor rather than a boundary contract.
## Boundary notes
Do not use this skill when no other module or service depends on the behavior.
## Verification hooks
The response should avoid boundary language and should not create an artificial contract concern.

