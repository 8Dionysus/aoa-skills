# SKILL_INDEX

This file is the repository-wide map of public skills.

## Current skills

| name | scope | status | summary |
|---|---|---|---|
| aoa-change-protocol | core | canonical | Codex skill for bounded change execution using plan, scoped edits, validation, and concise reporting. |
| aoa-tdd-slice | core | canonical | Codex skill for implementing a small feature slice through test-first change discipline. |
| aoa-contract-test | core | canonical | Codex skill for designing or extending contract-oriented validation at service or module boundaries. |
| aoa-bounded-context-map | core | canonical | Codex skill for carving or clarifying domain or system boundaries and their interfaces. |
| aoa-property-invariants | core | canonical | Codex skill for expressing domain or system invariants as property-oriented tests and checks. |
| aoa-invariant-coverage-audit | core | canonical | Codex skill for auditing whether existing checks actually constrain the stable invariants that matter, and for reporting the smallest bounded gaps. |
| aoa-approval-gate-check | risk | canonical | Codex skill for classifying whether a requested action should proceed, wait for explicit approval, or be refused. |
| aoa-adr-write | core | canonical | Codex skill for recording a meaningful architectural or workflow decision with rationale and tradeoffs. |
| aoa-automation-opportunity-scan | core | scaffold | Codex skill for detecting reviewed or repeated project processes that are candidates for automation, classifying whether they are seed-ready, and routing them to the right owner layer without granting schedule or mutation authority. |
| aoa-core-logic-boundary | core | evaluated | Codex skill for clarifying which logic belongs in the reusable core versus glue, orchestration, or infrastructure detail. |
| aoa-port-adapter-refactor | core | evaluated | Codex skill for refactoring toward clearer ports and adapters so reusable logic is less entangled with infrastructure details. |
| aoa-quest-harvest | core | scaffold | Codex skill for giving the final promotion verdict on one repeated reviewed quest unit without collapsing skills, playbooks, orchestrator classes, proof, or memory into one layer. |
| aoa-session-donor-harvest | core | scaffold | Codex skill for turning a reviewed session into a bounded HARVEST_PACKET, routing reusable units to the right AoA owner layer, and handing off to the next honest post-session skill when needed. |
| aoa-session-route-forks | core | scaffold | Codex skill for turning reviewed session evidence into explicit next-route forks with likely gains, costs, risks, owner targets, and stop conditions. |
| aoa-session-self-diagnose | core | scaffold | Codex skill for classifying drift, friction, proof gaps, and ownership confusion from a reviewed session into a bounded diagnosis packet without mutating anything yet. |
| aoa-session-self-repair | core | scaffold | Codex skill for turning a reviewed diagnosis packet into the smallest honest repair packet with checkpoint posture, rollback markers, and explicit owner-layer targets. |
| aoa-session-progression-lift | core | scaffold | Codex skill for lifting reviewed session evidence into a bounded multi-axis progression delta with explicit unlock hints and no fake single-score authority. |
| aoa-source-of-truth-check | core | canonical | Codex skill for checking whether canonical docs and repository guidance have clear ownership and do not silently conflict. |
| abyss-safe-infra-change | project | evaluated | Thin abyss overlay for bounded infrastructure or configuration changes with repo-relative operational surfaces, explicit local authority, and reviewable risk notes. |
| abyss-sanitized-share | project | evaluated | Thin abyss overlay for turning raw repo-local technical material into a shareable public-safe surface with explicit local thresholds and canonical placement notes. |
| atm10-change-protocol | project | evaluated | Thin atm10 overlay for bounded change execution with repo-relative paths, commands, and explicit local approval notes. |
| atm10-source-of-truth-check | project | evaluated | Thin atm10 overlay for clarifying repo-local document authority, canonical files, and review posture without changing the base workflow. |
| aoa-local-stack-bringup | risk | evaluated | Codex skill for reviewable local multi-service bring-up through rendered runtime truth, readiness checks, and one explicit lifecycle path. |
| aoa-dry-run-first | risk | canonical | Codex skill for preferring simulation, inspection, or preview paths before real execution with operational consequences. |
| aoa-safe-infra-change | risk | canonical | Codex skill for making bounded infrastructure or configuration changes with explicit risk framing and reversible execution discipline. |
| aoa-sanitized-share | risk | canonical | Codex skill for preparing findings, logs, or diagnostics for sharing without leaking secrets or private operational detail. |

## Project-Core Skill Kernel

The permanent project-core session-growth kernel in this repo is:

- `aoa-session-donor-harvest`
- `aoa-automation-opportunity-scan`
- `aoa-session-route-forks`
- `aoa-session-self-diagnose`
- `aoa-session-self-repair`
- `aoa-session-progression-lift`
- `aoa-quest-harvest`

This kernel is authored under `repo-project-core-kernel`. The older
`repo-session-harvest-family` profile remains as a backward-compatible
operational alias for the same seven-skill surface.

## Notes

- `scaffold` means the skill shape exists, but it should still evolve through technique linkage, examples, and project overlays.
- `evaluated` means behavior-oriented evidence exists through autonomy checks and trigger-boundary fixtures.
- `canonical` means the skill is the current default public reference for its workflow class with explicit promotion rationale.
- the documented maturity ladder is `scaffold`, `linked`, `reviewed`, `evaluated`, `canonical`, and `deprecated`.
