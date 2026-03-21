# Evaluation Snapshot

## Prompt

Compare planning a bounded operational change with preparing a sanitized share of it and choose the clearer fit when the system still needs the change itself.

## Expected selection

Decision: use `aoa-safe-infra-change`.

## Why

- The task is to shape and verify the operational change itself.
- A sanitized share may be useful afterward, but it does not replace the bounded change plan, validation path, or rollback thinking.

## Expected object

- This is a safe-infra-change case, not a sanitized-share case.
- A bounded change plan or recommendation that names the operational surface, the validation path, and rollback or recovery notes.

## Boundary notes

- If the main task later becomes preparing a public-safe incident summary or shareable artifact, move to `aoa-sanitized-share`.

## Verification hooks

- Confirm the response keeps the focus on the operational surface and bounded execution plan.
- Confirm it does not substitute communication hygiene for validation and rollback thinking.
