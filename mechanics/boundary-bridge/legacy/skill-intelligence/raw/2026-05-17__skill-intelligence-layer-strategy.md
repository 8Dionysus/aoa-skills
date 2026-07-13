# Skill Intelligence Layer Strategy Artifact

- status: temporary_strategy_artifact
- created_at: 2026-05-17
- owner_repo_under_review: /srv/AbyssOS/aoa-skills
- workspace_root: /srv/AbyssOS
- purpose: prepare the full execution route for skill indexing, RAG, Agentic RAG, DAG, registry, router, and adoption work before implementation
- authority: legacy planning note only; it does not replace AGENTS.md, DESIGN.md, docs/ARCHITECTURE.md, source skills, config, generated surfaces, or sibling-owner truth

## 0. Why This Artifact Exists

The next move is larger than adding search over `SKILL.md` files.

The AoA skill layer already has a canon, generated companions, runtime seams,
trigger evaluations, trust policy, and downstream install surfaces. The real
task is to turn those pieces into a coherent Skill Intelligence Layer:

```text
source canon
  -> deterministic registry
  -> portable lexical search
  -> optional semantic retrieval and rerank
  -> policy gate
  -> boundary-aware explanation
  -> safe activation, suggestion, or manual handoff
  -> adoption and freshness feedback
```

The goal is not "let embeddings choose a skill". The goal is to help a future
local coding agent move through AoA skills with precision, provenance, review
discipline, and source-owner boundaries intact.

## 1. Current Ground Rules

### 1.1 aoa-skills is the source owner for skill meaning

Current `aoa-skills/AGENTS.md` says this repository owns:

- canonical skill bundle wording and workflow structure
- trigger boundaries, invocation posture, skill inputs and outputs
- skill-level technique dependency declarations
- generated catalogs, matrices, portable exports, and bridge manifests derived
  from canonical skills
- repo-local mechanics for movement, adoption, export, recurrence, checkpoint,
  quest integration, and review pressure

It does not own technique truth, proof doctrine, routing truth, memory truth,
KAG, stats, playbooks, role truth, runtime inventory, downstream adoption truth,
or hidden control-plane authority.

This means the Skill Intelligence Layer can be born in `aoa-skills`, but it
must route parts of the system outward instead of absorbing sibling repos.

### 1.2 Generated surfaces are useful but not source truth

Current `DESIGN.md` and `docs/ARCHITECTURE.md` already contain the right law:

- `SKILL.md`, `techniques.yaml`, and bundle-local support artifacts own skill
  meaning.
- `.agents/skills/*`, generated catalogs, runtime cards, and adapter surfaces
  carry or summarize meaning.
- Generated and exported surfaces should be deterministic, reproducible, and
  source-linked.
- If generated output drifts, repair source/config/builder and regenerate.

The registry must follow this posture.

### 1.3 External market direction matches AoA direction

The web reconnaissance before this artifact found a stable pattern across
current skill ecosystems:

- Skills use progressive disclosure: name, description, and path are visible
  first; full instructions and resources are loaded after selection.
- Description quality is not cosmetic. It is a routing and discovery surface.
- Trigger evals and near-miss negative examples are required to keep routing
  honest.
- Tool and skill registries separate metadata/discovery from installed code.
- Community signals show practical pain around context bloat, too many skills,
  stale indexes, unsafe third-party skill bundles, and unclear activation.

Useful external anchors:

- https://developers.openai.com/codex/skills
- https://agentskills.io/specification
- https://agentskills.io/client-implementation/adding-skills-support
- https://agentskills.io/skill-creation/optimizing-descriptions
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- https://modelcontextprotocol.io/registry/about

AoA should not copy any one vendor shape blindly. The durable fit is:
progressive disclosure, local-first registry, explicit trust and activation
policy, deterministic generated surfaces, optional semantic acceleration, and
source-linked explanation.

## 2. Reconnaissance Snapshot

### 2.1 aoa-skills current surfaces

Observed in this pass:

