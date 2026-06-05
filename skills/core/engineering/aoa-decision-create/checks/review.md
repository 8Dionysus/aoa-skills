# Review Checklist

## Purpose

Use this checklist when reviewing work that claims to use `aoa-decision-create`.

## When it applies

- a real durable decision has been made
- the owner repository has an appropriate decision lane
- graph context can help choose placement, neighbors, or ID context
- local indexes and the workspace graph need refresh after the source note

## Review checklist

- [ ] A real durable decision exists; the note is not process noise.
- [ ] Related graph context was checked before selecting placement and ID context.
- [ ] The new record follows the target repo's decision route card and template.
- [ ] Generated decision indexes were rebuilt from source metadata.
- [ ] The workspace decision graph was refreshed or checked after the write.

## Not a fit

- Existing rationale lookup belongs to `aoa-decision-find`.
- Existing source-record repair belongs to `aoa-decision-correct`.
