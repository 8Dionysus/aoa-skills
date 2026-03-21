# Evaluation Snapshot
## Prompt
Add a short note for a tiny self-evident edit where the diff already explains everything.
## Expected selection
do_not_use
## Why
This is a tiny and self-evident change, and the note would only restate an obvious diff with no real decision content.
## Expected object
A deflection that recommends a simpler edit or no ADR at all because the change does not justify decision documentation.
## Boundary notes
Do not turn trivial wording fixes into ADRs. If the task is actually about authority or source-of-truth questions, use a different skill.
## Verification hooks
The response should say the change is too small to justify ADR-style rationale and should not fabricate decision depth.

