#!/usr/bin/env python3
"""CLI adapter for committed skill evidence-readout freshness validation."""

from __future__ import annotations

from validation.validators.skill_evidence_readout_surface import *  # noqa: F401,F403
from validation.validators.skill_evidence_readout_surface import main_validate as main


if __name__ == "__main__":
    raise SystemExit(main())
