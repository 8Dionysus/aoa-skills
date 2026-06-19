#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = "mechanics/release-support/manifests/release_manifest.bundle.json"


def abyss_machine_repo_candidates() -> list[Path]:
    env_root = os.environ.get("ABYSS_MACHINE_REPO_ROOT")
    candidates: list[Path] = []
    if env_root:
        candidates.append(Path(env_root))
    candidates.extend(
        [
            Path.home() / "src" / "abyss-machine",
            Path("/srv/AbyssOS/abyss-machine"),
        ]
    )
    return candidates


def locate_abyss_machine_repo() -> Path | None:
    candidates = abyss_machine_repo_candidates()
    for candidate in candidates:
        if (candidate / "src" / "abyss_machine" / "artifact_bundles.py").is_file():
            return candidate
    return None


def import_artifact_bundles() -> tuple[Any | None, str | None]:
    repo = locate_abyss_machine_repo()
    if repo is not None:
        src_root = repo / "src"
        if str(src_root) not in sys.path:
            sys.path.insert(0, str(src_root))
    try:
        from abyss_machine import artifact_bundles
    except ImportError as exc:
        return None, str(exc)
    return artifact_bundles, None


def default_tmp_root() -> Path | None:
    for raw in (os.environ.get("ABYSS_MACHINE_TMP_ROOT"), "/srv/abyss-machine/tmp"):
        if not raw:
            continue
        path = Path(raw)
        if path.is_dir():
            return path
    return None


def run_bundle(manifest: Path, bundle_dir: Path | None) -> dict[str, Any]:
    artifact_bundles, import_error = import_artifact_bundles()
    if artifact_bundles is None:
        return {
            "ok": False,
            "schema": "aoa_skills_abyss_machine_artifact_bundle_validation_v1",
            "error": "abyss-machine artifact_bundles module is unavailable",
            "detail": import_error,
            "checked_roots": [str(candidate) for candidate in abyss_machine_repo_candidates()],
        }

    tmp_root = default_tmp_root()
    with tempfile.TemporaryDirectory(prefix="aoa-skills-artifact-bundle-", dir=tmp_root) as tmp:
        target = bundle_dir or Path(tmp) / "release-manifest"
        build = artifact_bundles.build_sidecars(target, manifest_ref=manifest)
        sign = artifact_bundles.sign_bundle(target)
        verify = artifact_bundles.verify_bundle(target)
        release = artifact_bundles.release_check(target, enforcement="blocking")
        return {
            "ok": bool(build.get("ok") and sign.get("ok") and verify.get("ok") and release.get("ok")),
            "schema": "aoa_skills_abyss_machine_artifact_bundle_validation_v1",
            "manifest": str(manifest),
            "bundle_dir": str(target),
            "artifact_class": "aoa_skills_release_manifest",
            "steps": {
                "build_sidecars": build,
                "sign": sign,
                "verify": verify,
                "release_check": release,
            },
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--bundle-dir")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = repo_root / manifest
    bundle_dir = Path(args.bundle_dir).resolve() if args.bundle_dir else None
    payload = run_bundle(manifest, bundle_dir)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0 if payload.get("ok") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
