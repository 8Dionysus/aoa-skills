# Skill walkthroughs

This derived file makes the runtime path concrete inside `aoa-skills`.
`SKILL.md` remains the meaning-authoritative source; walkthroughs are inspect aids.

## Shared inspection path

1. Open the capsule view for a fast bounded summary.
2. Open the sections view for source-owned expand-time reads.
3. Open the full `SKILL.md` only when section detail still is not enough.
4. Open the evidence view to inspect runtime examples and review surfaces.

Common inspection order:

- `capsule`
- `sections`
- `full`
- `evidence`

Common expand sections:

- `Procedure`
- `Contracts`
- `Risks and anti-patterns`
- `Verification`

## aoa-adr-write

- scope: `core`
- status: `evaluated`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-adr-write/SKILL.md`
- pick summary: Record a meaningful architectural or workflow decision so future changes can understand the rationale rather than only the outcome.

### Use when

- a decision changes structure, boundaries, tooling, or workflow expectations
- future contributors will need to know why a path was chosen
- several plausible options existed and the reasoning matters
- the team or project risks repeating the same debate later

### Do not use when

- the change is tiny and self-evident
- the note would only restate an obvious diff with no real decision content
- the main problem is unclear authoritative documentation rather than decision rationale; use aoa-source-of-truth-check first
- the main problem is deciding whether logic belongs in the core or at the edge; use aoa-core-logic-boundary first

### Object use shape

- concise decision note or ADR draft
- statement of rationale
- consequence notes
- verification that the note matches the actual change

### Support artifacts

- `runtime_example` (selected): `skills/aoa-adr-write/examples/example.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-adr-write.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-adr-write.md`

## aoa-approval-gate-check

- scope: `risk`
- status: `canonical`
- invocation mode: `explicit-only`
- skill path: `skills/aoa-approval-gate-check/SKILL.md`
- pick summary: Classify whether a requested action should proceed, wait for explicit approval, or be refused at the current authority level.

### Use when

- a task may be destructive, operationally sensitive, or security-relevant
- the current authority level is unclear
- the agent needs to classify whether the next step is safe, explicit-only, or out of bounds

### Do not use when

- the task is clearly low-risk and already bounded by an ordinary workflow
- no meaningful approval boundary exists in the current context
- the authority is already clear and the main need is choosing a preview path before execution; use aoa-dry-run-first
- the task is only about preparing a public-safe artifact for sharing; use aoa-sanitized-share

### Object use shape

- classification of the action: safe to proceed, explicit approval required, or do not execute
- note on whether explicit approval is needed
- bounded next-step recommendation
- report of unresolved authority assumptions

### Support artifacts

- `runtime_example` (selected): `skills/aoa-approval-gate-check/examples/runtime.md`
- `review_checklist`: `skills/aoa-approval-gate-check/checks/review.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-approval-gate-check.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-approval-gate-check.md`

## aoa-bounded-context-map

- scope: `core`
- status: `canonical`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-bounded-context-map/SKILL.md`
- pick summary: Clarify or carve system and domain boundaries so changes stay semantically scoped and interface-aware.

### Use when

- a project mixes several domains or subsystems
- naming is drifting or overloaded
- the task needs a clearer boundary before coding safely
- an agent is likely to confuse nearby concepts without sharper separation

### Do not use when

- the change is tiny and fully local
- the boundary is already clear and agreed on, and the real task is validating the interface contract; use aoa-contract-test
- the main problem is deciding whether logic belongs in the core or at the edge; use aoa-core-logic-boundary first

### Object use shape

- named contexts or subsystems
- rough boundary map
- interface notes between contexts
- ambiguity notes and recommended vocabulary

### Support artifacts

- `runtime_example` (selected): `skills/aoa-bounded-context-map/examples/example.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-bounded-context-map.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-bounded-context-map.md`

## aoa-change-protocol

- scope: `core`
- status: `canonical`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-change-protocol/SKILL.md`
- pick summary: Bounded workflow for Codex to plan a change, keep it scoped, verify it explicitly, and report it clearly.

### Use when

- the change affects code, config, docs, or operational surfaces in a meaningful way
- the task benefits from an explicit plan and verification path
- the task touches more than a trivial wording fix

### Do not use when

- the edit is tiny and has no meaningful review or operational consequence
- a more specific risk skill should be used instead

### Object use shape

- explicit plan
- scoped change
- named verification result
- concise final report

### Support artifacts

- `runtime_example` (selected): `skills/aoa-change-protocol/examples/runtime.md`
- `review_checklist`: `skills/aoa-change-protocol/checks/review.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-change-protocol.md`

## aoa-contract-test

- scope: `core`
- status: `canonical`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-contract-test/SKILL.md`
- pick summary: Design or extend contract-oriented validation at module, service, or workflow boundaries.

