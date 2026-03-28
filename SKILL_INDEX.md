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
| aoa-core-logic-boundary | core | evaluated | Codex skill for clarifying which logic belongs in the reusable core versus glue, orchestration, or infrastructure detail. |
| aoa-port-adapter-refactor | core | evaluated | Codex skill for refactoring toward clearer ports and adapters so reusable logic is less entangled with infrastructure details. |
| aoa-source-of-truth-check | core | canonical | Codex skill for checking whether canonical docs and repository guidance have clear ownership and do not silently conflict. |
| abyss-safe-infra-change | project | evaluated | Thin abyss overlay for bounded infrastructure or configuration changes with repo-relative operational surfaces, explicit local authority, and reviewable risk notes. |
| abyss-sanitized-share | project | evaluated | Thin abyss overlay for turning raw repo-local technical material into a shareable public-safe surface with explicit local thresholds and canonical placement notes. |
| atm10-change-protocol | project | evaluated | Thin atm10 overlay for bounded change execution with repo-relative paths, commands, and explicit local approval notes. |
| atm10-source-of-truth-check | project | evaluated | Thin atm10 overlay for clarifying repo-local document authority, canonical files, and review posture without changing the base workflow. |
| aoa-local-stack-bringup | risk | evaluated | Codex skill for reviewable local multi-service bring-up through rendered runtime truth, readiness checks, and one explicit lifecycle path. |
| aoa-dry-run-first | risk | canonical | Codex skill for preferring simulation, inspection, or preview paths before real execution with operational consequences. |
| aoa-safe-infra-change | risk | canonical | Codex skill for making bounded infrastructure or configuration changes with explicit risk framing and reversible execution discipline. |
| aoa-sanitized-share | risk | canonical | Codex skill for preparing findings, logs, or diagnostics for sharing without leaking secrets or private operational detail. |

## Notes

- `scaffold` means the skill shape exists, but it should still evolve through technique linkage, examples, and project overlays.
- `evaluated` means behavior-oriented evidence exists through autonomy checks and trigger-boundary fixtures.
- `canonical` means the skill is the current default public reference for its workflow class with explicit promotion rationale.
- the documented maturity ladder is `scaffold`, `linked`, `reviewed`, `evaluated`, `canonical`, and `deprecated`.
