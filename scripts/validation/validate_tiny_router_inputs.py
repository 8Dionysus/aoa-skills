#!/usr/bin/env python3
"""CLI adapter for the tiny-router generated-surface validator."""

from __future__ import annotations

from validation.validators.tiny_router_surface import *  # noqa: F401,F403
from validation.validators.tiny_router_surface import main


if __name__ == "__main__":
    raise SystemExit(main())
