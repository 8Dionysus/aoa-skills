"""Safe YAML loading with the optional libyaml implementation."""

from __future__ import annotations

from typing import Any

import yaml


_SAFE_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def safe_load(stream: Any) -> Any:
    """Parse YAML with SafeLoader semantics, using libyaml when available."""

    return yaml.load(stream, Loader=_SAFE_LOADER)
