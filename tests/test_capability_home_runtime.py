from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from runtime import capability_home


def test_parse_inputs_preserves_global_and_targeted_selectors() -> None:
    assert capability_home.parse_inputs(
        [
            "evaluation-selection-need=manual://need",
            "mode.eval.apply::selection=artifact://selection",
        ]
    ) == [
        {
            "type": "evaluation-selection-need",
            "ref": "manual://need",
        },
        {
            "target": "mode.eval.apply",
            "port": "selection",
            "ref": "artifact://selection",
        },
    ]


def test_plan_returns_nonzero_for_valid_blocked_dag(
    monkeypatch,
    capsys,
) -> None:
    captured: dict[str, object] = {}
    blocked = {
        "schema_version": "aoa-task-local-dag-v2",
        "status": "blocked",
        "blockers": ["missing-input:selection"],
    }
    monkeypatch.setattr(
        capability_home.capability_home_port,
        "load_port",
        lambda *args: SimpleNamespace(
            graph_json=Path("derived/custom-capability-graph.json")
        ),
    )
    monkeypatch.setattr(
        capability_home.capability_home_port,
        "load_owner_graph",
        lambda port: {"source": {"content_hash": "sha256:test"}},
    )
    monkeypatch.setattr(
        capability_home.capability_system,
        "build_task_dag",
        lambda *args, **kwargs: (
            captured.update(kwargs)
            or blocked
        ),
    )
    monkeypatch.setattr(
        capability_home.capability_home_port,
        "validate_task_dag",
        lambda *args: [],
    )

    exit_code = capability_home.main(
        [
            "--owner-root",
            "/owner",
            "plan",
            "compose a blocked plan",
            "--select",
            "mode.eval.apply",
        ]
    )

    assert exit_code == 2
    assert captured["source_graph_path"] == Path(
        "derived/custom-capability-graph.json"
    )
    assert '"status": "blocked"' in capsys.readouterr().out
