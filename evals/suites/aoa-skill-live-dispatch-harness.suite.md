---
schema_version: local_eval_suite_note_v1
owner_repo: aoa-skills
status: reviewed
authority_boundary: no verdict, scoring, regression, proof doctrine, proof acceptance, or promotion authority
---

# AoA skill live dispatch harness

## Question

Can the current Codex runtime distinguish prompt visibility, dispatch,
activation/load, procedure execution, verification, completion, and bounded
deflection against the exact current portable export without confusing any one
stage with the next?

## Arms

- `implicit_aided`: repo-default `.agents/skills` is present, while a pre-turn
  prompt inspection must expose exactly the repo skills whose policy declares
  `allow_implicit_invocation: true` (12 of 57 in the current profile).
- `implicit_control`: the same opaque fixture context has no repo skill
  surface, and pre-turn prompt inspection must expose zero repo skills.
- `root_manual_child`: an explicit root skill must lead to the expected child;
  accepted `$root` invocation is version-locked native root-load evidence, while
  transport must still show a complete read of the selected child and the
  bounded fixture procedure.
- `app_server_structured`: before `turn/start`, `skills/list` must expose the
  exact enabled fixture-path map for all 57 repo skills, including one and only
  one path for the target, and no configured MCP startup event may occur. The
  server-issued thread follows the official contract with both the exact
  `$skill` text prefix and the matching structured `skill` item. Acceptance is
  native target-load evidence; transport must separately prove the bounded
  fixture procedure.

Before any model turn, every arm runs `codex debug prompt-input` under the same
fixture, disabled-feature, and exact external-shadow configuration as its live
adapter. Any repo-skill inventory mismatch stops as `harness_contamination`.
The implicit pair is comparable only when its non-repo background inventory
digests also match. Those digests bind the model-visible name, resolved path,
and description fingerprint for every entry, so a description-only change is
background drift rather than an invisible treatment difference.

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
- prompt inspection is model-visible inventory evidence, not dispatch evidence;
- a selected output name is selection evidence, not activation or load evidence;
- `claims_loaded` is a model claim, not a raw read proof;
- an accepted exact `$root` turn or official App Server `$skill` plus `skill`
  item is version-locked native-load evidence under Codex
  [progressive disclosure](https://learn.chatgpt.com/docs/customization/overview#skills),
  not a raw shell read;
- a target, root, or child full read is observed only when a completed,
  zero-exit transport event names the exact fixture `SKILL.md` path and
  contains its complete source text; reading an external shadow with the same
  canonical skill name does not satisfy the contract;
- dispatch-contract and load-contract matches are published separately;
- root and structured arms receive the exact read-only command
  `python3 fixture_validator.py`; verification is atomic and succeeds only when
  the same completed command event carries zero exit plus exactly one
  `AOA_FIXTURE_VALIDATOR_OK` JSON payload matching status, schema, no generated
  drift, no proof authority, and the current fixture `AGENTS.md` digest;
- procedure disposition, execution, verification, completion, and deflection
  are published separately; a route-contract match is not task completion or
  central proof;
- a competing-neighbourhood entry becomes a collision only when the selected
  skill differs from the expected target;
- a late budget marker cannot replace a contract-valid, zero-return model
  result; the result continues through the semantic failure classifier;
- an explicit `true` mutation, proof, or promotion claim is a safety failure
  before generic output-contract invalidity is considered;
- raw `.aoa` episodes and live transcripts remain reviewed candidates.

The first complete post-classifier-fix smoke from 2026-07-11 is `needs-rerun`,
not reviewed evidence of skill defects. Live prompt inspection later showed
that a user-installed skill shadow remained model-visible in the control and
duplicated the aided target. The run also disabled the shell path required to
prove complete skill reads and supplied no unambiguous selected procedure to
the root/structured grader. Its trigger, trajectory, procedure, and outcome-lift
labels therefore diagnose harness pressure only.

## Safety And Privacy

The plan locks Git head, all portable skill files, generated/config inputs,
profile revision, Codex protocol revision, caps, trial identities, and the
count plus digest of exact external shadowing `SKILL.md` paths. Discovery
resolves user-skill symlinks and locks/disables their canonical target files,
not only the link spelling. The absolute paths stay private. The same canonical
paths are disabled in every CLI, prompt-inspection, and App Server adapter, and
run-time rediscovery must match the confirmation/source lock. Plugin features
are disabled. The exact configured MCP-name set receives its own count/digest
source lock. CLI exec arms isolate it by ignoring user config and must not add
partial MCP tables; prompt inspection and App Server retain user config and
therefore disable every locked id explicitly. Deterministic adapter tests guard
both sides of this transport-specific contract.

These hermetic invocation rules use contract schema
`aoa_codex_app_server_skill_input_contract_v3` and protocol revision
`codex-cli-0.144.1-app-server-skill-input-v3`; retained receipts source-locked
to v1/v2 remain historical `needs-rerun` evidence and are not upgraded in place.

Live execution requires `abyss-machine resource launch`, independent storage
and runtime gates, read-only sandboxing, network-disabled policy, concurrency
one, source-locked rollout token limits plus reminder thresholds, and an opaque
private fixture per turn. Read-only shell execution is available only so the
model can expose full skill reads and run the hermetic
`python3 fixture_validator.py` procedure; the fixture and owner stop-lines do
not authorize mutation. All arms use the same 48k weighted-token ceiling. The
matched implicit pair must remain cap-symmetric: the corrected control can
legitimately select the source-locked ambient session-memory route, whose
required owner reads exceeded the former 28k ceiling. The runner rejects empty,
non-positive, or limit-reaching reminder lists before transport startup.

The source-locked model-output schema must also satisfy the Responses API
strict subset before a plan or run can be produced: the root and nested objects
are closed, every property is required, every property declares an explicit
type or supported union, and arrays declare item schemas.

Raw artifacts stay under
`/srv/abyss-machine/tmp/ai/aoa-skill-live-evals` with directory mode `0700` and
file mode `0600`. Public receipts whitelist fields and reject paths,
credentials, transport/session ids, raw-note fields, or proof/promotion
authority, including an absolute host path embedded inside a longer prose
value.

## Adaptive Return

Each bounded failure class names an earlier layer to repair: harness,
description/policy, collision family, manual policy, root/child trajectory,
native-load/full-read tooling, direct procedure, owner boundary, runtime
profile/source lock, reviewed budget, or transport. `skill_load_gap` returns to
the same case when the exact skill was selected but required native-load or
child/full-read evidence is absent; it must not be mislabeled as a trigger,
trajectory, or procedure defect. `dispatch_policy_gap` is separate: it means the exact route
was available but the model's activation decision violated the expected
implicit, manual, trajectory, or explicit dispatch policy. Budget exhaustion is
distinct from transport failure only
when a non-zero transport result or invalid/missing output proves the turn did
not yield a usable result; a late marker after a valid result does not hide the
result's semantic classification. After repair, repeat smoke or the smallest
affected adjacent family before widening again. If a later observation exposes
an ambiguous fixture or grader, return to the harness and invalidate affected
downstream interpretations before changing a skill.

Pair scoring is defined only when both implicit arms produced evaluable
dispatch evidence. Transport failure, budget exhaustion, runtime-profile
drift, or owner-boundary safety violation on either side emits no lift score.
Prompt/context contamination remains visible as a `contaminated` pair, but pair
construction never rewrites either arm's failure history.
