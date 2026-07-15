# Repository Skill Home Port

This contract lets a repository expose its own admitted callable procedures to
Codex without making `aoa-skills` their author and without copying the shared
catalog into every repository.

## Admission Comes First

Create a top-level `skills/` home only after manual work has established at
least one repository-specific bundle with:

- a stable independent trigger and negative applicability;
- a distinct input/output contract and useful composition boundary;
- held-out benefit over no skill and the likely containing bundle;
- acceptable coexistence with the prompt-visible library;
- an owner decision that records the evidence-backed admission.

Do not create an empty port, keep candidates here, or use this contract to
turn ordinary repository instructions, facts, tools, tests, or playbooks into
skills. Raw trials and task-local DAGs remain in the session/runtime.

## Authored And Derived Surfaces

An admitted owner repository contains:

```text
skills/
├── port.manifest.json
└── <bundle-name>/
    ├── SKILL.md
    └── optional owned resources

.agents/skills/             # generated copy; never source truth
└── <bundle-name>/
```

`skills/<bundle-name>/` is canonical. The owner owns procedure meaning, local
adaptation, version, lifecycle, admission, and evidence posture.
`aoa-skills` owns only the common manifest grammar and deterministic projection
mechanism. KAG may index the owner reference and relations but does not acquire
procedure authority.

The manifest conforms to `schemas/skill-home-port.schema.json`. It lists only
admitted, prompt-advertised bundles, requires an owner and admission reference,
and declares one repo-scoped generated-copy projection at `.agents/skills`.
The projection list must exactly equal the admitted bundle list; partial or
copied shared catalogs are forbidden.

An `explicit-only`, deferred, or experimental candidate stays outside the
port. Codex does not honor such a visibility label after a bundle is placed in
`.agents/skills`, so v1 does not claim a distinction the host cannot enforce.

## Build And Check

From an `aoa-skills` checkout, preview an owner repository without writing:

```bash
python scripts/build_home_skill_projection.py --owner-root /path/to/owner
```

Write declared bundles only:

```bash
python scripts/build_home_skill_projection.py --owner-root /path/to/owner --execute
```

If undeclared entries exist, the builder stops. Inspect them, then make removal
an explicit act. Declared bundle copies are staged and checked before pruning
begins:

```bash
python scripts/build_home_skill_projection.py \
  --owner-root /path/to/owner --execute --prune
```

CI checks source shape and byte/executable-bit parity through the pinned
composite action or direct validator:

```bash
python scripts/validate_home_skill_port.py --owner-root /path/to/owner
```

Pin external action use to an exact reviewed `aoa-skills` commit. A green check
means only that the declared owner files exist and the repo projection matches
them structurally. It does not prove that the bundle triggers correctly,
improves an agent result, remains safe across models, or deserves admission.

## Lifecycle

Re-run manual isolated, negative, held-out, and coexistence cases when a bundle
or model/workflow changes materially. Improve, split, merge, lower visibility,
or retire in the owner repository. Update the owner decision and manifest,
then rebuild the projection. Remove the permanent test or validator rule when
the durable contract it protects is retired; do not preserve obsolete green
counts.
