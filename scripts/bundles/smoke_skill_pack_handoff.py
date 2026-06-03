#!/usr/bin/env python3
"""Run a bounded stage/inspect/install/verify smoke path for one skill-pack profile."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any, Mapping


def render_command(command: list[str]) -> str:
    quoted: list[str] = []
    for arg in command:
        if any(character.isspace() for character in arg):
            escaped = arg.replace("\\", "\\\\").replace('"', '\\"')
            quoted.append(f'"{escaped}"')
        else:
            quoted.append(arg)
    return " ".join(quoted)


def run_step(command: list[str], *, repo_root: pathlib.Path) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    result: dict[str, Any] | None = None
    stdout = completed.stdout.strip()
    if stdout:
        try:
            parsed = json.loads(stdout)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict):
            result = parsed
    return {
        "command": render_command(command),
        "status": "ok" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "result": result,
        "stderr": completed.stderr.strip() or None,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        f"# Skill pack handoff smoke: {report['profile']}",
        "",
        f"Verified: {report['verified']}",
        f"Transport: {report['transport']}",
        f"Work root: {report['work_root']}",
        "",
        "## Steps",
    ]
    for step_name in (
        "stage",
        "inspect_dir",
        "inspect_archive",
        "install_dir",
        "verify_dir",
        "install_archive",
        "verify_archive",
    ):
        step = report["steps"].get(step_name)
        if step is None:
            continue
        lines.append(f"- {step_name}: {step['status']} ({step['command']})")
    return "\n".join(lines)


def build_report(
    *,
    profile: str,
    transport: str,
    work_root: pathlib.Path,
    steps: Mapping[str, Any],
) -> dict[str, Any]:
    applicable_steps = [step for step in steps.values() if step is not None]
    verified = all(step["status"] == "ok" for step in applicable_steps)
    return {
        "profile": profile,
        "transport": transport,
        "work_root": str(work_root),
        "verified": verified,
        "steps": dict(steps),
    }


def execute_smoke(
    *,
    repo_root: pathlib.Path,
    profile: str,
    transport: str,
    work_root: pathlib.Path,
) -> dict[str, Any]:
    bundle_root = work_root / "bundle"
    archive_path = work_root / f"{profile}.zip"
    install_dir_root = work_root / "install-dir"
    install_archive_root = work_root / "install-archive"

    use_dir = transport in {"dir", "both"}
    use_archive = transport in {"zip", "both"}
    stage_command = [
        sys.executable,
        "scripts/stage_skill_pack.py",
        "--repo-root",
        ".",
        "--profile",
        profile,
        "--output-root",
        str(bundle_root),
        "--execute",
        "--overwrite",
        "--format",
        "json",
    ]
    if use_archive:
        stage_command.extend(["--archive-path", str(archive_path)])

    steps: dict[str, Any] = {
        "stage": run_step(stage_command, repo_root=repo_root),
        "inspect_dir": None,
        "inspect_archive": None,
        "install_dir": None,
        "verify_dir": None,
        "install_archive": None,
        "verify_archive": None,
    }
    if steps["stage"]["status"] != "ok":
        return build_report(profile=profile, transport=transport, work_root=work_root, steps=steps)

    if use_dir:
        steps["inspect_dir"] = run_step(
            [
                sys.executable,
                "scripts/inspect_skill_pack.py",
                "--bundle-root",
                str(bundle_root),
                "--format",
                "json",
            ],
            repo_root=repo_root,
        )
        if steps["inspect_dir"]["status"] != "ok":
            return build_report(profile=profile, transport=transport, work_root=work_root, steps=steps)

    if use_archive:
        steps["inspect_archive"] = run_step(
            [
                sys.executable,
                "scripts/inspect_skill_pack.py",
                "--bundle-archive",
                str(archive_path),
                "--format",
                "json",
            ],
            repo_root=repo_root,
        )
        if steps["inspect_archive"]["status"] != "ok":
            return build_report(profile=profile, transport=transport, work_root=work_root, steps=steps)

    if use_dir:
        steps["install_dir"] = run_step(
            [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                profile,
                "--bundle-root",
                str(bundle_root),
                "--dest-root",
                str(install_dir_root),
                "--mode",
                "copy",
                "--execute",
                "--overwrite",
                "--format",
                "json",
            ],
            repo_root=repo_root,
        )
        if steps["install_dir"]["status"] != "ok":
            return build_report(profile=profile, transport=transport, work_root=work_root, steps=steps)
        steps["verify_dir"] = run_step(
            [
                sys.executable,
                "scripts/verify_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                profile,
                "--bundle-root",
                str(bundle_root),
                "--install-root",
                str(install_dir_root),
                "--format",
                "json",
            ],
            repo_root=repo_root,
        )
        if steps["verify_dir"]["status"] != "ok":
            return build_report(profile=profile, transport=transport, work_root=work_root, steps=steps)

    if use_archive:
        steps["install_archive"] = run_step(
            [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                profile,
                "--bundle-archive",
                str(archive_path),
                "--dest-root",
                str(install_archive_root),
                "--mode",
                "copy",
                "--execute",
                "--overwrite",
                "--format",
                "json",
            ],
            repo_root=repo_root,
        )
        if steps["install_archive"]["status"] != "ok":
            return build_report(profile=profile, transport=transport, work_root=work_root, steps=steps)
        steps["verify_archive"] = run_step(
            [
                sys.executable,
                "scripts/verify_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                profile,
                "--bundle-archive",
                str(archive_path),
                "--install-root",
                str(install_archive_root),
                "--format",
                "json",
            ],
            repo_root=repo_root,
        )

    return build_report(profile=profile, transport=transport, work_root=work_root, steps=steps)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing the packaging scripts")
    parser.add_argument("--profile", default="repo-core-only", help="Resolved install profile to smoke test")
    parser.add_argument(
        "--transport",
        choices=("dir", "zip", "both"),
        default="both",
        help="Which staged handoff transport(s) to smoke test",
    )
    parser.add_argument(
        "--work-root",
        default=None,
        help="Optional directory to hold staged and installed smoke artifacts",
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    parser.add_argument("--keep-temp", action="store_true", help="Keep an auto-created temporary work root")
    args = parser.parse_args(argv)

    repo_root = pathlib.Path(args.repo_root).resolve()
    if args.work_root is not None:
        work_root = pathlib.Path(args.work_root).expanduser().resolve()
        work_root.mkdir(parents=True, exist_ok=True)
        report = execute_smoke(
            repo_root=repo_root,
            profile=args.profile,
            transport=args.transport,
            work_root=work_root,
        )
    elif args.keep_temp:
        work_root = pathlib.Path(tempfile.mkdtemp(prefix="aoa-skills-packaging-smoke-"))
        report = execute_smoke(
            repo_root=repo_root,
            profile=args.profile,
            transport=args.transport,
            work_root=work_root,
        )
    else:
        with tempfile.TemporaryDirectory(prefix="aoa-skills-packaging-smoke-") as tmpdir:
            work_root = pathlib.Path(tmpdir)
            report = execute_smoke(
                repo_root=repo_root,
                profile=args.profile,
                transport=args.transport,
                work_root=work_root,
            )

    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render_markdown(report))
    return 0 if report["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
