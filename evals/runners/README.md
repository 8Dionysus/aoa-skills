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

Run the confirmed command only as the child of the plan packet's
`resource_launch_prefix`. The wrapper must produce the expected
`ABYSS_RESOURCE_CLASS`, `ABYSS_RESOURCE_KIND=agent`, and
`abyss-machine-agent-<class>-*.service` cgroup. The runner independently calls
the storage write preflight and checks the exact Codex version before creating
its private run directory.

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

See `evals/suites/aoa-skill-live-dispatch-harness.suite.md` and
`docs/decisions/AOA-SK-D-0037-source-locked-live-skill-dispatch-evidence.md` for
the evidence and authority boundaries.
