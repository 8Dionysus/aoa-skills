# AGENTS.md

## Applies to

This card applies to `stats/` and all descendants.

## Role

`stats/` is the owner-local measurement port for the bounded skill canon. It
defines skill-domain questions, populations, measures, evidence refs, and
authority ceilings while remaining compatible with the central `aoa-stats`
protocol.

It does not own cross-repository aggregation, eval verdicts, runtime routing,
skill promotion, downstream adoption, user assessment, or private usage
telemetry.

## Read before editing

1. Root `AGENTS.md`, `CHARTER.md`, and `DESIGN.md`.
2. `README.md` and `port.manifest.json` in this district.
3. The owner source and consuming mechanic named by the measurement.
4. The central `aoa-stats` measurement and local-port contracts.

## Boundaries

- Derive only from public owner surfaces and retain portable evidence refs.
- Keep packet refs repository-relative and raw prompts or usage content out of
  packets.
- Treat generated trigger coverage as a projection of authored skill and
  activation-policy sources, not as runtime success or an eval verdict.
- Keep live/reference posture explicit; the current export is reference-only.
- Do not add a measure without a real owner question and a named consumer.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

```bash
python scripts/validation/validate_local_stats_port.py
python -m unittest tests.test_local_stats_port
```

The repository-wide lane remains `source-fast`; its command sequence is owned
by `config/validation_lanes.json`.

## Closeout

Report the question, population, source revision, reference/live posture,
authority ceiling, owner trigger evidence inspected, whether the reference
packet was refreshed, and which validation route ran.
