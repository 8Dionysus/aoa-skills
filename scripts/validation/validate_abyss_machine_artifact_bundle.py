#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = "mechanics/release-support/manifests/release_manifest.bundle.json"
DEFAULT_BUNDLE_DIR = REPO_ROOT / "dist" / "abyss-artifact-bundle" / "aoa-skills-release-manifest"
DEFAULT_REGISTRY_DIR = REPO_ROOT / "dist" / "abyss-artifact-registry" / "aoa-skills-release-manifest"
DEFAULT_SUBJECT_STORE_ROOT = REPO_ROOT / "dist" / "abyss-artifact-subjects" / "aoa-skills-release-manifest"
ARTIFACT_CLASS = "aoa_skills_release_manifest"
OWNER_REPO = "aoa-skills"
CONSUMER_INTENT = "agent"
CONSUMER_REF = "aoa-skills:release-manifest"
TRUST_ROOT_MODE = "host_managed"
PRODUCER = "aoa-skills release manifest builder from generated export surfaces"
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


def public_seed_root() -> Path:
    return Path(os.environ.get("ABYSS_MACHINE_PUBLIC_SEED_ROOT", "/usr/local/share/abyss-machine")).expanduser()


def import_from_package_root(package_root: Path) -> tuple[Any, Path, str] | None:
    root = package_root.expanduser().resolve()
    if (root / "abyss_machine" / "artifact_bundles.py").is_file():
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from abyss_machine import artifact_bundles

        return artifact_bundles, public_seed_root(), str(root)
    return None


def import_artifact_bundles() -> tuple[Any | None, Path | None, str | None, str | None]:
    package_root = os.environ.get("ABYSS_MACHINE_PACKAGE_ROOT")
    if package_root:
        imported = import_from_package_root(Path(package_root))
        if imported is not None:
            artifact_bundles, abyss_machine_root, package_root_text = imported
            return artifact_bundles, abyss_machine_root, package_root_text, None

    repo = locate_abyss_machine_repo()
    if repo is not None:
        src_root = repo / "src"
        if str(src_root) not in sys.path:
            sys.path.insert(0, str(src_root))
        try:
            from abyss_machine import artifact_bundles
        except ImportError as exc:
            return None, None, None, str(exc)
        return artifact_bundles, repo, None, None

    installed = import_from_package_root(Path("/usr/local/libexec"))
    if installed is not None:
        artifact_bundles, abyss_machine_root, package_root_text = installed
        return artifact_bundles, abyss_machine_root, package_root_text, None

    try:
        from abyss_machine import artifact_bundles
    except ImportError as exc:
        return None, None, None, str(exc)
    return artifact_bundles, getattr(artifact_bundles, "REPO_ROOT", None), None, None


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


def public_location_ref(value: Any) -> str | None:
    if value in {None, ""}:
        return None
    resolved = Path(str(value)).expanduser().resolve()
    repo_root = REPO_ROOT.resolve()
    if resolved == repo_root or resolved.is_relative_to(repo_root):
        return path_ref(resolved)
    for candidate in abyss_machine_repo_candidates():
        if resolved == candidate.expanduser().resolve():
            return "repo:abyss-machine"
    seed_root = public_seed_root().resolve()
    if resolved == seed_root or resolved.is_relative_to(seed_root):
        suffix = resolved.relative_to(seed_root).as_posix()
        return "public-seed:abyss-machine" + (f"/{suffix}" if suffix != "." else "")
    if resolved == Path("/usr/local/libexec").resolve():
        return "package:/usr/local/libexec"
    digest = hashlib.sha256(str(resolved).encode("utf-8")).hexdigest()[:12]
    return f"host-path-redacted:{digest}"


def copy_bundle(bundle_dir: Path, target: Path) -> Path:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(bundle_dir, target)
    return target


