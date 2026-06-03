#!/usr/bin/env python3
"""CLI adapter for the Agent Skills export/runtime validator."""

from __future__ import annotations

from validation.validators.agent_skills_export_surface import *  # noqa: F401,F403
from validation.validators.agent_skills_export_surface import main


if __name__ == "__main__":
    raise SystemExit(main())
