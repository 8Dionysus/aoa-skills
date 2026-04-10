# Evaluation Snapshot
## Prompt
The diff is still changing, verification is not done, and the work clearly needs more repair before any commit boundary would be honest.
## Expected selection
do_not_use
## Why
The route has not reached a stable commit boundary yet, so forcing a commit skill now would hide unfinished repair and missing verification.
## Expected object
A deflection that keeps the route in repair or verification instead of forcing a commit boundary too early.
## Boundary notes
Do not use this skill while the patch still needs coding or tests. Reach a bounded verified diff first, or use the broader change workflow instead.
## Verification hooks
The response should refuse the commit boundary now and redirect toward more repair or verification rather than inventing a premature commit step.
