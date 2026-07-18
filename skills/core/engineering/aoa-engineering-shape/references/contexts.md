# Map bounded contexts

### Mode: contexts

Use this mode for one concrete ambiguity where meanings, responsibilities,
owners, portability postures, or lifecycle surfaces are overloaded. Do not use
it for a tiny local edit, a stable consumer contract, a single reusable rule,
or a dependency seam whose responsibility boundary is already clear.

Required inputs:

- target area and the exact ambiguity constraining the next change
- current vocabulary, responsibilities, neighboring contexts, and interfaces
- target-specific owner declarations and stronger owner routes
- portability, lifecycle, authority, generated/source, or handoff distinctions
  that materially affect this ambiguity

Return a `bounded-context-map` containing named responsibility centers,
inside/outside rules, target-bound owners or unresolved owner edges, interfaces,
translations, portability posture, vocabulary corrections, and the next-change
stop line.

Procedure:

1. Confirm one concrete ambiguity. Route broad architecture, taxonomy, or
   governance programs away instead of pretending to map everything.
2. Select two to four boundary lenses that change where the next work belongs,
   which owner is stronger, or what must stay out of scope. Drop any lens that
   only adds a label.
3. Name contexts by responsibility rather than directory, team, current
   implementation, or tool.
4. For each context, state what it owns, consumes, produces, and must not own.
5. Distinguish portable meaning from ecosystem integration, local
   implementation, generated projection, and historical provenance when these
   coexist.
6. Trace interfaces, translations, handoffs, and stop lines. Preserve typed
   cross-relations instead of forcing every relation into a hierarchy.
7. Resolve overloaded terms and state how the map constrains the next change,
   including what must route elsewhere.

Boundary lenses:

| Lens | Use when | Clarifying question | Common failure |
|---|---|---|---|
| Object kind | Different object classes are treated as one thing. | Is this a procedure, workflow, eval, memory object, route, role, generated view, runtime body, or source node? | One object becomes a weak substitute for another. |
| Owner | More than one repository or surface could claim the truth. | Which owner can change this meaning, and which surfaces only point to it? | A local note absorbs stronger owner law. |
| Layer | Procedure, execution, proof, routing, memory, role, derived, runtime, and source layers are blending. | Which layer owns meaning, and which only composes, derives, runs, or routes it? | Layer labels decorate the map while authority still drifts. |
| Surface state | Authored source, generated output, export, adapter, archive, candidate, receipt, and live evidence are mixed. | Is the surface authoritative, derived, transported, historical, provisional, or operational evidence? | Generated or historical material acts as current source truth. |
| Lifecycle | Seed, candidate, evaluated, admitted, deprecated, live, and planned posture are confused. | What is true now, what is planned, and what is only provenance? | A future direction or old receipt becomes current status. |
| Workflow or process | Task, session, checkpoint, closeout, playbook, and roadmap are treated as equivalent. | Is this temporary execution context, reviewed evidence, durable procedure, or program direction? | Session-local hints become durable canon. |
| Authority or proof | Claims, evidence, tests, evals, verdicts, assumptions, and trust language are blending. | What claim is being made, what can prove it, and what remains unproven? | Proof language becomes stronger than evidence. |
| Portability | Public reusable meaning and local integration details both matter. | What must work without local paths, secrets, runtime state, or ecosystem-only assumptions? | A portable surface quietly depends on private context. |
| Runtime or body | Docs, config, service state, storage, automation, and source code are confused. | Is the change authoring meaning, configuring behavior, running infrastructure, or reporting a run? | Documentation pretends to operate the system. |
| Interface or handoff | Contexts touch through a seam, adapter, export, import, bridge, or review route. | What crosses the boundary, in what shape, and who receives it next? | The map names contexts but leaves exchange implicit. |
| Vocabulary | One term means different things in different contexts. | Which term should be narrowed, qualified, or retired for this task? | Synonyms multiply while responsibilities stay unclear. |
| Time or freshness | Current, historical, generated-at, released, stale, and planned facts are mixed. | Which facts are current enough, and which require fresh verification? | An old plan or timestamp drives a current decision. |
| Risk or approval | The boundary crosses destructive, security, privacy, public, or irreversible action. | What requires approval, preview, sanitization, or rollback? | Risk-heavy work hides behind ordinary wording. |
| Role or agency | Actor, role, persona, skill, playbook, runtime agent, and autonomy language are blurring. | Who acts, under which contract, and what authority is not granted? | Role language becomes hidden execution authority. |
| Scale | File, package, repository, workspace, federation, and public profile scope are mixed. | What is the smallest scope that can honestly resolve the ambiguity? | A local ambiguity turns into federation governance. |

Compact output shape:

| Field | Required content |
|---|---|
| Concrete ambiguity | The one next change or overloaded meaning being constrained. |
| Selected lenses | Only lenses that change an owner, boundary, handoff, or stop line. |
| Responsibility centers | What each context owns, consumes, produces, and must not own. |
| Stronger owner or source | Exact governing declaration, or an unresolved owner edge. |
| Interfaces | Typed handoffs or translations between contexts. |
| Vocabulary | Preferred qualified terms and the overloaded term to avoid. |
| Route-away lines | Work that belongs to a stronger owner or another mode. |
| Next-change constraint | What the next diff may touch and must leave alone. |
| Verification | How the ambiguity was reduced without claiming adoption. |

Contracts and risks:

- mapping cannot transfer authority from a stronger owner
- public portable meaning must remain usable without hidden local deployment
- do not multiply contexts, rename without reducing ambiguity, exhaust a lens
  checklist, or freeze one repository/session shape as universal law

Verify that the ambiguity is smaller, each material interface and route-away is
visible, the selected distinctions are necessary, and a future change can tell
both what belongs and what stays out of scope.
