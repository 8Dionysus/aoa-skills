# Workflow Candidate Bridge

## Purpose

This part keeps requested-only skill candidates behind Agon lawful moves in one
bounded intake route.

These are not promoted skills. They are requests for future skill work.

## Boundary

`aoa-skills` may later own:

- bounded agent-facing workflow contracts;
- trigger boundaries;
- execution checklists;
- verification guidance;
- technique traceability.

It must not own:

- lawful move vocabulary;
- arena session law;
- proof verdicts;
- durable scars;
- routing sovereignty;
- ToS canonization.

## Candidate index

The seed adds:

```text
mechanics/agon/parts/workflow-candidate-bridge/config/agon_skill_binding_candidates.seed.json
mechanics/agon/parts/workflow-candidate-bridge/schemas/agon-skill-binding-candidate.schema.json
mechanics/agon/parts/workflow-candidate-bridge/examples/agon_skill_binding_candidate.example.json
generated/agon_skill_binding_candidates.min.json
```

Each candidate is `requested_not_landed`.

Promotion into a real skill requires the normal `aoa-skills` bundle review path.

## Validation

```bash
python mechanics/agon/parts/workflow-candidate-bridge/scripts/build_agon_skill_binding_candidates.py --check
python mechanics/agon/parts/workflow-candidate-bridge/scripts/validate_agon_skill_binding_candidates.py
python -m pytest -q mechanics/agon/parts/workflow-candidate-bridge/tests/test_agon_skill_binding_candidates.py
```

## One-line rule

A skill may later execute a lawful move in bounded form. It must never define the law that made the move lawful.