- `generated/skill_catalog.min.json`: 45 skills
- `generated/skill_bundle_index.json`: 45 skills
- `generated/runtime_discovery_index.min.json`: 45 skills
- `generated/tiny_router_capsules.min.json`: 45 skills
- `generated/trust_policy_matrix.json`: 45 skills
- `generated/skill_graph.json`: 120 nodes, 692 edges
- `generated/skill_quality_audit.json`: 45 skills, 0 blocked
- source `skills/**/SKILL.md`: 45 skill bundles
- repo export `.agents/skills/**/SKILL.md`: 45 skill bundles
- workspace install `/srv/AbyssOS/.agents/skills/**/SKILL.md`: 25 skill bundles at the time of this pass

Important existing generated or source surfaces:

- `SKILL_INDEX.md`
- `generated/skill_catalog*.json`
- `generated/skill_bundle_index.*`
- `generated/runtime_discovery_index*.json`
- `generated/runtime_disclosure_index.json`
- `generated/runtime_router_hints.json`
- `generated/runtime_activation_aliases.json`
- `generated/runtime_tool_schemas.json`
- `generated/runtime_session_contract.json`
- `generated/runtime_prompt_blocks.json`
- `generated/runtime_seam_manifest.json`
- `generated/skill_graph.*`
- `generated/skill_boundary_matrix.*`
- `generated/skill_evaluation_matrix.*`
- `generated/skill_quality_audit.*`
- `generated/skill_promotion_pressure.*`
- `generated/skill_reality_trials.*`
- `generated/support_resource_index.json`
- `generated/trust_policy_matrix.json`
- `generated/tiny_router_*`
- `config/skill_policy_matrix.json`
- `config/tiny_router_skill_bands.json`
- `config/description_trigger_eval_policy.json`
- `config/runtime_guardrail_policy.json`
- `config/skill_pack_profiles.json`
- `schemas/skill_bundle_index.schema.json`
- `schemas/skill_graph.schema.json`
- `schemas/skill_boundary_matrix.schema.json`
- `scripts/build_catalog.py`
- `scripts/build_tiny_router_inputs.py`
- `scripts/skill_runtime_seam.py`
- `scripts/inspect_skill.py`
- `scripts/validate_agent_skills.py`
- `scripts/validate_tiny_router_inputs.py`
- `scripts/audit_workspace_skill_adoption.py`

### 2.2 Current runtime seam

`scripts/skill_runtime_seam.py` already provides a dedicated-tool runtime seam
around the generated `.agents/skills/*` export. It uses a flow shaped like:

```text
discover -> disclose -> activate -> session status/deactivate
```

This is close to the needed future API, but it is currently filter/disclosure
oriented, not a full retrieval, freshness, graph, or explanation layer.

### 2.3 Current router seam

`aoa-routing/scripts/two_stage_skill_router.py` already consumes
`aoa-skills/generated/tiny_router_skill_signals.json` and
`aoa-skills/generated/tiny_router_candidate_bands.json`.

The route is intentionally thin:

```text
preselect -> decision-packet -> route
```

This is valuable. The future Skill Intelligence Layer should integrate with
this shape rather than replace it. The split should be:

- `aoa-skills`: owns skill registry, skill retrieval corpus, skill activation
  policy, skill boundary explanation, skill install/adoption freshness inputs
- `aoa-routing`: owns wider owner-route and dispatch policy that decides where
  a task belongs in the federation
- `aoa-sdk`: may expose typed APIs and CLI helpers over source-owned generated
  surfaces

### 2.4 .aoa retrieval strategy is a strong donor

The `.aoa` strategy artifact already names a mature retrieval shape:

```text
index(documents, provenance) -> index_receipt
search(query, filters, k) -> hits
rerank(query, hits, policy) -> ranked_hits
status() -> freshness/capability
explain(hit) -> raw refs + segment refs + index refs
```

It also states the correct rule:

- portable SQLite/FTS5 first
- optional `abyss-machine` and `abyss-stack` acceleration later
- acceleration is not authority
- every hit must point back to source refs

For skills, the equivalent should be:

```text
index(skill sections, generated capsules, resources, policy, provenance)
search(intent, filters, k)
rerank(intent, hits, policy)
status(source/export/install freshness)
explain(skill candidate and rejection)
```

### 2.5 Sibling-owner map

Observed owner split from route cards:

- `Agents-of-Abyss`: constitutional center, ecosystem identity, layer map,
  federation rules, program-level direction.
