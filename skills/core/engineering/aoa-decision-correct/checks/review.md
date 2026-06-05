# Review Checklist

## Purpose

Use this checklist when reviewing work that claims to use `aoa-decision-correct`.

## When it applies

- an existing decision record is stale, incomplete, misindexed, or superseded
- graph lookup shows a mismatch that must be checked against the source note
- generated decision indexes may be out of sync with source metadata
- semantic corrections need reviewable history rather than silent rewrites

## Review checklist

- [ ] The source decision note was inspected before any generated index or graph fix.
- [ ] The correction class is explicit: metadata, source surface, status, supersession, typo, or index drift.
- [ ] Semantic changes preserve reviewable history instead of silently rewriting meaning.
- [ ] Repo-local indexes were regenerated when metadata changed.
- [ ] The workspace graph was refreshed or checked against the corrected source state.

## Not a fit

- Plain lookup belongs to `aoa-decision-find`.
- A new durable decision belongs to `aoa-decision-create`.
