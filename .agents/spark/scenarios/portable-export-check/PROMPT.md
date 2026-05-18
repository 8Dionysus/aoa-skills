# Spark Prompt: portable-export-check

```text
You are running a standalone Spark portable-export-check session.

Read:
- root AGENTS.md
- .agents/AGENTS.md
- .agents/spark/AGENTS.md
- .agents/spark/registry.json
- .agents/spark/scenarios/portable-export-check/README.md
- mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md
- the source skill bundle, export, or support resource named by the user

Task:
Inspect portable export parity, support-resource carriage, source route,
generated/export drift, and adoption-facing risk for the named scope.

Rules:
- audit first
- do not hand-edit .agents/skills/* as source truth
- if a fix is requested, change source/config/builder first and regenerate
- keep one scope
- finish as done-or-handoff

Return:
- scope read
- export/source parity findings with file paths
- source or builder route
- validation run or still needed
- done result or handoff packet
```
