# Evaluation Snapshot

## Prompt

Compare interface-contract validation with context-carving work and choose the clearer fit when the boundary is already clear.

## Expected selection

Decision: use `aoa-contract-test`.

## Why

- The interface boundary is already agreed on, so the value now comes from explicit validation rather than more boundary carving.
- The next bounded object is a contract-style test or assertion over that stable interface.

## Expected object

- This is a contract-test case, not a bounded-context-map case.
- A contract-style test or boundary assertion that captures the expected shape or behavior across the interface.

## Boundary notes

- If the interface itself becomes semantically unclear again, step back to `aoa-bounded-context-map` before finalizing the contract.

## Verification hooks

- Confirm the response centers on interface validation and does not invent a new context-map exercise.
