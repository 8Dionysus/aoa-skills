# Evaluation Snapshot
## Prompt
The bounded diff is already applied, the targeted checks are green, and the next honest move is one local commit with an explicit stop line before push.
## Expected selection
use
## Why
The coding and verification work are already bounded enough that the main remaining seam is one honest local commit boundary rather than more implementation.
## Expected object
A bounded local commit decision that carries forward the real validation state and stops before push or publish.
## Boundary notes
Use this skill when the diff is already ready and the route needs one intentional local commit. Do not widen it into push, PR, or publish choreography.
## Verification hooks
The response should mention the bounded diff, the named validation state, and the explicit stop line before push or publish.
