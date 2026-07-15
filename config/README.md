# Configuration

| File | Owns |
| --- | --- |
| `openai_skill_extensions.json` | optional OpenAI host metadata defaults |
| `portable_skill_overrides.json` | explicit source-to-portable overrides |
| `skill_pack_profiles.json` | default advertised pack and all-source research pack |
| `skill_policy_matrix.json` | bundle visibility and invocation policy |
| `validation_lanes.json` | executable command authority for repository checks |

These files adapt authored capability and skill sources. They do not own skill
meaning or outcome status, and they contain no runtime secrets.
