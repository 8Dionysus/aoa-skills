from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from skill_model import questbook_model
from validation.validators.questbook_surface import validate_questbook_surface


def test_questbook_read_models_are_owner_local_and_current() -> None:
    outputs = questbook_model.build_outputs(REPO_ROOT)

    assert validate_questbook_surface(REPO_ROOT) == []
    assert questbook_model.discover_quest_ids(REPO_ROOT) == ()
    for relative_path, expected in outputs.items():
        assert (REPO_ROOT / relative_path).read_text(encoding="utf-8") == expected
