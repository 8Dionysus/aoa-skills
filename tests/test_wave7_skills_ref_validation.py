import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class Wave7SkillsRefValidationTests(unittest.TestCase):
    def run_command(self, command, env=None):
        return subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )

    def test_wrapper_skips_cleanly_when_validator_missing(self):
        env = os.environ.copy()
        env["PATH"] = ""
        env.pop("SKILLS_REF_BIN", None)
        completed = self.run_command(
            [sys.executable, "scripts/run_skills_ref_validation.py", "--repo-root", ".", "--format", "json"],
            env=env,
        )
        self.assertEqual(completed.returncode, 0, msg=completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "skipped")

    def test_wrapper_uses_explicit_validator_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = pathlib.Path(tmpdir)
            fake_validator = tmpdir_path / "skills-ref.py"
            fake_validator.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env python3
                    import sys
                    if len(sys.argv) < 3 or sys.argv[1] != 'validate':
                        sys.exit(2)
                    print(f'validated {sys.argv[2]}')
                    sys.exit(0)
                    """
                ),
                encoding="utf-8",
            )
            fake_validator.chmod(fake_validator.stat().st_mode | stat.S_IXUSR)

            env = os.environ.copy()
            env["PATH"] = env.get("PATH", "")
            completed = self.run_command(
                [
                    sys.executable,
                    "scripts/run_skills_ref_validation.py",
                    "--repo-root",
                    ".",
                    "--skills-ref-bin",
                    str(fake_validator),
                    "--format",
                    "json",
                ],
                env=env,
            )
            self.assertEqual(completed.returncode, 0, msg=completed.stderr)
            payload = json.loads(completed.stdout)
            source_catalog = json.loads((REPO_ROOT / "generated" / "skill_catalog.min.json").read_text())
            self.assertEqual(payload["status"], "passed")
            self.assertEqual(payload["passed_count"], len(source_catalog["skills"]))


if __name__ == "__main__":
    unittest.main()
