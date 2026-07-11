# Source-Locked Live Skill Dispatch Evidence

- Decision ID: AOA-SK-D-0037
- Status: Accepted
- Date: 2026-07-11
- Owner surface: `evals/runners/run_live_skill_dispatch.py`,
  `evals/suites/aoa-skill-live-dispatch.plan.json`, and the related schemas

## Index Metadata

- Original date: 2026-07-11
- Surface classes: validation guard, export/runtime, review/governance
- Skill lanes: none
- Mechanic parents: none
- Guard families: evaluation/public surface, export/runtime, release/tooling
- Posture: accepted source-locked live evidence route

## Context

Generated trigger cases, static descriptions, installed-skill counts, and
session mentions do not prove that a current Codex runtime can distinguish,
load, follow, or correctly defer an AoA skill. Raw model transcripts can expose
that pressure, but they are private, costly, runtime-dependent, and too weak to
become proof or promotion authority by themselves.

The repository needs a repeatable live check without turning ordinary CI into a
model benchmark or letting a convenient aggregate score erase dispatch,
manual-policy, trajectory, owner-boundary, and transport failures.

## Options Considered

- Infer effectiveness from session mentions, generated trigger fixtures, and
  installed files only.
- Run broad model-backed checks automatically in CI and retain raw transcripts
  with repository reports.
- Keep deterministic harness validation in the normal test lane and require a
  source-locked, operator-confirmed, host-routed campaign for every live cohort.

## Decision

Choose the third option.

The live harness has four observable arms:

- paired implicit aided and no-skill control turns for dispatch and observed
  outcome lift;
- explicit root-to-child trajectories where the child `SKILL.md` read must be
  visible in transport events;
- structured App Server skill input, bound to an exact enabled skill path and
  the server-issued thread id;
- deterministic harness tests that validate all schemas, cohort expansion,
  adapters, privacy projection, and stop-lines without making model calls.

Live execution defaults to `plan`, binds model, effort, Git head, all portable
skill files, generated/config inputs, profile revision, Codex protocol revision,
caps, and trial identities into exact confirmation tokens, and requires a
second token for every cohort beyond smoke.

The source-locked caps include both the rollout token limit and its required
list of remaining-token reminder thresholds. Every CLI and App Server arm must
pass both values explicitly under strict config so an installed Codex contract
change fails in deterministic adapter tests or pre-turn smoke, not midway
through a campaign.

Planning also validates the model-output schema against the bounded Responses
API strict-output contract before issuing a confirmation token. Draft 2020-12
validity alone is insufficient because a locally valid `const` or `enum`
without an explicit type is rejected by the runtime API.

The run must execute inside `abyss-machine resource launch`; the runner verifies
the resource class, agent kind, and cgroup, independently requires a storage
write preflight for its private host-owned root, and stops on runtime drift,
privacy contamination, owner-boundary widening, or transport failure.

Raw prompts, events, transport identifiers, and model output remain in `0600`
files below the source-locked `0700` host-private root. Public receipts are
field-whitelisted projections with digests, per-arm observations, paired deltas,
failure classes, and review status. They publish no raw text and no aggregate
score.

## Rationale

This route measures different evidence stages without collapsing them. A skill
surface being present is not the same as being selected; structured input is
not the same as a full child read; a model load claim is not the same as
following the procedure; and a route-contract match is still reviewed candidate
evidence rather than central proof.

Source locks make a rerun comparable. Paired controls expose whether the skill
surface changed the observed route instead of crediting general model knowledge.
Host routing bounds resource and storage pressure. Private/raw and public/digest
separation keeps review possible without publishing session material.

## Consequences

- Positive: dispatch, manual reachability, structured selection, trajectory,
  and paired outcome-lift pressure can be reproduced against an exact source and
  runtime protocol.
- Positive: failures carry bounded adaptive return routes instead of one score.
- Positive: ordinary CI proves the harness contract without spending model
  turns or treating model quality as deterministic repository proof.
- Tradeoff: Codex App Server upgrades require an explicit protocol-contract and
  source-lock refresh before live use.
- Tradeoff: single cohort observations remain candidate evidence; review and
  repeated runs are needed before changing skill status or promotion posture.
- Follow-up: use reviewed smoke and pilot receipts to repair the smallest skill
  cohort first, then rerun affected downstream cohorts before widening to all
  57 skills.

## Current Applicability

As of 2026-07-11:

- Still valid: central verdict, scoring, regression, proof doctrine, and proof
  acceptance remain in `aoa-evals`.
- Still valid: `.aoa` raw session episodes remain reviewed candidate evidence,
  not automatic proof of skill use or success.
- Current protocol lock: `codex-cli 0.144.1` App Server skill input v1.
- Superseded by: none.

## Boundaries

This decision does not make `aoa-skills` a central model-evaluation owner. It
does not allow automatic skill promotion, public raw transcripts, unattended
high-cost cohorts, or execution of repository mutation tasks. A green route
receipt does not prove that every procedure step was followed or that the task
was completed outside the bounded fixture.

## Validation

- `python -m pytest -q tests/test_live_skill_dispatch_harness.py`
- `python scripts/lanes/ci_gate.py --mode source-fast`
- local eval-port validation through the current `aoa-evals` owner
- decision-index regeneration and parity check
- exact `codex --version`, App Server schema contract, resource-wrapper cgroup,
  and storage-preflight checks before a live turn
