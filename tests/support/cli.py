from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_ROOT = REPO_ROOT / "scripts"


def command_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    result = dict(os.environ if env is None else env)
    existing = result.get("PYTHONPATH")
    scripts_root = str(SCRIPTS_ROOT)
    result["PYTHONPATH"] = scripts_root if not existing else f"{scripts_root}{os.pathsep}{existing}"
    return result


def run_python(
    *args: str,
    cwd: Path = REPO_ROOT,
    check: bool = False,
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        env=command_env(env),
        check=False,
    )
    if check and completed.returncode != 0:
        raise AssertionError(
            f"command failed: {sys.executable} {' '.join(args)}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def command_text(command: Sequence[str]) -> str:
    return " ".join(command)
