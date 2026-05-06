# Agon Wave IV Skill Landing

## Scope

This landing receives candidate requests from `Agents-of-Abyss` Wave IV owner binding.

It does not create canonical skills.

## Validation

```bash
python scripts/build_agon_skill_binding_candidates.py --check
python scripts/validate_agon_skill_binding_candidates.py
python -m pytest -q tests/test_agon_skill_binding_candidates.py
```

## Exit criteria

- candidate requests are deterministic;
- all candidates remain `requested_not_landed`;
- no candidate defines lawful move vocabulary;
- no candidate issues proof verdicts;
- no candidate writes durable scars;
- no candidate opens an arena session;
- no candidate silently widens task scope.

## Later growth

A later skill wave may choose reviewed candidates after practice guidance exists or after an explicit single-technique exception.

Do not convert every lawful move into a skill immediately. A named strike is not automatically a trained strike.
