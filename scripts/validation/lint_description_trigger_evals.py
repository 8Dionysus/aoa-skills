#!/usr/bin/env python3
"""CLI adapter for description-trigger eval linting."""

from __future__ import annotations

from validation.validators.trigger_eval_surface import *  # noqa: F401,F403
from validation.validators.trigger_eval_surface import main_description as main


if __name__ == "__main__":
    raise SystemExit(main())
