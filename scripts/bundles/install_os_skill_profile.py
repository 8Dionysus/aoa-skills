#!/usr/bin/env python3
"""Preview, install, or verify one federated OS-level Codex skill profile."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any
import uuid

from export import home_skill_port
from skill_model import skill_source_model


PROFILE_CONFIG = Path("config/os_skill_profiles.json")
INSTALL_RECEIPT = ".aoa-os-skill-profile.json"
SOURCE_RECEIPT = ".aoa-skill-source.json"
SOURCE_RECEIPT_SCHEMA = "aoa_skill_source_receipt_v1"


class ProfileError(ValueError):
    pass


@dataclass(frozen=True)
class ResolvedSkill:
    name: str
    owner_repo: str
    owner_root: Path
    source_path: Path
    source_relative: str
    version: str
    digest: str
    file_count: int
    owner_ref: str
    dirty: bool | None


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_root_overrides(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ProfileError(f"--source-root must use REPO=PATH: {value!r}")
        repo, raw_path = value.split("=", 1)
        if not repo or repo in result:
            raise ProfileError(f"duplicate or empty --source-root repo: {repo!r}")
        path = Path(raw_path).expanduser().resolve()
        if not path.is_dir():
            raise ProfileError(f"source root is missing for {repo}: {path}")
        result[repo] = path
    return result


def repo_identity(root: Path) -> tuple[str, bool | None]:
    try:
        ref = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "-C", str(root), "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return ref, dirty
    except (OSError, subprocess.CalledProcessError):
        return "working-tree", None


def resolve_owner_root(
    source: dict[str, Any],
    *,
    repo_root: Path,
    os_root: Path,
    overrides: dict[str, Path],
) -> Path:
    repo = source.get("repo")
    if not isinstance(repo, str) or not repo:
        raise ProfileError("every source requires a repo")
    if repo in overrides:
        return overrides[repo]
    root = source.get("root")
    if root == "self":
        return repo_root
    if not isinstance(root, str) or not root or Path(root).is_absolute() or ".." in Path(root).parts:
        raise ProfileError(f"source {repo} root must be a safe OS-root-relative path or 'self'")
    resolved = (os_root / root).resolve()
    try:
        resolved.relative_to(os_root)
    except ValueError as exc:
        raise ProfileError(f"source {repo} resolves outside OS root: {resolved}") from exc
    if not resolved.is_dir():
        raise ProfileError(f"source root is missing for {repo}: {resolved}")
    return resolved


def _resolved_skill(
    *,
    name: str,
    repo: str,
    owner_root: Path,
    source_path: Path,
    source_relative: str,
    version: str,
) -> ResolvedSkill:
    source_receipt_path = source_path / SOURCE_RECEIPT
    if source_receipt_path.exists() or source_receipt_path.is_symlink():
        raise ProfileError(
            f"canonical skill source must not contain install-local {SOURCE_RECEIPT}: {repo}:{name}"
        )
    snapshot = home_skill_port.tree_snapshot(source_path, label=f"{repo}:{name} source")
    ref, dirty = repo_identity(owner_root)
    return ResolvedSkill(
        name=name,
        owner_repo=repo,
        owner_root=owner_root,
        source_path=source_path,
        source_relative=source_relative,
        version=version,
        digest=home_skill_port.tree_digest(snapshot),
        file_count=len(snapshot),
        owner_ref=ref,
        dirty=dirty,
    )


def resolve_profile(
    *,
    repo_root: Path,
    config_path: Path,
    profile_name: str,
    os_root: Path,
    overrides: dict[str, Path],
) -> tuple[dict[str, Any], list[ResolvedSkill]]:
    document = load_json(config_path)
    if document.get("schema_version") != "aoa_os_skill_profiles_v1":
        raise ProfileError("unsupported OS skill profile schema")
    profile = (document.get("profiles") or {}).get(profile_name)
    if not isinstance(profile, dict):
        raise ProfileError(f"unknown OS skill profile: {profile_name}")
    if profile.get("runtime") != "codex" or profile.get("scope") != "user":
        raise ProfileError("OS skill profile must target Codex user scope")
    if profile.get("install_mode") != "managed-copy":
        raise ProfileError("OS skill profile install_mode must be managed-copy")
    install_root = profile.get("install_root")
    if not isinstance(install_root, str) or not install_root.startswith("$HOME/"):
        raise ProfileError("OS skill profile install_root must start with '$HOME/'")
    install_relative = Path(install_root.removeprefix("$HOME/"))
    if (
        not install_relative.parts
        or install_relative.is_absolute()
        or ".." in install_relative.parts
    ):
        raise ProfileError("OS skill profile install_root must stay inside $HOME")
    sources = profile.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ProfileError("OS skill profile sources must be non-empty")

    resolved: list[ResolvedSkill] = []
    names: dict[str, str] = {}
    for source in sources:
        if not isinstance(source, dict):
            raise ProfileError("OS skill profile source must be an object")
        kind = source.get("kind")
        repo = source.get("repo")
        if not isinstance(repo, str):
            raise ProfileError("OS skill profile source repo must be a string")
        owner_root = resolve_owner_root(source, repo_root=repo_root, os_root=os_root, overrides=overrides)
        requested = source.get("skills")
        if not isinstance(requested, list) or not requested:
            raise ProfileError(f"source {repo} skills must be non-empty")

        additions: list[ResolvedSkill] = []
        if kind == "shared-home":
            catalog = {item.name: item for item in skill_source_model.load_skill_sources(owner_root)}
            for name in requested:
                if not isinstance(name, str) or name not in catalog:
                    raise ProfileError(f"shared source {repo} has no skill {name!r}")
                item = catalog[name]
                relative = item.skill_md_path.parent.relative_to(owner_root).as_posix()
                additions.append(
                    _resolved_skill(
                        name=name,
                        repo=repo,
                        owner_root=owner_root,
                        source_path=item.skill_md_path.parent,
                        source_relative=relative,
                        version=str(item.metadata.get("version", "source-current")),
                    )
                )
        elif kind == "owner-port":
            port = home_skill_port.load_port_definition(owner_root)
            if port.owner_repo != repo:
                raise ProfileError(f"owner port repo mismatch: profile={repo} manifest={port.owner_repo}")
            by_name = {bundle.name: bundle for bundle in port.bundles}
            for name in requested:
                if not isinstance(name, str) or name not in by_name:
                    raise ProfileError(f"owner port {repo} does not expose {name!r}")
                bundle = by_name[name]
                additions.append(
                    _resolved_skill(
                        name=name,
                        repo=repo,
                        owner_root=owner_root,
                        source_path=owner_root / bundle.path,
                        source_relative=bundle.path.as_posix(),
                        version=bundle.version,
                    )
                )
        elif kind == "direct-home":
            for entry in requested:
                if not isinstance(entry, dict):
                    raise ProfileError(f"direct source {repo} entries must be objects")
                name = entry.get("name")
                path = entry.get("path")
                version = entry.get("version")
                if not isinstance(name, str) or not home_skill_port.NAME_RE.fullmatch(name):
                    raise ProfileError(f"direct source {repo} has invalid name")
                if not isinstance(path, str) or Path(path).is_absolute() or ".." in Path(path).parts:
                    raise ProfileError(f"direct source {repo}:{name} has invalid path")
                source_path = (owner_root / path).resolve()
                try:
                    source_path.relative_to(owner_root)
                except ValueError as exc:
                    raise ProfileError(f"direct source {repo}:{name} escapes owner root") from exc
                additions.append(
                    _resolved_skill(
                        name=name,
                        repo=repo,
                        owner_root=owner_root,
                        source_path=source_path,
                        source_relative=path,
                        version=str(version or "owner-current"),
                    )
                )
        else:
            raise ProfileError(f"unsupported source kind for {repo}: {kind!r}")

        for item in additions:
            if item.name in names:
                raise ProfileError(
                    f"global skill name collision: {item.name} from {names[item.name]} and {item.owner_repo}"
                )
            names[item.name] = item.owner_repo
            resolved.append(item)
    return profile, resolved


def installed_receipt(dest_root: Path) -> dict[str, Any] | None:
    path = dest_root / INSTALL_RECEIPT
    if path.is_symlink():
        raise ProfileError(f"managed install receipt must not be a symlink: {path}")
    if not path.exists():
        return None
    if not path.is_file():
        raise ProfileError(f"managed install receipt must be a regular file: {path}")
    value = load_json(path)
    if not isinstance(value, dict) or value.get("schema_version") != "aoa_os_skill_install_v1":
        raise ProfileError(f"managed install receipt has unsupported shape: {path}")
    installed_at = value.get("installed_at")
    if not isinstance(installed_at, str) or not installed_at:
        raise ProfileError(f"managed install receipt has no installed_at value: {path}")
    skills = value.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ProfileError(f"managed install receipt skills must be non-empty: {path}")
    seen: set[str] = set()
    for index, item in enumerate(skills):
        name = item.get("name") if isinstance(item, dict) else None
        if not isinstance(name, str) or not home_skill_port.NAME_RE.fullmatch(name):
            raise ProfileError(
                f"managed install receipt skills[{index}] has an unsafe name: {name!r}"
            )
        if name in seen:
            raise ProfileError(f"managed install receipt contains duplicate skill: {name}")
        seen.add(name)
    return value


def _installed_tree_snapshot(target: Path, *, label: str) -> dict[str, dict[str, Any]]:
    snapshot = home_skill_port.tree_snapshot(target, label=label)
    snapshot.pop(SOURCE_RECEIPT, None)
    return snapshot


def _source_receipt(
    *,
    profile_name: str,
    profile: dict[str, Any],
    skill: ResolvedSkill,
) -> dict[str, Any]:
    return {
        "schema_version": SOURCE_RECEIPT_SCHEMA,
        "profile": profile_name,
        "runtime": profile["runtime"],
        "scope": profile["scope"],
        "mode": profile["install_mode"],
        "name": skill.name,
        "owner_repo": skill.owner_repo,
        "owner_root": str(skill.owner_root),
        "owner_ref": skill.owner_ref,
        "owner_dirty": skill.dirty,
        "source_path": skill.source_relative,
        "version": skill.version,
        "digest": skill.digest,
        "claim_limit": (
            "machine-local canonical source locator only; owner authority, current parity, "
            "routing, and outcomes require separate verification"
        ),
    }


def _source_receipt_status(target: Path, expected: dict[str, Any]) -> str:
    path = target / SOURCE_RECEIPT
    if not path.is_file() or path.is_symlink():
        return "missing"
    try:
        actual = load_json(path)
    except (OSError, json.JSONDecodeError):
        return "invalid"
    return "current" if actual == expected else "drift"


def build_plan(
    *,
    profile_name: str,
    profile: dict[str, Any],
    skills: list[ResolvedSkill],
    dest_root: Path,
) -> dict[str, Any]:
    previous = installed_receipt(dest_root) if dest_root.exists() else None
    managed_before = {
        item.get("name")
        for item in (previous or {}).get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    entries = []
    for skill in skills:
        target = dest_root / skill.name
        expected_source_receipt = _source_receipt(
            profile_name=profile_name,
            profile=profile,
            skill=skill,
        )
        source_receipt_status = "missing"
        if not target.exists() and not target.is_symlink():
            status = "missing"
            target_digest = None
        elif target.is_symlink():
            status = "managed-drift" if skill.name in managed_before else "unmanaged-collision"
            target_digest = None
        elif not target.is_dir():
            status = "managed-drift" if skill.name in managed_before else "unmanaged-collision"
            target_digest = None
        else:
            target_snapshot = _installed_tree_snapshot(target, label=f"installed {skill.name}")
            target_digest = home_skill_port.tree_digest(target_snapshot)
            source_receipt_status = _source_receipt_status(target, expected_source_receipt)
            if target_digest == skill.digest:
                if skill.name in managed_before:
                    status = "current" if source_receipt_status == "current" else "managed-drift"
                else:
                    status = "adoptable-identical"
            else:
                status = "managed-drift" if skill.name in managed_before else "unmanaged-collision"
        entries.append(
            {
                "name": skill.name,
                "owner_repo": skill.owner_repo,
                "owner_root": str(skill.owner_root),
                "owner_ref": skill.owner_ref,
                "owner_dirty": skill.dirty,
                "source_path": skill.source_relative,
                "version": skill.version,
                "source_digest": skill.digest,
                "target": str(target),
                "target_digest": target_digest,
                "status": status,
                "file_count": skill.file_count,
                "source_receipt_status": source_receipt_status,
            }
        )
    selected = {skill.name for skill in skills}
    stale_managed = sorted(name for name in managed_before - selected if isinstance(name, str))
    plan = {
        "schema_version": "aoa_os_skill_install_plan_v1",
        "profile": profile_name,
        "runtime": profile["runtime"],
        "scope": profile["scope"],
        "mode": profile["install_mode"],
        "destination": str(dest_root),
        "skills": entries,
        "stale_managed": stale_managed,
        "unrelated_entries_preserved": True,
        "claim_limit": (
            "canonical source and installed byte/mode parity plus machine-local source-handle "
            "parity only; no routing or outcome claim"
        ),
    }
    plan["install_receipt_status"] = _install_receipt_status(previous, plan)
    return plan


def _receipt_from_plan(
    plan: dict[str, Any],
    *,
    installed_at: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "aoa_os_skill_install_v1",
        "profile": plan["profile"],
        "runtime": plan["runtime"],
        "scope": plan["scope"],
        "mode": plan["mode"],
        "installed_at": installed_at or datetime.now(timezone.utc).isoformat(),
        "claim_limit": (
            "install-time provenance and machine-local owner-source locator only; "
            "current parity, routing, and outcomes require separate verification"
        ),
        "skills": [
            {
                "name": item["name"],
                "owner_repo": item["owner_repo"],
                "owner_root": item["owner_root"],
                "owner_ref": item["owner_ref"],
                "owner_dirty": item["owner_dirty"],
                "source_path": item["source_path"],
                "version": item["version"],
                "digest": item["source_digest"],
            }
            for item in plan["skills"]
        ],
    }


def _install_receipt_status(
    previous: dict[str, Any] | None,
    plan: dict[str, Any],
) -> str:
    if previous is None:
        return "missing"
    expected = _receipt_from_plan(plan, installed_at=previous["installed_at"])
    return "current" if previous == expected else "drift"


def plan_is_current(
    plan: dict[str, Any],
    *,
    allow_dirty_source: bool,
) -> bool:
    dirty_sources = [item["name"] for item in plan["skills"] if item["owner_dirty"] is True]
    return (
        all(item["status"] == "current" for item in plan["skills"])
        and not plan["stale_managed"]
        and plan["install_receipt_status"] == "current"
        and (allow_dirty_source or not dirty_sources)
    )


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def execute_plan(
    plan: dict[str, Any],
    skills: list[ResolvedSkill],
    *,
    replace_unmanaged: bool,
    prune_managed: bool,
    allow_dirty_source: bool,
) -> None:
    dirty_sources = [item["name"] for item in plan["skills"] if item["owner_dirty"] is True]
    if dirty_sources and not allow_dirty_source:
        raise ProfileError(
            "dirty owner sources require explicit --allow-dirty-source for a reviewed "
            "non-production trial: " + ", ".join(dirty_sources)
        )
    collisions = [item["name"] for item in plan["skills"] if item["status"] == "unmanaged-collision"]
    if collisions and not replace_unmanaged:
        raise ProfileError(
            "unmanaged collisions require explicit --replace-unmanaged after review: " + ", ".join(collisions)
        )
    if plan["stale_managed"] and not prune_managed:
        raise ProfileError(
            "stale managed entries require explicit --prune-managed after review: " + ", ".join(plan["stale_managed"])
        )
    if plan_is_current(plan, allow_dirty_source=allow_dirty_source):
        return
    dest_root = Path(plan["destination"])
    dest_root.mkdir(parents=True, exist_ok=True)
    by_name = {skill.name: skill for skill in skills}
    backups: list[tuple[Path, Path]] = []
    staged: list[Path] = []
    installed: list[Path] = []
    temporary_files: list[Path] = []
    committed = False
    try:
        for item in plan["skills"]:
            if item["status"] == "current":
                continue
            skill = by_name[item["name"]]
            stage = Path(tempfile.mkdtemp(prefix=f".{skill.name}.stage-", dir=dest_root))
            staged.append(stage)
            shutil.copytree(skill.source_path, stage, dirs_exist_ok=True, copy_function=shutil.copy2)
            stage_digest = home_skill_port.tree_digest(
                home_skill_port.tree_snapshot(stage, label=f"staged {skill.name}")
            )
            if stage_digest != skill.digest:
                raise ProfileError(f"staged copy differs from source: {skill.name}")
            target = dest_root / skill.name
            if target.exists() or target.is_symlink():
                backup = dest_root / f".{skill.name}.backup-{uuid.uuid4().hex}"
                os.replace(target, backup)
                backups.append((target, backup))
            os.replace(stage, target)
            staged.remove(stage)
            installed.append(target)
        for item in plan["skills"]:
            if item["status"] == "current":
                continue
            skill = by_name[item["name"]]
            target = dest_root / skill.name
            source_receipt_path = target / SOURCE_RECEIPT
            source_receipt_text = json.dumps(
                _source_receipt(
                    profile_name=plan["profile"],
                    profile={
                        "runtime": plan["runtime"],
                        "scope": plan["scope"],
                        "install_mode": plan["mode"],
                    },
                    skill=skill,
                ),
                ensure_ascii=False,
                indent=2,
            ) + "\n"
            temporary_source_receipt = target / f".{SOURCE_RECEIPT}.tmp-{uuid.uuid4().hex}"
            temporary_files.append(temporary_source_receipt)
            temporary_source_receipt.write_text(source_receipt_text, encoding="utf-8")
            os.replace(temporary_source_receipt, source_receipt_path)
            temporary_files.remove(temporary_source_receipt)
        if prune_managed:
            for name in plan["stale_managed"]:
                target = dest_root / name
                if target.exists() or target.is_symlink():
                    backup = dest_root / f".{name}.backup-{uuid.uuid4().hex}"
                    os.replace(target, backup)
                    backups.append((target, backup))
        receipt_path = dest_root / INSTALL_RECEIPT
        receipt_text = json.dumps(_receipt_from_plan(plan), ensure_ascii=False, indent=2) + "\n"
        temporary_receipt = dest_root / f".{INSTALL_RECEIPT}.tmp-{uuid.uuid4().hex}"
        temporary_files.append(temporary_receipt)
        temporary_receipt.write_text(receipt_text, encoding="utf-8")
        if receipt_path.exists() or receipt_path.is_symlink():
            backup = dest_root / f".{INSTALL_RECEIPT}.backup-{uuid.uuid4().hex}"
            os.replace(receipt_path, backup)
            backups.append((receipt_path, backup))
        os.replace(temporary_receipt, receipt_path)
        temporary_files.remove(temporary_receipt)
        installed.append(receipt_path)
        committed = True
    except Exception:
        for target in reversed(installed):
            _remove_path(target)
        for target, backup in reversed(backups):
            if backup.exists() or backup.is_symlink():
                os.replace(backup, target)
        raise
    finally:
        for stage in staged:
            if stage.exists():
                shutil.rmtree(stage)
        for temporary_file in temporary_files:
            if temporary_file.exists() or temporary_file.is_symlink():
                temporary_file.unlink()
    if committed:
        cleanup_failures = []
        for _, backup in backups:
            try:
                _remove_path(backup)
            except OSError as exc:
                cleanup_failures.append(f"{backup}: {exc}")
        if cleanup_failures:
            raise ProfileError(
                "installation committed but backup cleanup failed: " + "; ".join(cleanup_failures)
            )


def format_plan(plan: dict[str, Any]) -> str:
    lines = [
        f"profile: {plan['profile']}",
        f"destination: {plan['destination']}",
        f"mode: {plan['mode']}",
        f"install receipt: {plan['install_receipt_status']}",
    ]
    for item in plan["skills"]:
        lines.append(
            f"- {item['name']}: {item['status']} owner={item['owner_repo']} "
            f"ref={item['owner_ref']} source={item['source_path']} digest={item['source_digest']} "
            f"source_handle={item['source_receipt_status']}"
        )
    if plan["stale_managed"]:
        lines.append("stale managed: " + ", ".join(plan["stale_managed"]))
    lines.append(f"claim limit: {plan['claim_limit']}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--config", default=PROFILE_CONFIG.as_posix())
    parser.add_argument("--profile", default="os-user-default")
    parser.add_argument("--os-root", default="/srv/AbyssOS")
    parser.add_argument("--source-root", action="append", default=[], metavar="REPO=PATH")
    parser.add_argument("--dest-root", default=None)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--execute", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--replace-unmanaged", action="store_true")
    parser.add_argument("--prune-managed", action="store_true")
    parser.add_argument(
        "--allow-dirty-source",
        action="store_true",
        help="allow an explicitly reviewed non-production install from dirty Git owners",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (args.replace_unmanaged or args.prune_managed) and not args.execute:
        raise SystemExit("--replace-unmanaged and --prune-managed require --execute")
    repo_root = Path(args.repo_root).resolve()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = repo_root / config_path
    os_root = Path(args.os_root).resolve()
    try:
        overrides = parse_root_overrides(args.source_root)
        profile, skills = resolve_profile(
            repo_root=repo_root,
            config_path=config_path,
            profile_name=args.profile,
            os_root=os_root,
            overrides=overrides,
        )
        install_root = profile["install_root"]
        home_root = Path.home().resolve()
        default_dest_root = (home_root / install_root.removeprefix("$HOME/")).resolve()
        try:
            default_dest_root.relative_to(home_root)
        except ValueError as exc:
            raise ProfileError(
                f"default destination resolves outside $HOME: {default_dest_root}"
            ) from exc
        if args.dest_root:
            requested_dest = Path(args.dest_root).expanduser()
            if requested_dest.is_symlink():
                raise ProfileError(f"destination root must not be a symlink: {requested_dest}")
            dest_root = requested_dest.resolve()
        else:
            dest_root = default_dest_root
        if args.allow_dirty_source and dest_root == default_dest_root:
            raise ProfileError(
                "--allow-dirty-source is restricted to an explicit non-production "
                "--dest-root"
            )
        if dest_root == Path("/") or dest_root == Path.home().resolve():
            raise ProfileError(f"refusing unsafe destination root: {dest_root}")
        if dest_root.exists() and not dest_root.is_dir():
            raise ProfileError(f"destination root must be a directory: {dest_root}")
        plan = build_plan(profile_name=args.profile, profile=profile, skills=skills, dest_root=dest_root)
        if args.execute:
            execute_plan(
                plan,
                skills,
                replace_unmanaged=args.replace_unmanaged,
                prune_managed=args.prune_managed,
                allow_dirty_source=args.allow_dirty_source,
            )
            plan = build_plan(profile_name=args.profile, profile=profile, skills=skills, dest_root=dest_root)
            if not plan_is_current(plan, allow_dirty_source=args.allow_dirty_source):
                raise ProfileError("OS skill profile remained non-current after execution")
    except (OSError, json.JSONDecodeError, ProfileError, home_skill_port.PortContractError) as exc:
        raise SystemExit(str(exc))
    print(json.dumps(plan, ensure_ascii=False, indent=2) if args.format == "json" else format_plan(plan))
    if args.check:
        return 0 if plan_is_current(
            plan,
            allow_dirty_source=args.allow_dirty_source,
        ) else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
