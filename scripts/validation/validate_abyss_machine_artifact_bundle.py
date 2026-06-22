#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = "mechanics/release-support/manifests/release_manifest.bundle.json"
ARTIFACT_CLASS = "aoa_skills_release_manifest"
OWNER_REPO = "aoa-skills"
EXPECTED_REQUIRED_CONTROLS = ["abi_signature"]


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


def path_ref(path: Path) -> str:
    resolved = path.expanduser().resolve()
    try:
        return resolved.relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(resolved)


def copy_bundle(bundle_dir: Path, target: Path) -> Path:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(bundle_dir, target)
    return target


def assert_expected_controls(verify: dict[str, Any]) -> None:
    required = verify.get("required_controls")
    verified = verify.get("verified_controls")
    if required != EXPECTED_REQUIRED_CONTROLS:
        raise ValueError(f"unexpected required controls: {required!r}")
    if verified != EXPECTED_REQUIRED_CONTROLS:
        raise ValueError(f"unexpected verified controls: {verified!r}")


def registry_roundtrip(
    artifact_bundles: Any,
    bundle_dir: Path,
    registry_dir: Path,
    *,
    lifecycle_state: str,
    evidence_ref: str,
) -> dict[str, Any]:
    registered = artifact_bundles.write_bundle_registry_record(
        bundle_dir,
        registry_dir,
        lifecycle_state=lifecycle_state,
        consumer_refs=["aoa-skills:release-manifest"],
        evidence_refs=[evidence_ref],
    )
    latest = artifact_bundles.read_bundle_registry(registry_dir, artifact_class=ARTIFACT_CLASS)
    latest_record = latest.get("latest_by_artifact_class", {}).get(ARTIFACT_CLASS)
    return {
        "ok": bool(
            registered.get("ok")
            and isinstance(latest_record, dict)
            and latest_record.get("record_id") == registered.get("record", {}).get("record_id")
            and latest_record.get("lifecycle_state") == lifecycle_state
        ),
        "registered": registered,
        "latest": latest,
    }


def registry_roundtrip_with_subject_store(
    artifact_bundles: Any,
    bundle_dir: Path,
    registry_dir: Path,
    store_root: Path,
    *,
    lifecycle_state: str,
    evidence_ref: str,
) -> dict[str, Any]:
    env_root = "ABYSS_MACHINE_ARTIFACT_SUBJECT_STORE_ROOT"
    env_roots = "ABYSS_MACHINE_ARTIFACT_SUBJECT_STORE_ROOTS"
    old_root = os.environ.get(env_root)
    old_roots = os.environ.get(env_roots)
    os.environ[env_root] = str(store_root)
    os.environ[env_roots] = str(store_root)
    try:
        return registry_roundtrip(
            artifact_bundles,
            bundle_dir,
            registry_dir,
            lifecycle_state=lifecycle_state,
            evidence_ref=evidence_ref,
        )
    finally:
        if old_root is None:
            os.environ.pop(env_root, None)
        else:
            os.environ[env_root] = old_root
        if old_roots is None:
            os.environ.pop(env_roots, None)
        else:
            os.environ[env_roots] = old_roots


def trust_gate_allow_latest(
    artifact_bundles: Any,
    registry_dir: Path,
    registry: dict[str, Any],
) -> dict[str, Any]:
    record = registry.get("registered", {}).get("record", {})
    trust_gate = artifact_bundles.trust_gate(
        registry_dir,
        artifact_class=ARTIFACT_CLASS,
        subject_digest=str(record.get("subject_digest") or ""),
        consumer_intent="agent",
        expected_source_repo=OWNER_REPO,
    )
    inspected_claims = trust_gate.get("inspected_claims", {})
    return {
        "ok": bool(
            trust_gate.get("ok")
            and trust_gate.get("verdict") in {"allow", "warn"}
            and trust_gate.get("decision", {}).get("model") == "fail_closed_consumer_admission"
            and trust_gate.get("decision", {}).get("allow") is True
            and inspected_claims.get("registry_latest", {}).get("selected_record_is_latest") is True
            and inspected_claims.get("controls", {}).get("required_controls_missing") == []
            and inspected_claims.get("source", {}).get("source_repo_matched") is True
        ),
        "trust_gate": trust_gate,
    }


def verify_missing_abi(artifact_bundles: Any, bundle_dir: Path, tmp_root: Path) -> dict[str, Any]:
    candidate = copy_bundle(bundle_dir, tmp_root / "missing-abi")
    path = candidate / artifact_bundles.ABI_SIDECAR
    if path.exists():
        path.unlink()
    verification = artifact_bundles.verify_bundle(candidate)
    return {
        "ok": verification.get("ok") is False and bool(verification.get("missing")),
        "verification": verification,
    }


def verify_unverified_latest_rejected(artifact_bundles: Any, bundle_dir: Path, tmp_root: Path) -> dict[str, Any]:
    candidate = copy_bundle(bundle_dir, tmp_root / "unverified-latest")
    path = candidate / artifact_bundles.ABI_SIDECAR
    if path.exists():
        path.unlink()
    registered = artifact_bundles.write_bundle_registry_record(
        candidate,
        tmp_root / "unverified-registry",
        lifecycle_state="release-ready",
    )
    return {
        "ok": registered.get("ok") is False
        and any("successful bundle verification" in item for item in registered.get("errors", [])),
        "registered": registered,
    }


