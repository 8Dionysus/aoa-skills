from __future__ import annotations

from typing import Any, Mapping, Sequence


VALID_IMPLICIT_ACTIVATION_POLICIES = ("invoke", "suggest", "manual")
ALLOW_IMPLICIT_BY_POLICY = {
    "invoke": True,
    "suggest": False,
    "manual": False,
}


def resolve_implicit_activation_policy(
    policy_entry: Mapping[str, Any] | None,
    skill_name: str,
) -> str:
    if not isinstance(policy_entry, Mapping):
        raise ValueError(f"{skill_name}: missing policy matrix entry")
    value = policy_entry.get("implicit_activation_policy")
    if value not in VALID_IMPLICIT_ACTIVATION_POLICIES:
        raise ValueError(
            f"{skill_name}: implicit_activation_policy must be one of "
            f"{list(VALID_IMPLICIT_ACTIVATION_POLICIES)!r}, got {value!r}"
        )
    return str(value)


def allow_implicit_invocation(
    policy_entry: Mapping[str, Any] | None,
    skill_name: str,
) -> bool:
    return ALLOW_IMPLICIT_BY_POLICY[
        resolve_implicit_activation_policy(policy_entry, skill_name)
    ]


def manual_invocation_required(
    policy_entry: Mapping[str, Any] | None,
    skill_name: str,
) -> bool:
    return not allow_implicit_invocation(policy_entry, skill_name)


def required_case_classes(
    eval_policy: Mapping[str, Any],
    *,
    activation_policy: str,
    invocation_mode: str,
) -> Sequence[str]:
    by_activation = eval_policy.get("required_case_classes_by_activation_policy")
    if isinstance(by_activation, Mapping) and activation_policy in by_activation:
        classes = by_activation[activation_policy]
    else:
        classes = eval_policy.get("required_case_classes", {}).get(invocation_mode)
    if not isinstance(classes, list) or not all(isinstance(item, str) for item in classes):
        raise ValueError(
            "description trigger policy cannot resolve required case classes for "
            f"activation={activation_policy!r}, invocation={invocation_mode!r}"
        )
    return classes
