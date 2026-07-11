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
text item deliberately has no `$skill` prefix; activation comes only from the
structured `skill` item. These causality/isolation rules use contract schema
`aoa_codex_app_server_skill_input_contract_v2` and protocol revision
`codex-cli-0.144.1-app-server-skill-input-v2`; retained receipts source-locked
to v1 remain historical `needs-rerun` evidence.

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
procedure. Root/child and structured arms receive the exact command
`python3 fixture_validator.py`. Transport evidence records full `SKILL.md`
reads only from the exact fixture paths with complete source content.
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
Public measures keep prompt visibility, selection, model load claim, full-read
evidence, dispatch/load matches, procedure disposition, execution,
verification, completion, and deflection separate. A correct selection without
the required activation/read evidence returns `skill_load_gap` to the same
case. A wrong activation decision after the route is available is instead
`dispatch_policy_gap`; neither class is proof of a skill defect or completed
work.

Implicit lift is omitted when either arm has a transport, budget, runtime, or
owner-boundary safety failure. Contamination remains an explicit pair outcome
but never rewrites either arm's recorded classification. Public review also
walks every string value and rejects an absolute host path even when it is
embedded in prose, in addition to credential and transport-id leakage.

The 2026-07-11 complete post-classifier smoke is retained only as a
`needs-rerun` harness diagnosis. User-skill prompt contamination, a disabled
full-read/shell path, and an ambiguous route/procedure grader make its former
trigger, trajectory, procedure, and lift interpretations non-actionable.

See `evals/suites/aoa-skill-live-dispatch-harness.suite.md` and
`docs/decisions/AOA-SK-D-0037-source-locked-live-skill-dispatch-evidence.md` for
the evidence and authority boundaries.