- `aoa-skills`: bounded execution workflows and skill-derived catalogs,
  matrices, exports, and bridge manifests.
- `aoa-techniques`: reusable engineering practice, technique IDs, contracts,
  method topology, technique generated catalogs.
- `aoa-evals`: bounded proof doctrine, eval bundles, generated proof surfaces.
- `aoa-routing`: thin navigation and dispatch layer; routing projections and
  recommended paths; no activation authority.
- `aoa-sdk`: typed Python SDK and control-plane helper layer; consumes sibling
  surfaces; exposes local-first APIs without owning sibling meaning.
- `aoa-memo`: explicit memory and recall layer; memory is not proof or current
  truth.
- `aoa-playbooks`: recurring scenario composition; not one skill or one
  technique.
- `aoa-agents`: role/persona/handoff/model-tier layer; not runtime autonomy.
- `aoa-kag`: provenance-aware derived knowledge substrate; graph/retrieval
  projections without replacing authored meaning.
- `aoa-stats`: derived observability and movement summaries; weaker than owner
  truth.
- `abyss-stack`: runtime/deployment/storage/lifecycle/infrastructure posture.
- `8Dionysus`: public route map and shared-root projection source.

### 2.6 Sanitization and risk note

A pre-mutation guard for `public-share` correctly flagged public-share risk and
required explicit risk review. This artifact is therefore written as a sanitized
planning artifact:

- no raw hook dumps
- no private transcript excerpts
- no secrets
- no broad public claims
- no generated JSON pasted as authority
- no promotion of this note into route law

## 3. Target System Shape

### 3.1 Name

Working name:

```text
AoA Skill Intelligence Layer
```

Possible future component names:

- `skill_registry`
- `skill_search`
- `skill_explain`
- `skill_graph`
- `skill_freshness`
- `skill_router_bridge`

Avoid names that imply hidden autonomy or source replacement.

### 3.2 Core contract

The layer should answer:

1. Which skills are candidates for this task?
2. Why are they candidates?
3. Which near-miss skills were rejected and why?
4. Is the skill allowed to auto-invoke, only suggest, or manual only?
5. Which source files own the skill meaning?
6. Which generated, exported, or installed copies are stale?
7. Which sibling repo owns the next route if the task is not skill-layer work?
8. Which supporting docs, checks, examples, or resources should be loaded next?
9. Which evals, boundary cases, or reality trials support this routing claim?
10. What is the smallest safe next action?

### 3.3 The registry must be multi-surface, not one flat table

Recommended logical views:

- `skill_identity`: name, scope, status, canonical path, source hash, summary
- `skill_sections`: normalized sections from `SKILL.md`
- `skill_policy`: invocation mode, implicit activation policy, trust posture,
  mutation surface, confirmation seams
- `skill_resources`: checks, examples, references, scripts, assets,
  selected runtime artifact
- `skill_lineage`: technique dependencies, source repo/commit when available,
  composition/decomposition pressure
- `skill_boundaries`: adjacent skills, confusing near-misses, collision family
- `skill_evidence`: eval cases, reality trials, quality audit, promotion
  pressure, review records
- `skill_graph`: nodes and edges for skill-technique-eval-resource-policy
  relationships
- `skill_install`: source export, repo export, workspace install, downstream
  install, content hash, freshness
- `skill_search_doc`: retrieval-ready text chunks with source refs and section
  roles

### 3.4 RAG model

Use staged retrieval, not one embedding call:

```text
intent text
  -> stage 0 owner-route precheck
  -> stage 1 tiny-router lexical/band shortlist
  -> stage 2 portable FTS5 search over skill capsules and sections
  -> stage 3 optional semantic retrieval over chunked skill docs/resources
  -> stage 4 optional rerank with policy and boundary features
  -> stage 5 explanation packet
  -> stage 6 activation/suggestion/manual handoff
```

The RAG layer returns evidence packets, not detached summaries.

Each hit should include:

- skill name
- candidate class: invoke, suggest, manual, rejected, route-away
- score details by stage
- matched sections
- source refs
- policy refs
- loaded support refs
- rejection or caution reasons
- freshness status

