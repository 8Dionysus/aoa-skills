# Map source authority

### Mode: authority-map

Use this mode when guidance, source, config, schema, manifests, generated/export
outputs, installed copies, runtime receipts, status snapshots, legacy material,
or entrypoints overlap or disagree. Do not use it for a known deterministic
rebuild with no authority ambiguity, ordinary documentation edits, decision
rationale, or a core-versus-edge question.

Required inputs:

- target concern and all material candidate surfaces
- target-specific owner and route declarations when available
- consumers, derivation/fan-out paths, current contradictions, portability and
  lifecycle posture

Return an `authority-map` containing canonical homes by concern, role of every
surface, conflicts, source-to-consumer fan-out, active/history/generated split,
unresolved owner edges, repair handoff, effect, claim limit, and stop line.

Procedure:

1. Inventory only surfaces relevant to the named concern: authored source,
   config/schema, active contract, entrypoint, decision rationale, provenance,
   legacy history, generated/export reader, installed copy, runtime receipt,
   cache, or operational observation.
2. Read target-specific owner law and classify each surface by role. Do not
   infer authority from timestamp, detail, path prominence, availability, or
   machine proximity.
3. When the ambiguity is wider than ordinary documentation, choose the
   narrowest authority shape below. Use the shape to constrain one concern,
   one authoritative source, its weaker companions, and one verification path;
   do not turn the table into a checklist.
4. Trace which authored source produces which derived consumers and identify
   stale routes, contradictions, duplicated truth, or missing return-to-owner
   handles.
5. Resolve conflicts from owner law. If no governing declaration exists, keep
   the edge unresolved rather than selecting the newest or most convenient
   surface.
6. For one source feeding several consumers, name the complete fan-out and the
   owner rebuild/handoff route. Keep entrypoints short when canonical detail
   already exists.
7. Preserve active, historical/provenance, generated, decision, installed, and
   runtime roles instead of moving truth into a convenient reader.
8. Return the smallest clarification or owner handoff authorized by the task;
   do not silently rebuild or edit.

Authority shapes:

| Shape | Authoritative for | Weaker companions | Common failure | Verify |
|---|---|---|---|---|
| Overview to canonical detail | Orientation, public entry, start route, or quick status. | README, manifest, index, and route cards. | Overview silently becomes the full manual or copies changing state. | It stays short and names the canonical homes. |
| Source, config, schema, or manifest | Runtime behavior, allowed values, validation shape, or registry identity. | Generated docs, examples, reports, compact catalogs, and installed copies. | A readable generated summary overrides source-owned fields. | The source path is explicit and every derivative has a rebuild route. |
| Operations or runbook | Current run, deploy, recovery, rotation, or inspection procedure. | README snippets, issue notes, incident history, and terminal logs. | Historical incident text becomes current operating law. | The runbook owns current commands and links history as evidence only. |
| Generated, exported, compact, or installed | Derived transport, lookup, release artifact, or compatibility view. | Catalogs, exports, installed copies, compact indexes, and reports. | A transport or fresh timestamp becomes authoring truth. | Builder, owner source, return handle, and parity/rebuild path are named. |
| Legacy, provenance, or history | Lineage, receipts, preserved raw material, or audit trail. | Active contracts, roadmaps, tutorials, and generated indexes. | Old wording is treated as a current instruction. | Active surfaces link to history without importing its law. |
| Decision, ADR, or review note | Why a choice was made, alternatives, or a reviewed gate result. | README, roadmap, changelog, code comment, and generated report. | Rationale is hidden in status prose or mistaken for current procedure. | Future maintainers can reach the rationale from the active owner route. |
| Public entrypoint with owner overlay | Portable public meaning plus an optional route to deployment-local detail. | Private paths, secrets, host names, runtime commands, and local mirrors. | Public use requires hidden local OS knowledge or leaks owner-local details. | Public text stands alone; the overlay remains owner-qualified and optional. |
| Sibling or downstream owner context | Meaning owned by another repository, organ, or runtime layer. | Local summaries, bridge notes, and cross-repository indexes. | A nearby local file captures stronger sibling authority. | The owner route is explicit and the local surface remains a pointer or consumer. |
| Status, roadmap, or changelog | Current direction, planned movement, shipped changes, or open follow-up. | README counters, old plans, release reports, and checkpoint notes. | One status surface accumulates chronology and starts directing implementation. | Current status stays bounded; history and detailed plans have named homes. |

For a broad ambiguity, include the selected shape in the result and fill only
the fields that materially reduce it:

| Field | Required content |
|---|---|
| Concern | One authority question being resolved. |
| Candidate surfaces | Only surfaces that appear to carry authority for that concern. |
| Selected shape | The narrowest shape that changes classification or handoff. |
| Authoritative source | Exact governing surface, or `unresolved`. |
| Weaker companions | Their permitted roles and prohibited authority claims. |
| Consumers and fan-out | Every material derived or downstream surface in scope. |
| Conflict or stale route | The exact contradiction, missing return handle, or drift. |
| Verification path | Owner check, rebuild/parity route, or blocked input needed next. |

Contracts and risks:

- generated, compact, exported, installed, cached, and runtime surfaces remain
  weaker than their authored owners
- public portable surfaces must remain understandable without a hidden local OS
- avoid status chronology in entrypoints, over-formalizing tiny surfaces,
  creating labels without reducing ambiguity, or hiding sibling authority

Verify that every material concern has an explicit canonical or unresolved
home, conflicts remain visible, consumer fan-out is complete, and future work
can identify both the owner and the correct repair route.
