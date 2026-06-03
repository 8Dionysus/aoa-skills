#!/usr/bin/env python3
"""CLI adapter for support-resource naming and file-count lint."""

from __future__ import annotations

from validation.validators.support_resource_surface import *  # noqa: F401,F403
from validation.validators.support_resource_surface import main_lint as main


if __name__ == "__main__":
    raise SystemExit(main())
