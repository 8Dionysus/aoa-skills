# Spark Swarm Recipe — aoa-skills

Рекомендуемый путь назначения: `Spark/SWARM.md`

## Для чего этот рой
Используй Spark здесь для одного skill или одного thin overlay за раз: trigger boundaries, support artifacts, generated surfaces, evidence view, manifest-driven refresh и bounded bridge с `aoa-techniques`. Рой должен помнить, что это execution canon, а не proof, memory, role или playbook layer.

## Читать перед стартом
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/BRIDGE_SPEC.md`
- `docs/RUNTIME_PATH.md`
- `docs/EVALUATION_PATH.md`
- `SKILL_INDEX.md`

## Форма роя
- **Coordinator**: выбирает один skill или один overlay seam
- **Scout**: картографирует `SKILL.md`, manifest, technique refs, generated surfaces и tests
- **Builder**: правит только выбранный skill/overlay
- **Verifier**: запускает validate / inspect / build loop
- **Boundary Keeper**: следит, чтобы skill не превратился в technique, playbook, eval или role layer

## Параллельные дорожки
- Lane A: `SKILL.md` / manifest / support artifacts
- Lane B: generated catalog or evidence surfaces if needed
- Lane C: targeted tests / evaluation evidence / drift review
- Не запускай больше одного пишущего агента на одну и ту же семью файлов.

## Allowed
- tighten one bounded workflow bundle
- чинить trigger boundaries и verification wording
- освежать generated surfaces, walkthroughs, evaluation matrix или public surface
- делать thin overlay changes без скрытых project assumptions
- делать explicitly named bridge refresh with `aoa-techniques`

## Forbidden
- изобретать новый technique meaning внутри skills
- превращать skill в playbook
- переносить proof claims из `aoa-evals` сюда
- тащить сюда memory or role contract semantics
- массово refresh-ить несколько skills в одном проходе

## Launch packet для координатора
```text
We are working in aoa-skills with a one-repo one-swarm setup.
Pick exactly one target:
- one named skill
- one named overlay
- one named bridge drift seam

First return:
1. chosen target
2. exact files to touch
3. whether generated surfaces are expected to change
4. whether aoa-techniques follow-up is likely

Split the swarm:
- Scout: map only
- Builder: one minimal diff lane
- Verifier: run validate/inspect/build loop
- Boundary Keeper: anti-layer-collapse review
```

## Промпт для Scout
```text
Map only. Do not edit.
Return:
- target skill files
- related generated surfaces
- related tests/evidence surfaces
- whether technique refs have drifted
- whether this should stay a skill or belongs elsewhere
```

## Промпт для Builder
```text
Make the smallest reviewable change.
Rules:
- keep the workflow bounded and executable
- preserve traceability to techniques
- keep overlays thin
- if generated surfaces change, rebuild them explicitly and say why
```

## Промпт для Verifier
```text
Run the repo validation loop and report actual results.
Preferred target-aware commands:
- python scripts/validate_skills.py --skill <skill>
- python scripts/build_catalog.py --check
- python scripts/inspect_skill.py --skill <skill>
- python scripts/inspect_skill.py --skill <skill> --view evidence
If generated surfaces changed, also run:
- python scripts/build_catalog.py
Optional bridge check when relevant:
- python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques
```

## Промпт для Boundary Keeper
```text
Review only for anti-scope.
Check:
- this is still a bounded workflow bundle
- not a technique canon patch
- not a proof-layer patch
- not a memory or role contract patch
- overlays stayed thin
- only explicitly named skills were refreshed
```

## Verify
```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py --skill <skill>
python scripts/build_catalog.py --check
python scripts/inspect_skill.py --skill <skill>
python scripts/inspect_skill.py --skill <skill> --view evidence
python scripts/build_catalog.py   # only if generated surfaces changed
```

## Done when
- ровно один skill or overlay seam обновлён
- generated surfaces в порядке или не тронуты
- skill остаётся bounded, reviewable and executable
- bridge drift, если был, назван явно

## Handoff
Если изменение поднимает reusable practice, следующий ход идёт в `aoa-techniques`. Если поднимает bounded proof claim, следующий ход идёт в `aoa-evals`.