### 3.5 Agentic RAG model

Agentic RAG should be a bounded review loop:

```text
1. interpret intent
2. retrieve candidates
3. apply owner and policy gates
4. disambiguate near-miss skills
5. ask for or infer safe route mode
6. load only needed source sections/resources
7. produce decision packet
8. optionally activate or suggest
9. record evidence and gaps
```

Hard constraints:

- manual skills can be surfaced but not hidden-invoked
- suggest skills can be candidate suggestions but not hidden-invoked
- risk-ring skills remain explicit and confirmation-aware
- routing hints cannot overrule skill policy
- semantic similarity cannot overrule trust/freshness
- stale installed copies cannot pretend to be current
- generated surfaces cannot become the skill source

### 3.6 DAG model

The DAG should make skill selection explainable and future-proof.

Candidate node kinds:

- `skill`
- `skill_section`
- `skill_resource`
- `skill_policy`
- `skill_eval_case`
- `skill_boundary_case`
- `skill_install_copy`
- `technique`
- `eval`
- `route_surface`
- `owner_repo`
- `playbook`
- `memory_object`
- `agent_profile`
- `runtime_surface`
- `decision_record`
- `adoption_receipt`

Candidate edge kinds:

- `owns`
- `generated_from`
- `exports_to`
- `installed_as`
- `depends_on_technique`
- `evaluated_by`
- `conflicts_with`
- `adjacent_to`
- `suggests_next`
- `requires_policy`
- `routes_away_to`
- `supports`
- `stale_against`
- `supersedes`
- `compatible_with`

The DAG should answer:

- why this skill and not its neighbor?
- which technique/eval supports this skill?
- where is the installed copy and is it stale?
- what owner repo should receive the next change?
- what support resource should be loaded before activation?
- what policy stops hidden invocation?

## 4. Implementation Phases

### Phase 0: Decision and boundary grounding

Goal: make the future work explicit before code changes.

Tasks:

- Decide whether this strategy becomes:
  - a decision record,
  - roadmap entry,
  - mechanics/release-support plan,
  - or implementation quest.
- Confirm whether first implementation lives entirely in `aoa-skills`.
- Name the sibling handoff boundaries:
  - `aoa-routing` for cross-owner dispatch
  - `aoa-sdk` for typed API/CLI helpers
  - `aoa-evals` for proof and regression suites
  - `aoa-kag` for broader graph/retrieval substrate if needed later
  - `.aoa` for session-memory search and history, not skill truth
- Re-run a narrow route check before implementation.

Exit gate:

- one accepted owner-route note exists
- no sibling owner truth is imported into `aoa-skills`

### Phase 1: Skill registry schema and builder

Goal: build a deterministic registry from existing source/generated inputs.

Candidate files:

- `schemas/skill_intelligence_registry.schema.json`
- `scripts/build_skill_intelligence_registry.py`
- `generated/skill_intelligence_registry.json`
- `generated/skill_intelligence_registry.min.json`

Inputs:

- `skills/**/SKILL.md`
- `skills/**/techniques.yaml`
- bundle support artifacts
- `config/skill_policy_matrix.json`
- `config/skill_pack_profiles.json`
- `generated/skill_catalog.min.json`
- `generated/skill_bundle_index.json`
- `generated/skill_graph.json`
- `generated/skill_boundary_matrix.json`
- `generated/skill_evaluation_matrix.json`
- `generated/skill_quality_audit.json`
- `generated/support_resource_index.json`
- `generated/trust_policy_matrix.json`
- `generated/runtime_discovery_index.min.json`
- `generated/tiny_router_capsules.min.json`

Registry output should include:

- source refs
- content hashes
- section map
- policy map
- support artifact inventory
- install/export refs
- graph refs
- eval and boundary refs
- freshness inputs
- search document refs

Exit gate:

- builder is deterministic
- schema validation passes
- generated registry points back to source paths
- no hand-edited generated output

### Phase 2: Portable SQLite/FTS index

Goal: give clean-machine skill search without a semantic backend.

Candidate files:

- `scripts/build_skill_search_index.py`
- `scripts/search_skills.py`
- `generated/skill_search_manifest.json`
- maybe `.aoa` or local ignored runtime cache for `.sqlite` if the database
  should not be committed

