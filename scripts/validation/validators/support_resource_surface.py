"""Support-resource generated/export validators for aoa-skills."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

from skill_model import skill_layout


PROFILE = "codex-facing-wave-8-support-bundles"
TARGETED_SKILLS = (
    "aoa-safe-infra-change",
    "aoa-local-stack-bringup",
    "aoa-dry-run-first",
)
STANDARD_DIRS = ("scripts", "references", "assets")
LEGACY_DIRS = ("agents", "checks", "examples")
TEXT_FILE_SUFFIXES = {".json", ".jsonl", ".md", ".py", ".svg", ".txt", ".yaml", ".yml"}
REQUIRED_GENERATED_FILES = (
    "generated/deterministic_resource_manifest.json",
    "generated/support_resource_index.json",
    "generated/structured_output_schema_index.json",
    "generated/support_resource_bridge_map.json",
    "generated/deterministic_resource_eval_cases.jsonl",
    "generated/expected_existing_aoa_support_dirs.json",
)


def normalized_file_bytes(path: Path) -> bytes:
    if path.suffix.lower() in TEXT_FILE_SUFFIXES:
        normalized_text = (
            path.read_text(encoding="utf-8")
            .replace("\r\n", "\n")
            .replace("\r", "\n")
        )
        return normalized_text.encode("utf-8")
    return path.read_bytes()


def sha256(path: Path) -> str:
    return hashlib.sha256(normalized_file_bytes(path)).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def collect_rel_files(base: Path) -> list[str]:
    return [
        path.relative_to(base).as_posix()
        for path in sorted(p for p in base.rglob("*") if p.is_file())
    ]


def collect_file_records(base: Path) -> list[dict[str, str]]:
    return [
        {
            "path": path.relative_to(base).as_posix(),
            "sha256": sha256(path),
            "bytes": str(len(normalized_file_bytes(path))),
        }
        for path in sorted(p for p in base.rglob("*") if p.is_file())
    ]


def validate_required_generated_files(repo_root: Path, errors: list[str]) -> bool:
    for rel_path in REQUIRED_GENERATED_FILES:
        if not (repo_root / rel_path).exists():
            errors.append(f"Missing generated support file: {rel_path}")
    return not errors


def load_support_documents(repo_root: Path) -> dict[str, Any]:
    return {
        "manifest": load_json(repo_root / "generated" / "deterministic_resource_manifest.json"),
        "support_index": load_json(repo_root / "generated" / "support_resource_index.json"),
        "schema_index": load_json(repo_root / "generated" / "structured_output_schema_index.json"),
        "bridge_map": load_json(repo_root / "generated" / "support_resource_bridge_map.json"),
        "eval_cases": load_jsonl(repo_root / "generated" / "deterministic_resource_eval_cases.jsonl"),
        "expected_existing": load_json(repo_root / "generated" / "expected_existing_aoa_support_dirs.json"),
    }


def validate_profiles(docs: dict[str, Any], errors: list[str]) -> None:
    for label, doc in {
        "generated/deterministic_resource_manifest.json": docs["manifest"],
        "generated/support_resource_index.json": docs["support_index"],
        "generated/structured_output_schema_index.json": docs["schema_index"],
        "generated/support_resource_bridge_map.json": docs["bridge_map"],
        "generated/expected_existing_aoa_support_dirs.json": docs["expected_existing"],
    }.items():
        if doc.get("profile") != PROFILE:
            errors.append(f"{label}: profile must be {PROFILE!r}")


def build_indexes(docs: dict[str, Any]) -> dict[str, Any]:
    return {
        "manifest_by_name": {
            entry["name"]: entry for entry in docs["manifest"].get("skills", [])
        },
        "support_index_by_name": {
            entry["name"]: entry for entry in docs["support_index"].get("skills", [])
        },
        "bridge_by_name": docs["bridge_map"].get("skills", {}),
        "expected_by_name": docs["expected_existing"].get("skills", {}),
        "eval_case_names": {entry.get("skill_name") for entry in docs["eval_cases"]},
    }


def validate_skill_sets(indexes: dict[str, Any], errors: list[str]) -> None:
    expected_names = set(TARGETED_SKILLS)
    if set(indexes["manifest_by_name"]) != expected_names:
        errors.append("deterministic_resource_manifest.json skill set mismatch")
    if set(indexes["support_index_by_name"]) != expected_names:
        errors.append("support_resource_index.json skill set mismatch")
    if set(indexes["bridge_by_name"]) != expected_names:
        errors.append("support_resource_bridge_map.json skill set mismatch")
    if set(indexes["expected_by_name"]) != expected_names:
        errors.append("expected_existing_aoa_support_dirs.json skill set mismatch")
    if indexes["eval_case_names"] != expected_names:
        errors.append("deterministic_resource_eval_cases.jsonl skill set mismatch")


def validate_standard_dir(
    *,
    skill: str,
    dirname: str,
    path: Path,
    manifest_entry: dict[str, Any] | None,
    index_entry: dict[str, Any] | None,
    bridge_entry: dict[str, Any],
    errors: list[str],
) -> None:
    if not path.exists():
        errors.append(f"{skill}: missing {dirname}/")
        return
    files = sorted(p for p in path.rglob("*") if p.is_file())
    if not files:
        errors.append(f"{skill}: {dirname}/ is empty")
        return
    actual_records = collect_file_records(path)
    rel_paths = [item["path"] for item in actual_records]
    if manifest_entry is None:
        return
    manifest_records = manifest_entry["standard_dirs"].get(dirname, [])
    manifest_paths = [item["path"] for item in manifest_records]
    if manifest_paths != rel_paths:
        errors.append(f"{skill}: deterministic_resource_manifest {dirname}/ mismatch")
    if manifest_records != actual_records:
        errors.append(f"{skill}: deterministic_resource_manifest {dirname}/ digest mismatch")
    if bridge_entry.get("standard_support_dirs", {}).get(dirname) != rel_paths:
        errors.append(f"{skill}: support_resource_bridge_map {dirname}/ mismatch")
    if index_entry is not None and index_entry.get("standard_dir_counts", {}).get(dirname) != len(rel_paths):
        errors.append(f"{skill}: support_resource_index {dirname} count mismatch")


def validate_legacy_dir(
    *,
    skill: str,
    dirname: str,
    path: Path,
    manifest_entry: dict[str, Any] | None,
    index_entry: dict[str, Any] | None,
    bridge_entry: dict[str, Any],
    expected_entry: dict[str, Any],
    errors: list[str],
) -> None:
    expected_paths = expected_entry.get(dirname, [])
    if not path.exists():
        errors.append(f"{skill}: missing legacy {dirname}/")
        return
    actual_records = collect_file_records(path)
    rel_paths = [item["path"] for item in actual_records]
    if rel_paths != expected_paths:
        errors.append(f"{skill}: expected_existing_aoa_support_dirs {dirname}/ mismatch")
    if manifest_entry is not None:
        manifest_records = manifest_entry["legacy_dirs"].get(dirname, [])
        manifest_paths = [item["path"] for item in manifest_records]
        if manifest_paths != rel_paths:
            errors.append(f"{skill}: deterministic_resource_manifest legacy {dirname}/ mismatch")
        if manifest_records != actual_records:
            errors.append(f"{skill}: deterministic_resource_manifest legacy {dirname}/ digest mismatch")
    if bridge_entry.get("legacy_support_dirs", {}).get(dirname) != rel_paths:
        errors.append(f"{skill}: support_resource_bridge_map legacy {dirname}/ mismatch")
    if index_entry is not None and index_entry.get("legacy_dir_counts", {}).get(dirname) != len(rel_paths):
        errors.append(f"{skill}: support_resource_index legacy {dirname} count mismatch")


def validate_support_file_posture(
    *,
    skill: str,
    skill_root: Path,
    errors: list[str],
    warnings: list[str],
    schemas: list[str],
) -> None:
    for script in sorted((skill_root / "scripts").glob("*.py")):
        text = script.read_text(encoding="utf-8")
        first_line = text.splitlines()[0] if text else ""
        if not first_line.startswith("#!"):
            warnings.append(f"{skill}: script without shebang: {script.name}")
    for reference in sorted((skill_root / "references").glob("*.md")):
        lines = reference.read_text(encoding="utf-8").splitlines()
        if not lines or not lines[0].startswith("# "):
            warnings.append(
                f"{skill}: reference should start with a top-level heading: {reference.name}"
            )
    for schema in sorted((skill_root / "assets").glob("*.schema.json")):
        payload = load_json(schema)
        schemas.append(schema.name)
        if payload.get("type") != "object":
            errors.append(f"{skill}: schema {schema.name} must have top-level type=object")
        if "title" not in payload:
            errors.append(f"{skill}: schema {schema.name} missing title")
        if "required" not in payload:
            warnings.append(f"{skill}: schema {schema.name} has no required list")


def validate_portable_mirror(
    *,
    skill: str,
    skill_root: Path,
    portable_root: Path,
    errors: list[str],
) -> None:
    for dirname in STANDARD_DIRS:
        canonical = skill_root / dirname
        portable = portable_root / dirname
        if not portable.exists():
            errors.append(f"{skill}: missing portable mirror {portable}")
            continue
        for file_path in sorted(p for p in canonical.rglob("*") if p.is_file()):
            rel = file_path.relative_to(canonical)
            portable_file = portable / rel
            if not portable_file.exists():
                errors.append(f"{skill}: portable mirror missing {dirname}/{rel.as_posix()}")
            elif sha256(file_path) != sha256(portable_file):
                errors.append(f"{skill}: portable mirror drift in {dirname}/{rel.as_posix()}")


def validate_skill_resource_surface(
    *,
    repo_root: Path,
    skill: str,
    indexes: dict[str, Any],
    check_portable: bool,
    errors: list[str],
    warnings: list[str],
    schemas: list[str],
) -> None:
    skill_root = skill_layout.skill_dir_path(repo_root, skill)
    portable_root = repo_root / ".agents" / "skills" / skill
    manifest_entry = indexes["manifest_by_name"].get(skill)
    index_entry = indexes["support_index_by_name"].get(skill)
    bridge_entry = indexes["bridge_by_name"].get(skill, {})
    expected_entry = indexes["expected_by_name"].get(skill, {})
    if not skill_root.exists():
        errors.append(f"Missing skill overlay root: {skill_root}")
        return
    for dirname in STANDARD_DIRS:
        validate_standard_dir(
            skill=skill,
            dirname=dirname,
            path=skill_root / dirname,
            manifest_entry=manifest_entry,
            index_entry=index_entry,
            bridge_entry=bridge_entry,
            errors=errors,
        )
    for dirname in LEGACY_DIRS:
        validate_legacy_dir(
            skill=skill,
            dirname=dirname,
            path=skill_root / dirname,
            manifest_entry=manifest_entry,
            index_entry=index_entry,
            bridge_entry=bridge_entry,
            expected_entry=expected_entry,
            errors=errors,
        )
    validate_support_file_posture(
        skill=skill,
        skill_root=skill_root,
        errors=errors,
        warnings=warnings,
        schemas=schemas,
    )
    if check_portable:
        validate_portable_mirror(
            skill=skill,
            skill_root=skill_root,
            portable_root=portable_root,
            errors=errors,
        )


def validate_schema_index(docs: dict[str, Any], errors: list[str]) -> None:
    schema_index_by_skill: dict[str, list[dict[str, Any]]] = {}
    for schema_entry in docs["schema_index"].get("schemas", []):
        schema_index_by_skill.setdefault(schema_entry["skill"], []).append(schema_entry)
    for skill in TARGETED_SKILLS:
        if len(schema_index_by_skill.get(skill, [])) != 1:
            errors.append(
                f"{skill}: structured_output_schema_index.json should have exactly one schema entry"
            )


def validate(repo_root: Path, check_portable: bool) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    schemas: list[str] = []
    if not validate_required_generated_files(repo_root, errors):
        return {
            "status": "fail",
            "errors": errors,
            "warnings": warnings,
            "validated_schema_count": 0,
        }
    docs = load_support_documents(repo_root)
    indexes = build_indexes(docs)
    validate_profiles(docs, errors)
    validate_skill_sets(indexes, errors)
    for skill in TARGETED_SKILLS:
        validate_skill_resource_surface(
            repo_root=repo_root,
            skill=skill,
            indexes=indexes,
            check_portable=check_portable,
            errors=errors,
            warnings=warnings,
            schemas=schemas,
        )
    validate_schema_index(docs, errors)
    return {
        "status": "ok" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "validated_schema_count": len(schemas),
    }


def lint(repo_root: Path) -> dict[str, object]:
    errors: list[str] = []
    notes: list[str] = []
    for skill in TARGETED_SKILLS:
        skill_dir = skill_layout.skill_dir_path(repo_root, skill)
        assets_dir = skill_dir / "assets"
        scripts_dir = skill_dir / "scripts"
        references_dir = skill_dir / "references"
        template_files = sorted(assets_dir.glob("*.template.json"))
        schema_files = sorted(assets_dir.glob("*.schema.json"))
        if len(template_files) != 1:
            errors.append(f"{skill}: expected exactly one *.template.json file")
        if len(schema_files) != 1:
            errors.append(f"{skill}: expected exactly one *.schema.json file")
        if len(list(scripts_dir.glob("*.py"))) < 2:
            notes.append(f"{skill}: fewer than two python helpers")
        if len(list(references_dir.glob("*.md"))) < 2:
            notes.append(f"{skill}: fewer than two markdown references")
    return {"status": "ok" if not errors else "fail", "errors": errors, "notes": notes}


def parse_validate_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate deterministic support-resource bundles.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--check-portable", action="store_true", help="Compare canonical files vs .agents mirrors.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON.")
    return parser.parse_args(argv)


def main_validate(argv: Sequence[str] | None = None) -> int:
    args = parse_validate_args(argv)
    result = validate(Path(args.repo_root).resolve(), check_portable=args.check_portable)
    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))
    return 0 if result["status"] == "ok" else 2


def parse_lint_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint support-resource naming and file-count conventions.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON.")
    return parser.parse_args(argv)


def main_lint(argv: Sequence[str] | None = None) -> int:
    args = parse_lint_args(argv)
    result = lint(Path(args.repo_root).resolve())
    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))
    return 0 if result["status"] == "ok" else 2
