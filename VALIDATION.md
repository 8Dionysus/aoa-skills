# Validation routes

Executable entrypoints are loaded only after the touched owner surface is
known. Reusable command composition remains canonical in
`config/validation_lanes.json`; this file owns human entry routes, not a second
copy of manifest sequences.

## Source fast

```bash
PYTHONPATH=scripts python scripts/lanes/ci_gate.py --mode source-fast
```

## Docs

```bash
git diff --check
```

## GitHub

Use the narrowest local lane that mirrors the job. For release-facing workflow
changes, run the owner wrappers below; for wording-only templates use the
[Docs](#docs) route.

```bash
PYTHONPATH=scripts python scripts/lanes/ci_gate.py --mode release
PYTHONPATH=scripts python scripts/lanes/release_check.py --include-packaging-smoke
```

## Decisions

Regenerate indexes only when decision metadata changed, then verify currentness.

```bash
PYTHONPATH=scripts python scripts/decisions/generate_decision_indexes.py
PYTHONPATH=scripts python scripts/decisions/generate_decision_indexes.py --check
```

Finish with the [Docs](#docs) hygiene route.

## Tests

Run the focused test first, then the durable repository suite.

```bash
PYTHONPATH=scripts python -m pytest -q tests
```
