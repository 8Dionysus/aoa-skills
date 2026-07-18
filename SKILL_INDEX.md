# AoA Skill Index

This is the compact human route. Machine-readable discovery uses
`generated/agent_skill_catalog.min.json` and `generated/capability_graph.json`.

| Bundle | Purpose | Visibility |
| --- | --- | --- |
| `aoa-decision` | find, record, or correct durable repository decisions | advertised |
| `aoa-engineering-shape` | shape code and boundaries through internal engineering modes | deferred |
| `aoa-eval` | select or apply an exact eval, or propose a bounded no-fit response | advertised challenger |
| `aoa-verification` | contract, audit coverage, or express a stable property | deferred |
| `aoa-knowledge-stewardship` | preserve owner truth and route reviewed knowledge | advertised challenger |
| `aoa-checkpoint-closeout-bridge` | bridge closed reviewed session evidence to an owner closeout route | advertised transitional |
| `aoa-memo-writeback` | notice a memory-worthy closeout and prepare one bounded owner candidate or no-write decision | advertised challenger |
| `aoa-session-harvest` | derive bounded reusable candidates from reviewed session evidence | advertised challenger |
| `aoa-session-recovery` | diagnose recurring session/workflow failure and carry one bounded repair | advertised challenger |

Advertised bundles are current candidate or transitional front doors, not
claims of general outcome superiority. Deferred bundles remain available only
for explicit research and manual trials and must not become implicitly active.

Capability navigation roots are `engineering`, `stewardship`, `sessions`,
`operations`, and `projects`. Modes, workflows, tools, guards, adapters, and
human gates remain typed graph objects until evidence justifies a separate
callable bundle.
