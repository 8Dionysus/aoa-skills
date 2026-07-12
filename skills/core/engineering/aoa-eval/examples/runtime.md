# Example

## Scenario

A repo change may need an eval, but the owner route is unclear.

## Why this skill fits

- the task has eval-lane pressure, not only ordinary test work
- the next step is route selection before implementation
- central proof, local intake, MCP access, and session evidence must stay separate

## Expected inputs

- target repository and touched paths
- OS Abyss eval session-start packet when `aoa-evals` is available:
  `python scripts/aoa_eval_session_start.py --json`
- the packet's selected source root, Git commit, dirty/divergent posture, and
  freshness blockers as live-workspace routing evidence
- `eval_forge_front_door` refs when present:
  `EVAL_FORGE_OPERATING_PATH.md`, `SESSION_MINING_CRITERIA.md`,
  `LOCAL_PORT_DECISION_MATRIX.md`, the latest route-review report, worksheet
  example, and exact route commands
- local `evals/PORT.yaml` and nearby validators
- central `aoa-evals` owner boundary
- any `.aoa` evidence refs only if session mining is being considered

## Expected outputs

- exactly one selected subskill route
- owner-boundary statement
- readiness blockers and stop lines from the session-start packet when present
- exact source tree or commit used when the requested evidence is merge- or
  publication-bound
- stop line when the safe owner surface is missing

## Boundary notes

- `aoa-eval` is a router, not a proof owner
- session-start packets and generated dashboards are read-only route aids
- preserve a dirty canonical checkout; do not rewrite it to imitate an exact
  merged source
- Eval Forge front-door refs and commands are routing aids, not proof
  acceptance
- local intake pressure is weaker than central `aoa-evals` proof
- `.aoa` refs are candidate evidence only

## Verification notes

- verify that one route is chosen
- read the selected child's complete `SKILL.md` before applying its procedure;
  a returned child name proves selection, not load
- verify local and central owner surfaces are named
- verify Forge front-door refs were considered before local design or session
  mining when they are available
- verify candidate packets before using session evidence
- verify no central proof file is written through an access plane
