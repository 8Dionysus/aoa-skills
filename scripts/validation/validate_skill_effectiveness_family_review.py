#!/usr/bin/env python3
"""CLI adapter for whole-family skill-effectiveness review validation."""

from __future__ import annotations

from validation.validators.skill_effectiveness_family_review_surface import *  # noqa: F401,F403
from validation.validators.skill_effectiveness_family_review_surface import main_validate as main


if __name__ == "__main__":
    raise SystemExit(main())