def sanitize_public_payload(payload: Any) -> Any:
    local_root = str(REPO_ROOT.resolve())
    if isinstance(payload, dict):
        return {key: sanitize_public_payload(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [sanitize_public_payload(item) for item in payload]
    if isinstance(payload, str) and (payload == local_root or payload.startswith(local_root + os.sep)):
        return path_ref(Path(payload))
    return payload


def sanitize_public_json_tree(root: Path) -> None:
    for path in sorted(root.rglob("*")) if root.exists() else []:
        if not path.is_file() or path.suffix not in {".json", ".jsonl"}:
            continue
        if path.suffix == ".jsonl":
            lines: list[str] = []
            changed = False
            for line in path.read_text(encoding="utf-8").splitlines():
                payload = json.loads(line)
                sanitized = sanitize_public_payload(payload)
                changed = changed or sanitized != payload
                lines.append(json.dumps(sanitized, ensure_ascii=False, sort_keys=True))
            if changed:
                path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        sanitized = sanitize_public_payload(payload)
        if sanitized != payload:
            path.write_text(json.dumps(sanitized, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def public_payload_leaks(*roots: Path) -> list[str]:
    forbidden = [
        str(REPO_ROOT.resolve()),
        str(Path.home()),
        "/srv/abyss-machine/tmp",
    ]
    leaks: list[str] = []
    for root in roots:
        if not root.exists():
            continue
        paths = [root] if root.is_file() else sorted(root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix not in {".json", ".jsonl"}:
                continue
            text = path.read_text(encoding="utf-8")
            for marker in forbidden:
                if marker and marker in text:
                    leaks.append(f"{path}: {marker}")
    return leaks


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
    manifest: Path,
    abyss_repo_root: Path,
) -> dict[str, Any]:
    promoted = artifact_bundles.promote_bundle_evidence(
        bundle_dir,
        registry_dir,
        lifecycle_state=lifecycle_state,
        consumer_refs=[CONSUMER_REF],
        evidence_refs=[evidence_ref],
        source_repo=OWNER_REPO,
        source_ref=path_ref(manifest),
        producer=PRODUCER,
        trust_root_mode=TRUST_ROOT_MODE,
        repo_root=abyss_repo_root,
    )
    latest = artifact_bundles.read_bundle_registry(registry_dir, artifact_class=ARTIFACT_CLASS)
    latest_record = latest.get("latest_by_artifact_class", {}).get(ARTIFACT_CLASS)
    return {
        "ok": bool(
            promoted.get("ok")
            and isinstance(latest_record, dict)
            and latest_record.get("record_id") == promoted.get("promotion", {}).get("record_id")
            and latest_record.get("lifecycle_state") == lifecycle_state
        ),
        "promoted": promoted,
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
    manifest: Path,
    abyss_repo_root: Path,
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
            manifest=manifest,
            abyss_repo_root=abyss_repo_root,
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
    *,
    require_subject_store: bool = True,
) -> dict[str, Any]:
    record = registry.get("promoted", {}).get("record", {})
    trust_gate = artifact_bundles.trust_gate(
        registry_dir,
        artifact_class=ARTIFACT_CLASS,
        subject_digest=str(record.get("subject_digest") or ""),
        consumer_intent="agent",
        expected_source_repo=OWNER_REPO,
        expected_trust_root_mode=TRUST_ROOT_MODE,
    )
    inspected_claims = trust_gate.get("inspected_claims", {})
    decision = trust_gate.get("decision", {})
    blockers = trust_gate.get("blockers", [])
    expected_pre_materialization_blocker = bool(
        not require_subject_store
        and trust_gate.get("verdict") == "deny"
        and decision.get("allow") is False
        and blockers == ["required_artifact_subject_store_not_verified"]
        and inspected_claims.get("artifact_subject_store", {}).get("required") is True
        and inspected_claims.get("artifact_subject_store", {}).get("ok") is False
    )
    allowed_after_materialization = bool(
        trust_gate.get("ok")
        and trust_gate.get("verdict") in {"allow", "warn"}
        and decision.get("model") == "fail_closed_consumer_admission"
        and decision.get("allow") is True
    )
    return {
        "ok": bool(
            (allowed_after_materialization or expected_pre_materialization_blocker)
            and decision.get("model") == "fail_closed_consumer_admission"
            and inspected_claims.get("registry_latest", {}).get("selected_record_is_latest") is True
            and inspected_claims.get("controls", {}).get("required_controls_missing") == []
            and inspected_claims.get("source", {}).get("source_repo_matched") is True
            and inspected_claims.get("trust_root", {}).get("trust_root_mode_matched") is True
            and (
                not require_subject_store
                or inspected_claims.get("artifact_subject_store", {}).get("ok") is True
            )
        ),
        "expected_pre_materialization_blocker": expected_pre_materialization_blocker,
        "trust_gate": trust_gate,
    }


def verify_missing_abi(artifact_bundles: Any, abyss_repo_root: Path, bundle_dir: Path, tmp_root: Path) -> dict[str, Any]:
    candidate = copy_bundle(bundle_dir, tmp_root / "missing-abi")
    path = candidate / artifact_bundles.ABI_SIDECAR
    if path.exists():
        path.unlink()
    verification = artifact_bundles.verify_bundle(candidate, repo_root=abyss_repo_root)
    return {
        "ok": verification.get("ok") is False and bool(verification.get("missing")),
        "verification": verification,
    }


def verify_wrong_external_subject(
    artifact_bundles: Any,
    abyss_repo_root: Path,
    bundle_dir: Path,
    tmp_root: Path,
) -> dict[str, Any]:
    candidate = copy_bundle(bundle_dir, tmp_root / "wrong-external-subject")
    path = candidate / artifact_bundles.ABI_SIDECAR
    sidecar = json.loads(path.read_text(encoding="utf-8"))
    external_subject = sidecar.get("external_subject")
    if not isinstance(external_subject, dict):
        return {"ok": False, "error": "ABI sidecar has no external_subject"}
    external_subject["sha256"] = "sha256:" + ("0" * 64)
    path.write_text(json.dumps(sidecar, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    verification = artifact_bundles.verify_bundle(candidate, repo_root=abyss_repo_root)
    return {
        "ok": verification.get("ok") is False
        and any("subject digest does not match ABI external_subject sha256" in item for item in verification.get("errors", [])),
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


def verify_terminal_registry_state(
    artifact_bundles: Any,
    bundle_dir: Path,
    tmp_root: Path,
    manifest: Path,
    abyss_repo_root: Path,
) -> dict[str, Any]:
    registry_dir = tmp_root / "terminal-registry"
    release_ready = registry_roundtrip(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        lifecycle_state="release-ready",
        evidence_ref="terminal-state-rehearsal",
        manifest=manifest,
        abyss_repo_root=abyss_repo_root,
    )
    revoked = artifact_bundles.write_bundle_registry_record(
        bundle_dir,
        registry_dir,
        lifecycle_state="revoked",
        revocation_reason="aoa-skills release manifest terminal-state rehearsal",
        source_repo=OWNER_REPO,
        source_ref=path_ref(manifest),
        producer=PRODUCER,
        trust_root_mode=TRUST_ROOT_MODE,
        repo_root=abyss_repo_root,
    )
    revoked_gate = artifact_bundles.trust_gate(
        registry_dir,
        artifact_class=ARTIFACT_CLASS,
        record_id=str(release_ready.get("promoted", {}).get("record", {}).get("record_id") or ""),
        consumer_intent="agent",
        expected_source_repo=OWNER_REPO,
        expected_trust_root_mode=TRUST_ROOT_MODE,
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
    abyss_repo_root: Path,
    store_root: Path | None = None,
) -> dict[str, Any]:
    target_store_root = store_root or tmp_root / "subject-store"
    pre_registry = registry_roundtrip(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        lifecycle_state="release-ready",
        evidence_ref="materialized-subject-store-precondition",
        manifest=manifest,
        abyss_repo_root=abyss_repo_root,
    )
    materialized = artifact_bundles.materialize_artifact_subjects(
        bundle_dir,
        store_root=target_store_root,
        registry_dir=registry_dir,
        manifest_ref=manifest,
        consumer_intent=CONSUMER_INTENT,
        expected_source_repo=OWNER_REPO,
        expected_trust_root_mode=TRUST_ROOT_MODE,
        repo_root=abyss_repo_root,
    )
    refreshed_registry = registry_roundtrip_with_subject_store(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        target_store_root,
        lifecycle_state="release-ready",
        evidence_ref="materialized-subject-store-rehearsal",
        manifest=manifest,
        abyss_repo_root=abyss_repo_root,
    )
    latest_record = refreshed_registry.get("latest", {}).get("latest_by_artifact_class", {}).get(ARTIFACT_CLASS, {})
    store_status = latest_record.get("artifact_subject_store") if isinstance(latest_record, dict) else {}
    gate = artifact_bundles.trust_gate(
        registry_dir,
        artifact_class=ARTIFACT_CLASS,
        subject_digest=str(materialized.get("aggregate_digest") or ""),
        consumer_intent=CONSUMER_INTENT,
        expected_source_repo=OWNER_REPO,
        expected_trust_root_mode=TRUST_ROOT_MODE,
    )
    return {
        "ok": bool(
            pre_registry.get("ok")
            and materialized.get("ok")
            and refreshed_registry.get("ok")
            and isinstance(store_status, dict)
            and store_status.get("ok") is True
            and gate.get("verdict") in {"allow", "warn"}
            and gate.get("inspected_claims", {}).get("artifact_subject_store", {}).get("ok") is True
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
    abyss_repo_root: Path,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="aoa-skills-artifact-negative-", dir=default_tmp_root()) as tmp:
        tmp_root = Path(tmp)
        checks = {
            "missing_abi": verify_missing_abi(artifact_bundles, abyss_repo_root, bundle_dir, tmp_root),
            "wrong_external_subject": verify_wrong_external_subject(artifact_bundles, abyss_repo_root, bundle_dir, tmp_root),
            "unverified_latest_rejected": verify_unverified_latest_rejected(artifact_bundles, bundle_dir, tmp_root),
            "terminal_registry_state": verify_terminal_registry_state(
                artifact_bundles,
                bundle_dir,
                tmp_root,
                manifest,
                abyss_repo_root,
            ),
            "materialized_subject_store": verify_materialized_subject_store(
                artifact_bundles,
                manifest,
                bundle_dir,
                tmp_root / "materialized-registry",
                tmp_root,
                abyss_repo_root,
                tmp_root / "subject-store",
            ),
        }
    return {
        "ok": all(bool(item.get("ok")) for item in checks.values()),
        "checks": checks,
    }


def run_bundle(
    manifest: Path,
    bundle_dir: Path | None,
    registry_dir: Path | None,
    subject_store_root: Path | None,
    *,
    clean: bool = True,
) -> dict[str, Any]:
    artifact_bundles, abyss_machine_root, package_root, import_error = import_artifact_bundles()
    if artifact_bundles is None:
        return {
            "ok": False,
            "schema": "aoa_skills_abyss_machine_artifact_bundle_validation_v1",
            "error": "abyss-machine artifact_bundles module is unavailable",
            "detail": import_error,
            "checked_roots": [str(candidate) for candidate in abyss_machine_repo_candidates()],
        }

    target = bundle_dir or DEFAULT_BUNDLE_DIR
    registry_path = registry_dir or DEFAULT_REGISTRY_DIR
    store_root = subject_store_root or DEFAULT_SUBJECT_STORE_ROOT
    if clean and target.exists():
        shutil.rmtree(target)
    if clean and registry_path.exists():
        shutil.rmtree(registry_path)
    if clean and store_root.exists():
        shutil.rmtree(store_root)

    abyss_root = abyss_machine_root or artifact_bundles.REPO_ROOT
    target.mkdir(parents=True, exist_ok=True)
    build = artifact_bundles.build_sidecars(target, manifest_ref=manifest, repo_root=abyss_root)
    sign = artifact_bundles.sign_bundle(target, repo_root=abyss_root)
    verify = artifact_bundles.verify_bundle(target, repo_root=abyss_root)
    release = artifact_bundles.release_check(target, enforcement="blocking", repo_root=abyss_root)
    assert_expected_controls(verify)
    registry = registry_roundtrip(
        artifact_bundles,
        target,
        registry_path,
        lifecycle_state="release-ready",
        evidence_ref=f"{path_ref(target)}/artifact.verify.json",
        manifest=manifest,
        abyss_repo_root=abyss_root,
    )
    pre_materialization_gate = trust_gate_allow_latest(
        artifact_bundles,
        registry_path,
        registry,
        require_subject_store=False,
    )
    materialized = artifact_bundles.materialize_artifact_subjects(
        target,
        store_root=store_root,
        registry_dir=registry_path,
        manifest_ref=manifest,
        consumer_intent=CONSUMER_INTENT,
        expected_source_repo=OWNER_REPO,
        expected_trust_root_mode=TRUST_ROOT_MODE,
        repo_root=abyss_root,
    )
    registry_with_subject_store = registry_roundtrip_with_subject_store(
        artifact_bundles,
        target,
        registry_path,
        store_root,
        lifecycle_state="release-ready",
        evidence_ref="materialized-subject-store",
        manifest=manifest,
        abyss_repo_root=abyss_root,
    )
    trust_gate = trust_gate_allow_latest(artifact_bundles, registry_path, registry_with_subject_store)
    subject_store_gate = artifact_bundles.trust_gate(
        registry_path,
        artifact_class=ARTIFACT_CLASS,
        subject_digest=str(materialized.get("aggregate_digest") or ""),
        consumer_intent=CONSUMER_INTENT,
        expected_source_repo=OWNER_REPO,
        expected_trust_root_mode=TRUST_ROOT_MODE,
    )
    sanitize_public_json_tree(target)
    sanitize_public_json_tree(registry_path)
    sanitize_public_json_tree(store_root)
    public_safe_leaks = public_payload_leaks(target, registry_path, store_root)
    latest_registry = artifact_bundles.read_bundle_registry(registry_path, artifact_class=ARTIFACT_CLASS)
    adversarial = run_adversarial_checks(artifact_bundles, manifest, target, abyss_root)
    return {
        "ok": bool(
            build.get("ok")
            and sign.get("ok")
            and verify.get("ok")
            and release.get("ok")
            and registry.get("ok")
            and pre_materialization_gate.get("ok")
            and materialized.get("ok")
            and registry_with_subject_store.get("ok")
            and trust_gate.get("ok")
            and subject_store_gate.get("ok")
            and subject_store_gate.get("verdict") in {"allow", "warn"}
            and subject_store_gate.get("decision", {}).get("allow") is True
            and subject_store_gate.get("inspected_claims", {}).get("artifact_subject_store", {}).get("ok") is True
            and adversarial.get("ok")
            and not public_safe_leaks
        ),
        "schema": "aoa_skills_abyss_machine_artifact_bundle_validation_v1",
        "manifest": path_ref(manifest),
        "bundle_dir": path_ref(target),
        "registry_dir": path_ref(registry_path),
        "subject_store_root": path_ref(store_root),
        "artifact_class": ARTIFACT_CLASS,
        "required_controls": verify.get("required_controls"),
        "verified_controls": verify.get("verified_controls"),
        "abyss_machine_repo_root": str(abyss_root),
        "abyss_machine_package_root": package_root,
        "public_safe": {"ok": not public_safe_leaks, "leaks": public_safe_leaks},
        "registry": latest_registry,
        "pre_materialization_gate": pre_materialization_gate,
        "materialized_subject_store": materialized,
        "registry_with_subject_store": registry_with_subject_store,
        "trust_gate": trust_gate,
        "subject_store_gate": subject_store_gate,
        "adversarial_checks": adversarial,
        "steps": {
            "build_sidecars": build,
            "sign": sign,
            "verify": verify,
            "release_check": release,
        },
    }


def compact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    registry = payload.get("registry") if isinstance(payload.get("registry"), dict) else {}
    latest = registry.get("latest_by_artifact_class") if isinstance(registry.get("latest_by_artifact_class"), dict) else {}
    latest_record = latest.get(ARTIFACT_CLASS) if isinstance(latest, dict) else None
    adversarial = payload.get("adversarial_checks") if isinstance(payload.get("adversarial_checks"), dict) else {}
    checks = adversarial.get("checks") if isinstance(adversarial.get("checks"), dict) else {}
    trust_gate = payload.get("trust_gate") if isinstance(payload.get("trust_gate"), dict) else {}
    gate_payload = trust_gate.get("trust_gate") if isinstance(trust_gate.get("trust_gate"), dict) else {}
    subject_store_gate = payload.get("subject_store_gate") if isinstance(payload.get("subject_store_gate"), dict) else {}
    return {
        "ok": payload.get("ok"),
        "schema": payload.get("schema"),
        "manifest": payload.get("manifest"),
        "artifact_class": payload.get("artifact_class"),
        "required_controls": payload.get("required_controls"),
        "verified_controls": payload.get("verified_controls"),
        "bundle_dir": payload.get("bundle_dir"),
        "registry_dir": payload.get("registry_dir"),
        "subject_store_root": payload.get("subject_store_root"),
        "abyss_machine_repo_root": public_location_ref(payload.get("abyss_machine_repo_root")),
        "abyss_machine_package_root": public_location_ref(payload.get("abyss_machine_package_root")),
        "public_safe": payload.get("public_safe"),
        "registry": {
            "ok": registry.get("ok"),
            "lifecycle_state": latest_record.get("lifecycle_state") if isinstance(latest_record, dict) else None,
            "latest_record_id": latest_record.get("record_id") if isinstance(latest_record, dict) else None,
            "source_repo": latest_record.get("source_repo") if isinstance(latest_record, dict) else None,
            "trust_root_mode": latest_record.get("trust_root_mode") if isinstance(latest_record, dict) else None,
        },
        "trust_gate": {
            "ok": trust_gate.get("ok"),
            "verdict": gate_payload.get("verdict"),
        },
        "subject_store_gate": {
            "ok": subject_store_gate.get("ok"),
            "verdict": subject_store_gate.get("verdict"),
        },
        "adversarial_checks": {
            "ok": adversarial.get("ok"),
            "checks": {name: item.get("ok") for name, item in checks.items() if isinstance(item, dict)},
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--bundle-dir")
    parser.add_argument("--registry-dir")
    parser.add_argument("--subject-store-root")
    parser.add_argument("--no-clean", action="store_true", help="do not remove previous generated bundle, registry, or subject-store directories first")
    parser.add_argument("--full-json", action="store_true", help="print the full nested verifier payload")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = repo_root / manifest
    bundle_dir = Path(args.bundle_dir).resolve() if args.bundle_dir else None
    registry_dir = Path(args.registry_dir).resolve() if args.registry_dir else None
    subject_store_root = Path(args.subject_store_root).resolve() if args.subject_store_root else None
    payload = run_bundle(
        manifest,
        bundle_dir,
        registry_dir,
        subject_store_root,
        clean=not args.no_clean,
    )
    output = payload if args.full_json else compact_payload(payload)
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0 if payload.get("ok") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
