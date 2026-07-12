# Live Eval Runners

This directory holds owner-local runner implementations for the `aoa-skills`
eval port. The runners may produce candidate evidence; they do not own central
verdicts, scoring, regression truth, proof acceptance, or promotion.

## Live Skill Dispatch

`run_live_skill_dispatch.py` separates two layers:

- deterministic source-contract validation, exercised by
  `tests/test_live_skill_dispatch_harness.py`;
- explicitly confirmed live cohorts, whose raw evidence stays below the
  source-locked host-private root.

The default action is a read-only plan. A live run additionally requires the
exact confirmation token printed by that plan. `pilot13`, `full-collision`, and
`coverage-closure` require the printed high-cost token as well.
The pilot plan also publishes outcome-contract coverage and remains executable
only at 11 of 11 implicit pairs; an incomplete pilot stops before storage,
resource, runtime, or model preflight even when both confirmation tokens match.

Planning discovers exact external `SKILL.md` files whose canonical names
shadow the repo export, including canonical targets behind symlinked user-skill
directories. Only their count and deterministic digest enter the
confirmation/source lock; absolute paths remain private. A confirmed run
rediscovers the set and disables those canonical file paths in every CLI, App
Server, and prompt-inspection adapter. Plugin features are disabled. The exact
configured MCP-name inventory is separately count/digest locked. CLI exec arms
use `--ignore-user-config` and must not synthesize otherwise absent MCP tables;
prompt inspection and App Server, which retain the user config needed by those
transports, disable every locked MCP id explicitly.

Before each model turn, the runner calls `codex debug prompt-input` under the
same fixture, skill-shadow, and feature-disable configuration, with the
transport-appropriate MCP isolation described above. The aided fixture must
expose exactly the repo skills with `allow_implicit_invocation: true`
(currently 12 of 57),
while the control must expose zero repo skills. The paired non-repo background
inventory digests must match. Each entry fingerprint binds its model-visible
name, resolved path, and description, so description-only drift is detected. A
mismatch stops before the model turn as `harness_contamination`.

