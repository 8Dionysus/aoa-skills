"""Shared validation lane loader for aoa-skills.

The executable command authority lives in ``config/validation_lanes.json``.
This module keeps the existing Python API stable for CI, release, and tests.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

Command = tuple[str, ...]

REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATION_LANES_PATH = REPO_ROOT / "config" / "validation_lanes.json"
SKILL_PACK_PROFILES_PATH = REPO_ROOT / "config" / "skill_pack_profiles.json"


def _load_manifest() -> dict[str, Any]:
    payload = json.loads(VALIDATION_LANES_PATH.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 2:
        raise ValueError(
            f"{VALIDATION_LANES_PATH}: unsupported schema_version "
            f"{payload.get('schema_version')!r}"
        )
    return payload


def _command(command: object, where: str) -> Command:
    if not isinstance(command, list) or not command:
        raise ValueError(f"{VALIDATION_LANES_PATH}: {where} must be a non-empty list")
    if any(not isinstance(part, str) or not part for part in command):
        raise ValueError(f"{VALIDATION_LANES_PATH}: {where} must contain strings")
    return tuple(command)


def _command_sequence(manifest: dict[str, Any], name: str) -> tuple[Command, ...]:
    sequences = manifest.get("command_sequences")
    if not isinstance(sequences, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: command_sequences must be a mapping")
    sequence = sequences.get(name)
    if not isinstance(sequence, list) or not sequence:
        raise ValueError(f"{VALIDATION_LANES_PATH}: missing command sequence {name!r}")
    return tuple(_command(command, f"command_sequences.{name}[{idx}]") for idx, command in enumerate(sequence))


def _single_command(manifest: dict[str, Any], name: str) -> Command:
    commands = manifest.get("single_commands")
    if not isinstance(commands, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: single_commands must be a mapping")
    return _command(commands.get(name), f"single_commands.{name}")


def _packaging_smoke_commands(
    manifest: dict[str, Any],
    profiles_doc: dict[str, Any],
) -> tuple[Command, ...]:
    single_commands = manifest.get("single_commands")
    if not isinstance(single_commands, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: single_commands must be a mapping")
    profiles = profiles_doc.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError(f"{SKILL_PACK_PROFILES_PATH}: profiles must be a non-empty mapping")

    commands_by_profile: dict[str, Command] = {}
    for name, raw_command in single_commands.items():
        if name != "packaging_smoke" and not name.startswith("packaging_smoke_"):
            continue
        command = _command(raw_command, f"single_commands.{name}")
        try:
            profile_index = command.index("--profile") + 1
            profile_name = command[profile_index]
        except (ValueError, IndexError) as exc:
            raise ValueError(
                f"{VALIDATION_LANES_PATH}: single_commands.{name} must name one --profile"
            ) from exc
        if profile_name in commands_by_profile:
            raise ValueError(
                f"{VALIDATION_LANES_PATH}: duplicate packaging smoke for profile {profile_name!r}"
            )
        commands_by_profile[profile_name] = command

    declared_profiles = tuple(profiles)
    missing = set(declared_profiles) - set(commands_by_profile)
    extra = set(commands_by_profile) - set(declared_profiles)
    if missing or extra:
        raise ValueError(
            f"{VALIDATION_LANES_PATH}: packaging smoke/profile drift; "
            f"missing={sorted(missing)!r}, extra={sorted(extra)!r}"
        )
    return tuple(commands_by_profile[name] for name in declared_profiles)


def _drift_paths(manifest: dict[str, Any], name: str) -> tuple[str, ...]:
    drift_paths = manifest.get("drift_paths")
    if not isinstance(drift_paths, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: drift_paths must be a mapping")
    paths = drift_paths.get(name)
    if not isinstance(paths, list) or not paths:
        raise ValueError(f"{VALIDATION_LANES_PATH}: missing drift path list {name!r}")
    if any(not isinstance(path, str) or not path for path in paths):
        raise ValueError(f"{VALIDATION_LANES_PATH}: drift_paths.{name} must contain strings")
    return tuple(paths)


_MANIFEST = _load_manifest()
_SKILL_PACK_PROFILES = json.loads(SKILL_PACK_PROFILES_PATH.read_text(encoding="utf-8"))

CAPABILITY_GENERATED_DRIFT_PATHS = _drift_paths(_MANIFEST, "capability_generated")
EXPORT_GENERATED_DRIFT_PATHS = _drift_paths(_MANIFEST, "export_generated")
OWNER_READMODEL_DRIFT_PATHS = _drift_paths(_MANIFEST, "owner_readmodels")
EXPORT_DRIFT_PATHS = (*CAPABILITY_GENERATED_DRIFT_PATHS, *EXPORT_GENERATED_DRIFT_PATHS)

SOURCE_FAST_COMMAND_SEQUENCE = _command_sequence(_MANIFEST, "source_fast")
CAPABILITY_GENERATED_CHECK_COMMAND_SEQUENCE = _command_sequence(
    _MANIFEST, "capability_generated_check"
)
EXPORT_GENERATED_CHECK_COMMAND_SEQUENCE = _command_sequence(
    _MANIFEST, "export_generated_check"
)
OWNER_READMODEL_CHECK_COMMAND_SEQUENCE = _command_sequence(
    _MANIFEST, "owner_readmodels_check"
)
EXPORT_FULL_COMMAND_SEQUENCE = _command_sequence(_MANIFEST, "export_full")
RELEASE_CHECK_COMMAND_SEQUENCE = _command_sequence(_MANIFEST, "release_check")
PACKAGING_SMOKE_USER_DEFAULT_COMMAND = _single_command(
    _MANIFEST, "packaging_smoke_user_default"
)
PACKAGING_SMOKE_COMMAND = _single_command(_MANIFEST, "packaging_smoke")
PACKAGING_SMOKE_CAPABILITY_SOURCES_COMMAND = _single_command(
    _MANIFEST, "packaging_smoke_capability_sources"
)
PACKAGING_SMOKE_COMMAND_SEQUENCE = _packaging_smoke_commands(
    _MANIFEST, _SKILL_PACK_PROFILES
)


def _command_text(command: Command) -> str:
    return " ".join(command)


def main(argv: list[str] | None = None) -> int:
    command_sequences = _MANIFEST["command_sequences"]
    parser = argparse.ArgumentParser(
        description=(
            "Inspect validation lane command sequences from "
            "config/validation_lanes.json without executing them."
        )
    )
    parser.add_argument(
        "lane",
        nargs="?",
        choices=sorted(command_sequences),
        help="Optional lane name to display.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the selected lane, or the full manifest when no lane is selected, as JSON.",
    )
    args = parser.parse_args(argv)

    if args.json:
        payload = command_sequences[args.lane] if args.lane else _MANIFEST
        print(json.dumps(payload, indent=2) + "\n", end="")
        return 0

    if args.lane:
        print(f"{args.lane}:")
        for command in _command_sequence(_MANIFEST, args.lane):
            print(f"- {_command_text(command)}")
        return 0

    print(f"validation lanes: {VALIDATION_LANES_PATH.relative_to(REPO_ROOT).as_posix()}")
    for name, sequence in sorted(command_sequences.items()):
        print(f"- {name}: {len(sequence)} commands")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
