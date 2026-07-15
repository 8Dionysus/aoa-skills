# Contributing

## Orient first

Read `AGENTS.md`, the nearest nested card, `CHARTER.md`, and the affected owner
source. Capability changes begin in `capabilities/`; callable procedure changes
begin in `skills/`. Do not begin from a generated catalog or exported bundle.

## Change loop

1. State the observed problem and the owner boundary.
2. Reproduce it manually on real or representative work.
3. Compare no-skill, current, and candidate behavior where the claim is about
   usefulness.
4. Change the smallest authored source that owns the behavior.
5. Re-run held-out manual cases, including negative and coexistence cases.
6. Add or change a test only when a stable invariant has emerged and the test
   cannot conceal the outcome behind a green proxy.
7. Rebuild derived surfaces and run the relevant structural lane.
8. Remove temporary traces, fixtures, workspaces, and other construction waste.

## Capability changes

Preserve one `primary_parent` and express all cross-links as typed relations.
Executable nodes require applicability, ABI, binding, execution, trust,
provenance, lifecycle, and failure contracts. External bindings must point to
current owner sources and may remain explicitly unavailable or unbound.

## Bundle changes

Keep `SKILL.md` focused and progressively disclosed. A new bundle needs an
independent trigger, ABI, composition value, and measured outcome lift. Modes
that do not meet that bar stay inside an existing bundle or the capability
graph. Do not add a technique dependency.

## Evidence

Keep raw session traces and task-local DAGs outside the repository. Durable
owner truth may include only reviewed contracts, compact held-out cases,
decisions, or lifecycle findings that belong to this repository. Shared proof
routes to `aoa-evals`.

## Commands

Use `config/validation_lanes.json` as command authority. Typical focused checks:

```bash
PYTHONPATH=scripts python scripts/validation/validate_skills.py --repo-root .
PYTHONPATH=scripts python scripts/validation/validate_capability_system.py --repo-root . --check-generated
PYTHONPATH=scripts python scripts/validation/validate_agent_skills.py --repo-root .
PYTHONPATH=scripts python -m pytest -q tests
```

Green checks mean the encoded contracts are internally consistent; they do not
prove that a skill improves an agent.
