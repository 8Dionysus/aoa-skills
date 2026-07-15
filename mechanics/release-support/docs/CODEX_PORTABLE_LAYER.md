# Portable Agent Skills Layer

`skills/**/SKILL.md` is authored procedure source. The export builder creates a
flat `.agents/skills/<name>/` package plus compact catalogs and release hashes.

Portable frontmatter follows the open Agent Skills shape. AoA-specific scope,
status, invocation posture, and source path are namespaced metadata. The source
`agents/openai.yaml` is preserved as a host adapter; policy maps `invoke` to
implicit visibility and `suggest` or `manual` to non-implicit posture.
That mapping is Codex-specific: other Agent Skills hosts may ignore the adapter
and expose every installed bundle.

Current derived outputs are:

- `.agents/skills/*`;
- `generated/agent_skill_catalog*.json`;
- `generated/portable_export_map.json`;
- `generated/skill_pack_profiles.resolved.json`;
- `generated/mcp_dependency_manifest.json`;
- `generated/release_manifest.json`.

There is no runtime technique dependency, legacy ring, tiny-router, generated
guardrail, or local-adapter ontology in this layer. Runtime hosts may build
their own retrieval/materialization over the portable contract.

Byte parity is checked by the export validator and pack verifier. Native host
visibility must be checked in a clean host context (for Codex, with its
prompt-input inspection surface); selection and outcome still need manual
trials.
