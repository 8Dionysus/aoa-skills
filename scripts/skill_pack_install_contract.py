from __future__ import annotations

import contextlib
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any, Mapping

import release_manifest_contract


STANDARD_INSTALL_ROOTS = {
    "repo": ".agents/skills",
    "user": "$HOME/.agents/skills",
    "admin": "/etc/codex/skills",
}
RESOLVED_PROFILES_PATH = Path("generated") / "skill_pack_profiles.resolved.json"
BUNDLE_MANIFEST_FILENAME = "bundle_manifest.json"
BUNDLE_SKILL_ROOT = ".agents/skills"
BUNDLE_ARCHIVE_FORMAT = "zip"
BUNDLE_ARCHIVE_ROOT_PREFIX = "aoa-skills"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def export_root(repo_root: Path) -> Path:
    return repo_root / ".agents" / "skills"


def bundle_root(root: str | Path) -> Path:
    return Path(root).expanduser().resolve()


def bundle_manifest_path(root: str | Path) -> Path:
    return bundle_root(root) / BUNDLE_MANIFEST_FILENAME


def bundle_skill_root(root: str | Path) -> Path:
    return bundle_root(root) / ".agents" / "skills"


def bundle_archive_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def bundle_archive_root_name(profile_name: str) -> str:
    return f"{BUNDLE_ARCHIVE_ROOT_PREFIX}-{profile_name}"


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


def load_bundle_manifest(root: str | Path) -> Mapping[str, Any]:
    manifest = load_json(bundle_manifest_path(root))
    if not isinstance(manifest, Mapping):
        raise ValueError("bundle manifest must parse to a mapping")
    return manifest


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


