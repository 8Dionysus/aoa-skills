#!/usr/bin/env python3
"""Stage a profile-scoped portable skill bundle for offline handoff."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
from typing import Any

import skill_pack_install_contract


def build_bundle_manifest(source: dict[str, Any]) -> dict[str, Any]:
    payloads: list[tuple[str, bytes]] = []
    skills: list[dict[str, Any]] = []
    for entry in source["skills"]:
        source_dir = pathlib.Path(entry["source_dir"])
        payloads.extend(
            skill_pack_install_contract.iter_directory_file_payloads(
                source_dir,
                relative_prefix=entry["relative_dir"],
            )
        )
        skills.append(
            {
                "name": entry["name"],
                "relative_dir": entry["relative_dir"],
                "skill_revision": entry["skill_revision"],
                "content_hash": entry["content_hash"],
            }
        )

    ordered_payloads = sorted(payloads, key=lambda item: item[0])
    return {
        "schema_version": 1,
        "profile": source["profile"],
        "profile_revision": source["profile_revision"],
        "scope": source["scope"],
        "install_mode": source["install_mode"],
        "install_root": source["install_root"],
        "skill_root": source["skill_root"],
        "skill_count": len(skills),
        "skills": skills,
        "release_identity": dict(source["release_identity"]),
        "file_digests": skill_pack_install_contract.file_digests_from_payloads(ordered_payloads),
        "bundle_digest": skill_pack_install_contract.payload_digest(ordered_payloads),
    }


def build_stage_plan(
    *,
    repo_root: pathlib.Path,
    profile_name: str,
    output_root: pathlib.Path,
    execute: bool,
) -> dict[str, Any]:
    source = skill_pack_install_contract.load_skill_pack_source(
        repo_root,
        profile_name=profile_name,
    )
    bundle_manifest = build_bundle_manifest(source)
    return {
        **bundle_manifest,
        "source_kind": source["source_kind"],
        "source_root": source["source_root"],
        "bundle_root": str(output_root),
        "execute": execute,
        "recommended_install_command": skill_pack_install_contract.recommended_install_command(
            profile_name=profile_name,
            bundle_root_override=output_root,
            mode="copy",
            execute=True,
        ),
        "recommended_verify_command": skill_pack_install_contract.recommended_verify_command(
            profile_name=profile_name,
            install_root=None,
            bundle_root_override=output_root,
            output_format="json",
        ),
    }


def ensure_clean_bundle_root(bundle_root: pathlib.Path, overwrite: bool) -> None:
    if not bundle_root.exists():
        return
    if not overwrite:
        raise SystemExit(f"bundle root exists: {bundle_root} (use --overwrite to replace)")
    if bundle_root.is_file() or bundle_root.is_symlink():
        bundle_root.unlink()
    else:
        shutil.rmtree(bundle_root)


def execute_stage(
    *,
    source: dict[str, Any],
    bundle_root: pathlib.Path,
    bundle_manifest: dict[str, Any],
    overwrite: bool,
) -> None:
    ensure_clean_bundle_root(bundle_root, overwrite)
    bundle_root.mkdir(parents=True, exist_ok=True)

    for entry in source["skills"]:
        source_dir = pathlib.Path(entry["source_dir"])
        target_dir = bundle_root / entry["relative_dir"]
        if source_dir.resolve() == target_dir.resolve():
            raise SystemExit(f"staging target matches source for {entry['name']}: {target_dir}")
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_dir, target_dir)

    skill_pack_install_contract.bundle_manifest_path(bundle_root).write_text(
        json.dumps(bundle_manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# Skill pack stage plan: {plan['profile']}",
        "",
        f"Profile revision: {plan['profile_revision']}",
        f"Bundle root: {plan['bundle_root']}",
        f"Execute: {plan['execute']}",
        f"Skill count: {plan['skill_count']}",
        f"Bundle digest: {plan['bundle_digest']}",
        f"Install: {plan['recommended_install_command']}",
        f"Verify: {plan['recommended_verify_command']}",
        "",
        "## Skills",
    ]
    for skill in plan["skills"]:
        lines.append(f"- {skill['name']}: {skill['relative_dir']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    parser.add_argument("--profile", required=True, help="Profile name from generated/skill_pack_profiles.resolved.json")
    parser.add_argument("--output-root", required=True, help="Directory where the staged bundle should live")
    parser.add_argument("--execute", action="store_true", help="Materialize the staged bundle")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing staged bundle root")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    bundle_root = pathlib.Path(args.output_root).expanduser().resolve()
    try:
        source = skill_pack_install_contract.load_skill_pack_source(
            repo_root,
            profile_name=args.profile,
        )
    except KeyError:
        raise SystemExit(f"unknown profile: {args.profile}")
    except ValueError as exc:
        raise SystemExit(str(exc))

    plan = build_stage_plan(
        repo_root=repo_root,
        profile_name=args.profile,
        output_root=bundle_root,
        execute=args.execute,
    )

    if args.execute:
        execute_stage(
            source=source,
            bundle_root=bundle_root,
            bundle_manifest={
                key: value
                for key, value in plan.items()
                if key
                not in {
                    "source_kind",
                    "source_root",
                    "bundle_root",
                    "execute",
                    "recommended_install_command",
                    "recommended_verify_command",
                }
            },
            overwrite=args.overwrite,
        )

    if args.format == "json":
        print(json.dumps(plan, indent=2))
    else:
        print(render_markdown(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