### Use when

- two modules or services interact across a meaningful boundary
- a smoke path or interface needs a stable validation contract
- a change risks breaking downstream assumptions

### Do not use when

- the change is entirely local and does not affect a meaningful boundary
- the boundary itself is still semantically unclear and naming is drifting; use aoa-bounded-context-map
- the main problem is expressing a broad invariant rather than a boundary contract; use aoa-property-invariants
- the main problem is auditing whether existing checks really cover a stable rule; use aoa-invariant-coverage-audit
- a broad system rewrite is needed before the boundary itself is stable

### Object use shape

- explicit contract assumptions
- tests or smoke summary changes
- verification notes
- downstream impact notes

### Support artifacts

- `runtime_example` (selected): `skills/aoa-contract-test/examples/example.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-contract-test.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-contract-test.md`

## aoa-core-logic-boundary

- scope: `core`
- status: `evaluated`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-core-logic-boundary/SKILL.md`
- pick summary: Clarify which logic belongs in the reusable core and which parts should remain glue, orchestration, or infrastructure detail.

### Use when

- a module mixes stable rules with wiring or execution detail
- the same logic is starting to appear in several places
- tests or reviews are muddy because the center of responsibility is unclear
- you need to decide whether something belongs in the core or at the edges

### Do not use when

- the task is a tiny isolated fix with no meaningful boundary ambiguity
- the code is already clearly partitioned
- the result would only rename folders without improving understanding
- the main problem is recording decision rationale rather than boundary placement; use aoa-adr-write first
- the boundary is already clear and the main task is introducing a port or adapter around a concrete dependency; use aoa-port-adapter-refactor

### Object use shape

- clarified boundary between core logic and surrounding glue
- notes on what should stay reusable versus edge-specific
- small refactor proposal or bounded implementation
- verification summary

### Support artifacts

- `runtime_example` (selected): `skills/aoa-core-logic-boundary/examples/example.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-core-logic-boundary.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-core-logic-boundary.md`

## aoa-dry-run-first

- scope: `risk`
- status: `evaluated`
- invocation mode: `explicit-only`
- skill path: `skills/aoa-dry-run-first/SKILL.md`
- pick summary: Prefer simulation, inspection, or preview paths before real execution for changes that can have meaningful operational consequences.

### Use when

- the task can be simulated, previewed, or inspected before real execution
- the action may delete, restore, migrate, reconfigure, or otherwise alter a live surface
- the cost of a mistaken execution is meaningfully higher than the cost of a preview step

### Do not use when

- no meaningful dry-run or preview path exists and the task is already clearly bounded and harmless
- the task is purely analytical and does not approach execution at all
- the central question is whether execution is authorized at all rather than how to preview it; use aoa-approval-gate-check
- the task is only about preparing a sanitized artifact for sharing; use aoa-sanitized-share

### Object use shape

- dry-run or preview recommendation
- bounded preview result or plan
- note on what the preview does and does not prove
- recommendation for next step

### Support artifacts

- `runtime_example` (selected): `skills/aoa-dry-run-first/examples/runtime.md`
- `review_checklist`: `skills/aoa-dry-run-first/checks/review.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-dry-run-first.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-dry-run-first.md`

## aoa-invariant-coverage-audit

- scope: `core`
- status: `canonical`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-invariant-coverage-audit/SKILL.md`
- pick summary: Audit whether existing tests or checks actually cover the stable invariants that matter, and identify the smallest bounded gaps that still leave example-only coverage too thin.

### Use when

- an existing test or check surface needs a review for invariant strength
- the question is whether current checks really constrain the stable rule
- you need to turn a loose example set into a bounded coverage audit

### Do not use when

- the main problem is defining the invariant itself rather than auditing coverage; use aoa-property-invariants first
- the invariant itself is still unknown and you need discovery work first
- the task is mostly about presentation details or a narrow snapshot
- you need a full boundary contract review rather than a coverage audit

### Object use shape

- invariant coverage map
- gap list for weak or missing checks
- bounded follow-up checks or revisions
- concise verification summary

### Support artifacts

- `runtime_example` (selected): `skills/aoa-invariant-coverage-audit/examples/example.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-invariant-coverage-audit.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md`

## aoa-port-adapter-refactor

