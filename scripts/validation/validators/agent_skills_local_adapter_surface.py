"""Local-adapter manifest validation phase for Agent Skills export."""

from __future__ import annotations

import pathlib
from typing import Any


def validate_local_adapter_skill_sets(
    *,
    manifest_by_name: dict[str, Any],
    manifest_min_by_name: dict[str, Any],
    actual_names: set[str],
    errors: list[str],
) -> None:
    expected_sets = {
        "generated/local_adapter_manifest.json": set(manifest_by_name),
        "generated/local_adapter_manifest.min.json": set(manifest_min_by_name),
    }
    for label, names in expected_sets.items():
        if names != actual_names:
            errors.append(
                f"{label} skill set {sorted(names)!r} does not match export {sorted(actual_names)!r}"
            )


def validate_local_adapter_entry(
    *,
    repo_root: pathlib.Path,
    skill_name: str,
    manifest_entry: Any,
    runtime_entry: Any,
    allow_implicit: bool,
    activation_policy: str,
    errors: list[str],
) -> None:
    if manifest_entry is None:
        errors.append(f"generated/local_adapter_manifest.json missing {skill_name}")
        return

    if manifest_entry.get("allow_implicit_invocation") != allow_implicit:
        errors.append(
            f"generated/local_adapter_manifest.json allow_implicit_invocation mismatch for {skill_name}"
        )
    if manifest_entry.get("implicit_activation_policy") != activation_policy:
        errors.append(
            f"generated/local_adapter_manifest.json implicit_activation_policy mismatch for {skill_name}"
        )
    if manifest_entry.get("trust_posture") != runtime_entry.get("trust_posture"):
        errors.append(f"generated/local_adapter_manifest.json trust_posture mismatch for {skill_name}")
    for allowlist_path in manifest_entry.get("allowlist_paths", []):
        if not (repo_root / allowlist_path).exists():
            errors.append(
                f"generated/local_adapter_manifest.json allowlist path does not exist: {allowlist_path}"
            )
