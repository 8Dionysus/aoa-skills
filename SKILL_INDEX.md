# SKILL_INDEX

This file is the repository-wide map of public skills.

## Current skills

| name | scope | status | summary |
|---|---|---|---|
| aoa-change-protocol | core | canonical | Skill for bounded change execution using plan, scoped edits, validation, and concise reporting. |
| aoa-commit-growth-seam | core | scaffold | Skill for turning a validated bounded diff into one intentional local commit with explicit scope review and a visible stop line before push or publish. |
| aoa-memo-writeback | core | scaffold | Skill for deciding whether session evidence and landed-work context should become a local memo candidate, reviewed-intake export, or explicit no-writeback stop line. |
| aoa-tdd-slice | core | canonical | Skill for implementing a small feature slice through test-first change discipline. |
| aoa-contract-test | core | canonical | Skill for designing or extending contract-oriented validation at service or module boundaries. |
| aoa-bounded-context-map | core | canonical | Skill for carving or clarifying domain or system boundaries and their interfaces. |
| aoa-property-invariants | core | canonical | Skill for expressing domain or system invariants as property-oriented tests and checks. |
| aoa-invariant-coverage-audit | core | canonical | Skill for auditing whether existing checks actually constrain the stable invariants that matter, and for reporting the smallest bounded gaps. |
| aoa-approval-gate-check | risk | canonical | Skill for classifying whether a requested action should proceed, wait for explicit approval, or be refused. |
| aoa-adr-write | core | canonical | Skill for recording a meaningful architectural or workflow decision with rationale and tradeoffs. |
| aoa-decision | core | evaluated | Router for decision-lane work that checks the workspace decision graph first, then selects the smallest find, create, or correct path. |
| aoa-decision-find | core | evaluated | Skill for graph-first decision lookup with source-note verification before claims become task context. |
| aoa-decision-create | core | evaluated | Skill for creating repo-local decision records with related graph context, local index rebuild, and graph refresh. |
| aoa-decision-correct | core | evaluated | Skill for correcting, superseding, or reindexing source decision notes before refreshing generated indexes and the workspace graph. |
| aoa-eval | core | scaffold | Router for eval-lane work that selects existing eval inspection, application, local intake pressure, design, or session mining while preserving owner boundaries. |
| aoa-eval-select | core | scaffold | Skill for inspecting central and repo-local eval surfaces before new eval work. |
| aoa-eval-apply | core | scaffold | Skill for running or routing an already selected eval, validator, test, or script and reporting evidence limits. |
| aoa-eval-local-need | core | scaffold | Skill for creating bounded repo-local eval need packets when no existing eval fits. |
| aoa-eval-design | core | scaffold | Skill for designing local eval suites or reports without claiming central proof authority. |
| aoa-eval-session-mining | core | scaffold | Skill for mining `.aoa` session evidence for missed eval triggers after web and repo owner gates. |
| aoa-automation-opportunity-scan | core | scaffold | Skill for detecting reviewed or repeated project processes that are candidates for automation, classifying whether they are seed-ready, and routing them to the right owner layer without granting schedule or mutation authority. |
| aoa-core-logic-boundary | core | evaluated | Skill for clarifying which logic belongs in the reusable core versus glue, orchestration, or infrastructure detail. |
| aoa-port-adapter-refactor | core | evaluated | Skill for refactoring toward clearer ports and adapters so reusable logic is less entangled with infrastructure details. |
| aoa-quest-harvest | core | scaffold | Skill for giving the final promotion verdict on one repeated reviewed quest unit without collapsing skills, playbooks, orchestrator classes, proof, or memory into one layer. |
| aoa-checkpoint-closeout-bridge | core | scaffold | Skill for bridging provisional checkpoint evidence into one explicit reviewed-closeout execution chain without turning notes into final authority. |
| aoa-session-donor-harvest | core | scaffold | Skill for turning a reviewed session into a bounded HARVEST_PACKET, routing reusable units to the right AoA owner layer, and handing off to the next honest post-session skill when needed. |
| aoa-session-route-forks | core | scaffold | Skill for turning reviewed session evidence into explicit next-route forks with likely gains, costs, risks, owner targets, and stop conditions. |
| aoa-session-self-diagnose | core | scaffold | Skill for classifying drift, friction, proof gaps, and ownership confusion from a reviewed session into a bounded diagnosis packet without mutating anything yet. |
| aoa-session-self-repair | core | scaffold | Skill for turning a reviewed diagnosis packet into the smallest honest repair packet with checkpoint posture, rollback markers, and explicit owner-layer targets. |
| aoa-session-progression-lift | core | scaffold | Skill for lifting reviewed session evidence into a bounded multi-axis progression delta with explicit unlock hints and no fake single-score authority. |
| aoa-source-of-truth-check | core | canonical | Skill for checking whether canonical docs and repository guidance have clear ownership and do not silently conflict. |
| aoa-summon | core | scaffold | Skill for delegating one bounded child route through quest-passport law, local coding-agent execution defaults, hard gates, governed return, and checkpoint-aware reviewed closeout planning. |
| abyss-safe-infra-change | project | evaluated | Thin abyss overlay for bounded infrastructure or configuration changes with repo-relative operational surfaces, explicit local authority, and reviewable risk notes. |
| abyss-sanitized-share | project | evaluated | Thin abyss overlay for turning raw repo-local technical material into a shareable public-safe surface with explicit local thresholds and canonical placement notes. |
| abyss-self-diagnostic-spine | project | scaffold | Thin abyss overlay for turning runtime-body evidence plus optional reviewed session references into one bounded diagnostic session artifact and an honest next-move class without granting silent self-mutation. |
| os-abyss-artifact-trust-loop | project | scaffold | OS Abyss artifact-trust loop for routing ABI, provenance, signatures, SBOM, C2PA, drift, and consumer gates through abyss-machine read models and owner-local producers. |
| atm10-change-protocol | project | evaluated | Thin atm10 overlay for bounded change execution with repo-relative paths, commands, and explicit local approval notes. |
| atm10-source-of-truth-check | project | evaluated | Thin atm10 overlay for clarifying repo-local document authority, canonical files, and review posture without changing the base workflow. |
| aoa-local-stack-bringup | risk | evaluated | Skill for reviewable local multi-service bring-up through rendered runtime truth, readiness checks, and one explicit lifecycle path. |
| aoa-dry-run-first | risk | canonical | Skill for preferring simulation, inspection, or preview paths before real execution with operational consequences. |
| aoa-safe-infra-change | risk | canonical | Skill for making bounded infrastructure or configuration changes with explicit risk framing and reversible execution discipline. |
| aoa-sanitized-share | risk | canonical | Skill for preparing findings, logs, or diagnostics for sharing without leaking secrets or private operational detail. |
| titan-approval-ledger | project | scaffold | Record explicit operator approval for Forge mutation or Delta judgment gates without treating approval records as owner truth. |
| titan-approval-loom | project | scaffold | Maintain the app-server bridge approval queue while preserving Forge and Delta gates, receipts, and visible operator intent. |
| titan-appserver-bridge | project | scaffold | Operate the Titan app-server bridge as inspectable thread, turn, event, approval, replay, and metrics state without hidden execution. |
| titan-appserver-plan | project | scaffold | Generate an inspectable Titan app-server launch plan as JSONL or equivalent plan output without starting hidden agent execution. |
| titan-closeout | project | scaffold | Close a Titan service-cohort session with role, risk, provenance, gate, verification, and next-owner summary. |
| titan-console | project | scaffold | Open or maintain a visible Titan operator-console state while keeping Forge and Delta locked until approvals exist. |
| titan-event-replay | project | scaffold | Replay Titan bridge or console events into inspectable state without granting runtime authority to the replay result. |
| titan-memory-loom | project | scaffold | Initialize or update Titan Memory Loom records as candidate memory with source refs, confidence, and authority warnings. |
| titan-memory-prune | project | scaffold | Propose redaction, tombstone, or pruning candidates for Titan memory without silent deletion or canon rewrite. |
| titan-mutation-gate | project | scaffold | Gate Forge workspace-write work with explicit intent, target paths, prechecks, validation, and rollback or stop posture. |
| titan-recall | project | scaffold | Retrieve Titan candidate memory records with source, record id, authority note, confidence, and verification path. |
| titan-receipt | project | scaffold | Create, validate, note, or close Titan session receipts as witnesses rather than final truth. |
| titan-runtime-gate | project | scaffold | Activate Forge mutation or Delta judgment lanes only through matching explicit runtime gates on a Titan receipt. |
| titan-summon | project | scaffold | Begin an explicit Titan service-cohort session with Atlas, Sentinel, and Mneme active and Forge or Delta locked. |
| titan-thread-turn-binding | project | scaffold | Bind Titan bridge events, approvals, and replay state to explicit thread and turn ids for inspectable continuity. |


