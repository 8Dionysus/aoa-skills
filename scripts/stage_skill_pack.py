#!/usr/bin/env python3
"""Stage a profile-scoped portable skill bundle for offline handoff."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
from typing import Any

import skill_pack_install_contract


def build_bundle_readme(*, source: dict[str, Any]) -> str:
    lines = [
        f"# aoa-skills bundle: {source['profile']}",
        "",
        "This staged bundle is a repo-local, profile-scoped handoff object.",
        "`bundle_manifest.json` is the canonical machine-readable contract for this bundle.",
        "`README.md` is a human-facing companion that points a receiver at inspect/import flows.",
        "",
        f"- Profile: `{source['profile']}`",
        f"- Profile revision: `{source['profile_revision']}`",
        f"- Latest tagged version: `{source['release_identity']['latest_tagged_version']}`",
        f"- Latest tagged date: `{source['release_identity']['latest_tagged_date']}`",
        f"- Has unreleased changes: `{str(source['release_identity']['has_unreleased_changes']).lower()}`",
        "",
        "## Skills",
    ]
    for entry in source["skills"]:
        lines.append(f"- `{entry['name']}`")
    lines.extend(
        [
            "",
            "## Inspect",
            "",
            "Directory bundle:",
            f"`{skill_pack_install_contract.recommended_inspect_command(bundle_root_override='<bundle-root>', output_format='json')}`",
            "",
            "ZIP handoff:",
            f"`{skill_pack_install_contract.recommended_inspect_command(bundle_archive_override='<bundle-archive>', output_format='json')}`",
            "",
            "## Import",
            "",
            "Directory bundle:",
            f"`{skill_pack_install_contract.recommended_import_command(profile_name=str(source['profile']), bundle_root_override='<bundle-root>', install_root='<install-root>', mode='copy', execute=True, output_format='json')}`",
            "",
            "ZIP handoff:",
            f"`{skill_pack_install_contract.recommended_import_command(profile_name=str(source['profile']), bundle_archive_override='<bundle-archive>', install_root='<install-root>', mode='copy', execute=True, output_format='json')}`",
            "",
            "## Advanced path",
            "",
            "Install only:",
            f"`{skill_pack_install_contract.recommended_install_command(profile_name=str(source['profile']), bundle_root_override='<bundle-root>', install_root='<install-root>', mode='copy', execute=True, output_format='json')}`",
            "",
            "Verify only:",
            f"`{skill_pack_install_contract.recommended_verify_command(profile_name=str(source['profile']), install_root='<install-root>', bundle_root_override='<bundle-root>', output_format='json')}`",
            "",
            "For archive-based advanced flows, replace `<bundle-root>` with `--bundle-archive <bundle-archive>` on the lower-level commands.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_bundle_manifest(source: dict[str, Any], *, readme_text: str) -> dict[str, Any]:
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

    payloads.append(
        (
            skill_pack_install_contract.BUNDLE_README_FILENAME,
            readme_text.encode("utf-8"),
        )
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
    archive_path: pathlib.Path | None,
    execute: bool,
) -> dict[str, Any]:
    source = skill_pack_install_contract.load_skill_pack_source(
        repo_root,
        profile_name=profile_name,
    )
    readme_text = build_bundle_readme(source=source)
    bundle_manifest = build_bundle_manifest(source, readme_text=readme_text)
    use_archive_transport = archive_path is not None
    return {
        **bundle_manifest,
        "source_kind": source["source_kind"],
        "source_root": source["source_root"],
        "bundle_root": str(output_root),
        "bundle_readme_path": str(skill_pack_install_contract.bundle_readme_path(output_root)),
        "archive_path": str(archive_path) if archive_path is not None else None,
        "archive_format": (
            skill_pack_install_contract.BUNDLE_ARCHIVE_FORMAT
            if archive_path is not None
            else None
        ),
        "archive_sha256": None,
        "archive_bytes": None,
        "execute": execute,
        "recommended_inspect_command": skill_pack_install_contract.recommended_inspect_command(
            bundle_archive_override=archive_path if use_archive_transport else None,
            bundle_root_override=None if use_archive_transport else output_root,
            output_format="json",
        ),
        "recommended_import_command": skill_pack_install_contract.recommended_import_command(
            profile_name=profile_name,
            bundle_archive_override=archive_path if use_archive_transport else None,
            bundle_root_override=None if use_archive_transport else output_root,
            install_root=None,
            mode="copy",
            execute=True,
            output_format="json",
        ),
        "recommended_install_command": skill_pack_install_contract.recommended_install_command(
            profile_name=profile_name,
            bundle_archive_override=archive_path if use_archive_transport else None,
            bundle_root_override=None if use_archive_transport else output_root,
            mode="copy",
            execute=True,
        ),
        "recommended_verify_command": skill_pack_install_contract.recommended_verify_command(
            profile_name=profile_name,
            install_root=None,
            bundle_archive_override=archive_path if use_archive_transport else None,
            bundle_root_override=None if use_archive_transport else output_root,
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
    readme_text: str,
    archive_path: pathlib.Path | None,
    overwrite: bool,
) -> dict[str, Any] | None:
    ensure_clean_bundle_root(bundle_root, overwrite)
    bundle_root.mkdir(parents=True, exist_ok=True)

    for entry in source["skills"]:
        source_dir = pathlib.Path(entry["source_dir"])
        target_dir = bundle_root / entry["relative_dir"]
        if source_dir.resolve() == target_dir.resolve():
            raise SystemExit(f"staging target matches source for {entry['name']}: {target_dir}")
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_dir, target_dir)

    skill_pack_install_contract.bundle_readme_path(bundle_root).write_text(
        readme_text,
        encoding="utf-8",
    )
    skill_pack_install_contract.bundle_manifest_path(bundle_root).write_text(
        json.dumps(bundle_manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    if archive_path is None:
        return None
    return skill_pack_install_contract.write_bundle_archive(
        bundle_root,
        archive_path,
        profile_name=str(bundle_manifest["profile"]),
        overwrite=overwrite,
    )


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# Skill pack stage plan: {plan['profile']}",
        "",
        f"Profile revision: {plan['profile_revision']}",
        f"Bundle root: {plan['bundle_root']}",
        f"Bundle README: {plan['bundle_readme_path']}",
        f"Archive path: {plan['archive_path'] or '-'}",
        f"Execute: {plan['execute']}",
        f"Skill count: {plan['skill_count']}",
        f"Bundle digest: {plan['bundle_digest']}",
        f"Inspect: {plan['recommended_inspect_command']}",
        f"Import: {plan['recommended_import_command']}",
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
    parser.add_argument(
        "--archive-path",
        default=None,
        help="Optional ZIP output path for the staged profile bundle",
    )
    parser.add_argument("--execute", action="store_true", help="Materialize the staged bundle")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing staged bundle root")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    bundle_root = pathlib.Path(args.output_root).expanduser().resolve()
    archive_path = (
        pathlib.Path(args.archive_path).expanduser().resolve()
        if args.archive_path is not None
        else None
    )
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
        archive_path=archive_path,
        execute=args.execute,
    )

    if args.execute:
        try:
            archive_info = execute_stage(
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
                        "bundle_readme_path",
                        "archive_path",
                        "archive_format",
                        "archive_sha256",
                        "archive_bytes",
                        "execute",
                        "recommended_inspect_command",
                        "recommended_import_command",
                        "recommended_install_command",
                        "recommended_verify_command",
                    }
                },
                readme_text=build_bundle_readme(source=source),
                archive_path=archive_path,
                overwrite=args.overwrite,
            )
        except ValueError as exc:
            raise SystemExit(str(exc))
        if archive_info is not None:
            plan.update(archive_info)

    if args.format == "json":
        print(json.dumps(plan, indent=2))
    else:
        print(render_markdown(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