def verify_terminal_registry_state(artifact_bundles: Any, bundle_dir: Path, tmp_root: Path) -> dict[str, Any]:
    registry_dir = tmp_root / "terminal-registry"
    release_ready = registry_roundtrip(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        lifecycle_state="release-ready",
        evidence_ref="terminal-state-rehearsal",
    )
    revoked = artifact_bundles.write_bundle_registry_record(
        bundle_dir,
        registry_dir,
        lifecycle_state="revoked",
        revocation_reason="aoa-skills release manifest terminal-state rehearsal",
    )
    revoked_gate = artifact_bundles.trust_gate(
        registry_dir,
        artifact_class=ARTIFACT_CLASS,
        record_id=str(release_ready.get("registered", {}).get("record", {}).get("record_id") or ""),
        consumer_intent="agent",
    )
    after_revoke = artifact_bundles.read_bundle_registry(registry_dir, artifact_class=ARTIFACT_CLASS)
    return {
        "ok": bool(
            release_ready.get("ok")
            and revoked.get("ok")
            and revoked_gate.get("verdict") == "deny"
            and revoked_gate.get("decision", {}).get("allow") is False
            and revoked_gate.get("inspected_claims", {}).get("lifecycle", {}).get("terminal_state") is True
            and not after_revoke.get("latest_by_artifact_class")
        ),
        "release_ready": release_ready,
        "revoked": revoked,
        "revoked_trust_gate": revoked_gate,
        "after_revoke": after_revoke,
    }


def verify_materialized_subject_store(
    artifact_bundles: Any,
    manifest: Path,
    bundle_dir: Path,
    registry_dir: Path,
    tmp_root: Path,
) -> dict[str, Any]:
    store_root = tmp_root / "subject-store"
    pre_registry = registry_roundtrip(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        lifecycle_state="release-ready",
        evidence_ref="materialized-subject-store-precondition",
    )
    materialized = artifact_bundles.materialize_artifact_subjects(
        bundle_dir,
        store_root=store_root,
        registry_dir=registry_dir,
        manifest_ref=manifest,
        consumer_intent="agent",
        expected_source_repo=OWNER_REPO,
    )
    refreshed_registry = registry_roundtrip_with_subject_store(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        store_root,
        lifecycle_state="release-ready",
        evidence_ref="materialized-subject-store-rehearsal",
    )
    latest_record = refreshed_registry.get("latest", {}).get("latest_by_artifact_class", {}).get(ARTIFACT_CLASS, {})
    store_status = latest_record.get("artifact_subject_store") if isinstance(latest_record, dict) else {}
    gate = artifact_bundles.trust_gate(
        registry_dir,
        artifact_class=ARTIFACT_CLASS,
        subject_digest=str(materialized.get("aggregate_digest") or ""),
        consumer_intent="agent",
        expected_source_repo=OWNER_REPO,
    )
    return {
        "ok": bool(
            pre_registry.get("ok")
            and materialized.get("ok")
            and refreshed_registry.get("ok")
            and isinstance(store_status, dict)
            and store_status.get("ok") is True
            and gate.get("verdict") == "allow"
        ),
        "pre_registry": pre_registry,
        "materialized": materialized,
        "refreshed_registry": refreshed_registry,
        "trust_gate": gate,
    }


def run_adversarial_checks(
    artifact_bundles: Any,
    manifest: Path,
    bundle_dir: Path,
    registry_dir: Path,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="aoa-skills-artifact-negative-", dir=default_tmp_root()) as tmp:
        tmp_root = Path(tmp)
        checks = {
            "missing_abi": verify_missing_abi(artifact_bundles, bundle_dir, tmp_root),
            "unverified_latest_rejected": verify_unverified_latest_rejected(artifact_bundles, bundle_dir, tmp_root),
            "terminal_registry_state": verify_terminal_registry_state(artifact_bundles, bundle_dir, tmp_root),
            "materialized_subject_store": verify_materialized_subject_store(
                artifact_bundles,
                manifest,
                bundle_dir,
                registry_dir,
                tmp_root,
            ),
        }
    return {
        "ok": all(bool(item.get("ok")) for item in checks.values()),
        "checks": checks,
    }


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
        registry_dir = Path(tmp) / "release-manifest-registry"
        build = artifact_bundles.build_sidecars(target, manifest_ref=manifest)
        sign = artifact_bundles.sign_bundle(target)
        verify = artifact_bundles.verify_bundle(target)
        release = artifact_bundles.release_check(target, enforcement="blocking")
        assert_expected_controls(verify)
        registry = registry_roundtrip(
            artifact_bundles,
            target,
            registry_dir,
            lifecycle_state="release-ready",
            evidence_ref=f"{path_ref(target)}/artifact.verify.json",
        )
        trust_gate = trust_gate_allow_latest(artifact_bundles, registry_dir, registry)
        adversarial = run_adversarial_checks(artifact_bundles, manifest, target, registry_dir)
        return {
            "ok": bool(
                build.get("ok")
                and sign.get("ok")
                and verify.get("ok")
                and release.get("ok")
                and registry.get("ok")
                and trust_gate.get("ok")
                and adversarial.get("ok")
            ),
            "schema": "aoa_skills_abyss_machine_artifact_bundle_validation_v1",
            "manifest": path_ref(manifest),
            "bundle_dir": path_ref(target),
            "registry_dir": path_ref(registry_dir),
            "artifact_class": ARTIFACT_CLASS,
            "required_controls": verify.get("required_controls"),
            "verified_controls": verify.get("verified_controls"),
            "registry": registry,
            "trust_gate": trust_gate,
            "adversarial_checks": adversarial,
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
