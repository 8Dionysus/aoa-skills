from __future__ import annotations

import json
import re
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
    expected_root = root_ingress_paths(inventory) | {"scripts/_ingress.py"}
    actual_root = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in SCRIPTS_DIR.glob("*.py")
    }

    assert actual_root == expected_root

    for rel_path in sorted(root_ingress_paths(inventory)):
        path = REPO_ROOT / rel_path
        text = path.read_text(encoding="utf-8")
        assert "from _ingress import expose" in text
        assert len(text.splitlines()) <= 4
        target = ingress_target(path)
        assert target_module_path(target).is_file(), target


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
