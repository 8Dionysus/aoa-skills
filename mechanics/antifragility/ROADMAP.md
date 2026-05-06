# Antifragility Roadmap

## Current Contour

Antifragility owns fallback authoring, via-negativa pruning, collision stress,
and risk guard ring posture. It keeps risk explicit without becoming a generic
risk drawer or deletion authority.

The risk guard ring is authored under `repo-project-risk-guard-ring`,
hard-gated through `generated/project_risk_guard_ring_governance.min.json`, and
aliased exactly by `repo-risk-explicit`.

Risk guard ring members:

- `aoa-approval-gate-check`
- `aoa-dry-run-first`
- `aoa-local-stack-bringup`
- `aoa-safe-infra-change`
- `aoa-sanitized-share`

Adjacent overlays such as `abyss-safe-infra-change` and
`abyss-sanitized-share` may be reported next to the ring, but they are not ring
members.

## Next Work

- Decide whether rollback drill belongs to release-support, experience, or a
  narrow antifragility part before moving it.
- Decide whether risk-guard ring governance needs a package-local validation
  note beyond the generated readout.
- Decide whether deterministic support-resource hardening belongs here or in
  release-support.
- Keep `repo-project-foundation` as the baseline install layer carrying kernel,
  outer ring, and risk ring together while excluding project overlays.

## When Time Comes

- Add collision-stress validation only when trigger overlap repeatedly misroutes
  risk skills.
- Add public-share safety notes only when sanitization decisions become hard to
  review from skill docs and release-support alone.
- Promote a new risk-ring member only when scope, invocation mode, collision
  family, and governance readout all stay aligned.

## Out Of Scope

- Runtime rollback, local cleanup, or release approval ownership.
- Treating pruning as deletion approval.
- Turning generated risk readouts into source truth.
