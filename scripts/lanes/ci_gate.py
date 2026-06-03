#!/usr/bin/env python3
"""Run CI lanes for the growth-first aoa-skills workflow."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from lanes import validation_lanes


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_GENERATED_GROUPS = ("reader", "public", "evaluation", "governance")
GENERATED_GROUPS = ("all", *CATALOG_GENERATED_GROUPS, "export", "runtime")

EXPORT_RELEVANT_PREFIXES = (
    ".agents/",
    "config/",
    "generated/",
    "mechanics/release-support/examples/",
)


def python_script_command_paths(commands: Sequence[Sequence[str]]) -> set[str]:
    paths: set[str] = set()
    for command in commands:
        if len(command) < 2 or command[0] != "python":
            continue
        script_path = command[1]
        if script_path.endswith(".py"):
            paths.add(script_path)
    return paths


EXPORT_RELEVANT_FILES = {
    ".github/workflows/codex-portable-export.yml",
    "config/validation_lanes.json",
    "requirements-dev.txt",
    "scripts/ci_gate.py",
    "scripts/validation_lanes.py",
    "scripts/export/release_manifest_contract.py",
    *python_script_command_paths(validation_lanes.EXPORT_FULL_COMMAND_SEQUENCE),
}
EXPORT_GENERATED_DRIFT_PATHS = validation_lanes.EXPORT_GENERATED_DRIFT_PATHS
RUNTIME_GENERATED_DRIFT_PATHS = validation_lanes.RUNTIME_GENERATED_DRIFT_PATHS
EXPORT_DRIFT_PATHS = validation_lanes.EXPORT_DRIFT_PATHS


def resolve_command(command: Sequence[str]) -> tuple[str, ...]:
    if command and command[0] == "python":
        return (sys.executable, *command[1:])
    return tuple(command)


def run_command(command: Sequence[str], repo_root: Path = REPO_ROOT) -> None:
    printable = " ".join(command)
    print(f"[ci-gate] {printable}", flush=True)
    subprocess.run(resolve_command(command), cwd=repo_root, check=True)


def capture_command(command: Sequence[str], repo_root: Path = REPO_ROOT) -> str:
    result = subprocess.run(
        resolve_command(command),
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def changed_files(base_ref: str | None, repo_root: Path = REPO_ROOT) -> list[str]:
    if not base_ref or set(base_ref) == {"0"}:
        return []
    result = subprocess.run(
        ("git", "diff", "--name-only", base_ref, "HEAD"),
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(
            f"[ci-gate] could not diff against {base_ref}; running the export lane",
            file=sys.stderr,
        )
        return ["<unknown>"]
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def export_relevant(paths: Sequence[str]) -> bool:
    if not paths:
        return True
    for path in paths:
        if path == "<unknown>":
            return True
        if path in EXPORT_RELEVANT_FILES:
            return True
        if path.startswith(EXPORT_RELEVANT_PREFIXES):
            return True
    return False


def release_identity(repo_root: Path = REPO_ROOT) -> dict[str, object]:
    manifest_path = repo_root / "generated" / "release_manifest.json"
    if not manifest_path.is_file():
        return {"release_manifest": "missing"}
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    identity = payload.get("release_identity", {})
    if not isinstance(identity, dict):
        return {"release_identity": "invalid"}
    return identity


def run_source_fast() -> None:
    for command in validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE:
        run_command(command)


def run_generated(group: str) -> None:
    if group == "all":
        run_command(("python", "scripts/build_catalog.py", "--check", "--group", "all"))
        run_generated("export")
        run_generated("runtime")
        run_command(("python", "scripts/generate_decision_indexes.py", "--check"))
        return

    if group in CATALOG_GENERATED_GROUPS:
        run_command(("python", "scripts/build_catalog.py", "--check", "--group", group))
    elif group == "export":
        run_export_generated()
    elif group == "runtime":
        run_runtime_generated()
    else:
        raise ValueError(group)

    if group == "governance":
        run_command(("python", "scripts/generate_decision_indexes.py", "--check"))


def run_export_generated() -> None:
    for command in validation_lanes.EXPORT_GENERATED_CHECK_COMMAND_SEQUENCE:
        run_command(command)


def run_runtime_generated() -> None:
    for command in validation_lanes.RUNTIME_GENERATED_CHECK_COMMAND_SEQUENCE:
        run_command(command)


def run_export(*, changed_only: bool, base_ref: str | None) -> None:
    if changed_only:
        paths = changed_files(base_ref)
        if not export_relevant(paths):
            print("[ci-gate] export lane skipped: no export/runtime generated inputs changed")
            for path in paths:
                print(f"[ci-gate] changed: {path}")
            return

    for command in validation_lanes.EXPORT_FULL_COMMAND_SEQUENCE:
        run_command(command)


def run_release() -> None:
    run_source_fast()
    run_command(("python", "scripts/release_check.py", "--include-packaging-smoke"))


def run_nightly() -> None:
    run_source_fast()
    run_generated("all")
    identity = release_identity()
    print("[ci-gate] nightly growth report")
    print(json.dumps({"release_identity": identity}, indent=2, sort_keys=True))
    if identity.get("has_unreleased_changes") is True:
        print("[ci-gate] main has unreleased growth; this is expected for the growth surface")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run growth-first CI lanes for aoa-skills.")
    parser.add_argument(
        "--mode",
        choices=("source-fast", "generated", "export", "release", "nightly"),
        required=True,
    )
    parser.add_argument(
        "--group",
        choices=GENERATED_GROUPS,
        default="all",
        help="Generated surface group for --mode generated.",
    )
    parser.add_argument(
        "--changed-only",
        action="store_true",
        help="For --mode export, skip the export lane when changed files do not touch export/runtime inputs.",
    )
    parser.add_argument(
        "--base-ref",
        help="Base git ref or SHA for --changed-only export detection.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.mode == "source-fast":
            run_source_fast()
        elif args.mode == "generated":
            run_generated(args.group)
        elif args.mode == "export":
            run_export(changed_only=args.changed_only, base_ref=args.base_ref)
        elif args.mode == "release":
            run_release()
        elif args.mode == "nightly":
            run_nightly()
        else:  # pragma: no cover - argparse enforces choices
            raise ValueError(args.mode)
    except subprocess.CalledProcessError as exc:
        print(f"[ci-gate] command failed with exit code {exc.returncode}", file=sys.stderr)
        return exc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
