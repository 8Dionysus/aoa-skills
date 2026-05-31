#!/usr/bin/env python3
"""CLI adapter for trigger-eval dataset linting."""

from __future__ import annotations

from validators.trigger_eval_surface import *  # noqa: F401,F403
from validators.trigger_eval_surface import main_trigger as main


if __name__ == "__main__":
    raise SystemExit(main())
