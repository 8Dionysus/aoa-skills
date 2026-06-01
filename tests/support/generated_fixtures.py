from __future__ import annotations

import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def copy_repo_paths(target_root: Path, relative_paths: list[str]) -> None:
    for relative_path in relative_paths:
        source_path = REPO_ROOT / relative_path
        target_path = target_root / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
