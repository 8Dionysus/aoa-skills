from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import release_manifest_contract


STANDARD_INSTALL_ROOTS = {
    "repo": ".agents/skills",
    "user": "$HOME/.agents/skills",
    "admin": "/etc/codex/skills",
}
RESOLVED_PROFILES_PATH = Path("generated") / "skill_pack_profiles.resolved.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def export_root(repo_root: Path) -> Path:
    return repo_root / ".agents" / "skills"


def expand_root(root: str, repo_root: Path) -> Path:
    if root == STANDARD_INSTALL_ROOTS["repo"]:
        return export_root(repo_root)
    if root.startswith("$HOME/"):
        return Path.home() / root.replace("$HOME/", "", 1)
    return Path(root)


def resolve_install_root(
    repo_root: Path,
    *,
    install_root_override: str | None,
    default_install_root: str,
) -> Path:
    if install_root_override:
        return Path(install_root_override).expanduser().resolve()
    return expand_root(default_install_root, repo_root).resolve()


def load_resolved_profiles(repo_root: Path) -> Mapping[str, Any]:
    return load_json(repo_root / RESOLVED_PROFILES_PATH)


def load_resolved_profile(repo_root: Path, profile_name: str) -> Mapping[str, Any]:
    resolved_profiles = load_resolved_profiles(repo_root)
    profile = resolved_profiles.get("profiles", {}).get(profile_name)
    if not isinstance(profile, Mapping):
        raise KeyError(profile_name)
    return profile


def load_release_manifest(repo_root: Path) -> Mapping[str, Any]:
    return load_json(repo_root / release_manifest_contract.RELEASE_MANIFEST_PATH)


def load_install_profile_revision(
    release_manifest: Mapping[str, Any],
    profile_name: str,
) -> Mapping[str, Any]:
    for entry in release_manifest.get("install_profile_revisions", []):
        if isinstance(entry, Mapping) and entry.get("name") == profile_name:
            return entry
    raise KeyError(profile_name)


def release_identity(release_manifest: Mapping[str, Any]) -> Mapping[str, Any]:
    identity = release_manifest.get("release_identity")
    if not isinstance(identity, Mapping):
        raise ValueError("generated/release_manifest.json field 'release_identity' must be a mapping")
    return identity


def _quote_command_arg(value: str) -> str:
    if not value:
        return '""'
    if any(character.isspace() or character in {'"', "'"} for character in value):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def recommended_verify_command(
    *,
    profile_name: str,
    install_root: Path | None,
    strict_root: bool = False,
    output_format: str = "json",
) -> str:
    args = [
        "python",
        "scripts/verify_skill_pack.py",
        "--repo-root",
        ".",
        "--profile",
        profile_name,
    ]
    if install_root is not None:
        args.extend(["--install-root", str(install_root)])
    if strict_root:
        args.append("--strict-root")
    args.extend(["--format", output_format])
    return " ".join(_quote_command_arg(arg) for arg in args)
