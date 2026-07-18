# Durable Test Topology

Tests are admitted only after manual work reveals a stable invariant worth
preserving. They do not score semantic quality or prove outcome benefit.

| File | Durable invariant |
| --- | --- |
| `test_capability_system.py` | exact migration accounting, graph integrity, discovery boundaries, ABI composition, conflict blocking |
| `test_source_export_contract.py` | source/export membership, graph-derived visibility policy, no technique dependency, reproducible hashes |
| `test_pack_handoff.py` | portable-hash identity, honest profile errors, directory and ZIP roundtrip |
| `test_home_skill_port.py` | admitted owner source, v2 OS-user exposure without same-name repo duplication, transitional v1 projection parity/prune, and build-residue boundaries |
| `test_questbook_model.py` | Questbook remains an independent durable-obligation read model |
| `test_validation_lanes.py` | command lanes point only to live scripts and exclude retired ontology |

Run focused tests after the corresponding manual reproduction, then
`PYTHONPATH=scripts python -m pytest -q tests`. Remove a test when its owner
contract is retired; do not keep it to preserve historical green counts.
