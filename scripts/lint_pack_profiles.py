#!/usr/bin/env python3
"""CLI adapter for skill-pack profile linting."""

from __future__ import annotations

from validators.pack_profile_surface import *  # noqa: F401,F403
from validators.pack_profile_surface import main


if __name__ == "__main__":
    raise SystemExit(main())
