# Capability graph

Derived from `capabilities/families/*.yaml`. This file is a read model, not capability authority.

Source content hash: `cc24f45231b0c1316416b50bd0e9b336889a40c6ea23ccc0cb94c3567cf88ba1`

## Semantic tree

- `aoa` (capability, deferred, challenger)
  - `engineering` (capability, deferred, challenger)
    - `engineering.evaluation` (capability, deferred, challenger)
      - `mode.eval.apply` (mode, internal, challenger)
      - `mode.eval.propose` (mode, internal, challenger)
      - `mode.eval.select` (mode, internal, challenger)
      - `skill.aoa-eval` (skill, deferred, degraded)
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
      - `workflow.operations.git-closeout` (workflow, deferred, healthy)
      - `workflow.operations.repository-change` (workflow, deferred, healthy)
      - `workflow.operations.tdd-slice` (workflow, deferred, healthy)
    - `operations.continuity` (capability, deferred, healthy)
      - `workflow.operations.checkpoint-closeout` (workflow, deferred, healthy)
      - `workflow.operations.delegation` (workflow, deferred, healthy)
    - `operations.safety` (capability, deferred, healthy)
      - `guard.operations.approval` (guard, deferred, healthy)
      - `guard.operations.preview` (guard, deferred, healthy)
      - `workflow.operations.local-stack-bringup` (workflow, internal, unavailable)
      - `workflow.operations.safe-infra-change` (workflow, internal, unavailable)
  - `projects` (capability, deferred, challenger)
    - `projects.abyss` (capability, deferred, challenger)
      - `adapter.abyss.artifact-trust` (adapter, deferred, healthy)
      - `adapter.abyss.safe-infra-change` (adapter, deferred, healthy)
      - `adapter.abyss.sanitized-share` (adapter, deferred, healthy)
      - `projects.abyss.diagnose-runtime` (capability, deferred, challenger)
        - `adapter.abyss.diagnostic-review` (adapter, deferred, challenger)
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
          - `tool.titan.approval-queue` (tool, internal, healthy)
          - `tool.titan.approval-record` (tool, internal, healthy)
          - `tool.titan.appserver-bridge` (tool, internal, healthy)
          - `tool.titan.appserver-plan` (tool, internal, healthy)
          - `tool.titan.console` (tool, internal, healthy)
          - `tool.titan.event-replay` (tool, internal, healthy)
          - `tool.titan.receipt` (tool, internal, healthy)
        - `projects.titan.session.memory` (capability, deferred, healthy)
          - `tool.titan.memory-ingest` (tool, internal, healthy)
          - `tool.titan.memory-recall` (tool, internal, healthy)
          - `tool.titan.memory-retention` (tool, internal, healthy)
      - `projects.titan.summon` (capability, deferred, healthy)
        - `guard.titan.mutation` (guard, internal, unavailable)
        - `guard.titan.runtime-transition` (guard, internal, unavailable)
        - `workflow.titan.summon` (workflow, internal, healthy)
  - `sessions` (capability, deferred, challenger)
    - `adapter.sessions.progression-review` (adapter, internal, healthy)
    - `sessions.harvest` (capability, deferred, challenger)
      - `mode.session-harvest.branch` (mode, internal, challenger)
      - `mode.session-harvest.classify` (mode, internal, challenger)
      - `mode.session-harvest.extract` (mode, internal, challenger)
      - `skill.aoa-session-harvest` (skill, deferred, degraded)
    - `sessions.recovery` (capability, deferred, challenger)
      - `mode.session-recovery.diagnose` (mode, internal, challenger)
      - `mode.session-recovery.propose-repair` (mode, internal, challenger)
      - `skill.aoa-session-recovery` (skill, deferred, degraded)
  - `stewardship` (capability, deferred, challenger)
    - `stewardship.decisions` (capability, deferred, challenger)
      - `mode.decision.correct` (mode, internal, challenger)
      - `mode.decision.find` (mode, internal, challenger)
      - `mode.decision.record` (mode, internal, challenger)
      - `skill.aoa-decision` (skill, advertised, challenger)
    - `stewardship.knowledge` (capability, deferred, challenger)
      - `mode.knowledge.authority-map` (mode, internal, challenger)
      - `mode.knowledge.memo-route` (mode, internal, challenger)
      - `mode.knowledge.sanitized-share` (mode, internal, challenger)
      - `skill.aoa-knowledge-stewardship` (skill, deferred, degraded)

## Typed relations

