# Schemas

| Schema | Contract |
| --- | --- |
| `capability-home-port.schema.json` | repository-owned capability source, projection, routing, and task-DAG port |
| `capability_family.schema.json` | authored family and executable node shape |
| `capability_graph.schema.json` | deterministic graph projection |
| `task_local_dag.schema.json` | legacy v1 session-local composition result |
| `task_local_dag_v2.schema.json` | typed session-local execution plan with stages, checkpoints, handoffs, and blockers |
| `skill_migration.schema.json` | exact legacy-to-v2 disposition map |
| `skill-frontmatter.schema.json` | portable `SKILL.md` frontmatter |
| `skill-home-port.schema.json` | admitted repository home and its v2 OS-user exposure; v1 repo projection remains migration compatibility |
| `release_manifest.schema.json` | portable release identity and hashes |

Schemas protect durable shape. They do not establish semantic usefulness or
proof authority.