- scope: `core`
- status: `evaluated`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-port-adapter-refactor/SKILL.md`
- pick summary: Refactor code toward clearer ports and adapters so reusable logic is less entangled with infrastructure details.

### Use when

- business or domain logic is tightly coupled to a concrete dependency
- tests are hard to write because external concerns leak into the core logic
- the same dependency pattern is beginning to repeat across modules
- a module needs a clearer seam before further change

### Do not use when

- the task is a tiny local fix with no architectural pressure
- there is no meaningful boundary to clarify yet
- the code would become more ceremonial than useful after extraction
- the main problem is deciding whether logic belongs in the core or at the edge; use aoa-core-logic-boundary first
- the main problem is clarifying repository docs or source-of-truth ownership; use aoa-source-of-truth-check first

### Object use shape

- clearer boundary between logic and infrastructure
- proposed or implemented port shape
- proposed or implemented adapter shape
- verification summary

### Support artifacts

- `runtime_example` (selected): `skills/aoa-port-adapter-refactor/examples/example.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-port-adapter-refactor.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md`

## aoa-property-invariants

- scope: `core`
- status: `canonical`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-property-invariants/SKILL.md`
- pick summary: Express stable system or domain truths as invariant-oriented tests and checks rather than only enumerating examples.

### Use when

- a rule should hold across many inputs or states
- examples alone feel too narrow
- the system has conservation, monotonicity, idempotency, or structural invariants
- safety or correctness depends on broad input coverage

### Do not use when

- the behavior is mostly about presentation details or narrow snapshots
- the main problem is checking whether existing checks really cover the invariant; use aoa-invariant-coverage-audit first
- the main problem is a boundary contract rather than a stable invariant; use aoa-contract-test
- no meaningful invariant is yet understood

### Object use shape

- explicit invariants
- property-oriented tests or checks
- notes on generator assumptions
- verification summary

### Support artifacts

- `runtime_example` (selected): `skills/aoa-property-invariants/examples/example.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-property-invariants.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-property-invariants.md`

## aoa-safe-infra-change

- scope: `risk`
- status: `evaluated`
- invocation mode: `explicit-only`
- skill path: `skills/aoa-safe-infra-change/SKILL.md`
- pick summary: Make bounded infrastructure or configuration changes with explicit risk framing, verification, and reversible execution discipline.

### Use when

- the task changes infrastructure, services, configuration, orchestration, or operational surfaces
- the change has runtime, safety, or deployment implications
- the task needs stronger verification and rollback thinking than a normal code edit

### Do not use when

- the task is a purely local code change with no operational implications
- a more specific risk skill should be used instead
- the operator has not provided enough authority for the requested action
- the main question is whether authority exists at all; use aoa-approval-gate-check
- the main need is to prefer or interpret a preview path before execution; use aoa-dry-run-first

### Object use shape

- explicit risk-aware plan
- bounded infrastructure or config change, or bounded execution recommendation
- verification result
- report with remaining risk notes

### Support artifacts

- `runtime_example` (selected): `skills/aoa-safe-infra-change/examples/runtime.md`
- `review_checklist`: `skills/aoa-safe-infra-change/checks/review.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-safe-infra-change.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-safe-infra-change.md`

## aoa-sanitized-share

- scope: `risk`
- status: `evaluated`
- invocation mode: `explicit-only`
- skill path: `skills/aoa-sanitized-share/SKILL.md`
- pick summary: Prepare findings, logs, examples, or diagnostics for sharing without leaking secrets, private topology, or unsafe operational detail.

### Use when

- logs, configs, diagnostics, reports, or examples may contain sensitive details
- a result needs to be shared publicly or with a broader audience
- raw material may reveal secrets, topology, internal identifiers, or unsafe context

### Do not use when

- the material is already clearly public-safe and minimal
- the task is to perform the underlying operational change rather than prepare a shareable surface
- the main task is deciding whether the underlying action should be allowed; use aoa-approval-gate-check
- the task is to preview or execute the operational change itself; use aoa-dry-run-first or aoa-safe-infra-change

### Object use shape

- sanitized shareable artifact, abstract summary, or recommendation not to share the raw material directly
- note on what was generalized or removed
- warning about any remaining ambiguity or sensitive edge

### Support artifacts

- `runtime_example` (selected): `skills/aoa-sanitized-share/examples/runtime.md`
- `review_checklist`: `skills/aoa-sanitized-share/checks/review.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-sanitized-share.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-sanitized-share.md`

## aoa-source-of-truth-check

