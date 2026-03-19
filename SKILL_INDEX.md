# SKILL_INDEX

This file is the repository-wide map of public skills.

## Current skills

| name | scope | status | summary |
|---|---|---|---|
| aoa-change-protocol | core | canonical | Codex skill for bounded change execution using plan, scoped edits, validation, and concise reporting. |
| aoa-tdd-slice | core | canonical | Codex skill for implementing a small feature slice through test-first change discipline. |
| aoa-contract-test | core | scaffold | Codex skill for designing or extending contract-oriented validation at service or module boundaries. |
| aoa-bounded-context-map | core | scaffold | Codex skill for carving or clarifying domain or system boundaries and their interfaces. |
| aoa-property-invariants | core | scaffold | Codex skill for expressing domain or system invariants as property-oriented tests and checks. |
| aoa-adr-write | core | scaffold | Codex skill for recording a meaningful architectural or workflow decision with rationale and tradeoffs. |
| aoa-core-logic-boundary | core | scaffold | Codex skill for clarifying which logic belongs in the reusable core versus glue, orchestration, or infrastructure detail. |
| aoa-port-adapter-refactor | core | scaffold | Codex skill for refactoring toward clearer ports and adapters so reusable logic is less entangled with infrastructure details. |
| aoa-source-of-truth-check | core | scaffold | Codex skill for checking whether canonical docs and repository guidance have clear ownership and do not silently conflict. |
| aoa-approval-gate-check | risk | scaffold | Codex skill for classifying whether a requested action should proceed, wait for explicit approval, or be refused. |
| aoa-dry-run-first | risk | scaffold | Codex skill for preferring simulation, inspection, or preview paths before real execution with operational consequences. |
| aoa-safe-infra-change | risk | scaffold | Codex skill for making bounded infrastructure or configuration changes with explicit risk framing and reversible execution discipline. |
| aoa-sanitized-share | risk | scaffold | Codex skill for preparing findings, logs, or diagnostics for sharing without leaking secrets or private operational detail. |

## Notes

- `scaffold` means the skill shape exists, but it should still evolve through technique linkage, examples, and project overlays.
- `evaluated` means behavior-oriented evidence exists through autonomy checks and trigger-boundary fixtures.
- `canonical` means the skill is the current default public reference for its workflow class with explicit promotion rationale.
- the documented maturity ladder is `scaffold`, `linked`, `reviewed`, `evaluated`, `canonical`, and `deprecated`.
