# QUESTBOOK integration — aoa-skills

## Purpose

This note shows how `QUESTBOOK.md` fits into `aoa-skills` as the public tracked surface for deferred skill obligations.

## Role split

- skill bundles remain the source of skill meaning
- `generated/public_surface.md`, `generated/governance_backlog.md`, and `generated/skill_evaluation_matrix.md` remain derived readouts
- `QUESTBOOK.md` holds deferred obligations that survive the current bounded diff
- overlay and local-adapter details may trigger quests, but they should not become a hidden second source of truth

## Good anchors in this repo

Use stable anchors such as:
- `docs/RUNTIME_PATH.md`
- `docs/EVALUATION_PATH.md`
- `docs/BRIDGE_SPEC.md`
- `generated/governance_backlog.md`
- `generated/skill_evaluation_matrix.md`
- `docs/CODEX_PORTABLE_LAYER.md`
- `docs/LOCAL_ADAPTER_CONTRACT.md`
- `docs/OVERLAY_SPEC.md`
- `docs/TWO_STAGE_SKILL_SELECTION.md`

## Initial posture

A skill quest should usually answer one of these:
- which workflow gap survived the current diff
- which proof or evaluation seam drifted
- which runtime export or local adapter contract needs bounded repair
- which repeated overlay exception wants promotion into a real skill or playbook
- which recurring cross-repo bridge refresh route wants automation classification without smuggling runtime authority

## Installed session-harvest posture

The explicit post-session session-harvest family may be installed into
repo-local `.agents/skills/`, but its source of truth remains the canonical
bundles in `aoa-skills`.

Use [ADAPTIVE_SKILL_ORCHESTRATION.md](ADAPTIVE_SKILL_ORCHESTRATION.md)
before invoking that family when a session still mixes task execution,
closeout, and promotion pressure.
That protocol helps the agent decide whether the honest next move is:

- more execution
- a bounded closeout read
- a checkpoint note
- a candidate harvest note
- or an explicit session-harvest family skill

The family is:

- `aoa-session-donor-harvest`
- `aoa-session-route-forks`
- `aoa-session-self-diagnose`
- `aoa-session-self-repair`
- `aoa-session-progression-lift`
- `aoa-quest-harvest`

- before that family, a lower-authority checkpoint-note lane may preserve
  repeated candidates, evidence refs, owner hints, and promotion conditions as
  a pre-harvest reviewed note
- a bounded applicability map or candidate-harvest note may also exist before
  the family as an orchestration aid; it is still lower-authority than the
  explicit session-harvest skills
- the checkpoint-note lane is additive and review-shaped; it is not a replacement for the reviewed session-harvest family
- checkpoint-note capture does not emit harvest verdicts, progression deltas,
  or core-skill application receipts
- use the family after a reviewed run, closure, or pause
- do not invoke it inside an active route
- it does not define orchestrator identity
- it does not replace playbook, memo, eval, or source-owned doctrine
- do not promote on one anecdotal repeat

The bounded `aoa-quest-harvest` verdict surface remains:

- `keep/open quest`
- `promote to skill`
- `promote to playbook`
- `promote to orchestrator surface`
- `promote to proof surface`
- `promote to memo surface`

## Manual-first pilot lane

- `AOA-SK-Q-0002` carried one surviving proof-alignment debt from `aoa-techniques` into the existing derived readouts `generated/governance_backlog.md` and `generated/skill_evaluation_matrix.md`.
- The bounded conclusion for this pass is that those two derived surfaces stay aligned while the remaining proof follow-through belongs in `aoa-evals`, not in a wider skill backlog.
- No ATM10-specific or overlay-specific anchor was introduced for this lane; the repo-local contract stayed inside the existing skill/runtime boundary.
- `AOA-SK-Q-0006` now captures the reviewed cross-repo route where an upstream `aoa-techniques` landing can trigger downstream drift detection, skill refresh, review truth-sync, and merge recovery.
- The bounded conclusion for this lane is still manual-first: classify the route for automation or playbook lift explicitly before granting any helper surface more authority.
- `AOA-SK-Q-0007` closed once the workspace checkpoint-growth route was written as a bounded session-harvest note and the bridge skill kept downstream self-diagnose, owner follow-through, and stats refresh explicit.
- The bounded conclusion for that lane is to keep `aoa-checkpoint-closeout-bridge` narrow while leaving broader automation classification in `AOA-SK-Q-0006`.
