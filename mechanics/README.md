# Mechanics

`mechanics/` is the owner-local home where `aoa-skills` participates in the
cross-project AoA mechanics.

This district keeps skill-layer movement around candidate intake, activation,
recurrence, release support, checkpoint carry, quest dispatch, adoption, and
downstream bridge pressure out of the flat docs surface without pretending those
surfaces are canonical skill bundles.

Skill bundles still live under `skills/`. Generated reader and export surfaces
still live under `generated/` and `.agents/skills/`.

## Owner-request receipts

[mechanics/OWNER_REQUEST_RECEIPTS.md](OWNER_REQUEST_RECEIPTS.md) is the
owner-local receipt surface for `Agents-of-Abyss` owner requests assigned to
`aoa-skills`.
It records which requests are landed here, which are accepted but not landed,
and which center claims must still remain blocked by owner-local proof,
canonical skill review, or later package work.

The receipt surface answers the center queue. It does not replace
`skills/**/SKILL.md`, generated exports, proof routes, or sibling-owner truth.

## Artifact topology

[mechanics/ARTIFACT_TOPOLOGY.md](ARTIFACT_TOPOLOGY.md) owns the placement law
for schemas, examples, config, generated companions, manifests, scripts, tests,
and quests that sit near mechanics.

Use it before moving artifacts between root technical districts and mechanic
homes. Root districts keep repo-wide contracts and root-published read models;
mechanic-owned substance lives with the package or nearest part.

## Cross-mechanics map

- [method-growth](method-growth/README.md): reviewed candidate lineage,
  candidate-ref refinery, first owner-status landing, governed followthrough,
  and adoption lifecycle posture.
- [growth-cycle](growth-cycle/README.md): adaptive orchestration, closeout and
  harvest separation, and session-growth kernel maturity guidance.
- [checkpoint](checkpoint/README.md): checkpoint-note protocol and the
  boundary from provisional carry into explicit reviewed closeout.
- [questbook](questbook/README.md): durable skill obligations,
  session-harvest posture, and generated quest dispatch projection boundaries.
- [recurrence](recurrence/README.md): live observation producers and
  recurrence-fed review decision closure around skill activation pressure.
- [antifragility](antifragility/README.md): fallback authoring, via negativa
  pruning, and collision-stress routing below skill canon.
- [rpg](rpg/README.md): ability-card and loadout reader posture over existing
  skill bundles.
- [agon](agon/README.md): requested-only bounded workflow candidates behind
  lawful moves, skill-binding candidate surfaces, and observation-only
  recurrence pressure.
- [audit](audit/README.md): audit contract, evaluation evidence, public-status
  readouts, activation checks, and review-evidence routing.
- [experience](experience/README.md): governance, consent, service handoff,
  office-task, receipt, installation, policy-hold, and rollback workflow
  posture below skill canon.
- [boundary-bridge](boundary-bridge/README.md): layer-position, technique-skill
  bridge, thin overlays, adapter wiring, tiny-router, and downstream
  stop-line surfaces.
- [release-support](release-support/README.md): portable export, install
  profiles, local adapter, runtime seams, support-resource packaging, and
  release verification surfaces.

## Package card standard

Each `mechanics/<slug>/README.md` is an agent-operable local card. It should
let a reader answer when to use the mechanic, what this repository owns, which
stronger owners keep final truth, what may enter, what may leave, what must not
be claimed, how to validate the route, and where to go next.

Use these headings in package READMEs:

| Heading | Purpose |
|---|---|
| `## Mechanic card` | compact package status and entry posture |
| `### Trigger` | when the local mechanic applies |
| `### Local owns` | what `aoa-skills` may author here |
| `### Stronger owner split` | AoA center or sibling owners that keep stronger truth |
| `### Inputs` | material that may enter this mechanic |
| `### Outputs` | material that may leave without becoming skill canon by itself |
| `### Must not claim` | stop-lines that keep the package below stronger owners |
| `### Validation` | where to find exact checks for this package |
| `### Next route` | the next active surface, provenance bridge, or owner route |

This mirrors the AoA center card shape, but adapts the authority. `aoa-skills`
does not say `Center owns`; it says what the skill-execution layer owns, then
routes stronger law or acceptance to `Agents-of-Abyss`, sibling repositories,
review records, generated companions, or downstream owners only when relevant.

## Active and historical split

When a mechanic has grown through historical batches, seeds, receipts, candidates, or
runtime/export pressure, do not flatten every file into the package root.

Prefer this shape:

- active route in `README.md`, `DIRECTION.md`, `PARTS.md`, and `parts/`
- provenance bridge in `PROVENANCE.md`
- checked landing history in `LANDING_LOG.md`
- future route pressure in `ROADMAP.md`
- artifact placement law in root `ARTIFACT_TOPOLOGY.md`
- source-to-active accounting in package-local `legacy/` when preserved source
  material exists

Use the package card first, then open active parts. Enter legacy only when the
source route matters.

## Boundary

Mechanics can prepare, route, constrain, and preserve skill-layer movement.
They do not replace canonical skill bundles, generated exports, proof doctrine,
playbook scenario canon, role contracts, routing policy, runtime infrastructure
truth, memory objects, or downstream project authority.

Generated surfaces may reflect mechanics, but they do not author mechanics
meaning.
