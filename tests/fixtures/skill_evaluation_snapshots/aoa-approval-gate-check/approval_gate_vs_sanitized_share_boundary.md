# Evaluation Snapshot

## Prompt

Compare deciding whether a sensitive incident artifact may be shared at all with preparing a sanitized version for broader circulation.

## Expected selection

Decision: use `aoa-approval-gate-check`.

## Why

- The first question is whether sharing the sensitive artifact is authorized at all.
- Sanitization only becomes relevant after the approval posture and sharing authority are explicit.

## Expected object

- This is an approval-gate case, not a sanitized-share case.
- A clear classification that names explicit approval or a bounded next step.

## Boundary notes

- If authority to share is already clear, move to `aoa-sanitized-share` for the public-safe artifact.

## Verification hooks

- Confirm the response classifies approval posture before proposing a sanitization workflow.
