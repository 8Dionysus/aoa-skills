---
schema_version: local_eval_suite_note_v1
owner_repo: aoa-skills
status: reviewed
authority_boundary: no verdict, scoring, regression, proof doctrine, proof acceptance, or promotion authority
---

# AoA skill live dispatch harness

## Question

Can the current Codex runtime distinguish AoA skill dispatch, explicit/manual
reachability, root-to-child trajectory, and structured skill input against the
exact current portable export without confusing availability or a model claim
with completed work?

## Arms

- `implicit_aided`: repo-default `.agents/skills` is present.
- `implicit_control`: the same opaque fixture context has no skill surface.
- `root_manual_child`: an explicit root skill must lead to the expected child,
  and transport evidence must show the child `SKILL.md` read.
- `app_server_structured`: `skills/list` must expose the exact enabled skill
  path, and `turn/start` receives both text and structured `skill` input using
  the server-issued thread id.

The paired implicit arms publish per-case observed lift in `{-1, 0, 1}` and an
effect class. They do not publish an aggregate score.

## Cohorts

| Cohort | Turns | Purpose | Host class |
| --- | ---: | --- | --- |
| `smoke` | 4 | one implicit pair, one trajectory, one structured input | light |
| `pilot13` | 30 | representative core, risk, project, and Titan pressure | medium |
| `full-collision` | 98 | all 49 collision cases as aided/control pairs | sustained |
| `coverage-closure` | 87 | uncovered skills, all root-child trajectories, and all non-invoke structured routes | sustained |

Every cohort beyond smoke requires a second exact high-cost token. Widen only
after reviewing the preceding cohort and repairing any return route it opens.

## Evidence Semantics

- fixture presence is availability evidence;
- a structured App Server item is selected-input evidence;
- `claims_loaded` is a model claim, not a raw read proof;
- a root child read is observed only from transport events naming the child
  `SKILL.md` and a read/completion marker;
- a route-contract match is deterministic receipt evidence, not task completion
  or central proof;
- raw `.aoa` episodes and live transcripts remain reviewed candidates.

## Safety And Privacy

The plan locks Git head, all portable skill files, generated/config inputs,
profile revision, Codex protocol revision, caps, and trial identities. Live
execution requires `abyss-machine resource launch`, independent storage and
runtime gates, read-only sandboxing, network-disabled tool policy, concurrency
one, source-locked rollout token limits plus reminder thresholds, and an opaque
private fixture per turn. The runner rejects empty, non-positive, or
limit-reaching reminder lists before transport startup.

The source-locked model-output schema must also satisfy the Responses API
strict subset before a plan or run can be produced: the root and nested objects
are closed, every property is required, every property declares an explicit
type or supported union, and arrays declare item schemas.

Raw artifacts stay under
`/srv/abyss-machine/tmp/ai/aoa-skill-live-evals` with directory mode `0700` and
file mode `0600`. Public receipts whitelist fields and reject paths,
credentials, transport/session ids, raw-note fields, or proof/promotion
authority.

## Adaptive Return

Each bounded failure class names an earlier layer to repair: harness,
description/policy, collision family, manual policy, root/child trajectory,
direct procedure, owner boundary, runtime profile/source lock, or transport.
After repair, repeat smoke or the smallest affected adjacent family before
widening again.