Index content:

- skill names and aliases
- summary and description
- trigger boundary
- do-not-use boundary
- inputs/outputs
- procedure
- risks
- verification
- examples/checks/references metadata
- policy and trust fields
- technique IDs
- boundary cases and negative phrases

Search filters:

- scope
- status
- invocation mode
- implicit activation policy
- trust posture
- mutation surface
- project family
- support artifact presence
- stale/fresh install status
- technique dependency
- collision family

Exit gate:

- query returns evidence-linked hits
- every hit has section/source refs
- no semantic backend required

### Phase 3: Explanation and policy gate

Goal: make routing decisions auditable.

Candidate interfaces:

- separate search and candidate-explanation interfaces;
- or a unified `scripts/skill_intelligence.py` with subcommands.

Explanation packet:

- selected skill
- top positive evidence
- top negative/near-miss evidence
- activation class: invoke, suggest, manual, rejected, route-away
- policy reason
- owner route reason
- freshness reason
- support docs to load next
- expected validation path

Exit gate:

- manual skills never become hidden activation
- suggest skills remain candidate-only
- risk-ring skills require explicit posture
- near-miss cases are visible

### Phase 4: Integration with tiny-router and aoa-routing

Goal: keep current router assets while giving them a deeper backend.

Tasks:

- Keep `tiny_router` as stage-1 low-context shortlist.
- Feed the registry/search layer into `aoa-routing` as optional stage-2
  evidence, not as routing authority.
- Add a cross-repo contract:
  - `aoa-skills` exposes skill candidate/explain packets
  - `aoa-routing` consumes them for broader owner-route decisions
  - `aoa-sdk` may wrap both behind typed APIs

Possible outputs:

- `generated/skill_router_evidence_packets.json`
- `generated/skill_router_contract.json`
- `aoa-routing` fixture updates later, in a separate downstream commit

Exit gate:

- two-stage router still validates
- no route hint auto-activates a skill
- owner-route stop-lines survive the integration

### Phase 5: Semantic backend and rerank provider

Goal: improve fuzzy retrieval without weakening source truth.

Provider contract:

```text
index(documents, provenance) -> receipt
search(query, filters, k) -> hits
rerank(query, hits, policy) -> ranked hits
status() -> freshness and capability
explain(hit) -> source refs and index refs
```

Portable default:

- SQLite FTS5

Optional providers:

- `abyss-machine` local search/rerank where available
- `abyss-stack` runtime service only if project runtime orchestration is needed
- future vector store only behind the same status/explain/freshness contract

Exit gate:

- semantic backend off: all tests still pass
- semantic backend on: every hit still points to source refs
- stale semantic index cannot be treated as current

### Phase 6: DAG and graph intelligence

Goal: move from flat retrieval to explainable topology.

Build from:

- `generated/skill_graph.json`
- technique dependencies
- eval catalog refs
- route-surface refs
- support resources
- install/adoption receipts
- boundary matrix
- quality audit
- promotion pressure

Outputs:

- graph view for humans
- JSON graph for agents
- query helpers for "why", "where", "what next"

Exit gate:

- graph edges are source-linked
- no generated graph becomes source authority
- graph can explain at least:
  - skill to technique
  - skill to eval
  - skill to installed copy
  - skill to adjacent/conflicting skill
  - skill to owner route

### Phase 7: Evals and reality trials

Goal: prove that routing quality improves and does not create surprise
activation.

Test classes:

- positive exact trigger
- positive fuzzy trigger
- negative near-miss
- collision family
- manual-only false activation
- suggest-only false activation
- risk-surface pre-mutation
- stale install
- wrong owner repo
- generated-source confusion
- unsafe third-party skill
- legacy wording trap
- project overlay vs core skill confusion

Likely owner split:

- `aoa-skills`: fixture cases, builder validation, local policy checks
- `aoa-evals`: reusable proof doctrine and broader eval bundles if the suite
  grows into a proof object

Exit gate:

- baseline eval exists before semantic backend is trusted
- false-positive manual activation is zero
- route-away cases are explicitly tested

### Phase 8: Workspace and downstream rollout

Goal: make the layer useful across `/srv/AbyssOS`.