The structured arm has a second pre-turn gate. App Server `skills/list` must
equal the full 57-skill fixture path map, with exactly one enabled path per repo
name, and no configured MCP startup event may appear before `turn/start`. Its
turn follows the
[official App Server skill-invocation contract](https://learn.chatgpt.com/docs/app-server#start-a-turn-invoke-a-skill):
the text begins with the exact `$skill` mention and the adjacent structured
`skill` item carries the same fixture name and path. An accepted official input
is version-locked native-load evidence, distinct from a raw shell full read.
These rules use contract schema `aoa_codex_app_server_skill_input_contract_v9`
and protocol revision `codex-cli-0.144.1-live-dispatch-evidence-v9`. Retained
v1-v8 receipts stay source-locked to their original protocol and review status;
they are never upgraded in place.

Run the confirmed command only as the child of the plan packet's
`resource_launch_prefix`. The wrapper must produce the expected
`ABYSS_RESOURCE_CLASS`, `ABYSS_RESOURCE_KIND=agent`, and
`abyss-machine-agent-<class>-*.service` cgroup. The runner independently calls
the storage write preflight and checks the exact Codex version before creating
its private run directory.

Every live arm has the same source-locked 48k weighted-token ceiling. In
particular, aided and control arms must remain cap-symmetric even when the
control selects a longer source-locked ambient route; widening only one side
would invalidate paired lift.

The sandbox remains read-only and network-disabled, but the read-only shell
tool is available for evidence-bearing reads and the hermetic fixture
procedure. Read-only skill-file inspection commands may precede the procedure;
they collect evidence and do not count as procedure commands. Root/child and
structured arms receive the one exact procedure command
`python3 fixture_validator.py`. Transport evidence records full `SKILL.md`
reads only from the exact fixture paths with complete source content. One
successful output may contain the whole file, or ordered successful outputs may
continuously cover it; overlapping chunks are allowed, unrelated exact-path
metadata outputs are ignored, and gaps or reverse-only coverage remain
incomplete. Public
measures keep the model's `claims_loaded` self-report, accepted native input,
and raw full-read events separate: the self-report never gates objective load
evidence, the explicit root is natively loaded, any expected or dynamically
selected child still requires a raw read, and the official App Server dual
input natively loads its target.
Every model command remains confined to the fixture root. An observed absolute
host, workspace, session-memory, user-config, other-repository, or
parent-traversal path is `harness_contamination` before budget, dispatch, load,
procedure, or lift interpretation. System executables and `/dev/null` are
tooling exceptions; they do not authorize data reads outside the fixture.
Verification requires the same completed exact-command event to carry zero
exit and exactly one `AOA_FIXTURE_VALIDATOR_OK` JSON payload bound to the
current fixture-guidance digest; split success/sentinel events do not pass.

Example planning command:

```bash
python evals/runners/run_live_skill_dispatch.py plan \
  --repo-root . \
  --cohort smoke \
  --model MODEL \
  --effort medium
```

Do not paste raw receipts into Git, issue trackers, or chat. Review them locally
and use the runner's `review` action to create a field-whitelisted public
receipt under `evals/reports/` only after assigning an explicit review status.
Public measures keep prompt visibility, selection, model load claim, accepted
native input, raw full-read evidence, dispatch/load matches, procedure
disposition, execution, verification, completion, and deflection separate.
Each implicit pair always reports route lift. It reports bounded downstream
procedure-outcome lift only when both arms carry the same source-locked outcome
contract; otherwise the outcome dimension is `not_scored_no_contract`. The
outcome matcher compares only the predeclared downstream procedure disposition,
command, verification, completion/deflection, and owner-boundary dimensions and
does not depend on route correctness. It does not grade completion of a real
repository task outside the fixture. A
correct selection without the required native-load or child/full-read evidence
returns `skill_load_gap` to the same case. A wrong activation decision after the
route is available is instead `dispatch_policy_gap`. A normal zero-return
transport whose final structured result violates the bounded output schema is
`output_contract_invalid`, not `transport_failure`; none of these classes is
proof of a skill defect or completed work.

A caught CLI or App Server transport exception preserves its observed elapsed
milliseconds plus any partial stdout/stderr; recoverable JSONL events and usage
continue through turn-start, budget, filesystem-scope, and failure-precedence
grading. After the private receipt is safely written, the `run` command
returns exit 1 with `status=stopped_early` and the bounded stop reason when the
cohort is incomplete. A complete cohort still returns exit 0 even when it
records negative skill evidence; process status reports measurement completeness,
not model quality.

Both lift dimensions are omitted when either arm has an output-contract,
transport, budget, runtime, or owner-boundary safety failure. Contamination
remains an explicit pair outcome but never rewrites either arm's recorded
classification. A source-locked aided route whose bounded downstream procedure
outcome misses the declared contract returns `bounded_outcome_miss` to joint
skill-procedure and contract review before the same case is repeated.
Public review also
walks every string value and rejects an absolute host path even when it is
embedded in prose, in addition to credential and transport-id leakage.

The 2026-07-11 complete post-classifier smoke is retained only as a
`needs-rerun` harness diagnosis. User-skill prompt contamination, a disabled
full-read/shell path, and an ambiguous route/procedure grader make its former
trigger, trajectory, procedure, and lift interpretations non-actionable.

The exact-merged-tree v3 rerun after the `aoa-eval` child-handoff repair is also
retained as `needs-rerun` harness evidence. Its first three arms exposed that
the v3 grader still treated `claims_loaded` as load proof, did not bind an
implicitly selected child to its required read, classified a zero-return
output-contract failure as transport failure, and let the phrase "one command"
obscure that read-only inspection commands were allowed. It supports no pair,
lift, or skill-effect conclusion and required the now-retained v4 rerun.

The exact-merged-tree v4 rerun is retained as a second `needs-rerun` harness
receipt. Its aided arm completed objective root and dynamic-child reads, but
the control then read a complete `aoa-eval` source file from an external
canonical checkout before exhausting its budget. The historical v4 grader
reported only `budget_exhausted`; local raw review established that filesystem
scope contamination occurred earlier. It supports no pair, lift, skill-effect,
or family conclusion. The v5 fixture-scope rerun must pass before widening.

The exact-merged-tree v5 rerun fixed filesystem isolation and completed all four
arms, but its aided root read arrived as two ordered exact-path chunks. The v5
grader required one command output to contain the entire root source and
therefore recorded a false `skill_load_gap` and `no_lift_both_incorrect`. Its
public receipt remains immutable `needs-rerun` evidence; raw replay under v6 is
a harness regression check, not a replacement live result. Repeat the smoke on
an exact merged v6 tree before widening to `pilot13`.

The exact-merged-tree v6 rerun passed prompt and fixture-scope gates, then its
first CLI transport timed out at the 180-second cap before any turn event,
output, usage, or pair. The historical v6 runner wrote a correct private
stopped-early receipt but returned process exit 0, so the host wrapper reported
success for an incomplete cohort. The public receipt remains immutable
`needs-rerun` evidence. V7 repairs duration and process-status observability;
the same smoke must wait for runtime availability and then run on an exact
merged v7 tree before `pilot13`.

The exact-merged-tree v7 smoke then completed all four arms and recorded a
positive generic pair lift. Its v7 implementation derived that field solely
from route-contract correctness, even though the implicit arms reported
different deflection dispositions and neither reported completion. The reviewed
public receipt therefore preserves v7 as positive route-contract evidence only.
V8 removes the ambiguous generic fields from new pairs, source-locks the smoke
outcome contract before planning, and requires a fresh exact-merged smoke before
`pilot13`.

The exact-merged v8 smoke completed four of four arms and reported positive
route lift but negative outcome lift. Source review showed that the answer key,
not the observed downstream procedure, had crossed its declared boundary: the
model-output contract defines `procedure_disposition` for the downstream skill
procedure, while the v8 key expected deflection of the larger unavailable
repository task. The aided arm completed and verified the exact fixture
procedure while preserving those external owner stop-lines. Its reviewed
public receipt therefore remains immutable `needs-rerun` harness evidence. V9
names the downstream-procedure scope explicitly, corrects the pre-authored key
from source, and requires replay plus a fresh exact-merged smoke before
`pilot13`.

See `evals/suites/aoa-skill-live-dispatch-harness.suite.md` and
`docs/decisions/AOA-SK-D-0037-source-locked-live-skill-dispatch-evidence.md` for
the evidence and authority boundaries.
