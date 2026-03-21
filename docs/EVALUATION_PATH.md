# Evaluation path

`EVALUATION_PATH.md` is the human guide for reading evaluation evidence in `aoa-skills`.
It is the layer for matrix outputs, snapshot-backed coverage, and evidence review.

Use this guide when you want to answer:
- what behavior evidence exists for a skill
- how to read the evaluation matrix
- whether the coverage is snapshot-backed and current

This guide is separate from runtime selection in `RUNTIME_PATH.md` and separate from derived public status in `PUBLIC_SURFACE.md`.
If you are choosing an object, start with runtime. If you are judging evidence, start here.

## Layer map

- `RUNTIME_PATH.md` - pick, inspect, expand, object use
- `EVALUATION_PATH.md` - evidence, matrix output, snapshot-backed coverage
- `PUBLIC_SURFACE.md` - derived governance and public-product signals

The generated matrices that already exist in this repository stay in their own layers:
- `generated/skill_walkthroughs.md` and `generated/skill_walkthroughs.json` are runtime inspect surfaces
- `generated/skill_evaluation_matrix.md` and `generated/skill_evaluation_matrix.json` are the derived evaluation evidence surfaces for this layer
- `generated/public_surface.md` and `generated/public_surface.json` are derived governance/public-product surfaces

## What counts as evaluation evidence

Evaluation evidence is repo-local and reviewable. Typical sources include:
- `tests/fixtures/skill_evaluation_cases.yaml`
- bundle-local checks or review artifacts when a skill provides them
- validator output that reflects the committed evaluation matrix
- snapshot-backed cases that keep the coverage stable across runs

Do not read public status as proof of behavior.
Do not read runtime wording as proof of evaluated coverage.

## Reading the matrix

The current evaluation matrix input is `tests/fixtures/skill_evaluation_cases.yaml`.
The current derived matrix output is `generated/skill_evaluation_matrix.md`.
Treat it as the source of truth for coverage questions such as:
- autonomy checks
- `use` trigger cases
- `do_not_use` trigger cases
- snapshot-backed boundary checks when a skill carries them

Read the repo-local matrix report directly with:

```bash
python scripts/report_skill_evaluation.py
```

Read the matrix in this order:
1. identify the skill
2. inspect the fixture rows for that skill
3. compare the explicit trigger cases
4. check any snapshot-backed coverage that accompanies the skill
5. verify the local validator output against the committed matrix

If upstream technique drift may explain a failed evaluation claim, consult the bridge drift report CLI:

```bash
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques
```

That report is related to evidence reading, but it is not itself evaluation doctrine.

## Snapshot-backed coverage

Snapshot-backed coverage means the reviewed cases and expected outputs are committed, stable, and local to the repository.
It is meant to catch boundary regressions and coverage drift without depending on live fetches or ad hoc state.

Snapshot-backed coverage should answer the question:
does the skill still behave the way the matrix claims it does?

## What this layer does not do

This guide does not decide:
- runtime selection
- public maturity status
- promotion rules
- canonical-candidate readiness
- release signaling

It also does not collapse into the generated runtime or public matrices.
Those stay in `generated/skill_walkthroughs.*`, `generated/skill_evaluation_matrix.*`, and `generated/public_surface.*`, which are separate derived surfaces.

## Future stubs

TODO: if a richer matrix rendering is ever needed, keep it as a repo-local derived surface rather than a live cross-repo fetch.

TODO: if LLM-executed evaluation is ever introduced, keep it behind an explicit repo-local CLI and document the output shape here without widening runtime selection.

TODO: if cross-repo evaluation evidence ever becomes necessary, derive it from existing repository facts instead of live remote reads.
