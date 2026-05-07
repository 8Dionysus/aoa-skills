# Growth-Cycle Roadmap

## Current Contour

Growth-cycle owns adaptive orchestration, reviewed-session harvest posture,
session-growth kernel maturity, and harvest-note boundaries. It keeps growth
evidence reviewable without becoming a hidden scheduler.

The permanent project-core session-growth kernel is:

- `aoa-session-donor-harvest`
- `aoa-checkpoint-closeout-bridge`
- `aoa-automation-opportunity-scan`
- `aoa-session-route-forks`
- `aoa-session-self-diagnose`
- `aoa-session-self-repair`
- `aoa-session-progression-lift`
- `aoa-quest-harvest`

The kernel is authored under `repo-project-core-kernel`, hard-gated repo-wide,
and exported with one detail receipt schema plus the shared
`core_skill_application_receipt` schema for each kernel skill. The per-skill
gate readout is `generated/project_core_kernel_governance.min.json`.

## Next Work

- Keep `docs/session-harvests/` as public evidence only while it remains useful;
  do not let it become promotion verdict authority.
- Keep the session-harvest family after reviewed run, closure, or pause; do not
  use it inside an active route.
- Keep donor harvest, checkpoint closeout bridge, automation scan, route forks,
  self-diagnosis, self-repair, progression lift, and quest harvest distinct so
  no leaf skill gains hidden routing authority.
- Keep `aoa-commit-growth-seam` and `aoa-summon` as explicit session-growth
  companion skills outside the hard-gated kernel until they receive the same
  detail-receipt contract.
- Keep project-core kernel skill meaning under `skills/`.
- Keep checkpoint protocol and candidate-ref identity in their own packages.

## When Time Comes

- Add a package-local receipt validator when repeated kernel receipt drift
  appears outside existing release checks.
- Promote a narrower profile only when it preserves the hard-gated kernel
  contract and explains why the profile is useful.
- Route final quest promotion triage through Questbook only after donor harvest
  and progression lift evidence are reviewed.

## Out Of Scope

- Hidden scheduling, automatic promotion, or silent self-mutation.
- Collapsing checkpoint, method-growth, questbook, stats, and memory into one
  growth bucket.
- Treating examples or checkpoint notes as final verdicts.
