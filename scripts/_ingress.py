"""Compatibility ingress for legacy root script paths."""

from __future__ import annotations

from importlib import import_module
import sys
from types import ModuleType
from typing import Any


def expose(module_name: str, namespace: dict[str, Any]) -> ModuleType:
    module = import_module(module_name)
    exported = getattr(module, "__all__", None)
    if exported is None:
        exported = tuple(name for name in vars(module) if not name.startswith("_"))

    for name in exported:
        namespace[name] = getattr(module, name)

    namespace["__doc__"] = module.__doc__
    namespace["__all__"] = tuple(exported)

    alias_name = namespace.get("__name__")
    if alias_name == "__main__":
        main = getattr(module, "main", None)
        if main is None:
            raise SystemExit(f"{module_name} has no main() entrypoint")
        raise SystemExit(main())

    if isinstance(alias_name, str):
        sys.modules[alias_name] = module

    return module