Rollout targets:

- `/srv/AbyssOS/.agents/skills`
- sibling repos consuming shared skill pack
- `aoa-routing` stage-2 routing
- `aoa-sdk` typed helpers
- `aoa-stats` derived observability, if adoption/freshness summaries are useful

Important:

- install/adoption truth must be separated from source truth
- generated and installed pack parity must be checkable
- copy-mode should remain default unless a target has verified symlink contract
- downstream commits should remain owner-safe and separate from `aoa-skills`

Exit gate:

- workspace adoption audit shows parity for intended targets
- stale installs are visible
- no downstream repo receives unreviewed source-law changes

## 5. Proposed CLI Surface

These names are provisional.

### 5.1 Build and validate

Build registry and search-index projections in parity mode, then validate both
contracts.

### 5.2 Query and explain

Exercise ordinary lookup, mutation-sensitive lookup, candidate explanation,
and policy-aware explanation.

### 5.3 Status and freshness

Inspect repo-local status, workspace-wide freshness, and adoption against the
project-foundation profile.

### 5.4 Future aoa-sdk wrapper

Later, after `aoa-skills` source implementation is stable, a future SDK wrapper
could expose skill search, candidate explanation, skill-graph inspection, and
workspace status as separate operations.

`aoa skills ...` remains skill-only. It should not become general route
authority, memory authority, or proof authority.

## 6. Data Model Draft

### 6.1 Registry top level

```json
{
  "schema_version": 1,
  "profile": "skill-intelligence-registry-v1",
  "owner_repo": "aoa-skills",
  "generated_at": "...",
  "source_inputs": [],
  "skills": [],
  "views": {},
  "freshness": {},
  "validation_refs": []
}
```

### 6.2 Skill entry

```json
{
  "name": "aoa-source-of-truth-check",
  "scope": "core",
  "status": "canonical",
  "source": {
    "skill_path": "skills/core/engineering/aoa-source-of-truth-check/SKILL.md",
    "techniques_path": "skills/core/engineering/aoa-source-of-truth-check/techniques.yaml",
    "content_hash": "..."
  },
  "policy": {
    "invocation_mode": "...",
    "implicit_activation_policy": "invoke|suggest|manual",
    "trust_posture": "...",
    "mutation_surface": "...",
    "requires_manual_invocation": false
  },
  "sections": [],
  "resources": [],
  "lineage": {},
  "boundaries": {},
  "evaluation": {},
  "graph_refs": [],
  "install_refs": [],
  "search_docs": []
}
```

### 6.3 Search document

```json
{
  "doc_id": "skill:aoa-source-of-truth-check:section:trigger-boundary",
  "skill_name": "aoa-source-of-truth-check",
  "section_role": "trigger_boundary",
  "source_path": ".../SKILL.md",
  "source_anchor": "## Trigger boundary",
  "text": "...",
  "policy_tags": [],
  "owner_tags": [],
  "risk_tags": []
}
```

### 6.4 Candidate packet

```json
{
  "intent": "...",
  "candidate": "aoa-source-of-truth-check",
  "candidate_class": "invoke|suggest|manual|rejected|route-away",
  "stage_scores": {},
  "positive_evidence": [],
  "negative_evidence": [],
  "policy_decision": {},
  "freshness": {},
  "next_load_refs": [],
  "explanation": "..."
}
```

## 7. Key Risks

### 7.1 Semantic layer steals authority

Risk:

- embeddings or rerank starts acting like source truth

Countermeasure:

- every result needs source refs, hashes, freshness, and policy explanation
- semantic backend remains optional

### 7.2 Manual skills become hidden activation

Risk:

- fuzzy match makes a risk skill execute silently

Countermeasure:

- activation class is computed from `implicit_activation_policy`
- eval suite includes zero-tolerance manual false activation cases

### 7.3 Router and skill boundaries collapse

Risk:

- `aoa-routing` or `aoa-skills` starts owning the other's job

Countermeasure:

- `aoa-skills` returns skill evidence packets
- `aoa-routing` decides broader owner routes
- neither overrides source-owned meaning

### 7.4 DAG becomes a fake world model

Risk:

- graph edges become claims stronger than source docs

Countermeasure:

- graph edges must be typed, source-linked, and weaker than owners
- graph is explanation and navigation, not authority

### 7.5 Installed skill packs drift silently

Risk:

- workspace root or sibling repo uses stale skill copy

Countermeasure:

- install refs and hashes in registry
- adoption audit becomes part of status
- status command names stale surfaces

### 7.6 Public-share leakage

Risk:

- planning or diagnostic artifacts expose raw logs or private session detail

Countermeasure:

- sanitized summaries only
- no raw hook dumps in strategy docs
- public-share guard before public docs or broad publication

## 8. Validation Strategy

### 8.1 Narrow builder checks

Check catalog and tiny-router projection parity, then validate tiny-router
inputs.

### 8.2 New registry checks

Future:

Check registry and search-index projection parity, then validate both new
contracts.

### 8.3 Search acceptance checks

Required query classes:

- "bounded repo change with validation" -> `aoa-change-protocol` likely
- "write architectural decision" -> `aoa-adr-write` likely
- "docs/source truth conflict" -> `aoa-source-of-truth-check` likely
- "property invariant behavior" -> `aoa-property-invariants` likely
- "prepare public-safe logs" -> `aoa-sanitized-share` manual/risk posture
- "production infra mutation" -> risk-ring explicit gate
- "continue reviewed session closeout" -> session-growth candidates, manual
- "route to technique" -> route-away or technique bridge, not skill takeover

### 8.4 Integration checks

Cover portable skills and support resources, evaluation and quality gates,
promotion pressure and workspace adoption, packaging smoke, and the repository
test suite.

### 8.5 Cross-repo checks

Later, when downstream changes occur:

- `aoa-routing`:
  - two-stage router projection parity and validation against `aoa-skills`
- `aoa-sdk`:
  - compatibility check for `aoa-skills`
  - typed helper tests if new API wrappers land
- `aoa-evals`:
  - eval bundle validation if routing proof moves there
- workspace:
  - adoption audit after install pack refresh

## 9. First Concrete Implementation Slice

The smallest useful first slice should be:

1. Add schema for `skill_intelligence_registry`.
2. Add builder that merges existing deterministic inputs.
3. Generate registry JSON and min JSON.
4. Add tests for:
   - all 45 skills present
   - source refs exist
   - policy fields present
   - support artifacts represented
   - graph refs represented
   - generated output deterministic
   - no manual skill classified as auto-invokable
5. Add a read-only `inspect/search` prototype only if it can be small.
6. Do not add semantic backend in the first slice.
7. Do not modify downstream repos in the first slice.

Why this first:

- It gives a durable source-derived base.
- It does not depend on model choice.
- It avoids premature semantic magic.
- It prepares RAG/DAG without making them authority.

## 10. Second Concrete Slice

After the registry is stable:

1. Add SQLite/FTS search build.
2. Add `query` CLI.
3. Add source-linked search hit packets.
4. Add policy-aware result classes.
5. Add examples and tests.
6. Add status/freshness report over source/export/install parity.

Exit:

- usable local search exists on a clean machine
- all hits explain source and policy
- no semantic backend required

## 11. Third Concrete Slice

After portable search works:

1. Add `explain` command.
2. Add near-miss and rejection explanations from boundary matrix.
3. Add tiny-router integration comparison.
4. Add false-positive/false-negative eval fixtures.
5. Prepare `aoa-routing` downstream contract proposal.

Exit:

- future agents can ask "why this skill" and receive a bounded packet
- route-away is first-class

## 12. Fourth Concrete Slice

Only then:

1. Add optional semantic provider contract.
2. Add provider `status()` and freshness gates.
3. Add rerank as optional improvement.
4. Add DAG/graph query helpers.
5. Add downstream typed wrappers.

Exit:

- semantic search improves recall without changing authority
- graph explains routes without replacing source

## 13. Open Questions Before Implementation

1. Should the first durable decision record live in `docs/decisions/`, or
   should this remain a legacy strategy until the first implementation slice is
   accepted?
2. Should the SQLite database be committed, generated on demand, or stored in a
   local ignored cache with a committed manifest?
3. Should `aoa-routing` consume `skill_intelligence_registry` directly, or only
   a smaller exported evidence packet?
