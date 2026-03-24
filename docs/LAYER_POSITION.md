# Layer Position

This note explains where `aoa-skills` sits in the AoA layer map and why its
boundary stays narrower than neighboring repositories.

Use it when the question is not "which skill should I open next?" but "what
kind of meaning does this repo own, and what stays upstream or downstream?"

## Why This Repo Exists

`aoa-skills` exists to hold the bounded execution layer of AoA.

That means this repo owns:

- reusable Codex-facing workflow bundles
- explicit runtime boundaries for agent use
- technique traceability and composition records
- derived runtime, evaluation, and governance reader surfaces built from
  committed skill sources

It does not own the reusable practice canon itself, scenario-level method,
verdict doctrine, routing policy, runtime infrastructure policy, or memory
objects.

## What Skills Inherit From Techniques

Skills inherit reusable practice from `aoa-techniques`.

- `aoa-techniques` owns technique meaning, bounded practice contracts, risks,
  validation, and adaptation notes
- `aoa-skills` packages one or more of those techniques into a reviewable
  agent-facing workflow
- a skill may summarize or compose techniques, but it should not silently
  replace technique canon or drift into a second technique repository

This is the skill-side landing slice for the AoA ontology spine: skills are one
bounded execution layer, not a place to absorb every neighboring layer.

## What Stays In Playbooks

Method lives in `aoa-playbooks`, not in `aoa-skills`.

- a skill packages bounded workflows and local execution guidance
- a playbook owns recurring scenario method, route structure, longer-horizon
  composition, and executable scenario canon
- skills may be called by playbooks and may support playbook execution, but
  they do not become the home of scenario-level method just because they are
  executable

This is the skill-side landing slice for `aoa-method-lives-in-playbooks`:
skills package workflows, while recurring scenario canon stays upstream in
`aoa-playbooks`.

## Boundary Reminder

When authoring or reviewing changes here:

- inherit reusable practice from `aoa-techniques`
- keep execution bundles bounded and reviewable
- route recurring scenario method up to `aoa-playbooks`
- route verdict doctrine to `aoa-evals`
- route routing policy, runtime policy, and memory meaning to their own repos

`aoa-skills` is the bounded execution layer in the AoA map, not a convenience
bucket for neighboring meanings.
