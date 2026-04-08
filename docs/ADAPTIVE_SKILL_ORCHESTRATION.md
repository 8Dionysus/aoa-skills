# Adaptive skill orchestration

This document defines how `aoa-skills` should be orchestrated when a session
touches more than one plausible skill, ring, or post-session promotion lane.

The goal is not to make skill use more rigid.
The goal is to keep skill use semantically honest so the agent does not confuse:

- doing the current task
- closing out what the task proved
- harvesting reusable outcomes from the session

## Problem shape

Hard keyword routing is not enough.
A request like "apply the core ring" can fail in two opposite ways:

- the agent runs too many skills mechanically
- the agent narrows too hard and misses the closeout or harvest layer

The correct response is an explicit applicability read, not blind expansion.

## Core rule

Treat skill orchestration as an adaptive interpretation problem:

- decide which skills apply now
- name which skills do not apply and why
- separate execution from closeout
- separate closeout from session harvest and promotion

Do not treat "ring application" as "run every skill in the ring."

## Three execution planes

### `task execution`

Use this plane for skills that directly help do the current work:

- bounded change
- contract hardening
- refactor
- audit of the target surface

### `session closeout`

Use this plane for skills that clarify what the session actually proved:

- source-of-truth clarification
- bounded-context clarification
- invariant coverage review
- explicit report of remaining gaps

### `harvest and promotion`

Use this plane when the session has produced reusable donor units or owner-layer
promotion pressure:

- repeated workflow candidates
- proof-surface candidates
- playbook candidates
- memo or agent-layer candidates
- automation readiness signals

This plane usually belongs to the explicit session-harvest family rather than
to the original task skills.

## Applicability map contract

Before saying a ring or skill family has been "applied", produce an
applicability map.

Each relevant skill must receive one of these statuses:

- `apply_now`
- `defer`
- `skip`

Each status must carry one short reason.

Use `defer` when:

- the skill is probably relevant, but only after another plane closes
- the current evidence is still too weak
- the surviving question belongs to closeout or harvest rather than execution

Use `skip` when:

- the current task does not match the skill boundary
- using the skill would be ceremonial rather than clarifying
- the real need belongs to a different owner layer

Use [SKILL_APPLICABILITY_MAP.template.md](../templates/SKILL_APPLICABILITY_MAP.template.md)
for a bounded written form.

## Ring request interpretation

When a user asks to apply a ring:

1. enumerate the ring members that are actually in scope
2. build the applicability map
3. run all `apply_now` skills
4. report all `defer` and `skip` decisions explicitly
5. check whether the session now requires a harvest move

Do not silently compress steps `4` and `5`.

## Skill handoff semantics

A skill should not only say when it applies.
It should also help another agent know when it is no longer enough.

Canonical `SKILL.md` bodies should therefore make these things explicit:

- what the skill produces
- when the skill is not enough
- common misroutes
- which next skills or owner layers are the honest handoff
- what promotion signals, if any, may survive the run

The `SKILL.md` template now carries those sections directly.

Note: this document does not require new frontmatter fields today.
Keep the current machine-checked metadata stable until the repo explicitly adds
validator support for more structured orchestration metadata.

## Session closeout check

After the execution-plane skills finish, ask these questions:

- what bounded result was actually achieved
- what stable truth was actually constrained
- what remained only trial-local or anecdotal
- what route or owner ambiguity survived
- what reusable object, if any, emerged here

If the answer to the last two questions is meaningful, the session likely needs
either a closeout note or a harvest step rather than a plain recap.

## Harvest trigger signals

Escalate toward the session-harvest family when one or more of these signals
survive closeout:

- a reusable workflow or donor pattern appeared
- owner-layer ambiguity remains after the task itself is done
- a repeated manual route looks stable enough for automation classification
- the session produced a likely proof, playbook, memo, or agent-layer object
- the next honest move is promotion triage rather than more execution

Use [SESSION_CANDIDATE_HARVEST.template.md](../templates/SESSION_CANDIDATE_HARVEST.template.md)
to keep that handoff bounded, and store committed public-safe harvest notes
under `docs/session-harvests/` rather than inside the skill-review surfaces.

## Relationship to checkpoint and session-harvest layers

This protocol does not replace the existing post-session family.

The honest route remains:

`task skills -> closeout read -> checkpoint note or candidate harvest note -> explicit session-harvest family`

Use:

- [CHECKPOINT_NOTE_PATH.md](CHECKPOINT_NOTE_PATH.md) for lower-authority checkpoint capture
- [QUESTBOOK_SKILL_INTEGRATION.md](QUESTBOOK_SKILL_INTEGRATION.md) for the installed session-harvest family posture

## Anti-patterns

- pretending every ring request means "use every skill"
- silently shrinking scope to avoid naming deferred skills
- treating closeout and harvest as the same thing
- using harvest language without an actual reusable object
- forcing owner-layer promotion before the task result is even clear
- treating a session recap as if it already were a harvest packet

## Minimal closeout deliverable

At the end of a non-trivial session, the agent should be able to answer:

- which skills ran now
- which skills were deferred and why
- which skills were skipped and why
- what the session actually proved
- what reusable candidates, if any, now exist
- what the next honest owner layer is
