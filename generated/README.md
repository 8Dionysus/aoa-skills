# Generated Projections

| Projection | Source and builder |
| --- | --- |
| `capability_graph.*` | `capabilities/`; `build_capability_graph.py` |
| `agent_skill_catalog*.json`, `portable_export_map.json` | `skills/` + config; `build_agent_skills.py` |
| `skill_pack_profiles.resolved.json`, `mcp_dependency_manifest.json`, `release_manifest.json` | source/export/config; `build_agent_skills.py` |
| `quest_catalog*`, `quest_dispatch*` | `quests/`; `build_questbook.py` |
| `agon_*_candidates.min.json` | requested candidate sources owned by Agon mechanics |

All files are derived. Edit their owner source and regenerate; never use a
manual generated patch to hide disagreement.
