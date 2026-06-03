"""Compatibility aliases for the validation validators organ."""

from __future__ import annotations

from importlib import import_module
import sys

_MODULES = (
    "agent_skills_export_contract",
    "agent_skills_export_surface",
    "generated_surface",
    "pack_profile_surface",
    "questbook_contract",
    "questbook_surface",
    "support_resource_surface",
    "tiny_router_surface",
    "trigger_eval_surface",
)

for _name in _MODULES:
    _module = import_module(f"validation.validators.{_name}")
    globals()[_name] = _module
    sys.modules[f"{__name__}.{_name}"] = _module

__all__ = _MODULES
