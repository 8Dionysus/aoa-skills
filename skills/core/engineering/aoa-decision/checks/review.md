# Review Checklist

## Purpose

Use this checklist when reviewing work that claims to use `aoa-decision`.

## When it applies

- the task touches decision records, decision indexes, or decision graph context
- the correct route may be find, create, or correct
- graph lookup can reduce broad repository reads
- repo-local decision files still need to remain authoritative

## Review checklist

- [ ] The work selected exactly one route: find, create, or correct.
- [ ] The workspace decision graph or named fallback was checked before broad repo reads.
- [ ] Repo-local decision files remain the source truth.
- [ ] Any write route reads the target repo's decision law before editing.
- [ ] The final report names graph freshness, source refs, and validation.

## Not a fit

- Pure source-of-truth ambiguity belongs to `aoa-source-of-truth-check`.
- A standalone decision note with no routing need belongs to `aoa-adr-write`.
