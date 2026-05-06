# Epistemic Candidate Boundary

This part keeps epistemic Agon workflow pressure candidate-only at the
`aoa-skills` layer.

## Purpose

Skills may later draft bounded packets, review bundles, or execution checklists
around epistemic Agon pressure. They do not decide truth, write memory, mutate
agent standing, activate live sessions, or promote a candidate into protocol.

## Inputs

- `mechanics/agon/parts/epistemic-candidate-boundary/config/agon_epistemic_skill_candidates.seed.json`
- `mechanics/agon/parts/epistemic-candidate-boundary/schemas/`
- `mechanics/agon/parts/epistemic-candidate-boundary/examples/`
- `generated/agon_epistemic_skill_candidates.min.json`
- reviewed practice evidence from the stronger owner route

## Outputs

- requested-only epistemic skill candidates
- bounded workflow notes for later review
- validation route for candidate shape

No output here is a live protocol, proof verdict, memory write, or skill
promotion.

## Validation

```bash
python mechanics/agon/parts/epistemic-candidate-boundary/scripts/build_agon_epistemic_skill_candidates.py --check
python mechanics/agon/parts/epistemic-candidate-boundary/scripts/validate_agon_epistemic_skill_candidates.py
python -m pytest -q mechanics/agon/parts/epistemic-candidate-boundary/tests/test_agon_epistemic_skill_candidates.py
```
