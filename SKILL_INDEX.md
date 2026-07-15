# AoA Skill Index

This is the compact human route. Machine-readable discovery uses
`generated/agent_skill_catalog.min.json` and `generated/capability_graph.json`.

| Bundle | Purpose | Visibility |
| --- | --- | --- |
| `aoa-decision` | find, record, or correct durable repository decisions | advertised |
| `aoa-engineering-shape` | shape code and boundaries through internal engineering modes | deferred |
| `aoa-eval` | select or apply an exact eval, or propose a bounded no-fit response | deferred |
| `aoa-verification` | contract, audit coverage, or express a stable property | deferred |
| `aoa-knowledge-stewardship` | preserve owner truth and route reviewed knowledge | deferred |
| `aoa-session-harvest` | derive bounded reusable candidates from session evidence | deferred |
| `aoa-session-recovery` | diagnose recurring session/workflow failure and propose a bounded repair | deferred |

Deferred bundles are source candidates for explicit research and manual trials;
they are not installed by the default profile and must not become implicitly
active.

Capability navigation roots are `engineering`, `stewardship`, `sessions`,
`operations`, and `projects`. Modes, workflows, tools, guards, adapters, and
human gates remain typed graph objects until evidence justifies a separate
callable bundle.
