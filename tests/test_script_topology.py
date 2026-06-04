from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TOPOLOGY_PATH = REPO_ROOT / "docs" / "validation" / "SCRIPT_TOPOLOGY.md"
INVENTORY_PATH = REPO_ROOT / "docs" / "validation" / "script_inventory.json"
INGRESS_RE = re.compile(r'expose\("([^"]+)", globals\(\)\)')


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def root_ingress_paths(inventory: dict) -> set[str]:
    paths: set[str] = set()
    for organ in inventory["organ_dirs"]:
        paths.update(organ["root_ingress"])
    return paths


def root_ingress_allowlist_paths(inventory: dict) -> set[str]:
    paths: set[str] = set()
    for group in inventory["root_ingress_allowlist"]:
        paths.update(group["paths"])
    return paths


def retired_root_ingress_paths(inventory: dict) -> set[str]:
    return {entry["path"] for entry in inventory["retired_root_ingress"]}


def ingress_target(path: Path) -> str:
    match = INGRESS_RE.search(path.read_text(encoding="utf-8"))
    assert match, f"{path.relative_to(REPO_ROOT).as_posix()} does not expose a target"
    return match.group(1)


def target_module_path(target: str) -> Path:
    return SCRIPTS_DIR / Path(*target.split(".")).with_suffix(".py")


def test_script_topology_doc_names_root_ingress_and_organs() -> None:
    text = TOPOLOGY_PATH.read_text(encoding="utf-8")
    compact_text = " ".join(text.split())

    for required in (
        "root script paths are compatibility ingress only",
        "Root wrappers are for command/front-door paths",
        "`scripts/validators/__init__.py` is a compatibility package",
        "`scripts/validation/validators/`",
        "Do not put new implementation or library wrappers in root `scripts/`",
    ):
        assert required in compact_text

    for organ in load_inventory()["organ_dirs"]:
        assert f"`{Path(organ['path']).name}/`" in text


def test_root_python_files_are_only_registered_ingress() -> None:
    inventory = load_inventory()
    expected_root = root_ingress_allowlist_paths(inventory) | {"scripts/_ingress.py"}
    actual_root = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in SCRIPTS_DIR.glob("*.py")
    }

    assert actual_root == expected_root
    assert root_ingress_paths(inventory) == root_ingress_allowlist_paths(inventory)

    for rel_path in sorted(root_ingress_paths(inventory)):
        path = REPO_ROOT / rel_path
        text = path.read_text(encoding="utf-8")
        assert "from _ingress import expose" in text
        assert len(text.splitlines()) <= 4
        target = ingress_target(path)
        assert target_module_path(target).is_file(), target


def test_root_ingress_allowlist_has_evidence_and_retirement_route() -> None:
    inventory = load_inventory()
    seen: set[str] = set()

    for group in inventory["root_ingress_allowlist"]:
        assert group["decision"] in {"keep", "migrate-first"}
        assert group["paths"], group
        assert group["owner_surface"], group
        assert group["reason"], group
        assert group["downstream_evidence"], group
        assert group["retirement_condition"], group

        owner_surface = REPO_ROOT / group["owner_surface"]
        assert owner_surface.exists(), group["owner_surface"]
        for evidence in group["downstream_evidence"]:
            if "*" in evidence:
                assert list(REPO_ROOT.glob(evidence)), evidence
            else:
                assert (REPO_ROOT / evidence).exists(), evidence

        for rel_path in group["paths"]:
            assert rel_path not in seen, rel_path
            seen.add(rel_path)
            path = REPO_ROOT / rel_path
            assert path.is_file(), rel_path
            assert target_module_path(ingress_target(path)).is_file(), rel_path


def test_retired_root_ingress_is_absent_but_target_remains() -> None:
    inventory = load_inventory()
    active = root_ingress_paths(inventory)

    for entry in inventory["retired_root_ingress"]:
        rel_path = entry["path"]
        assert rel_path not in active, rel_path
        assert not (REPO_ROOT / rel_path).exists(), rel_path
        assert (REPO_ROOT / entry["target"]).is_file(), entry
        assert entry["reason"], entry
        assert entry["retired_by"], entry


def test_inventory_organ_dirs_cover_all_implementation_scripts() -> None:
    expected_organs = {organ["path"] for organ in load_inventory()["organ_dirs"]}
    actual_organs: set[str] = set()
    for script_path in sorted(SCRIPTS_DIR.rglob("*.py")):
        rel_parts = script_path.relative_to(SCRIPTS_DIR).parts
        if len(rel_parts) < 2:
            continue
        organ = rel_parts[0]
        if organ == "validators":
            continue
        actual_organs.add(f"scripts/{organ}")

    assert actual_organs == expected_organs


