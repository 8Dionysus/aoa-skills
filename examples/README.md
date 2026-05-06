# Examples District

Root `examples/` is intentionally small.
It is for repo-owned examples that are not better owned by a mechanic package,
a skill bundle, a schema fixture, or generated validation output.

## Placement

| Example kind | Home |
|---|---|
| Root repo contract or cross-package walkthrough | `examples/` |
| Mechanic behavior, schema instance, receipt family, or route-local scaffold | `mechanics/<slug>/examples/` |
| Part-local mechanic contract | `mechanics/<slug>/parts/<part>/examples/` |
| Skill runtime scenario | `skills/<skill>/examples/` |
| Generated read model | `generated/` |
| Test fixture | `tests/fixtures/` |

## Current Root Examples

None.

## Before Editing

1. Name the source surface the example illustrates.
2. Check whether a mechanic package owns the behavior.
3. Keep example data public-safe and neutral.
4. Run the nearest validator for the owning surface.