| kind | source | target | condition |
|---|---|---|---|
| adapted-by | `mode.knowledge.authority-map` | `adapter.atm10.authority-map` | - |
| adapted-by | `mode.knowledge.sanitized-share` | `adapter.abyss.sanitized-share` | - |
| adapted-by | `workflow.operations.repository-change` | `adapter.atm10.repository-change` | - |
| adapted-by | `workflow.operations.safe-infra-change` | `adapter.abyss.safe-infra-change` | - |
| alternative-to | `mode.decision.find` | `mode.decision.correct` | - |
| alternative-to | `mode.decision.find` | `mode.decision.record` | - |
| alternative-to | `mode.decision.record` | `mode.decision.correct` | - |
| composes-with | `mode.engineering-shape.core` | `mode.verification.property` | The extracted core exposes a stable semantic property across inputs. |
| composes-with | `mode.engineering-shape.port-adapter` | `mode.verification.contract` | The new port is adopted as a stable consumer-visible boundary. |
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
| derived-from | `tool.titan.approval-queue` | `tool.titan.appserver-bridge` | - |
| extracts-to | `tool.titan.event-replay` | `tool.titan.memory-ingest` | - |
| guarded-by | `guard.titan.mutation` | `guard.titan.thread-turn-binding` | - |
| guarded-by | `guard.titan.runtime-transition` | `guard.titan.thread-turn-binding` | - |
| guarded-by | `workflow.operations.git-closeout` | `guard.operations.approval` | The requested Git boundary creates an external write or irreversible publication effect. |
| guarded-by | `workflow.operations.local-stack-bringup` | `guard.operations.approval` | - |
| guarded-by | `workflow.operations.safe-infra-change` | `guard.operations.approval` | - |
| guarded-by | `workflow.titan.closeout-audit` | `guard.titan.closeout-readiness` | - |
| hands-off-to | `mode.eval.select` | `mode.eval.apply` | Selection found an exact fit with a complete execution contract. |
| hands-off-to | `mode.eval.select` | `mode.eval.propose` | Selection recorded partial or no fit with a stable invariant and owner. |
| hands-off-to | `mode.session-harvest.extract` | `mode.session-harvest.classify` | One extracted unit has sufficient evidence for destination classification. |
| hands-off-to | `mode.session-recovery.diagnose` | `mode.session-recovery.propose-repair` | The diagnosis is reviewed and the target owner is known. |
| hands-off-to | `tool.titan.memory-recall` | `tool.titan.memory-retention` | - |
| implemented-by | `engineering.evaluation` | `skill.aoa-eval` | - |
| implemented-by | `engineering.shape` | `skill.aoa-engineering-shape` | - |
| implemented-by | `engineering.verification` | `skill.aoa-verification` | - |
| implemented-by | `projects.abyss.diagnose-runtime` | `adapter.abyss.diagnostic-review` | - |
| implemented-by | `projects.titan.session.closeout-audit` | `workflow.titan.closeout-audit` | - |
| implemented-by | `projects.titan.session.control` | `tool.titan.appserver-bridge` | - |
| implemented-by | `projects.titan.session.memory` | `tool.titan.memory-ingest` | - |
| implemented-by | `projects.titan.summon` | `workflow.titan.summon` | - |
| implemented-by | `sessions.harvest` | `skill.aoa-session-harvest` | - |
| implemented-by | `sessions.recovery` | `skill.aoa-session-recovery` | - |
| implemented-by | `stewardship.decisions` | `skill.aoa-decision` | - |
| implemented-by | `stewardship.knowledge` | `skill.aoa-knowledge-stewardship` | - |
| primary-parent | `adapter.abyss.artifact-trust` | `projects.abyss` | - |
| primary-parent | `adapter.abyss.diagnostic-review` | `projects.abyss.diagnose-runtime` | - |
| primary-parent | `adapter.abyss.safe-infra-change` | `projects.abyss` | - |
| primary-parent | `adapter.abyss.sanitized-share` | `projects.abyss` | - |
| primary-parent | `adapter.atm10.authority-map` | `projects.atm10` | - |
| primary-parent | `adapter.atm10.repository-change` | `projects.atm10` | - |
| primary-parent | `adapter.sessions.progression-review` | `sessions` | - |
| primary-parent | `engineering` | `aoa` | - |
| primary-parent | `engineering.evaluation` | `engineering` | - |
| primary-parent | `engineering.shape` | `engineering` | - |
| primary-parent | `engineering.verification` | `engineering` | - |
| primary-parent | `guard.operations.approval` | `operations.safety` | - |
| primary-parent | `guard.operations.preview` | `operations.safety` | - |
| primary-parent | `guard.titan.closeout-readiness` | `projects.titan.session.closeout-audit` | - |
| primary-parent | `guard.titan.mutation` | `projects.titan.summon` | - |
| primary-parent | `guard.titan.runtime-transition` | `projects.titan.summon` | - |
| primary-parent | `guard.titan.thread-turn-binding` | `projects.titan.session.control` | - |
| primary-parent | `human-gate.titan.closeout` | `projects.titan.session.closeout-audit` | - |
| primary-parent | `mode.decision.correct` | `stewardship.decisions` | - |
| primary-parent | `mode.decision.find` | `stewardship.decisions` | - |
| primary-parent | `mode.decision.record` | `stewardship.decisions` | - |
| primary-parent | `mode.engineering-shape.contexts` | `engineering.shape` | - |
| primary-parent | `mode.engineering-shape.core` | `engineering.shape` | - |
| primary-parent | `mode.engineering-shape.port-adapter` | `engineering.shape` | - |
| primary-parent | `mode.eval.apply` | `engineering.evaluation` | - |
| primary-parent | `mode.eval.propose` | `engineering.evaluation` | - |
| primary-parent | `mode.eval.select` | `engineering.evaluation` | - |
| primary-parent | `mode.knowledge.authority-map` | `stewardship.knowledge` | - |
| primary-parent | `mode.knowledge.memo-route` | `stewardship.knowledge` | - |
| primary-parent | `mode.knowledge.sanitized-share` | `stewardship.knowledge` | - |
| primary-parent | `mode.session-harvest.branch` | `sessions.harvest` | - |
| primary-parent | `mode.session-harvest.classify` | `sessions.harvest` | - |
| primary-parent | `mode.session-harvest.extract` | `sessions.harvest` | - |
| primary-parent | `mode.session-recovery.diagnose` | `sessions.recovery` | - |
| primary-parent | `mode.session-recovery.propose-repair` | `sessions.recovery` | - |
| primary-parent | `mode.verification.contract` | `engineering.verification` | - |
| primary-parent | `mode.verification.coverage-audit` | `engineering.verification` | - |
| primary-parent | `mode.verification.property` | `engineering.verification` | - |
| primary-parent | `operations` | `aoa` | - |
| primary-parent | `operations.change` | `operations` | - |
| primary-parent | `operations.continuity` | `operations` | - |
| primary-parent | `operations.safety` | `operations` | - |
| primary-parent | `projects` | `aoa` | - |
| primary-parent | `projects.abyss` | `projects` | - |
| primary-parent | `projects.abyss.diagnose-runtime` | `projects.abyss` | - |
| primary-parent | `projects.atm10` | `projects` | - |
| primary-parent | `projects.titan` | `projects` | - |
| primary-parent | `projects.titan.session` | `projects.titan` | - |
| primary-parent | `projects.titan.session.closeout-audit` | `projects.titan.session` | - |
| primary-parent | `projects.titan.session.control` | `projects.titan.session` | - |
| primary-parent | `projects.titan.session.memory` | `projects.titan.session` | - |
| primary-parent | `projects.titan.summon` | `projects.titan` | - |
| primary-parent | `sessions` | `aoa` | - |
| primary-parent | `sessions.harvest` | `sessions` | - |
| primary-parent | `sessions.recovery` | `sessions` | - |
| primary-parent | `skill.aoa-decision` | `stewardship.decisions` | - |
| primary-parent | `skill.aoa-engineering-shape` | `engineering.shape` | - |
| primary-parent | `skill.aoa-eval` | `engineering.evaluation` | - |
| primary-parent | `skill.aoa-knowledge-stewardship` | `stewardship.knowledge` | - |
| primary-parent | `skill.aoa-session-harvest` | `sessions.harvest` | - |
| primary-parent | `skill.aoa-session-recovery` | `sessions.recovery` | - |
| primary-parent | `skill.aoa-verification` | `engineering.verification` | - |
| primary-parent | `stewardship` | `aoa` | - |
| primary-parent | `stewardship.decisions` | `stewardship` | - |
| primary-parent | `stewardship.knowledge` | `stewardship` | - |
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
| primary-parent | `workflow.operations.local-stack-bringup` | `operations.safety` | - |
| primary-parent | `workflow.operations.repository-change` | `operations.change` | - |
| primary-parent | `workflow.operations.safe-infra-change` | `operations.safety` | - |
| primary-parent | `workflow.operations.tdd-slice` | `operations.change` | - |
| primary-parent | `workflow.titan.closeout-audit` | `projects.titan.session.closeout-audit` | - |
| primary-parent | `workflow.titan.summon` | `projects.titan.summon` | - |
| requires | `adapter.abyss.diagnostic-review` | `tool.abyss.aoa-diagnose` | - |
| requires | `guard.titan.closeout-readiness` | `human-gate.titan.closeout` | - |
| requires | `workflow.titan.closeout-audit` | `tool.titan.swarm-validate` | - |