def test_root_command_ingress_has_safe_help() -> None:
    for rel_path in sorted(root_ingress_paths(load_inventory())):
        result = subprocess.run(
            (sys.executable, rel_path, "--help"),
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        combined_output = f"{result.stdout}\n{result.stderr}"
        assert result.returncode == 0, f"{rel_path} --help failed:\n{combined_output}"
        assert "usage:" in combined_output or "Usage:" in combined_output, rel_path
        assert "--help" in combined_output, rel_path


def test_inventory_organ_dirs_match_ingress_targets() -> None:
    inventory = load_inventory()
    seen: set[str] = set()

    for organ in inventory["organ_dirs"]:
        organ_path = REPO_ROOT / organ["path"]
        assert organ_path.is_dir(), organ["path"]
        assert (organ_path / "__init__.py").is_file(), organ["path"]

        module_prefix = Path(organ["path"]).name
        for rel_path in organ["root_ingress"]:
            assert rel_path not in seen, rel_path
            seen.add(rel_path)
            target = ingress_target(REPO_ROOT / rel_path)
            assert target.startswith(f"{module_prefix}."), (rel_path, target)


def test_legacy_validators_package_is_alias_only() -> None:
    files = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in (SCRIPTS_DIR / "validators").glob("*")
        if path.is_file()
    }
    assert files == {"scripts/validators/__init__.py"}

    text = (SCRIPTS_DIR / "validators" / "__init__.py").read_text(encoding="utf-8")
    assert "validation.validators" in text


def test_local_adapter_manifest_builder_is_folded_into_export_builder() -> None:
    root_ingress = root_ingress_paths(load_inventory())
    assert "scripts/build_local_adapter_manifest.py" not in root_ingress
    assert not (SCRIPTS_DIR / "build_local_adapter_manifest.py").exists()
    assert not (SCRIPTS_DIR / "adapters" / "build_local_adapter_manifest.py").exists()

    export_builder = (SCRIPTS_DIR / "export" / "build_agent_skills.py").read_text(encoding="utf-8")
    adapter_phase = (SCRIPTS_DIR / "export" / "local_adapter_manifest.py").read_text(
        encoding="utf-8"
    )
    assert "def build_local_adapter_manifests(" not in export_builder
    assert "local_adapter_manifest.build_local_adapter_manifests(" in export_builder
    assert "def build_local_adapter_manifests(" in adapter_phase
    assert '"generated/local_adapter_manifest.min.json"' in adapter_phase


def test_project_surface_builder_is_phase_split() -> None:
    export_builder = (SCRIPTS_DIR / "export" / "build_agent_skills.py").read_text(encoding="utf-8")
    project_phase = (SCRIPTS_DIR / "export" / "project_surface.py").read_text(encoding="utf-8")

    assert "project_surface.build_project_core_kernel_doc(" in export_builder
    assert "project_surface.build_project_core_kernel_governance_doc(" in export_builder
    assert "project_surface.build_project_core_outer_ring_readiness_doc(" in export_builder
    assert "project_surface.build_project_risk_guard_ring_governance_doc(" in export_builder
    assert '"source_config": "config/project_core_skill_kernel.json"' not in export_builder
    assert '"source_config": "config/project_core_skill_kernel.json"' in project_phase
    assert '"generated/project_core_kernel_governance.min.json"' not in project_phase


def test_agent_skill_export_builder_main_stays_orchestration_route() -> None:
    builder_path = SCRIPTS_DIR / "export" / "build_agent_skills.py"
    builder_text = builder_path.read_text(encoding="utf-8")
    syntax_tree = ast.parse(builder_text)
    main_node = next(
        node for node in ast.walk(syntax_tree)
        if isinstance(node, ast.FunctionDef) and node.name == "main"
    )
    main_source = ast.get_source_segment(builder_text, main_node) or ""

    assert main_node.end_lineno - main_node.lineno + 1 <= 24
    assert "build_portable_skill_exports(" in main_source
    assert "build_generated_file_texts(" in main_source
    assert "write_generated_file_texts(" in main_source
    assert "for skill in" not in main_source
    assert "release_manifest_contract.build_release_manifest(" not in main_source


def test_portable_skill_export_builder_is_phase_split() -> None:
    builder_path = SCRIPTS_DIR / "export" / "build_agent_skills.py"
    builder_text = builder_path.read_text(encoding="utf-8")
    portable_phase = (SCRIPTS_DIR / "export" / "portable_skill_export.py").read_text(
        encoding="utf-8"
    )
    syntax_tree = ast.parse(builder_text)
    wrapper_node = next(
        node for node in ast.walk(syntax_tree)
        if isinstance(node, ast.FunctionDef) and node.name == "build_portable_skill_exports"
    )
    wrapper_source = ast.get_source_segment(builder_text, wrapper_node) or ""

    assert "portable_skill_export.build_portable_skill_exports(" in wrapper_source
    assert "for skill in" not in wrapper_source
    assert "for skill in skill_sections[\"skills\"]" in portable_phase
    assert "def artifact_tags(" not in builder_text
    assert "def artifact_tags(" in portable_phase


def test_moved_implementation_does_not_use_flat_repo_root_parent() -> None:
    offenders: list[str] = []
    for path in sorted(SCRIPTS_DIR.glob("**/*.py")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel.startswith("scripts/validators/") or rel in {
            "scripts/_ingress.py",
            "scripts/activation/activate_skill.py",
        }:
            continue
        text = path.read_text(encoding="utf-8")
        if "REPO_ROOT = Path(__file__).resolve().parents[1]" in text:
            offenders.append(rel)

    assert offenders == []
