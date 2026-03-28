# Evaluation Snapshot

## Prompt

Compare context carving with a seam-making refactor and choose the clearer fit when naming and subsystem boundaries are still unclear before any adapter work starts.

## Expected selection

Decision: use `aoa-bounded-context-map`.

## Why

- The main ambiguity is still which context owns the work and how adjacent concepts should be separated.
- Port or adapter work would be premature before the broader context boundary is named cleanly.

## Expected object

- This is a bounded-context-map case, not a port-adapter-refactor case.
- A first-pass context and boundary clarification that should happen before choosing a narrower dependency seam.

## Boundary notes

- Once the context boundary is clear and one concrete dependency remains the pressure point, `aoa-port-adapter-refactor` becomes the better next object.

## Verification hooks

- Confirm the response resolves the broader context boundary first and does not jump straight into seam extraction.
