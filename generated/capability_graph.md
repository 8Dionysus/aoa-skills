# Capability graph

Derived from `capabilities/families/*.yaml`. This file is a read model, not capability authority.

Source content hash: `3f15214684067194c7f55095867ebed779b7237485642364fd189bbe38b06602`

## Semantic tree

- `aoa` (capability, deferred, challenger)
  - `engineering` (capability, deferred, challenger)
    - `engineering.evaluation` (capability, deferred, challenger)
      - `mode.eval.apply` (mode, internal, challenger)
      - `mode.eval.design` (mode, internal, challenger)
      - `mode.eval.local-need` (mode, internal, challenger)
      - `mode.eval.select` (mode, internal, challenger)
      - `mode.eval.session-mining` (mode, internal, challenger)
      - `skill.aoa-eval` (skill, advertised, challenger)
      - `skill.aoa-evals` (skill, advertised, challenger)
    - `engineering.measurement` (capability, deferred, challenger)
      - `skill.aoa-stats` (skill, advertised, challenger)
    - `engineering.shape` (capability, deferred, challenger)
      - `mode.engineering-shape.contexts` (mode, internal, challenger)
      - `mode.engineering-shape.core` (mode, internal, challenger)
      - `mode.engineering-shape.port-adapter` (mode, internal, challenger)
      - `skill.aoa-engineering-shape` (skill, deferred, degraded)
    - `engineering.verification` (capability, deferred, challenger)
      - `mode.verification.contract` (mode, internal, challenger)
      - `mode.verification.coverage-audit` (mode, internal, challenger)
      - `mode.verification.property` (mode, internal, challenger)
      - `skill.aoa-verification` (skill, deferred, degraded)
  - `operations` (capability, deferred, challenger)
    - `operations.change` (capability, deferred, healthy)
      - `workflow.operations.git-closeout` (workflow, internal, unavailable)
      - `workflow.operations.local-commit` (workflow, deferred, healthy)
      - `workflow.operations.repository-change` (workflow, deferred, healthy)
      - `workflow.operations.tdd-slice` (workflow, deferred, healthy)
    - `operations.continuity` (capability, deferred, healthy)
      - `workflow.operations.checkpoint-closeout` (workflow, deferred, healthy)
      - `workflow.operations.delegation` (workflow, deferred, healthy)
    - `operations.safety` (capability, deferred, healthy)
      - `guard.operations.approval` (guard, deferred, healthy)
      - `guard.operations.preview` (guard, internal, unavailable)
      - `workflow.operations.local-stack-bringup` (workflow, internal, unavailable)
      - `workflow.operations.safe-infra-change` (workflow, internal, unavailable)
  - `projects` (capability, deferred, challenger)
    - `projects.abyss` (capability, deferred, challenger)
      - `adapter.abyss.safe-infra-change` (adapter, deferred, healthy)
      - `adapter.abyss.sanitized-share` (adapter, deferred, healthy)
      - `projects.abyss.artifact-trust` (capability, deferred, healthy)
        - `adapter.abyss.artifact-trust` (adapter, deferred, healthy)
        - `skill.os-abyss-artifact-trust-loop` (skill, advertised, challenger)
      - `projects.abyss.diagnose-runtime` (capability, deferred, challenger)
        - `adapter.abyss.diagnostic-review` (adapter, deferred, challenger)
        - `skill.abyss-self-diagnostic-spine` (skill, advertised, challenger)
        - `tool.abyss.aoa-diagnose` (tool, internal, healthy)
    - `projects.atm10` (capability, deferred, healthy)
      - `adapter.atm10.authority-map` (adapter, deferred, healthy)
      - `adapter.atm10.repository-change` (adapter, deferred, healthy)
    - `projects.titan` (capability, deferred, challenger)
      - `projects.titan.session` (capability, deferred, challenger)
        - `projects.titan.session.closeout-audit` (capability, deferred, degraded)
          - `guard.titan.closeout-readiness` (guard, internal, unavailable)
          - `human-gate.titan.closeout` (human-gate, internal, unavailable)
          - `tool.titan.swarm-validate` (tool, internal, degraded)
          - `workflow.titan.closeout-audit` (workflow, internal, degraded)
        - `projects.titan.session.control` (capability, deferred, healthy)
          - `guard.titan.thread-turn-binding` (guard, internal, unavailable)
          - `skill.titan-appserver-bridge` (skill, advertised, challenger)
          - `skill.titan-console` (skill, advertised, challenger)
          - `tool.titan.approval-queue` (tool, internal, healthy)
          - `tool.titan.approval-record` (tool, internal, healthy)
          - `tool.titan.appserver-bridge` (tool, internal, healthy)
          - `tool.titan.appserver-plan` (tool, internal, healthy)
          - `tool.titan.console` (tool, internal, healthy)
          - `tool.titan.event-replay` (tool, internal, healthy)
          - `tool.titan.receipt` (tool, internal, healthy)
        - `projects.titan.session.memory` (capability, deferred, healthy)
          - `skill.titan-memory-loom` (skill, advertised, challenger)
          - `tool.titan.memory-ingest` (tool, internal, healthy)
          - `tool.titan.memory-recall` (tool, internal, healthy)
          - `tool.titan.memory-retention` (tool, internal, healthy)
      - `projects.titan.summon` (capability, deferred, healthy)
        - `guard.titan.mutation` (guard, internal, unavailable)
        - `guard.titan.runtime-transition` (guard, internal, unavailable)
        - `workflow.titan.summon` (workflow, internal, healthy)
  - `sessions` (capability, deferred, challenger)
    - `sessions.checkpoint-closeout` (capability, deferred, challenger)
      - `mode.checkpoint-closeout.collect` (mode, internal, challenger)
      - `mode.checkpoint-closeout.execute` (mode, internal, challenger)
      - `skill.aoa-checkpoint-closeout-bridge` (skill, advertised, challenger)
    - `sessions.harvest` (capability, deferred, challenger)
      - `mode.session-harvest.automation-opportunity` (mode, internal, challenger)
      - `mode.session-harvest.branch` (mode, internal, challenger)
      - `mode.session-harvest.classify` (mode, internal, challenger)
      - `mode.session-harvest.extract` (mode, internal, challenger)
      - `mode.session-harvest.promote` (mode, internal, challenger)
      - `skill.aoa-session-harvest` (skill, advertised, challenger)
    - `sessions.memo-writeback` (capability, deferred, challenger)
      - `skill.aoa-memo-writeback` (skill, advertised, challenger)
    - `sessions.recovery` (capability, deferred, challenger)
      - `mode.session-recovery.diagnose` (mode, internal, challenger)
      - `mode.session-recovery.repair` (mode, internal, challenger)
      - `skill.aoa-session-recovery` (skill, advertised, challenger)
    - `skill.aoa-session-progression-lift` (skill, advertised, challenger)
    - `skill.aoa-summon` (skill, advertised, challenger)
  - `stewardship` (capability, deferred, challenger)
    - `stewardship.decisions` (capability, deferred, challenger)
      - `mode.decision.correct` (mode, internal, challenger)
      - `mode.decision.find` (mode, internal, challenger)
      - `mode.decision.record` (mode, internal, challenger)
      - `skill.aoa-decision` (skill, advertised, challenger)
    - `stewardship.knowledge` (capability, deferred, challenger)
      - `mode.knowledge.authority-map` (mode, internal, challenger)
      - `mode.knowledge.sanitized-share` (mode, internal, challenger)
      - `skill.aoa-knowledge-stewardship` (skill, advertised, challenger)
      - `stewardship.knowledge.memory` (capability, deferred, challenger)
        - `skill.aoa-memo` (skill, advertised, challenger)
      - `stewardship.knowledge.retrieve` (capability, deferred, challenger)
        - `skill.aoa-kag` (skill, advertised, challenger)

