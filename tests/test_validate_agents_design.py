from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

from tests.support.cli import command_env


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "validation" / "validate_agents_design.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_agents_design", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def valid_card() -> str:
    return """# AGENTS.md

## Applies to

Test lane.

## Role

Test role.

## Read before editing

Read test sources.

## Boundaries

Do not widen the test claim.

## Validation

Run the focused test.

## Closeout

Report the result.
"""


class ValidateAgentsDesignTests(unittest.TestCase):
    def test_repository_agents_mesh_validates(self) -> None:
        module = load_validator()
        self.assertEqual([], module.validate(REPO_ROOT))

    def test_cli_help_is_argparse_help(self) -> None:
        result = subprocess.run(
            (sys.executable, SCRIPT_PATH, "--help"),
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
            env=command_env(),
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("usage:", result.stdout)
        self.assertIn("--repo-root", result.stdout)
        self.assertNotIn("AGENTS design mesh is present", result.stdout)

    def test_missing_expected_card_fails(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for expected in module.EXPECTED_AGENT_CARDS:
                path = root / expected
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(valid_card(), encoding="utf-8")
            (root / module.EXPECTED_AGENT_CARDS[0]).unlink()
            issues = module.validate(root)

        self.assertTrue(any("expected AGENTS.md card is missing" in issue for issue in issues))

    def test_legacy_heading_shape_fails(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for expected in module.EXPECTED_AGENT_CARDS:
                path = root / expected
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(valid_card(), encoding="utf-8")
            target = root / module.EXPECTED_AGENT_CARDS[0]
            target.write_text("# AGENTS.md\n\n## Purpose\n\nOld shape.\n", encoding="utf-8")
            issues = module.validate(root)

        self.assertTrue(any("first section headings must be" in issue for issue in issues))

    def test_empty_canonical_section_fails(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for expected in module.EXPECTED_AGENT_CARDS:
                path = root / expected
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(valid_card(), encoding="utf-8")
            target = root / module.EXPECTED_AGENT_CARDS[0]
            target.write_text(valid_card().replace("Test role.", ""), encoding="utf-8")
            issues = module.validate(root)

        self.assertTrue(any("section '## Role' must not be empty" in issue for issue in issues))

    def test_untracked_scratch_agents_are_ignored_in_git_repo(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(("git", "init", "-q"), cwd=root, check=True)
            for expected in module.EXPECTED_AGENT_CARDS:
                path = root / expected
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(valid_card(), encoding="utf-8")
            subprocess.run(("git", "add", "-A"), cwd=root, check=True)

            scratch = root / "tmp" / "AGENTS.md"
            scratch.parent.mkdir()
            scratch.write_text("# AGENTS.md\n\n## Purpose\n\nScratch.\n", encoding="utf-8")

            self.assertEqual([], module.validate(root))


if __name__ == "__main__":
    unittest.main()
