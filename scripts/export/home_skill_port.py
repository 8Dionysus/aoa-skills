"""Owner-local skill home contracts for repository and OS-profile exposure."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any, Iterable


SCHEMA_VERSION_V1 = "aoa_skill_home_port_v1"
SCHEMA_VERSION_V2 = "aoa_skill_home_port_v2"
SCHEMA_VERSION_V3 = "aoa_skill_home_port_v3"
SUPPORTED_SCHEMA_VERSIONS = {SCHEMA_VERSION_V1, SCHEMA_VERSION_V2, SCHEMA_VERSION_V3}
CONTRACT_REF = "aoa-skills:schemas/skill-home-port.schema.json"
DEFAULT_MANIFEST = Path("skills/port.manifest.json")
PROJECTION_ROOT = Path(".agents/skills")
EXPOSURE_PROFILE = "os-user-default"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OWNER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
VERSION_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?$"
)
FORBIDDEN_TREE_NAMES = {".DS_Store", "__pycache__"}


class PortContractError(ValueError):
    """A deterministic source or projection contract failure."""

    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(str(error) for error in errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class BundleSpec:
    name: str
    path: Path
    version: str
    visibility: str
    admission_ref: Path


@dataclass(frozen=True)
class ExposureSpec:
    """One normalized eligibility contour from a v2 or v3 owner manifest."""

    runtime: str
    scope: str
    profile: str | None
    mode: str
    skills: tuple[str, ...]


@dataclass(frozen=True)
class PortDefinition:
    owner_root: Path
    manifest_path: Path
    schema_version: str
    owner_repo: str
    owner_ref: Path
    bundles: tuple[BundleSpec, ...]
    projection_root: Path | None
    exposures: tuple[ExposureSpec, ...]

    @property
    def exposure_profile(self) -> str | None:
        """Return the v2 profile marker while retaining the legacy accessor."""

        if self.schema_version == SCHEMA_VERSION_V2 and len(self.exposures) == 1:
            return self.exposures[0].profile
        return None


def _inside(root: Path, relative: Path, *, label: str) -> Path:
    if relative.is_absolute() or not relative.parts:
        raise PortContractError([f"{label} must be a non-empty relative path: {relative}"])
    if ".." in relative.parts:
        raise PortContractError([f"{label} must not escape the owner root: {relative}"])
    root_resolved = root.resolve()
    lexical_candidate = root_resolved / relative
    candidate = lexical_candidate.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise PortContractError([f"{label} resolves outside the owner root: {relative}"]) from exc
    current = root_resolved
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise PortContractError(
                [
                    f"{label} path component must not be a symlink: "
                    f"{current.relative_to(root_resolved)}"
                ]
            )
    return lexical_candidate


def _relative_path(value: Any, *, label: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} must be a non-empty relative path")
        return None
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{label} must remain inside the owner root: {value!r}")
        return None
    return path


def _unknown_keys(value: dict[str, Any], allowed: set[str], *, label: str) -> list[str]:
    return [f"{label} contains unsupported field {key!r}" for key in sorted(set(value) - allowed)]


def _frontmatter_name(skill_path: Path) -> str:
    lines = skill_path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise PortContractError([f"{skill_path} is missing YAML frontmatter"])
    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise PortContractError(
            [f"{skill_path} is missing a closing frontmatter delimiter"]
        ) from exc
    names = []
    for line in lines[1:closing]:
        match = re.fullmatch(r"name:\s*(['\"]?)([a-z0-9]+(?:-[a-z0-9]+)*)\1\s*", line)
        if match:
            names.append(match.group(2))
    if len(names) != 1:
        raise PortContractError([f"{skill_path} must declare exactly one simple frontmatter name"])
    return names[0]


def _tree_snapshot(root: Path, *, label: str) -> dict[str, dict[str, Any]]:
    if root.is_symlink():
        raise PortContractError([f"{label} must not be a symlink: {root}"])
    if not root.is_dir():
        raise PortContractError([f"{label} directory is missing: {root}"])

    snapshot: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root)
        if path.is_symlink():
            errors.append(f"{label} contains a symlink: {relative.as_posix()}")
            continue
        if any(part in FORBIDDEN_TREE_NAMES for part in relative.parts) or path.suffix == ".pyc":
            errors.append(f"{label} contains transient build residue: {relative.as_posix()}")
            continue
        if path.is_dir():
            continue
        if not path.is_file():
            errors.append(f"{label} contains a non-regular entry: {relative.as_posix()}")
            continue
        payload = path.read_bytes()
        snapshot[relative.as_posix()] = {
            "sha256": hashlib.sha256(payload).hexdigest(),
            "executable": bool(path.stat().st_mode & 0o111),
            "size": len(payload),
        }
    if errors:
        raise PortContractError(errors)
    if "SKILL.md" not in snapshot:
        raise PortContractError([f"{label} is missing SKILL.md"])
    return snapshot


def _tree_digest(snapshot: dict[str, dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for path, record in sorted(snapshot.items()):
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(record["sha256"]).encode("ascii"))
        digest.update(b"\0")
        digest.update(b"1" if record["executable"] else b"0")
        digest.update(b"\0")
    return digest.hexdigest()


def tree_snapshot(root: str | Path, *, label: str) -> dict[str, dict[str, Any]]:
    """Return the canonical regular-file snapshot used by skill-home consumers."""

    return _tree_snapshot(Path(root), label=label)


def tree_digest(snapshot: dict[str, dict[str, Any]]) -> str:
    """Return the canonical digest for a skill-home tree snapshot."""

    return _tree_digest(snapshot)


def matching_exposure(
    port: PortDefinition,
    *,
    skill: str,
    runtime: str,
    scope: str,
    profile: str,
    mode: str,
) -> ExposureSpec | None:
    """Return the exact normalized exposure that makes one skill eligible."""

    for exposure in port.exposures:
        if (
            exposure.runtime == runtime
            and exposure.scope == scope
            and exposure.profile == profile
            and exposure.mode == mode
            and skill in exposure.skills
        ):
            return exposure
    return None


def load_port_definition(
    owner_root: str | Path,
    manifest_path: str | Path = DEFAULT_MANIFEST,
) -> PortDefinition:
    owner_root_path = Path(owner_root).resolve()
    if not owner_root_path.is_dir():
        raise PortContractError([f"owner root is missing: {owner_root_path}"])

    manifest_relative = Path(manifest_path)
    manifest = _inside(owner_root_path, manifest_relative, label="manifest")
    if not manifest.is_file():
        raise PortContractError([f"skill home port manifest is missing: {manifest}"])
    try:
        document = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PortContractError([f"cannot read skill home port manifest: {exc}"]) from exc
    if not isinstance(document, dict):
        raise PortContractError(["skill home port manifest must be a JSON object"])

    schema_version = document.get("schema_version")
    if schema_version == SCHEMA_VERSION_V1:
        allowed_manifest_keys = {
            "schema_version",
            "contract_ref",
            "owner_repo",
            "owner_ref",
            "bundles",
            "projection",
        }
    elif schema_version == SCHEMA_VERSION_V2:
        allowed_manifest_keys = {
            "schema_version",
            "contract_ref",
            "owner_repo",
            "owner_ref",
            "bundles",
            "exposure",
        }
    elif schema_version == SCHEMA_VERSION_V3:
        allowed_manifest_keys = {
            "schema_version",
            "contract_ref",
            "owner_repo",
            "owner_ref",
            "bundles",
            "exposures",
        }
    else:
        allowed_manifest_keys = {
            "schema_version",
            "contract_ref",
            "owner_repo",
            "owner_ref",
            "bundles",
            "projection",
            "exposure",
            "exposures",
        }
    errors = _unknown_keys(document, allowed_manifest_keys, label="manifest")
    if not isinstance(schema_version, str) or schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append(
            "schema_version must equal one of "
            f"{sorted(SUPPORTED_SCHEMA_VERSIONS)!r}"
        )
        schema_version = "invalid"
    if document.get("contract_ref") != CONTRACT_REF:
        errors.append(f"contract_ref must equal {CONTRACT_REF!r}")

    owner_repo = document.get("owner_repo")
    if not isinstance(owner_repo, str) or not OWNER_RE.fullmatch(owner_repo):
        errors.append("owner_repo must be a stable repository identifier")
        owner_repo = "invalid"
    owner_ref = _relative_path(document.get("owner_ref"), label="owner_ref", errors=errors)

    raw_bundles = document.get("bundles")
    if not isinstance(raw_bundles, list) or not raw_bundles:
        errors.append("bundles must be a non-empty array; empty skill homes are forbidden")
        raw_bundles = []

    bundles: list[BundleSpec] = []
    seen_names: set[str] = set()
    seen_paths: set[Path] = set()
    required_bundle_keys = {"name", "path", "version", "lifecycle", "visibility", "admission_ref"}
    for index, raw_bundle in enumerate(raw_bundles):
        label = f"bundles[{index}]"
        if not isinstance(raw_bundle, dict):
            errors.append(f"{label} must be an object")
            continue
        errors.extend(_unknown_keys(raw_bundle, required_bundle_keys, label=label))
        missing = sorted(required_bundle_keys - set(raw_bundle))
        errors.extend(f"{label} is missing field {key!r}" for key in missing)

        name = raw_bundle.get("name")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"{label}.name must use lowercase kebab-case")
            continue
        if name in seen_names:
            errors.append(f"duplicate bundle name: {name}")
        seen_names.add(name)

        bundle_path = _relative_path(raw_bundle.get("path"), label=f"{label}.path", errors=errors)
        expected_path = Path("skills") / name
        if bundle_path is not None and bundle_path != expected_path:
            errors.append(f"{label}.path must equal {expected_path.as_posix()!r}")
        if bundle_path in seen_paths:
            errors.append(f"duplicate bundle path: {bundle_path}")
        if bundle_path is not None:
            seen_paths.add(bundle_path)

        version = raw_bundle.get("version")
        if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
            errors.append(f"{label}.version must be a semantic version")
            version = "0.0.0"
        if raw_bundle.get("lifecycle") != "admitted":
            errors.append(f"{label}.lifecycle must equal 'admitted'")
        visibility = raw_bundle.get("visibility")
        if visibility != "advertised":
            errors.append(
                f"{label}.visibility must equal 'advertised'; "
                "non-advertised candidates do not belong in the port"
            )
            visibility = "advertised"
        admission_ref = _relative_path(
            raw_bundle.get("admission_ref"), label=f"{label}.admission_ref", errors=errors
        )
        if bundle_path is not None and admission_ref is not None:
            bundles.append(
                BundleSpec(
                    name=name,
                    path=bundle_path,
                    version=version,
                    visibility=str(visibility),
                    admission_ref=admission_ref,
                )
            )

    bundle_names = [bundle.name for bundle in bundles]
    projection_root: Path | None = None
    exposures: list[ExposureSpec] = []
    if schema_version == SCHEMA_VERSION_V1:
        projection = document.get("projection")
        projection_skills: list[str] = []
        if not isinstance(projection, dict):
            errors.append("projection must be an object")
        else:
            projection_keys = {"runtime", "scope", "root", "mode", "skills"}
            errors.extend(_unknown_keys(projection, projection_keys, label="projection"))
            for key, expected in {
                "runtime": "codex",
                "scope": "repo",
                "root": PROJECTION_ROOT.as_posix(),
                "mode": "generated-copy",
            }.items():
                if projection.get(key) != expected:
                    errors.append(f"projection.{key} must equal {expected!r}")
            raw_projection_skills = projection.get("skills")
            if not isinstance(raw_projection_skills, list) or not raw_projection_skills:
                errors.append("projection.skills must be a non-empty array")
            elif not all(
                isinstance(item, str) and NAME_RE.fullmatch(item)
                for item in raw_projection_skills
            ):
                errors.append("projection.skills entries must use lowercase kebab-case")
            else:
                projection_skills = list(raw_projection_skills)
                if len(set(projection_skills)) != len(projection_skills):
                    errors.append("projection.skills contains duplicates")
        if projection_skills and projection_skills != bundle_names:
            errors.append(
                "projection.skills must exactly match bundles order; "
                "partial home projection is forbidden"
            )
        projection_root = PROJECTION_ROOT
        if projection_skills:
            exposures.append(
                ExposureSpec(
                    runtime="codex",
                    scope="repo",
                    profile=None,
                    mode="generated-copy",
                    skills=tuple(projection_skills),
                )
            )
    elif schema_version == SCHEMA_VERSION_V2:
        exposure = document.get("exposure")
        exposure_skills: list[str] = []
        if not isinstance(exposure, dict):
            errors.append("exposure must be an object")
        else:
            expected_exposure = {
                "runtime": "codex",
                "scope": "user",
                "profile": EXPOSURE_PROFILE,
                "mode": "profile-selected",
            }
            errors.extend(
                _unknown_keys(
                    exposure,
                    {*expected_exposure, "skills"},
                    label="exposure",
                )
            )
            for key, expected in expected_exposure.items():
                if exposure.get(key) != expected:
                    errors.append(f"exposure.{key} must equal {expected!r}")
            raw_exposure_skills = exposure.get("skills")
            if not isinstance(raw_exposure_skills, list) or not raw_exposure_skills:
                errors.append("exposure.skills must be a non-empty array")
            elif not all(
                isinstance(item, str) and NAME_RE.fullmatch(item)
                for item in raw_exposure_skills
            ):
                errors.append("exposure.skills entries must use lowercase kebab-case")
            else:
                exposure_skills = list(raw_exposure_skills)
                if len(set(exposure_skills)) != len(exposure_skills):
                    errors.append("exposure.skills contains duplicates")
        if exposure_skills and exposure_skills != bundle_names:
            errors.append("exposure.skills must exactly match bundles order")
        if exposure_skills:
            exposures.append(
                ExposureSpec(
                    runtime="codex",
                    scope="user",
                    profile=EXPOSURE_PROFILE,
                    mode="profile-selected",
                    skills=tuple(exposure_skills),
                )
            )
    elif schema_version == SCHEMA_VERSION_V3:
        raw_exposures = document.get("exposures")
        if not isinstance(raw_exposures, list):
            errors.append("exposures must be an array")
            raw_exposures = []

        seen_targets: set[tuple[str, str, str]] = set()
        exposure_keys = {"runtime", "scope", "profile", "mode", "skills"}
        for index, raw_exposure in enumerate(raw_exposures):
            label = f"exposures[{index}]"
            if not isinstance(raw_exposure, dict):
                errors.append(f"{label} must be an object")
                continue
            errors.extend(_unknown_keys(raw_exposure, exposure_keys, label=label))
            missing = sorted(exposure_keys - set(raw_exposure))
            errors.extend(f"{label} is missing field {key!r}" for key in missing)

            identifiers: dict[str, str] = {}
            for key in ("runtime", "scope", "profile"):
                value = raw_exposure.get(key)
                if not isinstance(value, str) or not NAME_RE.fullmatch(value):
                    errors.append(
                        f"{label}.{key} must use lowercase kebab-case safe identifier"
                    )
                else:
                    identifiers[key] = value
            if raw_exposure.get("mode") != "profile-eligible":
                errors.append(f"{label}.mode must equal 'profile-eligible'")

            raw_exposure_skills = raw_exposure.get("skills")
            exposure_skills: list[str] = []
            if not isinstance(raw_exposure_skills, list) or not raw_exposure_skills:
                errors.append(f"{label}.skills must be a non-empty array")
            elif not all(
                isinstance(item, str) and NAME_RE.fullmatch(item)
                for item in raw_exposure_skills
            ):
                errors.append(
                    f"{label}.skills entries must use lowercase kebab-case"
                )
            else:
                exposure_skills = list(raw_exposure_skills)
                if len(set(exposure_skills)) != len(exposure_skills):
                    errors.append(f"{label}.skills contains duplicates")
                unknown = sorted(set(exposure_skills) - set(bundle_names))
                if unknown:
                    errors.append(
                        f"{label}.skills contains unknown bundles: {', '.join(unknown)}"
                    )

            if len(identifiers) == 3:
                target = tuple(identifiers[key] for key in ("runtime", "scope", "profile"))
                if target in seen_targets:
                    errors.append(
                        f"duplicate exposure target: runtime={target[0]!r}, "
                        f"scope={target[1]!r}, profile={target[2]!r}"
                    )
                seen_targets.add(target)
                if (
                    raw_exposure.get("mode") == "profile-eligible"
                    and exposure_skills
                    and len(set(exposure_skills)) == len(exposure_skills)
                ):
                    exposures.append(
                        ExposureSpec(
                            runtime=identifiers["runtime"],
                            scope=identifiers["scope"],
                            profile=identifiers["profile"],
                            mode="profile-eligible",
                            skills=tuple(exposure_skills),
                        )
                    )

    if errors:
        raise PortContractError(errors)

    assert owner_ref is not None
    owner_ref_path = _inside(owner_root_path, owner_ref, label="owner_ref")
    if not owner_ref_path.is_file():
        errors.append(f"owner_ref does not resolve to a file: {owner_ref.as_posix()}")

    for bundle in bundles:
        source_dir = _inside(owner_root_path, bundle.path, label=f"bundle {bundle.name} path")
        admission_path = _inside(
            owner_root_path, bundle.admission_ref, label=f"bundle {bundle.name} admission_ref"
        )
        if not admission_path.is_file():
            errors.append(
                f"bundle {bundle.name} admission_ref does not resolve to a file: "
                f"{bundle.admission_ref.as_posix()}"
            )
        try:
            _tree_snapshot(source_dir, label=f"bundle {bundle.name} source")
            skill_name = _frontmatter_name(source_dir / "SKILL.md")
            if skill_name != bundle.name:
                errors.append(
                    f"bundle {bundle.name} frontmatter name differs from manifest: {skill_name!r}"
                )
        except PortContractError as exc:
            errors.extend(exc.errors)

    if errors:
        raise PortContractError(errors)

    projection_root_path = (
        _inside(owner_root_path, projection_root, label="projection.root")
        if projection_root is not None
        else None
    )
    return PortDefinition(
        owner_root=owner_root_path,
        manifest_path=manifest,
        schema_version=str(schema_version),
        owner_repo=str(owner_repo),
        owner_ref=owner_ref,
        bundles=tuple(bundles),
        projection_root=projection_root_path,
        exposures=tuple(exposures),
    )


def projection_plan(port: PortDefinition) -> dict[str, Any]:
    if port.schema_version != SCHEMA_VERSION_V1 or port.projection_root is None:
        raise PortContractError(
            [
                "repository projection planning applies only to deprecated v1 ports; "
                "v2/v3 owner homes are installed through the OS user profile"
            ]
        )
    projection_root = port.projection_root
    if projection_root.exists() and (projection_root.is_symlink() or not projection_root.is_dir()):
        raise PortContractError([f"projection root must be a real directory: {projection_root}"])

    expected_names = {bundle.name for bundle in port.bundles}
    actual_names = (
        {child.name for child in projection_root.iterdir()} if projection_root.is_dir() else set()
    )
    unexpected = sorted(actual_names - expected_names)
    bundle_records: list[dict[str, Any]] = []
    for bundle in port.bundles:
        source_dir = _inside(port.owner_root, bundle.path, label=f"bundle {bundle.name} path")
        source_snapshot = _tree_snapshot(source_dir, label=f"bundle {bundle.name} source")
        target_dir = projection_root / bundle.name
        if not target_dir.exists():
            status = "missing"
            target_snapshot: dict[str, dict[str, Any]] = {}
        else:
            target_snapshot = _tree_snapshot(target_dir, label=f"bundle {bundle.name} projection")
            status = "current" if target_snapshot == source_snapshot else "drift"
        bundle_records.append(
            {
                "name": bundle.name,
                "source": bundle.path.as_posix(),
                "target": (PROJECTION_ROOT / bundle.name).as_posix(),
                "status": status,
                "source_digest": _tree_digest(source_snapshot),
                "target_digest": _tree_digest(target_snapshot) if target_snapshot else None,
                "file_count": len(source_snapshot),
            }
        )

    clean = not unexpected and all(record["status"] == "current" for record in bundle_records)
    return {
        "schema_version": "aoa_skill_home_projection_plan_v1",
        "owner_repo": port.owner_repo,
        "manifest": port.manifest_path.relative_to(port.owner_root).as_posix(),
        "projection_root": PROJECTION_ROOT.as_posix(),
        "bundles": bundle_records,
        "unexpected_entries": unexpected,
        "clean": clean,
        "claim_limit": "structural owner and byte parity only; no skill quality or outcome claim",
    }


def source_plan(port: PortDefinition) -> dict[str, Any]:
    if port.schema_version not in {SCHEMA_VERSION_V2, SCHEMA_VERSION_V3}:
        raise PortContractError(
            ["OS-profile source planning applies only to v2/v3 owner-home ports"]
        )

    duplicate_repo_projections: list[str] = []
    bundle_records: list[dict[str, Any]] = []
    codex_user_exposed = {
        skill
        for exposure in port.exposures
        if exposure.runtime == "codex" and exposure.scope == "user"
        for skill in exposure.skills
    }
    for bundle in port.bundles:
        source_dir = _inside(
            port.owner_root,
            bundle.path,
            label=f"bundle {bundle.name} path",
        )
        source_snapshot = _tree_snapshot(
            source_dir,
            label=f"bundle {bundle.name} source",
        )
        repo_projection = port.owner_root / PROJECTION_ROOT / bundle.name
        if (
            bundle.name in codex_user_exposed
            and (repo_projection.exists() or repo_projection.is_symlink())
        ):
            duplicate_repo_projections.append(
                repo_projection.relative_to(port.owner_root).as_posix()
            )
        bundle_record = {
            "name": bundle.name,
            "version": bundle.version,
            "source": bundle.path.as_posix(),
            "source_digest": _tree_digest(source_snapshot),
            "file_count": len(source_snapshot),
        }
        if port.schema_version == SCHEMA_VERSION_V2:
            bundle_record["exposure_profile"] = port.exposure_profile
        else:
            bundle_record["exposures"] = [
                {
                    "runtime": exposure.runtime,
                    "scope": exposure.scope,
                    "profile": exposure.profile,
                    "mode": exposure.mode,
                }
                for exposure in port.exposures
                if bundle.name in exposure.skills
            ]
        bundle_records.append(bundle_record)

    if port.schema_version == SCHEMA_VERSION_V2:
        return {
            "schema_version": "aoa_skill_home_source_plan_v2",
            "owner_repo": port.owner_repo,
            "manifest": port.manifest_path.relative_to(port.owner_root).as_posix(),
            "bundles": bundle_records,
            "duplicate_repo_projections": duplicate_repo_projections,
            "clean": not duplicate_repo_projections,
            "claim_limit": (
                "owner source identity, package shape, profile eligibility, and "
                "same-name repo-projection absence only; no current profile membership, "
                "live user install, routing, or outcome claim"
            ),
        }

    return {
        "schema_version": "aoa_skill_home_source_plan_v3",
        "owner_repo": port.owner_repo,
        "manifest": port.manifest_path.relative_to(port.owner_root).as_posix(),
        "exposures": [
            {
                "runtime": exposure.runtime,
                "scope": exposure.scope,
                "profile": exposure.profile,
                "mode": exposure.mode,
                "skills": list(exposure.skills),
            }
            for exposure in port.exposures
        ],
        "bundles": bundle_records,
        "duplicate_repo_projections": duplicate_repo_projections,
        "clean": not duplicate_repo_projections,
        "claim_limit": (
            "owner source identity, package shape, profile eligibility, and "
            "same-name repo-projection absence only; no current profile membership, "
            "live user install, routing, or outcome claim"
        ),
    }


def validation_plan(port: PortDefinition) -> dict[str, Any]:
    if port.schema_version == SCHEMA_VERSION_V1:
        return projection_plan(port)
    return source_plan(port)


def apply_projection(port: PortDefinition, *, prune: bool = False) -> dict[str, Any]:
    before = projection_plan(port)
    if before["unexpected_entries"] and not prune:
        raise PortContractError(
            [
                "projection contains undeclared entries; rerun with explicit --prune after review: "
                + ", ".join(before["unexpected_entries"])
            ]
        )

    projection_root = port.projection_root
    projection_root.mkdir(parents=True, exist_ok=True)
    temporary_paths: list[Path] = []
    staged: list[tuple[BundleSpec, Path]] = []
    try:
        for bundle in port.bundles:
            source_dir = _inside(port.owner_root, bundle.path, label=f"bundle {bundle.name} path")
            temporary_dir = Path(
                tempfile.mkdtemp(prefix=f".{bundle.name}.tmp-", dir=projection_root)
            )
            temporary_paths.append(temporary_dir)
            shutil.copytree(
                source_dir,
                temporary_dir,
                dirs_exist_ok=True,
                copy_function=shutil.copy2,
            )
            source_snapshot = _tree_snapshot(source_dir, label=f"bundle {bundle.name} source")
            staged_snapshot = _tree_snapshot(
                temporary_dir, label=f"bundle {bundle.name} staged projection"
            )
            if staged_snapshot != source_snapshot:
                raise PortContractError(
                    [f"bundle {bundle.name} staged projection differs from source"]
                )
            staged.append((bundle, temporary_dir))

        if prune:
            for name in before["unexpected_entries"]:
                path = projection_root / name
                if path.is_symlink() or path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)
                else:
                    raise PortContractError(
                        [f"cannot prune non-regular projection entry: {path}"]
                    )

        for bundle, temporary_dir in staged:
            target_dir = projection_root / bundle.name
            if target_dir.is_symlink() or target_dir.is_file():
                target_dir.unlink()
            elif target_dir.is_dir():
                shutil.rmtree(target_dir)
            os.replace(temporary_dir, target_dir)
            temporary_paths.remove(temporary_dir)
    finally:
        for temporary_path in temporary_paths:
            if temporary_path.exists():
                shutil.rmtree(temporary_path)

    after = projection_plan(port)
    if not after["clean"]:
        raise PortContractError(["projection remained dirty after execution"])
    return after


def format_plan(plan: dict[str, Any]) -> str:
    lines = [f"owner: {plan['owner_repo']}", f"manifest: {plan['manifest']}"]
    if plan["schema_version"] == "aoa_skill_home_projection_plan_v1":
        lines.append(f"projection: {plan['projection_root']}")
        for bundle in plan["bundles"]:
            lines.append(
                f"- {bundle['name']}: {bundle['status']} "
                f"files={bundle['file_count']} source={bundle['source']} "
                f"target={bundle['target']}"
            )
        if plan["unexpected_entries"]:
            lines.append("unexpected: " + ", ".join(plan["unexpected_entries"]))
    elif plan["schema_version"] == "aoa_skill_home_source_plan_v2":
        for bundle in plan["bundles"]:
            lines.append(
                f"- {bundle['name']}: source={bundle['source']} "
                f"version={bundle['version']} files={bundle['file_count']} "
                f"digest={bundle['source_digest']} "
                f"eligible-profile={bundle['exposure_profile']}"
            )
        if plan["duplicate_repo_projections"]:
            lines.append(
                "duplicate repo projections: "
                + ", ".join(plan["duplicate_repo_projections"])
            )
    else:
        for exposure in plan["exposures"]:
            lines.append(
                f"exposure: runtime={exposure['runtime']} "
                f"scope={exposure['scope']} profile={exposure['profile']} "
                f"mode={exposure['mode']} skills={','.join(exposure['skills'])}"
            )
        for bundle in plan["bundles"]:
            eligible = bundle["exposures"]
            lines.append(
                f"- {bundle['name']}: source={bundle['source']} "
                f"version={bundle['version']} files={bundle['file_count']} "
                f"digest={bundle['source_digest']} "
                f"eligible-exposures={len(eligible)}"
            )
        if plan["duplicate_repo_projections"]:
            lines.append(
                "duplicate repo projections: "
                + ", ".join(plan["duplicate_repo_projections"])
            )
    lines.append(f"clean: {'yes' if plan['clean'] else 'no'}")
    lines.append(f"claim limit: {plan['claim_limit']}")
    return "\n".join(lines)
