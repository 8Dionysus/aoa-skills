#!/usr/bin/env python3
"""CLI adapter for the support-resource generated/export validator."""

from __future__ import annotations

from validators.support_resource_surface import *  # noqa: F401,F403
from validators.support_resource_surface import main_validate as main


if __name__ == "__main__":
    raise SystemExit(main())
