# Script Topology

| Organ | Owns |
| --- | --- |
| `builders/` | capability graph and Questbook read models |
| `export/` | shared portable bundles plus owner-home repo projections |
| `bundles/` | stage, inspect, import, install, verify, smoke handoff |
| `runtime/` | typed task-local capability DAG planning |
| `skill_model/` | current capability, source, section, layout, Questbook models |
| `validation/` | focused structural validators |
| `decisions/` | decision index parsing and deterministic generation |
| `lanes/` | command-manifest loading and lane execution |

Root `scripts/*.py` files are stable compatibility front doors implemented via
`_ingress.py`; new logic belongs in the narrowest organ. Retired activation,
router, technique refresh, stats proxy, governance, and 57-skill catalog code
must not return through a wrapper.

`export/build_home_skill_projection.py` is a cross-repository builder, not a
skill author or admission judge. It previews by default, requires explicit
`--execute` to write, and requires an additional `--prune` before removing
undeclared legacy projection entries.