## Project-Core Skill Kernel

The permanent project-core session-growth kernel in this repo is:

- `aoa-session-donor-harvest`
- `aoa-automation-opportunity-scan`
- `aoa-session-route-forks`
- `aoa-session-self-diagnose`
- `aoa-session-self-repair`
- `aoa-session-progression-lift`
- `aoa-quest-harvest`

This kernel is authored under `repo-project-core-kernel`. The older
`repo-session-harvest-family` profile remains as a backward-compatible
operational alias for the same seven-skill surface.

The kernel is repo-wide hard-gated:

- each kernel skill must keep its detail receipt schema
- each kernel skill must keep the shared core receipt schema
- the portable export must carry both refs
- the per-skill gate truth lives in `generated/project_core_kernel_governance.min.json`

## Project-Core Outer Ring

The next stable layer around that kernel is the engineering outer ring:

- `aoa-adr-write`
- `aoa-source-of-truth-check`
- `aoa-decision`
- `aoa-decision-find`
- `aoa-decision-create`
- `aoa-decision-correct`
- `aoa-bounded-context-map`
- `aoa-core-logic-boundary`
- `aoa-port-adapter-refactor`
- `aoa-change-protocol`
- `aoa-tdd-slice`
- `aoa-contract-test`
- `aoa-property-invariants`
- `aoa-invariant-coverage-audit`