4. Should `aoa-sdk` get CLI wrappers in the same release cycle or after the
   source layer stabilizes?
5. Should workspace install freshness be part of `aoa-skills` generated output
   or only an audit report?
6. Which semantic provider is first: none, `abyss-machine`, or a generic local
   embeddings adapter?
7. Do we need a separate `aoa-kag` projection for long-term graph/rag substrate,
   or can the first DAG stay local to `aoa-skills`?

## 14. Stop Lines

Stop and re-route if:

- implementation starts changing actual skill wording without a skill-editing
  reason
- generated files are hand-edited
- semantic backend becomes required for core behavior
- a routing output starts activating a skill
- a graph edge starts overriding source truth
- a sibling repo's doctrine is copied into `aoa-skills`
- public-share claims appear without sanitization review
- installed pack drift is hidden instead of reported

## 15. Suggested Next Session Opening

Recommended start:

```text
We are implementing the first slice of the AoA Skill Intelligence Layer from
aoa-skills/legacy/2026-05-17__skill-intelligence-layer-strategy.md.
Read root AGENTS.md, DESIGN.md, docs/ARCHITECTURE.md, generated/AGENTS.md,
schemas/AGENTS.md, scripts/AGENTS.md, and the strategy artifact. Do not add
semantic backend yet. First land the deterministic registry schema, builder,
generated outputs, and tests. Keep generated surfaces source-derived.
```

The first route should enter and guard the `aoa-skills` workspace for a bounded
code mutation, then inspect root guidance, design and architecture, the nearest
generated/schema/script cards, and this strategy artifact before implementation.

## 16. Current Artifact Closeout

This file is intentionally not linked from active route docs yet.

It should be treated as:

- a temporary planning artifact
- a strategy packet for the next implementation pass
- a record of current reconnaissance
- not an ADR
- not a roadmap
- not generated truth
- not a public release note

The next owner route is `aoa-skills` first, with later handoffs to
`aoa-routing`, `aoa-sdk`, `aoa-evals`, and possibly `aoa-kag` only after the
source-derived registry/search base exists.

## 17. Execution Closeout: First Slice Landed

Status: implemented in the local worktree.

Landed surfaces:

- `scripts/skill_intelligence_surface.py`
- `scripts/skill_intelligence.py`
- `schemas/skill_intelligence_registry.schema.json`
- `generated/skill_intelligence_registry.json`
- `generated/skill_intelligence_registry.min.json`
- `tests/test_skill_intelligence_surface.py`
- `scripts/build_catalog.py` integration for the new generated surface
- schema validation coverage in `tests/test_generated_surface_schemas.py`
- architecture, generated-lane, and changelog notes for the derived registry

The first slice now provides:

- deterministic registry over all source skills
- source refs, content hashes, policy/runtime/support/evaluation/graph evidence
- lexical SQLite FTS search with source-derived fallback
- candidate explanation with positive and boundary evidence
- status check for registry freshness and local install visibility
- minified portable registry without full search text

Kept out of scope on purpose:

- semantic backend
- committed SQLite database
- downstream repo mutation or rollout
- automatic skill status promotion
- routing authority changes
- edits to skill meaning

Notable correction during landing:

- the registry builder was made tolerant of minimal test repositories by falling
  back to authored `SKILL.md` and `techniques.yaml` evidence when runtime/support
  generated inputs are absent; real repo builds still consume the richer
  generated evidence when present.
- the SQLite search connection is explicitly closed, so release checks do not
  leave resource warnings.

Verification evidence:

- catalog and skill-intelligence projection parity;
- resource-warning-clean lookup and candidate explanation;
- focused skill-intelligence, generated-schema, and catalog tests;
- agent-card, skill-source, and portable-export validation;
- description-trigger, support-resource, and tiny-router parity;
- evaluation, quality, promotion-pressure, and workspace-adoption reports;
- the repository and release lanes, plus diff hygiene.

Current next route:

- commit this `aoa-skills` source slice when requested
- separately decide whether the adoption drift reported for sibling repos should
  be handled as a rollout task
- only after that, design the next semantic/RAG/DAG layer as an additive surface
  over the committed registry rather than a replacement for it
