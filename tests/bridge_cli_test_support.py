from __future__ import annotations

import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml


DEFAULT_REPO = "8Dionysus/aoa-techniques"


def run_git(repo_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


class BridgeCliTestCase(unittest.TestCase):
    maxDiff = None

    def make_repo_root(self, prefix: str) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix=prefix))
        self.addCleanup(shutil.rmtree, repo_root, True)
        return repo_root

    def make_techniques_repo(self) -> Path:
        repo_root = self.make_repo_root("aoa-techniques-bridge-")
        run_git(repo_root.parent, "init", "-q", str(repo_root))
        run_git(repo_root, "config", "user.email", "bridge-tests@example.com")
        run_git(repo_root, "config", "user.name", "Bridge Tests")
        return repo_root

    def commit_files(
        self,
        repo_root: Path,
        message: str,
        files: dict[str, str],
    ) -> str:
        for relative_path, text in files.items():
            target_path = repo_root / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(text, encoding="utf-8", newline="\n")
        run_git(repo_root, "add", ".")
        run_git(repo_root, "commit", "-q", "-m", message)
        return run_git(repo_root, "rev-parse", "HEAD")

    def write_skill_index(self, repo_root: Path, skill_names: list[str]) -> None:
        rows = "\n".join(
            f"| {skill_name} | core | scaffold | Test summary. |"
            for skill_name in skill_names
        )
        (repo_root / "skills").mkdir(parents=True, exist_ok=True)
        (repo_root / "SKILL_INDEX.md").write_text(
            "# SKILL_INDEX\n\n"
            "| name | scope | status | summary |\n"
            "|---|---|---|---|\n"
            f"{rows}\n",
            encoding="utf-8",
            newline="\n",
        )

    def add_skill_bundle(
        self,
        repo_root: Path,
        *,
        skill_name: str,
        techniques: list[dict],
        summary: str = "Test skill summary.",
        status: str = "scaffold",
        invocation_mode: str = "explicit-preferred",
        include_contracts_section: bool = True,
    ) -> None:
        skill_dir = repo_root / "skills" / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        contracts_section = "## Contracts\n\n- contract\n\n" if include_contracts_section else ""
        skill_md = (
            "---\n"
            f"name: {skill_name}\n"
            "scope: core\n"
            f"status: {status}\n"
            f"summary: {summary}\n"
            f"invocation_mode: {invocation_mode}\n"
            "technique_dependencies:\n"
            + "\n".join(f"  - {technique['id']}" for technique in techniques)
            + "\n---\n\n"
            + textwrap.dedent(
                f"""\
                # {skill_name}

                ## Intent

                Intent text.

                ## Trigger boundary

                Use this skill when:
                - needed

                Do not use this skill when:
                - not needed

                ## Inputs

                - input

                ## Outputs

                - output

                ## Procedure

                1. step

                {contracts_section}## Risks and anti-patterns

                - risk

                ## Verification

                - verify

                ## Technique traceability

                Traceability text.

                ## Adaptation points

                - adapt
                """
            )
        )
        (skill_dir / "SKILL.md").write_text(
            skill_md,
            encoding="utf-8",
            newline="\n",
        )

        manifest = {
            "skill_name": skill_name,
            "composition_mode": "bounded",
            "techniques": techniques,
        }
        (skill_dir / "techniques.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
            newline="\n",
        )

    def load_manifest(self, repo_root: Path, skill_name: str) -> dict:
        return yaml.safe_load(
            (repo_root / "skills" / skill_name / "techniques.yaml").read_text(
                encoding="utf-8"
            )
        )
