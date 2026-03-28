# Evaluation Snapshot

## Prompt

Compare first-pass context carving with a narrower core-versus-glue split and choose the clearer fit when domain language and subsystem boundaries are still mixed together.

## Expected selection

Decision: use `aoa-bounded-context-map`.

## Why

- The first problem is still semantic and contextual: the subsystem boundary is not named clearly enough yet.
- A narrower core-versus-glue split should happen only after the broader context boundary is understood.

## Expected object

- This is a bounded-context-map case, not a core-logic-boundary case.
- A first-pass context and boundary clarification that separates overlapping concepts before deciding the narrower core-versus-glue split.

## Boundary notes

- Once the context is named and stable, `aoa-core-logic-boundary` becomes the better follow-on object for core-versus-orchestration cleanup.

## Verification hooks

- Confirm the response names the broader context boundary before narrowing into reusable rules versus orchestration detail.
