# AGENTS.md

## Guidance for `examples/`

`examples/` is the root example district for repo-owned examples only.
Mechanic-owned examples live under `mechanics/<slug>/examples/` or the
nearest owning part.

Examples are illustrative, not canonical. They should make a contract easier to understand without becoming a second source of truth beside schemas, docs, or `SKILL.md`.

Every example that demonstrates a schema-backed shape should stay paired with the schema or doc that owns it. Keep names, required fields, and boundary wording aligned with that owner.

Do not add secrets, private workspace paths, real credentials, or unreduced personal data. Use neutral placeholders and explain what must be replaced.

When examples show degraded, receipt, or follow-through behavior, preserve the bounded posture: examples may show a next step, not grant open-ended task authority.

Verify with the relevant example validator when present, plus:

```bash
python scripts/build_openai_yaml_examples.py --map mechanics/boundary-bridge/examples/skill_mcp_wiring.map.json --output-dir mechanics/boundary-bridge/examples --check
python scripts/validate_semantic_agents.py
```
