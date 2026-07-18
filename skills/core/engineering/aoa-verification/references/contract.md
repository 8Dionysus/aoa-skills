# Verify a consumer contract

### Mode: contract

Use this mode when a named producer-consumer seam exposes a stable module,
service, CLI, schema, manifest, receipt, report, generated/export surface,
workflow handoff, tool result, or repo-to-repo ABI. Do not use it for a private
implementation detail, an unnamed consumer, an unresolved semantic boundary,
or a broad invariant better expressed as a property.

Required inputs:

- producer, named consumer, authoritative contract source, version posture
- inputs, outputs, errors, effects, compatibility, limits, and out-of-contract
  behavior
- manual expected, rejected, and motivating failure cases
- current named verification surface when one exists

Return a `contract-evidence-package` containing the explicit seam, protected
consumers, cases, oracle, current evidence, smallest authorized durable check or
no-check decision, downstream impact, claim limit, and stop line.

Procedure:

1. Establish the source-owned boundary and named consumers. Stop
   `blocked_missing_input` when either is unknown.
2. State inputs, outputs, behavior, errors, effects, compatibility, reporting
   shape, and what remains outside the contract.
3. Reproduce the motivating break or reconstruct why it would matter, then
   exercise at least one accepted and one rejected case manually.
4. Inspect the existing named check when present. Execute it only when the run
   adds evidence not already established by the manual cases and check source.
   If it cannot run in the current read-only environment without writes,
   missing infrastructure, or altered framework settings, record
   `not_executed` instead of retrying unless check execution is itself the
   requested task. If discovery or selection is required, hand off to
   `aoa-eval`; do not choose by filename prominence.
5. Add or revise a durable check only when the seam is stable, recurrence is
   real, the oracle is independent, and the write is explicitly authorized.
6. Ensure the check rejects the observed break before it accepts owner-approved
   behavior; separately verify reporting and consumer-visible failure shape.

Operational shapes:

When the seam is wider than an ordinary module or service interface, choose
the narrowest shape below. Use one producer, one named consumer, one stable
expectation, and one honest validation surface; do not treat the table as a
checklist.

| Shape | Producer | Consumer | Validate | Do not claim |
|---|---|---|---|---|
| Module, service, or API | Function, package, service, or endpoint. | Caller, client, downstream service, or workflow. | Input/output shape, errors, status, effects, compatibility smoke. | Internal implementation details are public contract. |
| CLI or tool report | Command, script, or local tool. | Automation, CI, another script, or operator workflow. | Flags, exit code, machine-readable output, report fields, failure mode. | Human log wording is stable unless explicitly documented. |
| Schema, manifest, or registry | Authored schema, config, registry, or manifest builder. | Validator, router, SDK, generated reader, or release check. | Required fields, version, enum, reference resolution, invalid-fixture failure. | Incidental field order or formatting is semantic truth. |
| Source to generated/export | Source-owned file, builder, or canonical bundle. | Generated catalog, export, adapter, or compact capsule consumer. | Field mapping, rebuild behavior, source ref, and declared freshness rule. | Generated output owns the meaning it summarizes. |
| Practice object or handoff | Practice atom, topology, capsule, or practice-to-skill bridge. | Execution skill, routing, eval, retrieval substrate, or downstream practice consumer. | Stable ID, object shape, topology fields, selected sections, handoff payload. | A practice object is automatically a skill, eval, role, memory object, or scenario. |
| Skill bundle or export | Canonical skill bundle and export builder. | Runtime, SDK, router, pack profile, or installed skill surface. | Metadata, trigger boundary, support refs, export path, trigger behavior. | An installed copy replaces authored bundle truth. |
| Eval proof or report | Eval bundle, runner, scorer, or verdict emitter. | Review gate, release support, metric summary, or regression reader. | Claim limit, fixture shape, scoring logic, verdict schema, report fields. | One eval proves total quality or intelligence. |
| Role contract or runtime seam | Profile, role contract, projection builder, or runtime binding. | Scenario, SDK, runtime harness, or handoff consumer. | Role fields, authority limits, handoff payload, projection artifact. | Role text grants hidden runtime authority. |
| Memory recall or writeback | Memory object, recall contract, writeback envelope, or retrieval export. | Router, retrieval substrate, eval, agent, or closeout workflow. | Inspect/capsule/expand shape, source refs, provenance, retention limit. | Recall output is fresh proof or live memory authority by itself. |
| Scenario or reentry | Scenario route, review packet, stress lane, or reentry gate. | Agent, routing, metrics, runtime, or follow-through workflow. | Phase route, handoff, fallback, evidence expectation, reentry fields. | A recurring scenario is a single skill or live runtime ledger. |
| Routing or SDK typed seam | Router hint, owner dispatch seam, SDK facade, CLI report, or typed loader. | Agent, script, CI, notebook, or downstream adapter. | Typed fields, owner refs, dispatch result, compatibility result, error report. | Routing or SDK owns the source meaning it points to. |
| Metrics receipt or summary ABI | Receipt publisher, shared envelope, event-kind registry, or summary builder. | Metric summary, dashboard, closeout, routing, or review reader. | Envelope fields, event kind, supersession, active view, summary schema. | Summary counts are owner truth or final promotion verdict. |

Compact contract pass:

| Field | Answer |
|---|---|
| Producer | |
| Named consumer | |
| Stable expectation | |
| Validation surface and oracle | |
| Out of contract | |
| Downstream impact if broken | |
| Source owner remains | |

Contracts and risks:

- consumer convenience, generated output, logs, snapshots, and current field
  order cannot become source authority
- one contract check protects one seam, not the whole system or federation
- avoid vague constraints, incidental internals, unnamed consumers, and
  broadening one local contract into universal law

Verify producer and consumer identity, source authority, accepted/rejected
cases, downstream impact, independent oracle, and the exact claim limit.
