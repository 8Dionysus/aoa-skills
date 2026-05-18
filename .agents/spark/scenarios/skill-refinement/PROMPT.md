# Spark Prompt: skill-refinement

```text
You are running a standalone Spark skill-refinement session.

Read:
- root AGENTS.md
- .agents/AGENTS.md
- .agents/spark/AGENTS.md
- .agents/spark/registry.json
- .agents/spark/scenarios/skill-refinement/README.md
- skills/AGENTS.md
- the target SKILL.md
- the target techniques.yaml when present
- directly relevant checks, examples, references, or agents/openai.yaml

Task:
Make one small patch that improves trigger boundaries, execution clarity,
support artifacts, portability, public safety, validation wording, or owner
routing for the named skill.

Rules:
- one skill bundle
- one bounded patch
- preserve source truth and public-safe wording
- keep technique links adjacent, not hidden runtime dependency
- run or name the narrowest local validation explicitly required
- finish as done-or-handoff

Return:
- files changed
- why the patch is bounded
- validation run
- skipped checks
- remaining risk
```
