# Separate reusable core logic

### Mode: core

Use this mode when a stable rule, mapping, scoring decision, transformation, or
contract is mixed with glue, orchestration, I/O, projection, rendering,
infrastructure, or presentation. Do not use it when owner/context is unresolved
enough to change the meaning, when no stable rule exists, or when the only
pressure is an already-understood concrete dependency seam.

Required inputs:

- target slice and target-specific owner or explicit unresolved owner edge
- stable-rule evidence, repetition or change pressure, surrounding edge work
- callers, consumers, compatibility constraints, and current behavior

Return a `core-logic-boundary` containing the reusable center, edge
responsibilities, inputs/outputs, compatibility projection, smallest migration
edge, verification need, unresolved questions, and stop line.

Procedure:

1. Identify the rule that survives delivery mechanisms. Do not promote code to
   the core merely because it contains conditionals.
2. Separate loading, policy selection, orchestration, persistence, transport,
   runtime discovery, generated/export writing, and rendering from the rule.
3. Define the smallest purpose-shaped input and output for the reusable center;
   do not freeze an incidental current representation as the domain model.
4. Preserve the current caller contract through a narrow delegation or
   compatibility projection when possible.
5. Propose or perform only the bounded extraction authorized by the task. Keep
   unrelated structure and cleanup out.
6. Name what future changes update together and what remains independent.

Core-boundary shapes:

Choose the narrowest row that fits the observed pressure. This is a routing
aid, not a checklist and not permission to introduce a new layer.

| Shape | Reusable center | Edge or glue | Do not promote | Verify |
|---|---|---|---|---|
| Code module or service slice | Stable rule, calculation, policy, state transition, or selection logic. | Parsing, retries, logging, persistence, transport, scheduling, and environment paths. | Delivery mechanics as domain truth. | Core cases stay small; edge behavior remains covered separately. |
| Skill bundle | Portable trigger, procedure, ABI, risks, and verification posture. | Installed projection, profile metadata, local overlay, runtime discovery. | Exported copy or router hint as skill truth. | Authored package remains source and projection refresh is deterministic. |
| Practice object | Atomic move, invariant posture, or reusable pattern. | Origin notes, examples, promotion notes, topology metadata. | Practice as skill, workflow, eval, role, or runtime law. | Core move stays stable while support notes remain explanatory. |
| Eval bundle | Scoring rule, proof contract, claim limit, and verdict semantics. | Fixture loading, report layout, rendering, runner plumbing. | Polished report text as proof logic. | Score-rule change is distinguishable from report churn. |
| Role contract | Authority limits, handoff posture, and collaboration mode. | Prompt projection, model routing, runtime binding, UI labels. | Runtime projection as hidden role authority. | Role source remains reviewable apart from projection glue. |
| Memory or provenance surface | Recall rule, writeback envelope, provenance, and retention boundary. | Storage adapter, index, cache, ranking, retrieval/export plumbing. | Retrieved text or cache as memory authority. | Provenance and retention survive storage changes. |
| Scenario or playbook | Recurring route, phase order, fallback, and evidence expectation. | Run notes, logs, scheduler hooks, orchestration scripts. | Recipe as hidden runtime engine. | Scenario can be reviewed without replaying a local run. |
| Routing or SDK seam | Typed loader, owner dispatch, compatibility, or facade contract. | CLI flags, formatting, local discovery, wrappers. | Router or SDK as owner of pointed-to meaning. | Typed behavior survives wrapper changes. |
| Metrics or receipt surface | Event envelope, receipt semantics, supersession, and active-view contract. | Dashboard rendering, summary prose, display aggregation, export packaging. | Counts or charts as owner verdict. | Envelope and claim limits survive report changes. |
| Generated or export builder | Source-to-output mapping, freshness check, and source-ref preservation. | Artifact bytes, compact formatting, sort order, install path. | Generated output as source-owned meaning. | Rebuild proves mapping while source remains stronger. |
| Mechanics or process docs | Local contract, part boundary, roadmap rule, and landing relation. | Legacy notes, logs, status prose, staging, folder ceremony. | Roadmap or provenance as active contract. | Active contract stays local and legacy remains historical. |
| Session or workflow surface | Stable phase order, stop condition, review gate, and handoff. | Checkpoint note, shell command, transcript detail, one-session evidence. | One trace as universal workflow law. | Reusable phase survives while local evidence stays evidence. |

Compact output shape:

| Field | Required content |
|---|---|
| Context already understood | The bounded owner/context whose meaning is stable enough to proceed. |
| Reusable center | Exact rule or behavior that survives delivery mechanisms. |
| Edge or glue | I/O, orchestration, projection, runtime, or presentation responsibilities. |
| Inputs and outputs | Small purpose-shaped ABI that avoids freezing incidental representation. |
| Compatibility projection | How current callers continue without hiding a rewrite. |
| Source owner | Exact owner declaration or unresolved edge. |
| Migration edge | Smallest authorized extraction or proposal. |
| Verification surface | Manual cases and separate edge checks required. |
| Future update rule | What changes together and what remains independent. |
| Stop line | What the current task must not restructure. |

Contracts and risks:

- derived, generated, adapter, report, and presentation surfaces never become
  source authority through convenience
- reusable does not mean universal; glue must not be relabeled as domain logic
- avoid broad rewrites, folder-only architecture, or purity that moves
  orchestration into the core

Verify that the rule is genuinely stability-shaped, the edge work remains at
the edge, caller behavior and effects stay compatible, no unrelated churn was
introduced, and unresolved owner or domain questions remain explicit.