def skill_bundle_revision_map(release_manifest: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    revisions: dict[str, dict[str, Any]] = {}
    for entry in release_manifest.get("skill_bundle_revisions", []):
        if isinstance(entry, Mapping) and isinstance(entry.get("name"), str):
            revisions[entry["name"]] = dict(entry)
    return revisions


def iter_directory_file_payloads(
    root_dir: Path,
    *,
    relative_prefix: str = "",
) -> list[tuple[str, bytes]]:
    resolved_root = root_dir.resolve()
    if not resolved_root.is_dir():
        raise ValueError(f"directory payloads require a directory: {root_dir}")
    payloads: list[tuple[str, bytes]] = []
    for path in sorted(
        (candidate for candidate in resolved_root.rglob("*") if candidate.is_file()),
        key=lambda candidate: candidate.relative_to(resolved_root).as_posix(),
    ):
        relative_path = path.relative_to(resolved_root).as_posix()
        if relative_prefix:
            relative_path = f"{relative_prefix.rstrip('/')}/{relative_path}"
        payloads.append(
            (
                relative_path,
                release_manifest_contract.normalized_file_bytes(path),
            )
        )
    return payloads


def file_digests_from_payloads(
    payloads: list[tuple[str, bytes]],
) -> list[dict[str, Any]]:
    return [
        {
            "path": relative_path,
            "sha256": release_manifest_contract.sha256_bytes(data),
            "bytes": len(data),
        }
        for relative_path, data in payloads
    ]


def payload_digest(payloads: list[tuple[str, bytes]]) -> str:
    digest = hashlib.sha256()
    for relative_path, data in payloads:
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
    return digest.hexdigest()


def record_digest(file_records: list[Mapping[str, Any]]) -> str:
    digest = hashlib.sha256()
    for record in file_records:
        digest.update(str(record["path"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(record["sha256"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(record["bytes"]).encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def archive_info(path: str | Path) -> dict[str, Any]:
    resolved_path = bundle_archive_path(path)
    data = resolved_path.read_bytes()
    return {
        "archive_path": str(resolved_path),
        "archive_format": BUNDLE_ARCHIVE_FORMAT,
        "archive_sha256": release_manifest_contract.sha256_bytes(data),
        "archive_bytes": len(data),
    }


def bundle_archive_payloads(
    bundle_root_dir: Path,
    *,
    profile_name: str,
) -> list[tuple[str, bytes]]:
    return iter_directory_file_payloads(
        bundle_root_dir,
        relative_prefix=bundle_archive_root_name(profile_name),
    )


def write_bundle_archive(
    bundle_root_dir: Path,
    archive_path: str | Path,
    *,
    profile_name: str,
    overwrite: bool,
) -> dict[str, Any]:
    resolved_archive_path = bundle_archive_path(archive_path)
    if resolved_archive_path.exists():
        if not overwrite:
            raise ValueError(
                f"bundle archive exists: {resolved_archive_path} (use --overwrite to replace)"
            )
        if resolved_archive_path.is_dir():
            shutil.rmtree(resolved_archive_path)
        else:
            resolved_archive_path.unlink()

    resolved_archive_path.parent.mkdir(parents=True, exist_ok=True)
    payloads = sorted(
        bundle_archive_payloads(bundle_root_dir, profile_name=profile_name),
        key=lambda item: item[0],
    )
    with zipfile.ZipFile(
        resolved_archive_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for relative_path, data in payloads:
            info = zipfile.ZipInfo(relative_path)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return archive_info(resolved_archive_path)


def _validated_archive_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members: list[zipfile.ZipInfo] = []
    for entry in archive.infolist():
        normalized_name = entry.filename.replace("\\", "/")
        path = PurePosixPath(normalized_name)
        if not normalized_name or normalized_name.endswith("/"):
            continue
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"bundle archive contains unsafe path: {entry.filename}")
        members.append(entry)
    return members


def discover_bundle_root(root_dir: Path) -> Path:
    candidates = sorted(
        {
            path.parent.resolve()
            for path in root_dir.rglob(BUNDLE_MANIFEST_FILENAME)
            if path.is_file()
        },
        key=lambda path: path.as_posix(),
    )
    if not candidates:
        raise ValueError("bundle archive is missing bundle_manifest.json")
    if len(candidates) != 1:
        raise ValueError(
            f"bundle archive must contain exactly one bundle root, found {len(candidates)}"
        )
    candidate = candidates[0]
    if not bundle_skill_root(candidate).is_dir():
        raise ValueError(
            f"bundle archive root is missing {BUNDLE_SKILL_ROOT}: {candidate}"
        )
    return candidate


def extract_bundle_archive(
    archive_path: str | Path,
    extract_root: Path,
) -> Path:
    resolved_archive_path = bundle_archive_path(archive_path)
    try:
        with zipfile.ZipFile(resolved_archive_path, mode="r") as archive:
            members = _validated_archive_members(archive)
            extract_root.mkdir(parents=True, exist_ok=True)
            for entry in members:
                normalized_name = entry.filename.replace("\\", "/")
                relative_path = PurePosixPath(normalized_name)
                target_path = extract_root.joinpath(*relative_path.parts)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(entry, mode="r") as source_handle:
                    with target_path.open("wb") as target_handle:
                        shutil.copyfileobj(source_handle, target_handle)
    except zipfile.BadZipFile as exc:
        raise ValueError(f"invalid bundle archive: {resolved_archive_path}") from exc
    return discover_bundle_root(extract_root)


def expected_skill_file_records_from_bundle(
    bundle_manifest: Mapping[str, Any],
    skill_name: str,
) -> list[dict[str, Any]]:
    prefix = f"{BUNDLE_SKILL_ROOT}/{skill_name}/"
    records: list[dict[str, Any]] = []
    for entry in bundle_manifest.get("file_digests", []):
        if not isinstance(entry, Mapping):
            continue
        raw_path = entry.get("path")
        if not isinstance(raw_path, str) or not raw_path.startswith(prefix):
            continue
        records.append(
            {
                "path": raw_path.removeprefix(prefix),
                "sha256": entry["sha256"],
                "bytes": entry["bytes"],
            }
        )
    return records


def load_skill_pack_source(
    repo_root: Path,
    *,
    profile_name: str,
    bundle_root_override: str | None = None,
) -> dict[str, Any]:
    if bundle_root_override:
        resolved_bundle_root = bundle_root(bundle_root_override)
        manifest = load_bundle_manifest(resolved_bundle_root)
        if manifest.get("profile") != profile_name:
            raise ValueError(
                f"bundle profile mismatch: expected {profile_name!r}, got {manifest.get('profile')!r}"
            )
        skills: list[dict[str, Any]] = []
        for entry in manifest.get("skills", []):
            if not isinstance(entry, Mapping):
                continue
            skill_name = entry["name"]
            skills.append(
                {
                    "name": skill_name,
                    "relative_dir": entry["relative_dir"],
                    "source_dir": str(resolved_bundle_root / entry["relative_dir"]),
                    "skill_revision": entry["skill_revision"],
                    "content_hash": entry["content_hash"],
                    "expected_files": expected_skill_file_records_from_bundle(manifest, skill_name),
                }
            )
        return {
            "source_kind": "staged_bundle",
            "bundle_root": str(resolved_bundle_root),
            "profile": profile_name,
            "profile_revision": manifest["profile_revision"],
            "scope": manifest["scope"],
            "install_mode": manifest["install_mode"],
            "install_root": manifest["install_root"],
            "skill_root": manifest["skill_root"],
            "release_identity": dict(manifest["release_identity"]),
            "skills": skills,
            "bundle_manifest": dict(manifest),
            "source_root": str(bundle_skill_root(resolved_bundle_root)),
        }

    profile = load_resolved_profile(repo_root, profile_name)
    release_manifest = load_release_manifest(repo_root)
    profile_revision = load_install_profile_revision(
        release_manifest,
        profile_name,
    )["profile_revision"]
    revision_map = skill_bundle_revision_map(release_manifest)
    resolved_export_root = export_root(repo_root)
    skills = []
    for skill_entry in profile["skills"]:
        skill_name = skill_entry["name"]
        revision_entry = revision_map[skill_name]
        skills.append(
            {
                "name": skill_name,
                "relative_dir": f"{BUNDLE_SKILL_ROOT}/{skill_name}",
                "source_dir": str(resolved_export_root / skill_name),
                "skill_revision": revision_entry["skill_revision"],
                "content_hash": revision_entry["content_hash"],
                "expected_files": None,
            }
        )
    return {
        "source_kind": "repo_export",
        "bundle_root": None,
        "profile": profile_name,
        "profile_revision": profile_revision,
        "scope": profile["scope"],
        "install_mode": profile["install_mode"],
        "install_root": profile["install_root"],
        "skill_root": BUNDLE_SKILL_ROOT,
        "release_identity": dict(release_identity(release_manifest)),
        "skills": skills,
        "source_root": str(resolved_export_root),
    }


@contextlib.contextmanager
def skill_pack_source_context(
    repo_root: Path,
    *,
    profile_name: str,
    bundle_root_override: str | None = None,
    bundle_archive_override: str | None = None,
):
    if bundle_root_override and bundle_archive_override:
        raise ValueError("use only one of --bundle-root or --bundle-archive")

    if bundle_archive_override is None:
        source = load_skill_pack_source(
            repo_root,
            profile_name=profile_name,
            bundle_root_override=bundle_root_override,
        )
        source["bundle_archive"] = None
        yield source
        return

    with tempfile.TemporaryDirectory(prefix="aoa-skills-bundle-archive-") as temp_dir:
        extracted_root = Path(temp_dir) / "extracted"
        discovered_bundle_root = extract_bundle_archive(
            bundle_archive_override,
            extracted_root,
        )
        source = load_skill_pack_source(
            repo_root,
            profile_name=profile_name,
            bundle_root_override=str(discovered_bundle_root),
        )
        source["source_kind"] = "staged_archive"
        source["bundle_root"] = None
        source["bundle_archive"] = str(bundle_archive_path(bundle_archive_override))
        yield source


def _quote_command_arg(value: str) -> str:
    if not value:
        return '""'
    if any(character.isspace() or character in {'"', "'"} for character in value):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def recommended_install_command(
    *,
    profile_name: str,
    bundle_root_override: Path | None = None,
    bundle_archive_override: Path | None = None,
    install_root: Path | None = None,
    mode: str = "copy",
    execute: bool = True,
    output_format: str | None = None,
) -> str:
    if bundle_root_override is not None and bundle_archive_override is not None:
        raise ValueError("use only one of bundle_root_override or bundle_archive_override")
    args = [
        "python",
        "scripts/install_skill_pack.py",
        "--repo-root",
        ".",
        "--profile",
        profile_name,
    ]
    if bundle_root_override is not None:
        args.extend(["--bundle-root", str(bundle_root_override)])
    if bundle_archive_override is not None:
        args.extend(["--bundle-archive", str(bundle_archive_override)])
    if install_root is not None:
        args.extend(["--dest-root", str(install_root)])
    if mode:
        args.extend(["--mode", mode])
    if execute:
        args.append("--execute")
    if output_format is not None:
        args.extend(["--format", output_format])
    return " ".join(_quote_command_arg(arg) for arg in args)


def recommended_verify_command(
    *,
    profile_name: str,
    install_root: Path | None,
    bundle_root_override: Path | None = None,
    bundle_archive_override: Path | None = None,
    strict_root: bool = False,
    output_format: str = "json",
) -> str:
    if bundle_root_override is not None and bundle_archive_override is not None:
        raise ValueError("use only one of bundle_root_override or bundle_archive_override")
    args = [
        "python",
        "scripts/verify_skill_pack.py",
        "--repo-root",
        ".",
        "--profile",
        profile_name,
    ]
    if bundle_root_override is not None:
        args.extend(["--bundle-root", str(bundle_root_override)])
    if bundle_archive_override is not None:
        args.extend(["--bundle-archive", str(bundle_archive_override)])
    if install_root is not None:
        args.extend(["--install-root", str(install_root)])
    if strict_root:
        args.append("--strict-root")
    args.extend(["--format", output_format])
    return " ".join(_quote_command_arg(arg) for arg in args)