- scope: `core`
- status: `evaluated`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-source-of-truth-check/SKILL.md`
- pick summary: Check whether repository guidance, canonical docs, and operational instructions have clear ownership and do not silently conflict.

### Use when

- a repository has several docs that may overlap or conflict
- contributors may not know which file to trust first
- a change touches docs, process, or operational guidance and the question is which file is authoritative
- confusion exists between overview docs and authoritative docs
- one authoritative source must stay aligned across multiple downstream consumer surfaces

### Do not use when

- the repository is tiny and has no meaningful source-of-truth ambiguity
- the task is purely code-local with no documentation or policy impact
- the authoritative files are already clear and the main need is recording rationale for a decision; use aoa-adr-write
- the main problem is deciding whether logic belongs in the core or at the edge; use aoa-core-logic-boundary first
- the main problem is broader policy design rather than document authority or ownership

### Object use shape

- clearer source-of-truth map
- fan-out map when one source feeds multiple downstream consumers
- note of overlaps or conflicts
- proposed or implemented document role clarification
- verification summary

### Support artifacts

- `runtime_example` (selected): `skills/aoa-source-of-truth-check/examples/example.md`
- `promotion_review`: `docs/reviews/status-promotions/aoa-source-of-truth-check.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-source-of-truth-check.md`

## aoa-tdd-slice

- scope: `core`
- status: `canonical`
- invocation mode: `explicit-preferred`
- skill path: `skills/aoa-tdd-slice/SKILL.md`
- pick summary: Implement a bounded feature slice through test-first discipline, minimal implementation, and explicit refactor boundaries.

### Use when

- a behavior change can be expressed as tests before implementation
- the task fits a bounded slice rather than a broad rewrite
- confidence and regression resistance matter

### Do not use when

- the task is purely exploratory and behavior is still undefined
- the task is mostly one-off glue with no reusable logic
- the main problem is a stable interface or boundary contract rather than a feature slice; use aoa-contract-test
- the main problem is invariant coverage rather than slice implementation; use aoa-property-invariants
- broader architectural restructuring is the real need

### Object use shape

- new or updated tests
- minimal implementation
- small refactor if needed
- verification summary

### Support artifacts

- `runtime_example` (selected): `skills/aoa-tdd-slice/examples/example.md`
- `candidate_review`: `docs/reviews/canonical-candidates/aoa-tdd-slice.md`

## atm10-change-protocol

- scope: `project`
- status: `scaffold`
- invocation mode: `explicit-preferred`
- skill path: `skills/atm10-change-protocol/SKILL.md`
- pick summary: Thin atm10 overlay for bounded change execution with repo-relative paths, commands, and explicit local approval notes.

### Use when

- the base aoa-change-protocol workflow is already correct, but an atm10- repo needs repo-relative paths, commands, or local approval notes
- a bounded non-trivial change still needs an explicit plan and verification path inside the local repo
- a contributor needs a thin local overlay rather than a fresh workflow design

### Do not use when

- the task really needs a broader playbook or scenario bundle rather than a thin overlay
- the work would introduce new upstream technique meaning instead of adapting the local repo surface
- a more specific risk skill is still the clearer fit, such as aoa-dry-run-first, aoa-safe-infra-change, or aoa-approval-gate-check
- the task does not need repo-relative local adaptation and the base skill can be used directly

### Object use shape

- bounded local change plan
- repo-relative command or path sketch
- verification note for the local repo surface
- concise handoff on what stays downstream and explicit

### Support artifacts

- `runtime_example` (selected): `skills/atm10-change-protocol/examples/example.md`

## atm10-source-of-truth-check

- scope: `project`
- status: `scaffold`
- invocation mode: `explicit-preferred`
- skill path: `skills/atm10-source-of-truth-check/SKILL.md`
- pick summary: Thin atm10 overlay for clarifying repo-local document authority, canonical files, and review posture without changing the base workflow.

### Use when

- the base aoa-source-of-truth-check workflow is already correct, but an atm10- repo needs local canonical-file patterns, repo-relative docs, or doc review rules
- contributors need a thin overlay that maps repo-relative docs such as README.md, docs/ARCHITECTURE.md, or docs/[canonical-guide].md
- confusion exists between overview docs and authoritative files inside one local repo

### Do not use when

- the main need is broader policy design rather than local document authority mapping
- the task is purely code-local and has no meaningful docs or guidance ambiguity
- the work would introduce new upstream technique meaning instead of thin local adaptation
- the main need is recording rationale for a decision rather than clarifying authority; use aoa-adr-write

### Object use shape

- local source-of-truth map
- bounded clarification note
- repo-relative canonical-file pattern
- verification summary for the local docs surface

### Support artifacts

- `runtime_example` (selected): `skills/atm10-source-of-truth-check/examples/example.md`

