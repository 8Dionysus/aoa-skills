# Review Checklist

## Purpose

Use this checklist when reviewing work that claims to use `aoa-decision`.

## When it applies

- the task touches decision records, decision indexes, or decision graph context
- the correct route may be find, record, or correct
- graph lookup can reduce broad repository reads
- repo-local decision files still need to remain authoritative

## Review checklist

- [ ] The work selected exactly one route: find, record, or correct.
- [ ] The narrowest available lookup route was used; a decision graph remained an optional aid rather than authority.
- [ ] Repo-local decision files remain the source truth.
- [ ] Any write route reads the target repo's decision law before editing.
- [ ] The final report names lookup freshness when relevant, owner-source refs, validation, and skipped checks.

## Not a fit

- Pure source-of-truth ambiguity belongs to the `authority-map` capability in
  `aoa-knowledge-stewardship`.
- A standalone accepted decision uses `aoa-decision` in `record` mode; do not
  load a retired child bundle.
