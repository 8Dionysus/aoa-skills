from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def source_skill_count(repo_root: Path = REPO_ROOT) -> int:
    catalog = json.loads(
        (repo_root / "generated" / "skill_catalog.min.json").read_text(encoding="utf-8")
    )
    return len(catalog["skills"])