## Typed relations

| kind | source | target | condition |
|---|---|---|---|
| adapted-by | `mode.knowledge.authority-map` | `adapter.atm10.authority-map` | - |
| adapted-by | `mode.knowledge.sanitized-share` | `adapter.abyss.sanitized-share` | - |
| adapted-by | `workflow.operations.checkpoint-closeout` | `skill.aoa-checkpoint-closeout-bridge` | The owner playbook remains scenario authority but lacks an executable aoa-playbooks MCP route. |
| adapted-by | `workflow.operations.repository-change` | `adapter.atm10.repository-change` | - |
| adapted-by | `workflow.operations.safe-infra-change` | `adapter.abyss.safe-infra-change` | - |
| alternative-to | `mode.decision.find` | `mode.decision.correct` | - |
| alternative-to | `mode.decision.find` | `mode.decision.record` | - |
| alternative-to | `mode.decision.record` | `mode.decision.correct` | - |
| composes-with | `mode.engineering-shape.core` | `mode.verification.property` | The extracted core exposes a stable semantic property across inputs. |
| composes-with | `mode.engineering-shape.port-adapter` | `mode.verification.contract` | The new port is adopted as a stable consumer-visible boundary. |
| composes-with | `skill.aoa-session-progression-lift` | `skill.aoa-summon` | An owner-reviewed progression or unlock posture is required by the anchored summon. |
| composes-with | `skill.titan-console` | `skill.titan-appserver-bridge` | - |
| composes-with | `skill.titan-console` | `skill.titan-memory-loom` | - |
| composes-with | `tool.titan.approval-record` | `tool.titan.console` | - |
| composes-with | `tool.titan.appserver-plan` | `tool.titan.console` | - |
| composes-with | `tool.titan.console` | `tool.titan.appserver-bridge` | - |
| composes-with | `tool.titan.memory-ingest` | `tool.titan.memory-recall` | - |
| composes-with | `workflow.operations.safe-infra-change` | `guard.operations.preview` | The bound owner supports a truthful preview for the exact mutation. |
| composes-with | `workflow.titan.summon` | `guard.titan.mutation` | Forge is explicitly requested for a bounded mutation. |
| composes-with | `workflow.titan.summon` | `guard.titan.runtime-transition` | A live Titan activation or role-gated transition is requested. |
| composes-with | `workflow.titan.summon` | `tool.titan.appserver-plan` | - |
| composes-with | `workflow.titan.summon` | `tool.titan.receipt` | - |
| conflicts-with | `mode.decision.record` | `mode.decision.correct` | Both modes target the same decision record in one task-local plan. |
| consumes | `tool.titan.event-replay` | `tool.titan.appserver-bridge` | - |
| derived-from | `adapter.abyss.artifact-trust` | `skill.os-abyss-artifact-trust-loop` | - |
| derived-from | `adapter.abyss.diagnostic-review` | `skill.abyss-self-diagnostic-spine` | - |
| derived-from | `tool.titan.approval-queue` | `tool.titan.appserver-bridge` | - |
| extracts-to | `tool.titan.event-replay` | `tool.titan.memory-ingest` | - |
| guarded-by | `guard.titan.mutation` | `guard.titan.thread-turn-binding` | - |
| guarded-by | `guard.titan.runtime-transition` | `guard.titan.thread-turn-binding` | - |
| guarded-by | `skill.aoa-summon` | `guard.operations.approval` | The child route requests effects that require explicit approval. |
| guarded-by | `workflow.operations.git-closeout` | `guard.operations.approval` | The requested Git boundary creates an external write or irreversible publication effect. |
| guarded-by | `workflow.operations.local-commit` | `guard.operations.approval` | A local commit requires explicit current authority for the exact staged boundary. |
| guarded-by | `workflow.operations.local-stack-bringup` | `guard.operations.approval` | - |
| guarded-by | `workflow.operations.safe-infra-change` | `guard.operations.approval` | - |
| guarded-by | `workflow.titan.closeout-audit` | `guard.titan.closeout-readiness` | - |
| hands-off-to | `mode.checkpoint-closeout.execute` | `skill.aoa-memo-writeback` | A bounded reusable closeout lesson survives after the report. |
| hands-off-to | `mode.eval.select` | `mode.eval.apply` | Selection found an exact fit with a complete execution contract. |
| hands-off-to | `mode.eval.select` | `mode.eval.design` | Selection recorded no fit and a stable invariant, owner path, and acceptance target exist. |
| hands-off-to | `mode.eval.select` | `mode.eval.local-need` | Selection recorded no fit and an admitted owner-local intake port exists. |
| hands-off-to | `mode.session-harvest.classify` | `mode.session-harvest.automation-opportunity` | The unit is a repeated manual route and automation readiness is the unresolved question. |
| hands-off-to | `mode.session-harvest.classify` | `mode.session-harvest.promote` | Exactly one isolated repeated quest-shaped unit remains and only its promotion verdict is unresolved. |
| hands-off-to | `mode.session-harvest.extract` | `mode.session-harvest.classify` | One extracted unit has sufficient evidence for destination classification. |
| hands-off-to | `mode.session-recovery.diagnose` | `mode.session-recovery.repair` | The diagnosis is reviewed and the target owner is known. |
| hands-off-to | `skill.aoa-eval` | `skill.aoa-evals` | The selected object is a central source bundle, named eval verdict, source-linked report, or proof-lifecycle question. |
| hands-off-to | `skill.aoa-evals` | `skill.aoa-eval` | The unresolved need is repository-local selection, application, intake, design, or session-hit classification. |
| hands-off-to | `skill.aoa-kag` | `skill.aoa-evals` | Retrieval resolves a central proof bundle, result, verdict, or proof-lifecycle question. |
| hands-off-to | `skill.aoa-kag` | `skill.aoa-memo` | Retrieval resolves an explicit memory object, candidate, lifecycle target, or memory read-model question. |
| hands-off-to | `skill.aoa-memo` | `skill.aoa-evals` | The unresolved claim is proof meaning rather than memory meaning. |
| hands-off-to | `skill.aoa-memo` | `skill.aoa-kag` | The responsible owner or exact source remains unknown and bounded cross-repository navigation is required. |
| hands-off-to | `skill.aoa-memo-writeback` | `skill.aoa-memo` | A concrete candidate, export, quarantine packet, memory object, lifecycle target, or read-model target now exists and needs owner recall, review, or evolution. |
| hands-off-to | `skill.aoa-stats` | `skill.aoa-evals` | The unresolved question is proof or verdict interpretation rather than a bounded measurement result. |
| hands-off-to | `skill.aoa-summon` | `skill.aoa-checkpoint-closeout-bridge` | A returned child changes the parent checkpoint or closeout posture. |
| hands-off-to | `skill.aoa-summon` | `skill.aoa-memo-writeback` | A reviewed child return contains one bounded memory-worthy lesson. |
| hands-off-to | `skill.titan-memory-loom` | `tool.titan.memory-retention` | - |
| hands-off-to | `tool.titan.memory-recall` | `tool.titan.memory-retention` | - |
| hands-off-to | `workflow.operations.local-commit` | `workflow.operations.git-closeout` | A separately authorized remote effect is requested and an evaluated host binding is available. |
| implemented-by | `engineering.evaluation` | `skill.aoa-eval` | - |
| implemented-by | `engineering.evaluation` | `skill.aoa-evals` | - |
| implemented-by | `engineering.measurement` | `skill.aoa-stats` | - |
| implemented-by | `engineering.shape` | `skill.aoa-engineering-shape` | - |
| implemented-by | `engineering.verification` | `skill.aoa-verification` | - |
| implemented-by | `projects.abyss.artifact-trust` | `skill.os-abyss-artifact-trust-loop` | - |
| implemented-by | `projects.abyss.diagnose-runtime` | `adapter.abyss.diagnostic-review` | - |
| implemented-by | `projects.abyss.diagnose-runtime` | `skill.abyss-self-diagnostic-spine` | - |
| implemented-by | `projects.titan.session.closeout-audit` | `workflow.titan.closeout-audit` | - |
| implemented-by | `projects.titan.session.control` | `skill.titan-appserver-bridge` | - |
| implemented-by | `projects.titan.session.control` | `skill.titan-console` | - |
| implemented-by | `projects.titan.session.control` | `tool.titan.appserver-bridge` | - |
| implemented-by | `projects.titan.session.memory` | `skill.titan-memory-loom` | - |
| implemented-by | `projects.titan.session.memory` | `tool.titan.memory-ingest` | - |
| implemented-by | `projects.titan.summon` | `workflow.titan.summon` | - |
| implemented-by | `sessions.checkpoint-closeout` | `skill.aoa-checkpoint-closeout-bridge` | - |
| implemented-by | `sessions.harvest` | `skill.aoa-session-harvest` | - |
| implemented-by | `sessions.recovery` | `skill.aoa-session-recovery` | - |
| implemented-by | `stewardship.decisions` | `skill.aoa-decision` | - |
| implemented-by | `stewardship.knowledge` | `skill.aoa-knowledge-stewardship` | - |
| implemented-by | `stewardship.knowledge.memory` | `skill.aoa-memo` | - |
| implemented-by | `stewardship.knowledge.retrieve` | `skill.aoa-kag` | - |
| primary-parent | `adapter.abyss.artifact-trust` | `projects.abyss.artifact-trust` | - |
| primary-parent | `adapter.abyss.diagnostic-review` | `projects.abyss.diagnose-runtime` | - |
| primary-parent | `adapter.abyss.safe-infra-change` | `projects.abyss` | - |
| primary-parent | `adapter.abyss.sanitized-share` | `projects.abyss` | - |
| primary-parent | `adapter.atm10.authority-map` | `projects.atm10` | - |
| primary-parent | `adapter.atm10.repository-change` | `projects.atm10` | - |
| primary-parent | `engineering` | `aoa` | - |
| primary-parent | `engineering.evaluation` | `engineering` | - |
| primary-parent | `engineering.measurement` | `engineering` | - |
| primary-parent | `engineering.shape` | `engineering` | - |
| primary-parent | `engineering.verification` | `engineering` | - |
| primary-parent | `guard.operations.approval` | `operations.safety` | - |
| primary-parent | `guard.operations.preview` | `operations.safety` | - |
| primary-parent | `guard.titan.closeout-readiness` | `projects.titan.session.closeout-audit` | - |
| primary-parent | `guard.titan.mutation` | `projects.titan.summon` | - |
| primary-parent | `guard.titan.runtime-transition` | `projects.titan.summon` | - |
| primary-parent | `guard.titan.thread-turn-binding` | `projects.titan.session.control` | - |
| primary-parent | `human-gate.titan.closeout` | `projects.titan.session.closeout-audit` | - |
| primary-parent | `mode.checkpoint-closeout.collect` | `sessions.checkpoint-closeout` | - |
| primary-parent | `mode.checkpoint-closeout.execute` | `sessions.checkpoint-closeout` | - |
| primary-parent | `mode.decision.correct` | `stewardship.decisions` | - |
| primary-parent | `mode.decision.find` | `stewardship.decisions` | - |
| primary-parent | `mode.decision.record` | `stewardship.decisions` | - |
| primary-parent | `mode.engineering-shape.contexts` | `engineering.shape` | - |
| primary-parent | `mode.engineering-shape.core` | `engineering.shape` | - |
| primary-parent | `mode.engineering-shape.port-adapter` | `engineering.shape` | - |
| primary-parent | `mode.eval.apply` | `engineering.evaluation` | - |
| primary-parent | `mode.eval.design` | `engineering.evaluation` | - |
| primary-parent | `mode.eval.local-need` | `engineering.evaluation` | - |
| primary-parent | `mode.eval.select` | `engineering.evaluation` | - |
| primary-parent | `mode.eval.session-mining` | `engineering.evaluation` | - |
| primary-parent | `mode.knowledge.authority-map` | `stewardship.knowledge` | - |
| primary-parent | `mode.knowledge.sanitized-share` | `stewardship.knowledge` | - |
| primary-parent | `mode.session-harvest.automation-opportunity` | `sessions.harvest` | - |
| primary-parent | `mode.session-harvest.branch` | `sessions.harvest` | - |
| primary-parent | `mode.session-harvest.classify` | `sessions.harvest` | - |
| primary-parent | `mode.session-harvest.extract` | `sessions.harvest` | - |
| primary-parent | `mode.session-harvest.promote` | `sessions.harvest` | - |
| primary-parent | `mode.session-recovery.diagnose` | `sessions.recovery` | - |
| primary-parent | `mode.session-recovery.repair` | `sessions.recovery` | - |
| primary-parent | `mode.verification.contract` | `engineering.verification` | - |
| primary-parent | `mode.verification.coverage-audit` | `engineering.verification` | - |
| primary-parent | `mode.verification.property` | `engineering.verification` | - |
| primary-parent | `operations` | `aoa` | - |
| primary-parent | `operations.change` | `operations` | - |
| primary-parent | `operations.continuity` | `operations` | - |
| primary-parent | `operations.safety` | `operations` | - |
| primary-parent | `projects` | `aoa` | - |
| primary-parent | `projects.abyss` | `projects` | - |
| primary-parent | `projects.abyss.artifact-trust` | `projects.abyss` | - |
| primary-parent | `projects.abyss.diagnose-runtime` | `projects.abyss` | - |
| primary-parent | `projects.atm10` | `projects` | - |
| primary-parent | `projects.titan` | `projects` | - |
| primary-parent | `projects.titan.session` | `projects.titan` | - |
| primary-parent | `projects.titan.session.closeout-audit` | `projects.titan.session` | - |
| primary-parent | `projects.titan.session.control` | `projects.titan.session` | - |
| primary-parent | `projects.titan.session.memory` | `projects.titan.session` | - |
| primary-parent | `projects.titan.summon` | `projects.titan` | - |
| primary-parent | `sessions` | `aoa` | - |
| primary-parent | `sessions.checkpoint-closeout` | `sessions` | - |
| primary-parent | `sessions.harvest` | `sessions` | - |
| primary-parent | `sessions.memo-writeback` | `sessions` | - |
| primary-parent | `sessions.recovery` | `sessions` | - |
| primary-parent | `skill.abyss-self-diagnostic-spine` | `projects.abyss.diagnose-runtime` | - |
| primary-parent | `skill.aoa-checkpoint-closeout-bridge` | `sessions.checkpoint-closeout` | - |
| primary-parent | `skill.aoa-decision` | `stewardship.decisions` | - |
| primary-parent | `skill.aoa-engineering-shape` | `engineering.shape` | - |
| primary-parent | `skill.aoa-eval` | `engineering.evaluation` | - |
| primary-parent | `skill.aoa-evals` | `engineering.evaluation` | - |
| primary-parent | `skill.aoa-kag` | `stewardship.knowledge.retrieve` | - |
| primary-parent | `skill.aoa-knowledge-stewardship` | `stewardship.knowledge` | - |
| primary-parent | `skill.aoa-memo` | `stewardship.knowledge.memory` | - |
| primary-parent | `skill.aoa-memo-writeback` | `sessions.memo-writeback` | - |
| primary-parent | `skill.aoa-session-harvest` | `sessions.harvest` | - |
| primary-parent | `skill.aoa-session-progression-lift` | `sessions` | - |
| primary-parent | `skill.aoa-session-recovery` | `sessions.recovery` | - |
| primary-parent | `skill.aoa-stats` | `engineering.measurement` | - |
| primary-parent | `skill.aoa-summon` | `sessions` | - |
| primary-parent | `skill.aoa-verification` | `engineering.verification` | - |
| primary-parent | `skill.os-abyss-artifact-trust-loop` | `projects.abyss.artifact-trust` | - |
| primary-parent | `skill.titan-appserver-bridge` | `projects.titan.session.control` | - |
| primary-parent | `skill.titan-console` | `projects.titan.session.control` | - |
| primary-parent | `skill.titan-memory-loom` | `projects.titan.session.memory` | - |
| primary-parent | `stewardship` | `aoa` | - |
| primary-parent | `stewardship.decisions` | `stewardship` | - |
| primary-parent | `stewardship.knowledge` | `stewardship` | - |
| primary-parent | `stewardship.knowledge.memory` | `stewardship.knowledge` | - |
| primary-parent | `stewardship.knowledge.retrieve` | `stewardship.knowledge` | - |
| primary-parent | `tool.abyss.aoa-diagnose` | `projects.abyss.diagnose-runtime` | - |
| primary-parent | `tool.titan.approval-queue` | `projects.titan.session.control` | - |
| primary-parent | `tool.titan.approval-record` | `projects.titan.session.control` | - |
| primary-parent | `tool.titan.appserver-bridge` | `projects.titan.session.control` | - |
| primary-parent | `tool.titan.appserver-plan` | `projects.titan.session.control` | - |
| primary-parent | `tool.titan.console` | `projects.titan.session.control` | - |
| primary-parent | `tool.titan.event-replay` | `projects.titan.session.control` | - |
| primary-parent | `tool.titan.memory-ingest` | `projects.titan.session.memory` | - |
| primary-parent | `tool.titan.memory-recall` | `projects.titan.session.memory` | - |
| primary-parent | `tool.titan.memory-retention` | `projects.titan.session.memory` | - |
| primary-parent | `tool.titan.receipt` | `projects.titan.session.control` | - |
| primary-parent | `tool.titan.swarm-validate` | `projects.titan.session.closeout-audit` | - |
| primary-parent | `workflow.operations.checkpoint-closeout` | `operations.continuity` | - |
| primary-parent | `workflow.operations.delegation` | `operations.continuity` | - |
| primary-parent | `workflow.operations.git-closeout` | `operations.change` | - |
| primary-parent | `workflow.operations.local-commit` | `operations.change` | - |
| primary-parent | `workflow.operations.local-stack-bringup` | `operations.safety` | - |
| primary-parent | `workflow.operations.repository-change` | `operations.change` | - |
| primary-parent | `workflow.operations.safe-infra-change` | `operations.safety` | - |
| primary-parent | `workflow.operations.tdd-slice` | `operations.change` | - |
| primary-parent | `workflow.titan.closeout-audit` | `projects.titan.session.closeout-audit` | - |
| primary-parent | `workflow.titan.summon` | `projects.titan.summon` | - |
| produces | `mode.eval.session-mining` | `mode.eval.design` | Reviewed evidence supports reproducible manual cases and a stable invariant. |
| produces | `mode.eval.session-mining` | `mode.eval.local-need` | Reviewed evidence establishes bounded owner-local eval pressure. |
| requires | `adapter.abyss.diagnostic-review` | `tool.abyss.aoa-diagnose` | - |
| requires | `guard.titan.closeout-readiness` | `human-gate.titan.closeout` | - |
| requires | `mode.checkpoint-closeout.execute` | `skill.aoa-session-harvest` | - |
| requires | `mode.checkpoint-closeout.execute` | `skill.aoa-session-progression-lift` | Reviewed evidence supports a progression node. |
| requires | `skill.abyss-self-diagnostic-spine` | `tool.abyss.aoa-diagnose` | - |
| requires | `skill.aoa-summon` | `workflow.operations.delegation` | Execute mode requires a callable host child-agent binding and a real returned runtime handle. |
| requires | `skill.titan-appserver-bridge` | `tool.titan.appserver-bridge` | - |
| requires | `skill.titan-appserver-bridge` | `tool.titan.event-replay` | - |
| requires | `skill.titan-console` | `tool.titan.approval-queue` | - |
| requires | `skill.titan-console` | `tool.titan.approval-record` | - |
| requires | `skill.titan-console` | `tool.titan.appserver-plan` | - |
| requires | `skill.titan-console` | `tool.titan.console` | - |
| requires | `skill.titan-console` | `tool.titan.receipt` | - |
| requires | `skill.titan-memory-loom` | `tool.titan.memory-ingest` | - |
| requires | `skill.titan-memory-loom` | `tool.titan.memory-recall` | - |
| requires | `workflow.titan.closeout-audit` | `tool.titan.swarm-validate` | - |