This ring is authored under `repo-project-core-outer-ring`. It is not a second
kernel. It is the reusable engineering workbench that sits around the
session-growth nucleus.

The outer ring is soft-gated and classification-backed:

- every ring skill must stay in the authored outer-ring manifest
- `repo-project-core-outer-ring` must match that manifest exactly
- `repo-core-only` must equal `kernel + outer ring` in canonical order
- every ring skill must stay `scope=core`
- every ring skill must stay `status=canonical` or `status=evaluated`
- the per-skill readiness truth lives in `generated/project_core_outer_ring_readiness.min.json`

## Project Risk Guard Ring

The next stable layer outside project-core is the explicit risk guard ring:

- `aoa-approval-gate-check`
- `aoa-dry-run-first`
- `aoa-local-stack-bringup`
- `aoa-safe-infra-change`
- `aoa-sanitized-share`

This ring is authored under `repo-project-risk-guard-ring`. The older
`repo-risk-explicit` profile remains as a backward-compatible alias for the
same five-skill safety perimeter.

The risk guard ring is repo-wide hard-gated:

- every risk-ring skill must stay in the authored manifest
- `repo-project-risk-guard-ring` must match that manifest exactly
- `repo-risk-explicit` must stay an exact alias of the same surface
- `repo-default` must continue to carry the whole risk guard ring
- every risk-ring skill must stay `scope=risk`
- every risk-ring skill must stay `status=canonical` or `status=evaluated`
- every risk-ring skill must stay `invocation_mode=explicit-only`
- every risk-ring skill must stay in the `safety-and-mutation-gating` collision family
- the per-skill gate truth lives in `generated/project_risk_guard_ring_governance.min.json`

`repo-core-only` remains the umbrella profile for project-core only. The risk
guard ring sits outside project-core, and project overlays stay outside all
three layers.

## Project Foundation

The baseline project install layer is now `repo-project-foundation`:

- `project-core kernel`
- `project-core outer ring`
- `project risk guard ring`

That means:

- `repo-project-foundation` equals `kernel + outer ring + risk guard ring` in canonical order
- it intentionally excludes `abyss-*` and `atm10-*` overlays
- it is the stable baseline for repo-local rollout and `/srv/AbyssOS/.agents/skills`
- it does not replace `repo-default`, which remains the wider profile that can still carry overlays

## Notes

- `scaffold` means the skill shape exists, but it should still evolve through technique linkage, examples, and project overlays.
- `evaluated` means behavior-oriented evidence exists through autonomy checks and trigger-boundary fixtures.
- `canonical` means the skill is the current default public reference for its workflow class with explicit promotion rationale.
- the documented maturity ladder is `scaffold`, `linked`, `reviewed`, `evaluated`, `canonical`, and `deprecated`.
