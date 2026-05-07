# Skill Reality Trials

This report is execution evidence for real repository skill dispatch.
It checks that authored skills are not only present, but selectable in
the repository contexts where future agents are expected to use them.
Generated dispatch reports are evidence, not source authority.

- trial count: 4
- pass: 4
- fail: 0

## Trials

| case | repo | expected | actual | verdict |
|---|---|---|---|---|
| `atm10_operator_dry_run_gate` | `ATM10-Agent` | `must_confirm=aoa-dry-run-first,aoa-approval-gate-check` | `must_confirm=aoa-approval-gate-check,aoa-dry-run-first,aoa-local-stack-bringup,aoa-safe-infra-change,aoa-sanitized-share; suggest_next=aoa-automation-opportunity-scan,aoa-session-route-forks,aoa-change-protocol` | `pass` |
| `aoa_skills_quality_audit` | `aoa-skills` | `activate_now=aoa-invariant-coverage-audit` | `activate_now=aoa-invariant-coverage-audit; must_confirm=aoa-checkpoint-closeout-bridge; suggest_next=aoa-automation-opportunity-scan,aoa-approval-gate-check,aoa-change-protocol` | `pass` |
| `aoa_downstream_source_truth` | `Agents-of-Abyss` | `suggest_next=aoa-source-of-truth-check` | `activate_now=aoa-adr-write; suggest_next=aoa-source-of-truth-check,aoa-session-self-repair,aoa-change-protocol` | `pass` |
| `atm10_bounded_change` | `ATM10-Agent` | `activate_now=aoa-change-protocol` | `activate_now=aoa-change-protocol; suggest_next=aoa-local-stack-bringup,aoa-safe-infra-change,aoa-quest-harvest` | `pass` |

## Reading

### atm10_operator_dry_run_gate

Operator automation should route into explicit risk-ring gates before action.

- report path: `/srv/AbyssOS/aoa-sdk/.aoa/skill-dispatch/ATM10-Agent.ingress.latest.json`
- host inventory: `True`
- actionability gaps: none
- repo context: ATM10-Agent
- phase: ingress
- mutation_surface: none
- top tiny-router band: risk-ops-safety (score=28)
- host skill inventory was auto-discovered from repo-install at /srv/AbyssOS/ATM10-Agent/.agents/skills (25 skills).
- top band was strong, but every matching skill remained explicit-only or otherwise non-auto.

### aoa_skills_quality_audit

Skill-quality work should activate coverage-audit behavior inside aoa-skills.

- report path: `/srv/AbyssOS/aoa-sdk/.aoa/skill-dispatch/aoa-skills.ingress.latest.json`
- host inventory: `True`
- actionability gaps: none
- repo context: aoa-skills
- phase: ingress
- mutation_surface: none
- top tiny-router band: property-audit (score=16)
- host skill inventory was auto-discovered from repo-install at /srv/AbyssOS/aoa-skills/.agents/skills (45 skills).
- runtime checkpoint note already carries a reviewed-closeout chain, so aoa-checkpoint-closeout-bridge was surfaced as the next explicit closeout skill.

### aoa_downstream_source_truth

Constitutional repo should keep downstream guidance tied to source-of-truth checks.

- report path: `/srv/AbyssOS/aoa-sdk/.aoa/skill-dispatch/Agents-of-Abyss.ingress.latest.json`
- host inventory: `True`
- actionability gaps: none
- repo context: Agents-of-Abyss
- phase: ingress
- mutation_surface: none
- top tiny-router band: decision-doc-authority (score=9)
- host skill inventory was auto-discovered from repo-install at /srv/AbyssOS/Agents-of-Abyss/.agents/skills (23 skills).

### atm10_bounded_change

Ordinary bounded repo mutation should activate the change protocol.

- report path: `/srv/AbyssOS/aoa-sdk/.aoa/skill-dispatch/ATM10-Agent.ingress.latest.json`
- host inventory: `True`
- actionability gaps: none
- repo context: ATM10-Agent
- phase: ingress
- mutation_surface: none
- top tiny-router band: change-validation (score=11)
- host skill inventory was auto-discovered from repo-install at /srv/AbyssOS/ATM10-Agent/.agents/skills (25 skills).

