# Skill-canon statistics

This directory is the owner-local stats port for `aoa-skills`. It names
measurements whose domain meaning belongs to the bounded execution canon and
hands their portable contracts and evidence refs to `aoa-stats`.

The port does not observe private use, score people, infer skill quality,
decide promotion, claim downstream adoption, or replace authored `SKILL.md`
and activation-policy meaning.

## Current question

`aoa-skills/description-trigger-contract-coverage-ratio` asks what fraction of
the current published skill records carry `coverage_ok: true` in the
owner-generated description-trigger manifest.

The consumer is the Audit description-trigger route. The statistic helps that
route notice cohort-level contract movement without turning a ratio into a
runtime-routing, evaluation, or status claim.

## Reference derivation

The denominator is every skill record in
`generated/description_trigger_eval_manifest.json`. The numerator is the
subset whose `coverage_ok` field is true. The current packet reports `57 / 57`
at source revision `bc0311e27e1c3519579d4b4a39bf974ea1254d83`; it is a
source-revision census, not live telemetry.

`coverage_ok` means only that the committed description-trigger suite contains
every case class required for that skill by the owner activation policy. It
does not establish runtime selection correctness, skill quality, safe
activation, eval success, actual use, adoption, promotion readiness, or owner
acceptance.

## Owner routes

- `port.manifest.json` owns the local question and measurement contract.
- `packets/` contains the revision-bound public reference packet.
- `generated/description_trigger_eval_manifest.json` is the immediate derived
  owner evidence surface.
- Authored skill bundles, activation policy, trigger cases, their builder, and
  their validator remain stronger than this statistic.
- `mechanics/audit/docs/DESCRIPTION_TRIGGER_EVALS.md` owns the consuming audit
  route.
