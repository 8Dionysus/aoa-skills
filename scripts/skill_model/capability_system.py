from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml
from jsonschema import Draft202012Validator


FAMILY_SCHEMA_PATH = Path("schemas/capability_family.schema.json")
GRAPH_SCHEMA_PATH = Path("schemas/capability_graph.schema.json")
LEGACY_DAG_SCHEMA_PATH = Path("schemas/task_local_dag.schema.json")
DAG_SCHEMA_PATH = Path("schemas/task_local_dag_v2.schema.json")
MIGRATION_SCHEMA_PATH = Path("schemas/skill_migration.schema.json")
MIGRATION_PATH = Path("capabilities/legacy-skill-migration.yaml")
FAMILY_ROOT = Path("capabilities/families")
GRAPH_JSON_PATH = Path("generated/capability_graph.json")
GRAPH_MARKDOWN_PATH = Path("generated/capability_graph.md")
KAG_CAPABILITY_GRAPH_NODE_PATH = Path("kag/nodes/capability-graph.json")
KAG_CAPABILITY_SOURCE_NODE_PATH = Path("kag/nodes/capability-source-home.json")
KAG_CAPABILITY_RETURN_EDGE_PATH = Path("kag/edges/capability_returns_to_owner.json")
KAG_PROVIDER_INDEX_PATH = Path("kag/indexes/provider_readiness_index.json")
KAG_MCP_RETURN_PATH = Path("kag/projections/mcp_capability_return.json")
KAG_VALIDATION_ROUTE_RECEIPT_PATH = Path("kag/receipts/validation_receipt.json")
GRAPH_SCHEMA_VERSION = "aoa-capability-graph-v1"
DAG_SCHEMA_VERSION = "aoa-task-local-dag-v2"
HARD_DEPENDENCY_RELATIONS = {"requires", "guarded-by", "verified-by"}
EXECUTABLE_KINDS = {"skill", "mode", "workflow", "tool", "guard", "adapter", "human-gate"}
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "please",
    "with",
    "а",
    "без",
    "в",
    "для",
    "и",
    "из",
    "к",
    "как",
    "какие",
    "какой",
    "кто",
    "между",
    "на",
    "надо",
    "не",
    "ничего",
    "но",
    "нужно",
    "о",
    "об",
    "от",
    "по",
    "при",
    "с",
    "то",
    "только",
    "том",
    "уже",
    "его",
    "есть",
    "здесь",
    "это",
    "этот",
    "что",
}
NEGATIVE_CONTEXT_TOKENS = {
    "без",
    "except",
    "кроме",
    "не",
    "no",
    "not",
    "only",
    "только",
    "unless",
    "without",
}
NEGATIVE_SCOPE_TOKENS = NEGATIVE_CONTEXT_TOKENS - {"only", "только"}

RUSSIAN_INFLECTIONS = tuple(
    sorted(
        {
            "иями",
            "ами",
            "ями",
            "ого",
            "его",
            "ому",
            "ему",
            "ими",
            "ыми",
            "иях",
            "ией",
            "иям",
            "ием",
            "ах",
            "ях",
            "ую",
            "юю",
            "ам",
            "ям",
            "ем",
            "ом",
            "ою",
            "ею",
            "ей",
            "ой",
            "ий",
            "ый",
            "ая",
            "яя",
            "ое",
            "ее",
            "ие",
            "ые",
            "ия",
            "ья",
            "ью",
            "а",
            "я",
            "ы",
            "и",
            "ь",
            "й",
            "у",
            "ю",
            "е",
            "о",
        },
        key=lambda value: (-len(value), value),
    )
)


class CapabilityContractError(ValueError):
    """Raised when authored capability sources violate durable contract law."""


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def dump_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise CapabilityContractError(f"{path} must contain a JSON object")
    return payload


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise CapabilityContractError(f"{path} must contain a YAML mapping")
    return payload


def relative_path(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def schema_issues(payload: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    issues: list[str] = []
    for error in sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path)):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        issues.append(f"{location}: {error.message}")
    return issues


def family_paths(repo_root: Path) -> list[Path]:
    root = repo_root / FAMILY_ROOT
    if not root.is_dir():
        raise CapabilityContractError(f"missing capability family root: {FAMILY_ROOT.as_posix()}")
    paths = sorted(root.glob("*.yaml"))
    if not paths:
        raise CapabilityContractError("capability family root contains no YAML sources")
    return paths


def load_families(repo_root: Path) -> list[tuple[Path, dict[str, Any]]]:
    schema = load_json(repo_root / FAMILY_SCHEMA_PATH)
    loaded: list[tuple[Path, dict[str, Any]]] = []
    issues: list[str] = []
    for path in family_paths(repo_root):
        payload = load_yaml(path)
        for issue in schema_issues(payload, schema):
            issues.append(f"{relative_path(path, repo_root)}: {issue}")
        loaded.append((path, payload))
    if issues:
        raise CapabilityContractError("\n".join(issues))
    return loaded


def load_migration_contract(repo_root: Path) -> dict[str, Any]:
    schema = load_json(repo_root / MIGRATION_SCHEMA_PATH)
    path = repo_root / MIGRATION_PATH
    payload = load_yaml(path)
    issues = schema_issues(payload, schema)
    if issues:
        raise CapabilityContractError(
            "\n".join(f"{MIGRATION_PATH.as_posix()}: {issue}" for issue in issues)
        )
    return payload


def node_map(families: Sequence[tuple[Path, Mapping[str, Any]]]) -> dict[str, dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {}
    duplicates: defaultdict[str, list[str]] = defaultdict(list)
    for path, family in families:
        for raw_node in family.get("nodes", []):
            node = dict(raw_node)
            node_id = str(node["id"])
            duplicates[node_id].append(path.as_posix())
            nodes.setdefault(node_id, node)
    duplicate_rows = {key: value for key, value in duplicates.items() if len(value) > 1}
    if duplicate_rows:
        details = "; ".join(f"{key}: {', '.join(value)}" for key, value in sorted(duplicate_rows.items()))
        raise CapabilityContractError(f"duplicate capability node ids: {details}")
    return nodes


def relation_rows(families: Sequence[tuple[Path, Mapping[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, family in families:
        for raw_relation in family.get("relations", []):
            relation = dict(raw_relation)
            relation["source_path"] = path.as_posix()
            rows.append(relation)
    return rows


def _check_primary_tree(
    nodes: Mapping[str, Mapping[str, Any]],
    *,
    expected_root: str = "aoa",
) -> list[str]:
    issues: list[str] = []
    roots = [node_id for node_id, node in nodes.items() if node.get("primary_parent") is None]
    if roots != [expected_root]:
        issues.append(
            f"primary tree must have exactly root {expected_root!r}; found {sorted(roots)}"
        )

    for node_id, node in nodes.items():
        parent = node.get("primary_parent")
        if parent is not None and parent not in nodes:
            issues.append(f"{node_id}: primary_parent '{parent}' does not exist")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visited:
            return
        if node_id in visiting:
            issues.append(f"primary tree cycle reaches '{node_id}'")
            return
        visiting.add(node_id)
        parent = nodes[node_id].get("primary_parent")
        if isinstance(parent, str) and parent in nodes:
            visit(parent)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in sorted(nodes):
        visit(node_id)
    return issues


def _check_local_binding(repo_root: Path, node: Mapping[str, Any]) -> list[str]:
    binding = node.get("binding")
    if not isinstance(binding, Mapping):
        return []
    ref = binding.get("ref")
    if not isinstance(ref, str) or not ref.startswith("skills/"):
        return []
    path_part = ref.split("#", 1)[0]
    skill_path = repo_root / path_part
    if not skill_path.is_file():
        return [f"{node['id']}: local binding ref does not exist: {path_part}"]
    issues: list[str] = []
    text = skill_path.read_text(encoding="utf-8")
    if node.get("kind") == "skill":
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            return [f"{node['id']}: local skill binding lacks YAML frontmatter"]
        try:
            closing = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
        except StopIteration:
            return [f"{node['id']}: local skill binding lacks closing frontmatter delimiter"]
        metadata = yaml.safe_load("\n".join(lines[1:closing])) or {}
        expected_name = str(node["id"]).removeprefix("skill.")
        if metadata.get("name") != expected_name:
            issues.append(
                f"{node['id']}: bound SKILL.md name is {metadata.get('name')!r}, expected {expected_name!r}"
            )
        if metadata.get("description") != node.get("description"):
            issues.append(
                f"{node['id']}: capability description must exactly match bound SKILL.md frontmatter description"
            )
    if node.get("kind") == "mode":
        operation = binding.get("operation")
        if re.search(rf"^##{{2,4}} Mode: {re.escape(str(operation))}$", text, flags=re.MULTILINE) is None:
            issues.append(f"{node['id']}: bound mode heading is missing: Mode: {operation}")
    return issues


def _local_skill_contract(
    repo_root: Path, node: Mapping[str, Any]
) -> tuple[Path, dict[str, Any]] | None:
    if node.get("kind") != "skill":
        return None
    binding = node.get("binding")
    if not isinstance(binding, Mapping):
        return None
    ref = binding.get("ref")
    if not isinstance(ref, str) or not ref.startswith("skills/"):
        return None
    skill_path = repo_root / ref.split("#", 1)[0]
    if skill_path.name != "SKILL.md":
        return None
    contract_path = skill_path.parent / "references" / "contract.yaml"
    if not contract_path.is_file():
        return None
    return contract_path, load_yaml(contract_path)


def _required_abi_type(node: Mapping[str, Any], direction: str) -> str | None:
    rows = node.get("abi", {}).get(direction, [])
    if not isinstance(rows, Sequence):
        return None
    for row in rows:
        if isinstance(row, Mapping) and row.get("required") is True and isinstance(row.get("type"), str):
            return str(row["type"])
    return None


def _check_local_skill_contracts(
    repo_root: Path, nodes: Mapping[str, Mapping[str, Any]]
) -> list[str]:
    issues: list[str] = []
    for skill_id, skill_node in sorted(nodes.items()):
        contract_result = _local_skill_contract(repo_root, skill_node)
        if contract_result is None:
            continue
        contract_path, contract = contract_result
        contract_ref = relative_path(contract_path, repo_root)
        identity = contract.get("identity")
        expected_name = skill_id.removeprefix("skill.")
        if not isinstance(identity, Mapping):
            issues.append(f"{skill_id}: {contract_ref} lacks identity mapping")
            continue
        if identity.get("name") != expected_name:
            issues.append(
                f"{skill_id}: {contract_ref} identity.name is {identity.get('name')!r}, expected {expected_name!r}"
            )
        owner_repo = skill_node.get("owner", {}).get("repo")
        if isinstance(owner_repo, str) and identity.get("owner") != owner_repo:
            issues.append(
                f"{skill_id}: {contract_ref} identity.owner is {identity.get('owner')!r}, expected {owner_repo!r}"
            )
        lifecycle = skill_node.get("lifecycle")
        if isinstance(lifecycle, Mapping):
            for field in ("version", "health"):
                if identity.get(field) != lifecycle.get(field):
                    issues.append(
                        f"{skill_id}: {contract_ref} identity.{field} is "
                        f"{identity.get(field)!r}, expected lifecycle {lifecycle.get(field)!r}"
                    )

        contract_modes = contract.get("modes")
        if not isinstance(contract_modes, Mapping):
            continue
        parent = skill_node.get("primary_parent")
        sibling_modes = {
            str(node.get("binding", {}).get("operation")): node
            for node in nodes.values()
            if node.get("kind") == "mode" and node.get("primary_parent") == parent
        }
        missing_modes = sorted(set(map(str, contract_modes)) - set(sibling_modes))
        extra_modes = sorted(set(sibling_modes) - set(map(str, contract_modes)))
        if missing_modes:
            issues.append(f"{skill_id}: contract modes lack graph nodes: {', '.join(missing_modes)}")
        if extra_modes:
            issues.append(f"{skill_id}: graph modes lack owner contract entries: {', '.join(extra_modes)}")
        for raw_operation, raw_mode_contract in contract_modes.items():
            operation = str(raw_operation)
            mode_node = sibling_modes.get(operation)
            if mode_node is None or not isinstance(raw_mode_contract, Mapping):
                continue
            reference = raw_mode_contract.get("reference")
            if not isinstance(reference, str) or not reference:
                issues.append(f"{skill_id}: contract mode {operation!r} lacks reference")
                continue
            expected_ref = relative_path(contract_path.parent / reference, repo_root)
            actual_ref = mode_node.get("binding", {}).get("ref")
            if actual_ref != expected_ref:
                issues.append(
                    f"{mode_node['id']}: binding ref is {actual_ref!r}, owner contract requires {expected_ref!r}"
                )
            input_abi = raw_mode_contract.get("input_abi")
            output_abi = raw_mode_contract.get("output_abi")
            graph_input_abi = _required_abi_type(mode_node, "inputs")
            graph_output_abi = _required_abi_type(mode_node, "outputs")
            if isinstance(input_abi, str) and graph_input_abi != input_abi:
                issues.append(
                    f"{mode_node['id']}: required input ABI is {graph_input_abi!r}, owner contract requires {input_abi!r}"
                )
            if isinstance(output_abi, str) and graph_output_abi != output_abi:
                issues.append(
                    f"{mode_node['id']}: required output ABI is {graph_output_abi!r}, owner contract requires {output_abi!r}"
                )
    return issues


def semantic_issues(
    repo_root: Path,
    families: Sequence[tuple[Path, Mapping[str, Any]]],
    *,
    expected_root: str = "aoa",
) -> list[str]:
    issues: list[str] = []
    family_ids: defaultdict[str, list[str]] = defaultdict(list)
    for path, family in families:
        family_ids[str(family["family_id"])].append(relative_path(path, repo_root))
    for family_id, paths in sorted(family_ids.items()):
        if len(paths) > 1:
            issues.append(f"duplicate family_id '{family_id}': {', '.join(paths)}")

    nodes = node_map(families)
    issues.extend(_check_primary_tree(nodes, expected_root=expected_root))
    issues.extend(_check_local_skill_contracts(repo_root, nodes))
    aliases: defaultdict[str, list[str]] = defaultdict(list)
    for node_id, node in sorted(nodes.items()):
        contract_level = node.get("contract_level")
        kind = node.get("kind")
        visibility = node.get("lifecycle", {}).get("visibility")
        if contract_level == "executable" and kind not in EXECUTABLE_KINDS:
            issues.append(f"{node_id}: executable contract cannot use node kind '{kind}'")
        if visibility == "advertised" and kind != "skill":
            issues.append(f"{node_id}: only independently callable skill bundles may be advertised")
        binding = node.get("binding")
        if isinstance(binding, Mapping) and kind in EXECUTABLE_KINDS and binding.get("kind") != kind:
            issues.append(
                f"{node_id}: node kind '{kind}' must match binding kind '{binding.get('kind')}'"
            )
        issues.extend(_check_local_binding(repo_root, node))
        for alias in node.get("aliases", []):
            aliases[str(alias["name"])].append(node_id)
        for source_ref in node.get("provenance", {}).get("source_refs", []):
            if source_ref.get("repo") == "aoa-techniques" and source_ref.get("role") not in {
                "optional-provenance",
                "historical-lineage",
            }:
                issues.append(
                    f"{node_id}: aoa-techniques may appear only as optional provenance, not required source"
                )

    for alias, owner_ids in sorted(aliases.items()):
        if len(owner_ids) > 1:
            issues.append(f"migration alias '{alias}' is claimed by multiple nodes: {', '.join(owner_ids)}")

    allowed_implementation_targets = EXECUTABLE_KINDS
    for relation in relation_rows(families):
        source = relation["source"]
        target = relation["target"]
        kind = relation["kind"]
        if source not in nodes:
            issues.append(f"{relation['source_path']}: relation source '{source}' does not exist")
            continue
        if target not in nodes:
            issues.append(f"{relation['source_path']}: relation target '{target}' does not exist")
            continue
        if source == target:
            issues.append(f"{relation['source_path']}: self relation is not allowed for '{source}'")
        if kind == "implemented-by" and nodes[target].get("kind") not in allowed_implementation_targets:
            issues.append(f"{source}: implemented-by target '{target}' is not executable")
        if kind in HARD_DEPENDENCY_RELATIONS and nodes[target].get("lifecycle", {}).get("state") == "retired":
            issues.append(f"{source}: active dependency points to retired target '{target}'")
    return issues


def migration_issues(
    migration: Mapping[str, Any],
    families: Sequence[tuple[Path, Mapping[str, Any]]],
) -> list[str]:
    """Validate the manually classified 57-skill migration against live capability truth."""
    issues: list[str] = []
    nodes = node_map(families)
    aliases: dict[str, str] = {}
    for node_id, node in sorted(nodes.items()):
        for alias in node.get("aliases", []):
            alias_name = str(alias["name"])
            aliases[alias_name] = node_id

    entries = migration.get("entries", [])
    seen_names: set[str] = set()
    seen_paths: set[str] = set()
    migration_aliases: dict[str, str] = {}
    for index, raw_entry in enumerate(entries):
        entry = dict(raw_entry)
        label = f"migration entry {index + 1} ({entry.get('legacy_name', '<unknown>')})"
        legacy_name = str(entry.get("legacy_name", ""))
        legacy_path = str(entry.get("legacy_path", ""))
        target_id = str(entry.get("target_id", ""))
        compatibility = str(entry.get("compatibility", ""))
        action = str(entry.get("action", ""))

        if legacy_name in seen_names:
            issues.append(f"{label}: duplicate legacy_name")
        seen_names.add(legacy_name)
        if legacy_path in seen_paths:
            issues.append(f"{label}: duplicate legacy_path")
        seen_paths.add(legacy_path)
        if Path(legacy_path).parent.name != legacy_name:
            issues.append(f"{label}: legacy_path parent must match legacy_name")

        target = nodes.get(target_id)
        if target is None:
            issues.append(f"{label}: target_id '{target_id}' does not exist")
            continue
        target_kind = str(target.get("kind", ""))
        if entry.get("target_kind") != target_kind:
            issues.append(
                f"{label}: target_kind {entry.get('target_kind')!r} does not match node kind {target_kind!r}"
            )
        target_owner = str(target.get("owner", {}).get("repo", ""))
        if entry.get("target_owner") != target_owner:
            issues.append(
                f"{label}: target_owner {entry.get('target_owner')!r} does not match node owner {target_owner!r}"
            )

        visibility = str(target.get("lifecycle", {}).get("visibility", ""))
        if action == "retain-advertised":
            if target_kind != "skill" or visibility != "advertised":
                issues.append(f"{label}: retain-advertised must target an advertised skill")
            if compatibility not in {"same-name", "same-name-transitional"} or target_id != f"skill.{legacy_name}":
                issues.append(f"{label}: retained skill must use same-name compatibility")
            if compatibility == "same-name-transitional" and entry.get("reason") != "preserve-execution-until-owner-mcp":
                issues.append(
                    f"{label}: transitional same-name retention must name the missing executable owner"
                )
        elif action == "defer-family":
            if target_kind != "skill" or visibility == "advertised":
                issues.append(f"{label}: defer-family must target a non-advertised skill")
            if compatibility != "same-name-deferred" or target_id != f"skill.{legacy_name}":
                issues.append(f"{label}: deferred family must use same-name-deferred compatibility")
        elif action == "merge-mode" and target_kind != "mode":
            issues.append(f"{label}: merge-mode must target a mode")
        elif action == "route-owner-object" and target_kind not in {"workflow", "tool", "guard", "adapter"}:
            issues.append(f"{label}: route-owner-object targets unsupported kind {target_kind!r}")

        alias_owner = aliases.get(legacy_name)
        if compatibility == "migration-alias":
            migration_aliases[legacy_name] = target_id
            if alias_owner != target_id:
                issues.append(
                    f"{label}: migration alias must exist exactly on target '{target_id}', found {alias_owner!r}"
                )
        elif alias_owner is not None:
            issues.append(
                f"{label}: compatibility {compatibility!r} forbids alias on '{alias_owner}'"
            )

    extra_aliases = sorted(set(aliases) - set(migration_aliases))
    if extra_aliases:
        issues.append("capability aliases lack migration entries: " + ", ".join(extra_aliases))
    return issues


def validate_sources(repo_root: Path) -> list[tuple[Path, dict[str, Any]]]:
    families = load_families(repo_root)
    issues = semantic_issues(repo_root, families)
    migration = load_migration_contract(repo_root)
    issues.extend(migration_issues(migration, families))
    if issues:
        raise CapabilityContractError("\n".join(issues))
    return families


def _flatten_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for key in sorted(value):
            if key in {"ref"} and re.fullmatch(r"[0-9a-f]{40,64}", str(value[key])):
                continue
            yield from _flatten_strings(value[key])
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            yield from _flatten_strings(item)


def normalize_token(token: str) -> str:
    token = token.replace("ё", "е")
    if len(token) < 5 or re.search(r"[^а-я]", token):
        return token
    for suffix in RUSSIAN_INFLECTIONS:
        if token.endswith(suffix) and len(token) - len(suffix) >= 4:
            return token[: -len(suffix)]
    return token


def tokenize_ordered(
    text: str,
    *,
    keep_negative_scope: bool = False,
) -> list[str]:
    tokens: list[str] = []
    for raw_token in re.findall(r"[^\W_]+(?:[-.][^\W_]+)*", text.lower(), flags=re.UNICODE):
        if len(raw_token) < 2 or (
            raw_token in STOPWORDS
            and not (keep_negative_scope and raw_token in NEGATIVE_SCOPE_TOKENS)
        ):
            continue
        parts = [raw_token]
        if "-" in raw_token or "." in raw_token:
            parts.extend(part for part in re.split(r"[-.]", raw_token) if part)
        for part in parts:
            if len(part) < 2 or (
                part in STOPWORDS
                and not (keep_negative_scope and part in NEGATIVE_SCOPE_TOKENS)
            ):
                continue
            tokens.append(normalize_token(part))
    return tokens


def tokenize(text: str) -> list[str]:
    return sorted(set(tokenize_ordered(text)))


def negative_scope_phrase_matches(
    query_tokens: Sequence[str],
    phrase_tokens: Sequence[str],
    *,
    scope_width: int = 3,
) -> set[str]:
    """Return phrase evidence only when an explicit negative scope also matches.

    Shared positive vocabulary is not negative evidence by itself.  A scope
    marker such as ``not`` or ``without`` admits those shared terms only when
    the query places a matching phrase term after the same marker, which is
    where these English and Russian negative forms take their object.
    """

    for phrase_index, scope_token in enumerate(phrase_tokens):
        if scope_token not in NEGATIVE_SCOPE_TOKENS:
            continue
        phrase_subject = {
            token
            for token in phrase_tokens[max(0, phrase_index - scope_width) : phrase_index]
            if token not in NEGATIVE_CONTEXT_TOKENS
        }
        phrase_scope = [
            token
            for token in phrase_tokens[phrase_index + 1 : phrase_index + 1 + scope_width]
            if token not in NEGATIVE_CONTEXT_TOKENS
        ]
        if not phrase_scope:
            continue
        for query_index, query_token in enumerate(query_tokens):
            if query_token != scope_token:
                continue
            query_subject = {
                token
                for token in query_tokens[max(0, query_index - scope_width) : query_index]
                if token not in NEGATIVE_CONTEXT_TOKENS
            }
            query_scope = {
                token
                for token in query_tokens[query_index + 1 : query_index + 1 + scope_width]
                if token not in NEGATIVE_CONTEXT_TOKENS
            }
            scope_matches = query_scope.intersection(phrase_scope)
            if scope_matches:
                return {
                    scope_token,
                    *scope_matches,
                    *(query_subject & phrase_subject),
                }
    return set()


def bound_retrieval_text(node: Mapping[str, Any], text: str) -> str:
    """Keep a mode's retrieval body inside its declared section of a shared bundle."""
    if node.get("kind") != "mode":
        return text
    binding = node.get("binding", {})
    operation = binding.get("operation") if isinstance(binding, Mapping) else None
    if not isinstance(operation, str) or not operation:
        return text
    heading = re.search(
        rf"^### Mode: {re.escape(operation)}\s*$",
        text,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    if heading is None:
        return text
    next_heading = re.search(r"^(?:## |### Mode: )", text[heading.end() :], flags=re.MULTILINE)
    end = heading.end() + next_heading.start() if next_heading is not None else len(text)
    return text[heading.start() : end]


def retrieval_document(
    node: Mapping[str, Any],
    *,
    immediate_executable_children: Sequence[Mapping[str, Any]] = (),
    supplemental_texts: Sequence[str] = (),
    include_depth_tokens: bool = False,
) -> dict[str, Any]:
    contract_parts = list(_flatten_strings(node))
    routing_parts = list(_flatten_strings(node.get("keywords", [])))
    description = str(node.get("description", ""))
    description_parts = re.split(r"\bDo not use\b", description, maxsplit=1, flags=re.IGNORECASE)
    positive_parts = [str(node.get("id", "")), str(node.get("title", "")), description_parts[0]]
    negative_parts = description_parts[1:] + list(
        _flatten_strings(node.get("applicability", {}).get("do_not_use_when", []))
    )
    positive_parts.extend(_flatten_strings(node.get("keywords", [])))
    positive_parts.extend(_flatten_strings(node.get("applicability", {}).get("use_when", [])))
    if node.get("kind") in {"capability", "skill"}:
        for child in immediate_executable_children:
            contract_parts.extend(_flatten_strings(child))
            routing_parts.extend(_flatten_strings(child.get("keywords", [])))
            child_description = str(child.get("description", ""))
            child_description_parts = re.split(
                r"\bDo not use\b", child_description, maxsplit=1, flags=re.IGNORECASE
            )
            positive_parts.extend(
                [str(child.get("id", "")), str(child.get("title", "")), child_description_parts[0]]
            )
            positive_parts.extend(_flatten_strings(child.get("keywords", [])))
            positive_parts.extend(_flatten_strings(child.get("applicability", {}).get("use_when", [])))
            negative_parts.extend(child_description_parts[1:])
            negative_parts.extend(
                _flatten_strings(child.get("applicability", {}).get("do_not_use_when", []))
            )
    search_parts = [*contract_parts, *supplemental_texts]
    search_text = "\n".join(search_parts)
    contract_text = "\n".join(contract_parts)
    package_text = "\n".join(supplemental_texts)
    positive_text = "\n".join(positive_parts)
    negative_text = "\n".join(negative_parts)
    lifecycle = node.get("lifecycle", {})
    document = {
        "id": node["id"],
        "kind": node["kind"],
        "visibility": lifecycle.get("visibility", "hidden"),
        "title": node["title"],
        "description": node["description"],
        "search_text": search_text,
        "positive_text": positive_text,
        "negative_text": negative_text,
        "negative_phrases": negative_parts,
        "routing_tokens": tokenize("\n".join(routing_parts)),
        "positive_tokens": tokenize(positive_text),
        "negative_tokens": tokenize(negative_text),
        "tokens": tokenize(search_text),
    }
    if include_depth_tokens:
        document["contract_tokens"] = tokenize(contract_text)
        document["package_tokens"] = tokenize(package_text)
    return document


def build_graph_payload(
    repo_root: Path,
    *,
    families: Sequence[tuple[Path, Mapping[str, Any]]] | None = None,
    family_root: Path = FAMILY_ROOT,
    graph_schema_path: Path | None = None,
    source_metadata: Mapping[str, Any] | None = None,
    include_retrieval_depth_tokens: bool = False,
) -> dict[str, Any]:
    if families is None:
        families = validate_sources(repo_root)
    nodes: list[dict[str, Any]] = []
    source_files: list[dict[str, str]] = []
    referenced_files: list[dict[str, str]] = []
    hash_material: list[bytes] = []
    for path, family in families:
        rel = relative_path(path, repo_root)
        raw = path.read_bytes()
        digest = sha256_bytes(raw)
        source_files.append({"path": rel, "sha256": digest})
        hash_material.extend([rel.encode("utf-8"), b"\0", raw, b"\0"])
        for raw_node in family["nodes"]:
            node = dict(raw_node)
            node["source_family"] = family["family_id"]
            node["source_path"] = rel
            nodes.append(node)

    local_contract_text: dict[str, str] = {}
    contract_by_skill_id: dict[str, tuple[Path, dict[str, Any]]] = {}
    for node in nodes:
        contract_result = _local_skill_contract(repo_root, node)
        if contract_result is None:
            continue
        contract_path, contract = contract_result
        skill_id = str(node["id"])
        contract_by_skill_id[skill_id] = contract_result
        raw = contract_path.read_bytes()
        contract_ref = relative_path(contract_path, repo_root)
        contract_digest = sha256_bytes(raw)
        node["owner_contract"] = contract
        node["owner_contract_ref"] = {"path": contract_ref, "sha256": contract_digest}
        local_contract_text[skill_id] = raw.decode("utf-8")

        parent = node.get("primary_parent")
        contract_modes = contract.get("modes")
        if not isinstance(contract_modes, Mapping):
            continue
        for mode_node in nodes:
            if mode_node.get("kind") != "mode" or mode_node.get("primary_parent") != parent:
                continue
            operation = mode_node.get("binding", {}).get("operation")
            mode_contract = contract_modes.get(operation)
            if not isinstance(mode_contract, Mapping):
                continue
            mode_node["mode_contract"] = dict(mode_contract)
            mode_node["owner_contract_ref"] = {"path": contract_ref, "sha256": contract_digest}

    local_binding_text: dict[str, str] = {}
    seen_referenced_paths: set[str] = set()
    for node in nodes:
        binding = node.get("binding")
        if not isinstance(binding, Mapping):
            continue
        ref = binding.get("ref")
        if not isinstance(ref, str) or not ref.startswith("skills/"):
            continue
        path_value = ref.split("#", 1)[0]
        path = repo_root / path_value
        text = path.read_text(encoding="utf-8")
        local_binding_text[str(node["id"])] = bound_retrieval_text(node, text)
        if path_value in seen_referenced_paths:
            continue
        seen_referenced_paths.add(path_value)
        raw = path.read_bytes()
        referenced_files.append({"path": path_value, "sha256": sha256_bytes(raw)})
        hash_material.extend([path_value.encode("utf-8"), b"\0", raw, b"\0"])

    for contract_path, _ in contract_by_skill_id.values():
        path_value = relative_path(contract_path, repo_root)
        if path_value in seen_referenced_paths:
            continue
        seen_referenced_paths.add(path_value)
        raw = contract_path.read_bytes()
        referenced_files.append({"path": path_value, "sha256": sha256_bytes(raw)})
        hash_material.extend([path_value.encode("utf-8"), b"\0", raw, b"\0"])

    relations: list[dict[str, Any]] = []
    for node in nodes:
        parent = node.get("primary_parent")
        if isinstance(parent, str):
            relations.append(
                {
                    "kind": "primary-parent",
                    "source": node["id"],
                    "target": parent,
                    "source_path": node["source_path"],
                }
            )
    for path, family in families:
        rel_path = relative_path(path, repo_root)
        for raw_relation in family["relations"]:
            relation = dict(raw_relation)
            relation["source_path"] = rel_path
            relations.append(relation)

    nodes.sort(key=lambda item: item["id"])
    relations.sort(key=lambda item: (item["kind"], item["source"], item["target"], item.get("condition", "")))
    source_payload: dict[str, Any] = {
        "root": family_root.as_posix(),
        "family_files": source_files,
        "referenced_files": sorted(referenced_files, key=lambda item: item["path"]),
        "content_hash": "",
    }
    if source_metadata:
        source_payload.update(dict(source_metadata))
        hash_material.extend(
            [
                b"source-metadata\0",
                canonical_json(source_metadata).encode("utf-8"),
                b"\0",
            ]
        )
    source_payload["content_hash"] = sha256_bytes(b"".join(hash_material))
    payload = {
        "schema_version": GRAPH_SCHEMA_VERSION,
        "authority": False,
        "source": source_payload,
        "roots": sorted(node["id"] for node in nodes if node.get("primary_parent") is None),
        "nodes": nodes,
        "relations": relations,
        "retrieval_documents": [],
    }
    children_by_parent: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    modes_by_binding_ref: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    modes_by_primary_parent: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    skills_by_primary_parent: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        parent = node.get("primary_parent")
        if isinstance(parent, str) and node.get("contract_level") == "executable":
            children_by_parent[parent].append(node)
        binding = node.get("binding")
        if node.get("kind") == "mode" and isinstance(binding, Mapping):
            if isinstance(parent, str):
                modes_by_primary_parent[parent].append(node)
            ref = binding.get("ref")
            if isinstance(ref, str):
                modes_by_binding_ref[ref].append(node)
        elif node.get("kind") == "skill" and isinstance(parent, str):
            skills_by_primary_parent[parent].append(node)

    def retrieval_children(node: Mapping[str, Any]) -> list[dict[str, Any]]:
        if node.get("kind") == "skill":
            binding = node.get("binding")
            ref = binding.get("ref") if isinstance(binding, Mapping) else None
            parent = node.get("primary_parent")
            if (
                isinstance(parent, str)
                and len(skills_by_primary_parent.get(parent, [])) == 1
                and modes_by_primary_parent.get(parent)
            ):
                return sorted(modes_by_primary_parent[parent], key=lambda item: str(item["id"]))
            if isinstance(ref, str):
                return sorted(modes_by_binding_ref.get(ref, []), key=lambda item: str(item["id"]))
        return children_by_parent.get(str(node["id"]), [])

    payload["retrieval_documents"] = [
        retrieval_document(
            node,
            immediate_executable_children=retrieval_children(node),
            supplemental_texts=[
                text
                for text in [
                    local_binding_text.get(str(node["id"])),
                    local_contract_text.get(str(node["id"])),
                    *[
                        local_binding_text.get(str(child["id"]))
                        for child in retrieval_children(node)
                    ],
                ]
                if text is not None
            ],
            include_depth_tokens=include_retrieval_depth_tokens,
        )
        for node in nodes
    ]
    graph_schema = load_json(graph_schema_path or (repo_root / GRAPH_SCHEMA_PATH))
    issues = schema_issues(payload, graph_schema)
    if issues:
        raise CapabilityContractError("derived capability graph violates schema:\n" + "\n".join(issues))
    return payload


def render_graph_markdown(payload: Mapping[str, Any]) -> str:
    nodes = {node["id"]: node for node in payload["nodes"]}
    children: defaultdict[str | None, list[str]] = defaultdict(list)
    for node_id, node in nodes.items():
        children[node.get("primary_parent")].append(node_id)
    for values in children.values():
        values.sort()

    lines = [
        "# Capability graph",
        "",
        "Derived from `capabilities/families/*.yaml`. This file is a read model, not capability authority.",
        "",
        f"Source content hash: `{payload['source']['content_hash']}`",
        "",
        "## Semantic tree",
        "",
    ]

    def render_subtree(node_id: str, depth: int) -> None:
        node = nodes[node_id]
        lifecycle = node["lifecycle"]
        lines.append(
            f"{'  ' * depth}- `{node_id}` ({node['kind']}, {lifecycle['visibility']}, {lifecycle['health']})"
        )
        for child_id in children.get(node_id, []):
            render_subtree(child_id, depth + 1)

    for root in payload["roots"]:
        render_subtree(root, 0)

    lines.extend(
        [
            "",
            "## Typed relations",
            "",
            "| kind | source | target | condition |",
            "|---|---|---|---|",
        ]
    )
    for relation in payload["relations"]:
        lines.append(
            f"| {relation['kind']} | `{relation['source']}` | `{relation['target']}` | {relation.get('condition', '-')} |"
        )
    return "\n".join(lines) + "\n"


def build_kag_provider_outputs(
    repo_root: Path,
    payload: Mapping[str, Any],
) -> dict[Path, str]:
    shared_bundles = [
        node
        for node in payload.get("nodes", [])
        if node.get("kind") == "skill"
        and node.get("owner", {}).get("repo") == "aoa-skills"
        and str(node.get("binding", {}).get("ref", "")).startswith("skills/")
    ]
    advertised_count = sum(
        1
        for node in shared_bundles
        if node.get("lifecycle", {}).get("visibility") == "advertised"
    )
    deferred_count = sum(
        1
        for node in shared_bundles
        if node.get("lifecycle", {}).get("visibility") == "deferred"
    )
    bundle_summary = (
        f"{len(shared_bundles)} shared callable source bundles "
        f"({advertised_count} advertised, {deferred_count} deferred)"
    )

    graph_source = {
        "repo": "aoa-skills",
        "path": GRAPH_JSON_PATH.as_posix(),
        "source_class": "skill_source",
        "role": "primary",
        "authority": "derived_readmodel",
    }
    capability_owner = {
        "repo": "aoa-skills",
        "path": "capabilities/README.md",
        "source_class": "skill_source",
        "role": "owner_route",
        "authority": "authored_source",
    }
    skill_owner = {
        "repo": "aoa-skills",
        "path": "skills/README.md",
        "source_class": "skill_source",
        "role": "owner_route",
        "authority": "authored_source",
    }

    def base_record(
        *,
        local_id: str,
        record_class: str,
        source_refs: Sequence[Mapping[str, str]],
        derived_method: str,
        checked_ref: str,
        payload_class: str,
        consumer_route: str,
        freshness_mode: str = "source_snapshot",
    ) -> dict[str, Any]:
        return {
            "schema_version": "aoa-local-kag-record-v1",
            "repo": "aoa-skills",
            "local_id": local_id,
            "record_class": record_class,
            "source_refs": [dict(item) for item in source_refs],
            "source_owner": "aoa-skills",
            "provenance_mode": "strict_source_linked",
            "derived_method": derived_method,
            "generated_or_authored": "generated_from_source",
            "status": "active",
            "owner_return_route": {
                "repo": "aoa-skills",
                "surface": "capabilities/README.md",
                "route_kind": "authored_meaning",
            },
            "freshness": {
                "mode": freshness_mode,
                "state": "current",
                "checked_ref": checked_ref,
            },
            "builder": {
                "route": "capability graph and provider-record builder",
                "surface": "scripts/builders/build_capability_graph.py",
            },
            "validator": {
                "route": "aoa-kag:scripts/validate_repo_local_kag_family.py",
                "lane": "local-kag",
            },
            "storage_posture": {
                "git_surface": (
                    "compact_readmodel"
                    if payload_class == "projection"
                    else "receipt"
                    if payload_class == "receipt"
                    else "portable_records"
                ),
                "payload_class": payload_class,
                "runtime_route": "source-repo",
            },
            "consumer_route": consumer_route,
        }

    graph_node = base_record(
        local_id="node:skills:capability-graph",
        record_class="node",
        source_refs=[graph_source, capability_owner],
        derived_method=(
            "deterministic projection of authored capability families, typed "
            f"relations, compatibility, and {bundle_summary}"
        ),
        checked_ref=GRAPH_JSON_PATH.as_posix(),
        payload_class="node",
        consumer_route="aoa-kag registry and capability retrieval",
    )
    graph_node.update(
        {
            "node_kind": "source_surface",
            "label": "aoa-skills semantic capability graph",
        }
    )

    source_node = base_record(
        local_id="node:skills:capability-source-home",
        record_class="node",
        source_refs=[
            capability_owner,
            skill_owner,
            {
                "repo": "aoa-skills",
                "path": MIGRATION_PATH.as_posix(),
                "source_class": "skill_source",
                "role": "supporting",
                "authority": "authored_control",
            },
        ],
        derived_method=(
            "source-linked route to authored capability families, the exact "
            f"{bundle_summary}, and the legacy functional-disposition map"
        ),
        checked_ref="capabilities/README.md",
        payload_class="node",
        consumer_route="aoa-kag registry and skill host adapters",
    )
    source_node.update(
        {
            "node_kind": "route_surface",
            "label": "canonical capability and callable skill source home",
        }
    )

    return_edge = base_record(
        local_id="edge:skills:capability-returns-to-owner",
        record_class="edge",
        source_refs=[graph_source, capability_owner, skill_owner],
        derived_method=(
            "source-linked return edge from the generated capability projection "
            "to authored capability semantics and owner skill packages"
        ),
        checked_ref=GRAPH_JSON_PATH.as_posix(),
        payload_class="edge",
        consumer_route="aoa-kag registry",
    )
    return_edge.update(
        {
            "from_id": "node:skills:capability-graph",
            "to_id": "node:skills:capability-source-home",
            "edge_kind": "returns_to",
            "edge_trace": (
                "generated/capability_graph.json returns to capabilities/README.md "
                "and authored family sources; callable procedures return to their "
                "owner packages under skills/ rather than to the derived graph"
            ),
        }
    )

    provider_index = base_record(
        local_id="index:skills:capability-provider",
        record_class="index",
        source_refs=[graph_source, capability_owner, skill_owner],
        derived_method=(
            "compact inventory of the semantic capability projection, "
            f"{bundle_summary}, and their authored return routes"
        ),
        checked_ref=GRAPH_JSON_PATH.as_posix(),
        payload_class="index",
        consumer_route="aoa-kag registry",
    )
    provider_index.update(
        {
            "index_kind": "inventory",
            "indexed_record_classes": ["node", "edge"],
            "source_record_ids": [
                "node:skills:capability-graph",
                "node:skills:capability-source-home",
                "edge:skills:capability-returns-to-owner",
            ],
        }
    )

    mcp_projection = base_record(
        local_id="projection:mcp:skills-capability-return",
        record_class="projection",
        source_refs=[
            graph_source,
            capability_owner,
            skill_owner,
            {
                "repo": "aoa-skills",
                "path": "generated/agent_skill_catalog.min.json",
                "source_class": "skill_source",
                "role": "supporting",
                "authority": "derived_readmodel",
            },
        ],
        derived_method=(
            "compact full-contract source-return projection over semantic "
            f"capabilities and {bundle_summary}"
        ),
        checked_ref=GRAPH_JSON_PATH.as_posix(),
        payload_class="projection",
        consumer_route="aoa-kag MCP capability discovery",
    )
    mcp_projection.update(
        {
            "projection_kind": "source_return_view",
            "source_record_ids": [
                "node:skills:capability-graph",
                "node:skills:capability-source-home",
                "edge:skills:capability-returns-to-owner",
                "index:skills:capability-provider",
            ],
            "consumer_shape": (
                "return canonical capability ID; owner repo, ref, path, and "
                "digest; applicability; input and output ABI; tool requirements "
                "and effects; lifecycle and health; compatibility and conflicts; "
                "source-return handle; binding availability; and the required "
                "conditional owner reference, then return to authored sources or "
                f"one of the {bundle_summary} without treating KAG as authority"
            ),
        }
    )

    validation_route = base_record(
        local_id="receipt:validation:skills-capability-provider",
        record_class="receipt",
        source_refs=[
            graph_source,
            capability_owner,
            {
                "repo": "aoa-skills",
                "path": "config/validation_lanes.json",
                "source_class": "validation_source",
                "role": "validation_receipt",
                "authority": "authored_control",
            },
        ],
        derived_method=(
            "deterministic source-linked route record emitted with capability "
            "graph parity; it carries no KAG acceptance or outcome verdict"
        ),
        checked_ref=GRAPH_JSON_PATH.as_posix(),
        payload_class="receipt",
        consumer_route="aoa-kag registry",
        freshness_mode="builder_receipt",
    )
    validation_route.update(
        {
            "receipt_kind": "validation",
            "result": "routed",
            "fallback_route": "scripts/lanes/ci_gate.py --mode source-fast",
        }
    )

    records = {
        KAG_CAPABILITY_GRAPH_NODE_PATH: graph_node,
        KAG_CAPABILITY_SOURCE_NODE_PATH: source_node,
        KAG_CAPABILITY_RETURN_EDGE_PATH: return_edge,
        KAG_PROVIDER_INDEX_PATH: provider_index,
        KAG_MCP_RETURN_PATH: mcp_projection,
        KAG_VALIDATION_ROUTE_RECEIPT_PATH: validation_route,
    }
    return {repo_root / path: dump_json(record) for path, record in records.items()}


def build_graph_outputs(repo_root: Path) -> dict[Path, str]:
    payload = build_graph_payload(repo_root)
    outputs = {
        repo_root / GRAPH_JSON_PATH: dump_json(payload),
        repo_root / GRAPH_MARKDOWN_PATH: render_graph_markdown(payload),
    }
    outputs.update(build_kag_provider_outputs(repo_root, payload))
    return outputs


def load_graph(repo_root: Path) -> dict[str, Any]:
    path = repo_root / GRAPH_JSON_PATH
    if not path.is_file():
        raise CapabilityContractError(
            f"missing {GRAPH_JSON_PATH.as_posix()}; run the capability graph builder first"
        )
    payload = load_json(path)
    schema = load_json(repo_root / GRAPH_SCHEMA_PATH)
    issues = schema_issues(payload, schema)
    if issues:
        raise CapabilityContractError("\n".join(issues))
    return payload


def graph_node_map(graph: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(node["id"]): dict(node) for node in graph.get("nodes", [])}


def graph_relations_from(graph: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    rows: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for raw in graph.get("relations", []):
        relation = dict(raw)
        rows[str(relation["source"])].append(relation)
    for value in rows.values():
        value.sort(key=lambda item: (item["kind"], item["target"]))
    return rows


def graph_relations_to(graph: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    rows: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for raw in graph.get("relations", []):
        relation = dict(raw)
        rows[str(relation["target"])].append(relation)
    for value in rows.values():
        value.sort(key=lambda item: (item["kind"], item["source"]))
    return rows


def discover(
    graph: Mapping[str, Any],
    query: str,
    *,
    limit: int = 8,
    include_internal: bool = True,
    kinds: set[str] | None = None,
    visibilities: set[str] | None = None,
    retrieval_depth: str = "full",
) -> list[dict[str, Any]]:
    if retrieval_depth not in {"compact", "contract", "full"}:
        raise CapabilityContractError(
            "retrieval_depth must be one of: compact, contract, full"
        )
    query_tokens = tokenize(query)
    ordered_query_tokens = tokenize_ordered(query, keep_negative_scope=True)
    query_token_set = set(query_tokens)
    normalized_query = " ".join(query_tokens)
    project_markers = {
        str(node["id"]).split(".", 1)[1]
        for node in graph.get("nodes", [])
        if str(node.get("primary_parent", "")) == "projects"
        and str(node.get("id", "")).startswith("projects.")
        and "." in str(node.get("id", ""))
    }
    results: list[dict[str, Any]] = []
    for document in graph.get("retrieval_documents", []):
        if kinds is not None and document.get("kind") not in kinds:
            continue
        visibility = document.get("visibility")
        if visibilities is not None and visibility not in visibilities:
            continue
        if not include_internal and visibility in {"internal", "hidden"}:
            continue
        title_tokens = set(tokenize(str(document.get("title", ""))))
        id_tokens = set(tokenize(str(document.get("id", ""))))
        routing_tokens = set(document.get("routing_tokens", []))
        positive_tokens = set(document.get("positive_tokens", []))
        negative_tokens = set(document.get("negative_tokens", []))
        negative_only_tokens = negative_tokens - positive_tokens - routing_tokens - title_tokens - id_tokens
        contract_tokens = set(
            document.get("contract_tokens", document.get("tokens", []))
        )
        package_tokens = set(document.get("package_tokens", []))
        all_tokens = set(document.get("tokens", []))
        score = 0.0
        matched: list[str] = []
        negative_matched: list[str] = []
        strongest_match = 0.0
        for token in query_tokens:
            token_score = 0.0
            if token in id_tokens:
                token_score = max(token_score, 6.0)
            if token in title_tokens:
                token_score = max(token_score, 5.0)
            if token in routing_tokens:
                token_score = max(token_score, 4.0)
            if token in positive_tokens:
                token_score = max(token_score, 2.5)
            if retrieval_depth in {"contract", "full"} and token in contract_tokens:
                token_score = max(token_score, 1.0)
            if retrieval_depth == "full" and token in package_tokens:
                token_score = max(token_score, 0.75)
            if retrieval_depth == "full" and token in all_tokens:
                token_score = max(token_score, 0.5)
            if token_score:
                matched.append(token)
                score += token_score
                strongest_match = max(strongest_match, token_score)
            if (
                token in negative_only_tokens
                and token not in NEGATIVE_CONTEXT_TOKENS
            ):
                negative_matched.append(token)
                score -= 3.0
        for negative_phrase in document.get("negative_phrases", []):
            ordered_phrase_tokens = tokenize_ordered(
                str(negative_phrase),
                keep_negative_scope=True,
            )
            phrase_specific_tokens = (
                set(ordered_phrase_tokens) & negative_only_tokens
            )
            overlap = query_token_set & phrase_specific_tokens
            phrase_matches: set[str] = set()
            if (
                len(overlap) >= 2
                and len(overlap) / max(len(phrase_specific_tokens), 1) >= 0.30
            ):
                phrase_matches.update(overlap)
            phrase_matches.update(
                negative_scope_phrase_matches(
                    ordered_query_tokens,
                    ordered_phrase_tokens,
                )
            )
            if phrase_matches:
                negative_matched.extend(phrase_matches)
                score -= 2.5 * len(phrase_matches)
        phrase_match = bool(
            normalized_query and normalized_query in str(document.get("positive_text", "")).lower()
        )
        if phrase_match:
            score += 3.0
        id_overlap = query_token_set & id_tokens
        id_match = bool(
            normalized_query
            and normalized_query == " ".join(tokenize(str(document.get("id", ""))))
        ) or len(id_overlap) >= 2
        document_project_markers = sorted(id_tokens & project_markers)
        project_scope_penalty = 0.0
        if document_project_markers and not query_token_set.intersection(document_project_markers):
            # Project adapters remain discoverable through strong domain terms,
            # but generic session/owner/evidence vocabulary must prefer the
            # reusable family unless the request actually names the project.
            project_scope_penalty = 2.5
            score -= project_scope_penalty
        if score <= 0 or (strongest_match < 4.0 and not id_match and not phrase_match) or (
            len(query_tokens) > 2
            and len(set(matched)) < 2
            and not id_match
            and not phrase_match
        ):
            continue
        if visibility == "advertised":
            score += 0.5
        if document.get("kind") == "capability":
            score += 2.0
        elif document.get("kind") == "mode":
            score += 2.5
        coverage = len(set(matched)) / max(len(query_tokens), 1)
        results.append(
            {
                "id": document["id"],
                "kind": document["kind"],
                "visibility": visibility,
                "title": document["title"],
                "description": document["description"],
                "score": round(score + coverage, 3),
                "matched_tokens": sorted(set(matched)),
                "negative_matched_tokens": sorted(set(negative_matched)),
                "coverage": round(coverage, 3),
                "strongest_match": strongest_match,
                "project_scope": document_project_markers,
                "project_scope_penalty": project_scope_penalty,
            }
        )
    results.sort(key=lambda item: (-item["score"], -item["coverage"], item["id"]))
    if not results or results[0]["score"] < 5.0:
        return []
    confidence_floor = results[0]["score"] * 0.45
    return [item for item in results if item["score"] >= confidence_floor][:limit]


def discover_two_stage(
    graph: Mapping[str, Any],
    query: str,
    *,
    candidate_limit: int = 8,
    rerank_limit: int = 8,
    prompt_visibilities: set[str] | None = None,
) -> dict[str, Any]:
    """Route through the prompt-visible catalogue, then rerank the owner graph.

    The first stage deliberately ignores package bodies and defaults to the
    advertised catalogue.  Loading one of those routers admits the bounded
    owner graph for the second stage, where full contracts and package
    resources may rerank leaves.  This preserves progressive disclosure:
    package-only vocabulary cannot make an unadvertised owner visible from the
    initial prompt, but it can disambiguate leaves after the owner router has
    matched.
    """

    visible = prompt_visibilities or {"advertised"}
    candidate_selection = discover(
        graph,
        query,
        limit=candidate_limit,
        include_internal=False,
        visibilities=visible,
        retrieval_depth="compact",
    )
    deep_results = (
        discover(
            graph,
            query,
            limit=max(rerank_limit * 4, rerank_limit),
            include_internal=True,
            retrieval_depth="full",
        )
        if candidate_selection
        else []
    )
    nodes = graph_node_map(graph)

    def executable_result(item: Mapping[str, Any]) -> bool:
        node = nodes.get(str(item.get("id")))
        if node is not None:
            return node.get("contract_level") == "executable"
        return item.get("kind") in {
            "skill",
            "mode",
            "workflow",
            "tool",
            "guard",
            "adapter",
            "human-gate",
        }

    deep_rerank = [
        item for item in deep_results if executable_result(item)
    ][:rerank_limit]
    deep_branches = [
        item for item in deep_results if not executable_result(item)
    ][:rerank_limit]
    return {
        "schema_version": "aoa-capability-retrieval-v1",
        "query": query,
        "candidate_selection": {
            "scope": "prompt-visible-compact-contracts",
            "retrieval_depth": "compact",
            "visibilities": sorted(visible),
            "candidates": candidate_selection,
        },
        "deep_rerank": {
            "scope": "selected-owner-full-contracts",
            "retrieval_depth": "full",
            "candidates": deep_rerank,
            "branches": deep_branches,
            "all_results": deep_results,
        },
        "owner_admitted": bool(candidate_selection),
        "candidates": deep_rerank,
    }


def _resolve_executable(
    node_id: str,
    nodes: Mapping[str, Mapping[str, Any]],
    relations_from: Mapping[str, Sequence[Mapping[str, Any]]],
) -> tuple[str | None, list[str]]:
    node = nodes[node_id]
    if node.get("contract_level") == "executable":
        return node_id, []
    candidates = [
        str(relation["target"])
        for relation in relations_from.get(node_id, [])
        if relation.get("kind") == "implemented-by"
        and relation.get("target") in nodes
        and nodes[str(relation["target"])].get("lifecycle", {}).get("state") not in {"retired", "deprecated"}
    ]
    if not candidates:
        return None, [f"{node_id}: no active implemented-by binding"]
    if len(candidates) > 1:
        return None, [f"{node_id}: ambiguous implementations: {', '.join(sorted(candidates))}"]
    return candidates[0], []


def _topology_cycle(nodes: Iterable[str], edges: Sequence[Mapping[str, Any]]) -> list[str] | None:
    node_set = set(nodes)
    indegree = {node_id: 0 for node_id in node_set}
    outgoing: defaultdict[str, set[str]] = defaultdict(set)
    for edge in edges:
        source = str(edge["source"])
        target = str(edge["target"])
        if source == target or source not in node_set or target not in node_set:
            continue
        if target not in outgoing[source]:
            outgoing[source].add(target)
            indegree[target] += 1
    queue = deque(sorted(node_id for node_id, degree in indegree.items() if degree == 0))
    visited: list[str] = []
    while queue:
        node_id = queue.popleft()
        visited.append(node_id)
        for target in sorted(outgoing.get(node_id, set())):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if len(visited) == len(node_set):
        return None
    return sorted(node_id for node_id, degree in indegree.items() if degree > 0)


def _dedupe_edges(edges: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str, str]] = set()
    result: list[dict[str, Any]] = []
    for raw in edges:
        edge = dict(raw)
        key = (
            str(edge["kind"]),
            str(edge["source"]),
            str(edge["target"]),
            str(edge.get("artifact_type", "")),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(edge)
    result.sort(key=lambda item: (item["kind"], item["source"], item["target"], item.get("artifact_type", "")))
    return result


def _execution_stages(
    node_ids: Iterable[str],
    edges: Sequence[Mapping[str, Any]],
) -> list[list[str]]:
    node_set = set(node_ids)
    indegree = {node_id: 0 for node_id in node_set}
    outgoing: defaultdict[str, set[str]] = defaultdict(set)
    for edge in edges:
        source = str(edge["source"])
        target = str(edge["target"])
        if source == target or source not in node_set or target not in node_set:
            continue
        if target not in outgoing[source]:
            outgoing[source].add(target)
            indegree[target] += 1
    stages: list[list[str]] = []
    ready = sorted(node_id for node_id, degree in indegree.items() if degree == 0)
    visited: set[str] = set()
    while ready:
        stage = [node_id for node_id in ready if node_id not in visited]
        if not stage:
            break
        stages.append(stage)
        next_ready: set[str] = set()
        for source in stage:
            visited.add(source)
            for target in outgoing.get(source, set()):
                indegree[target] -= 1
                if indegree[target] == 0:
                    next_ready.add(target)
        ready = sorted(next_ready)
    return stages if len(visited) == len(node_set) else []


def build_task_dag(
    graph: Mapping[str, Any],
    *,
    query: str,
    selected_capabilities: Sequence[str],
    external_inputs: Sequence[Mapping[str, str]] = (),
    source_graph_path: str | Path = GRAPH_JSON_PATH,
) -> dict[str, Any]:
    if not query.strip():
        raise CapabilityContractError("task-local DAG query must not be empty")
    selected = list(dict.fromkeys(selected_capabilities))
    if not selected:
        raise CapabilityContractError("at least one capability must be explicitly selected")
    nodes = graph_node_map(graph)
    relations_from = graph_relations_from(graph)
    relations_to = graph_relations_to(graph)
    blockers: list[str] = []
    warnings: list[str] = []
    execution_ids: set[str] = set()
    selected_to_binding: dict[str, str] = {}
    for node_id in selected:
        if node_id not in nodes:
            blockers.append(f"unknown selected capability: {node_id}")
            continue
        resolved, issues = _resolve_executable(node_id, nodes, relations_from)
        blockers.extend(issues)
        if resolved is not None:
            selected_to_binding[node_id] = resolved
            execution_ids.add(resolved)

    edges: list[dict[str, Any]] = []
    verification_by_node: dict[str, str] = {}
    queue = deque(sorted(execution_ids))
    expanded: set[str] = set()
    while queue:
        current = queue.popleft()
        if current in expanded:
            continue
        expanded.add(current)
        for relation in relations_from.get(current, []):
            kind = str(relation.get("kind"))
            if kind not in HARD_DEPENDENCY_RELATIONS:
                continue
            target_id = str(relation["target"])
            resolved, issues = _resolve_executable(target_id, nodes, relations_from)
            blockers.extend(issues)
            if resolved is None:
                continue
            execution_ids.add(resolved)
            queue.append(resolved)
            if kind == "verified-by":
                verification_by_node[current] = resolved
            edges.append(
                {
                    "kind": (
                        "guard"
                        if kind == "guarded-by"
                        else "verification"
                        if kind == "verified-by"
                        else "dependency"
                    ),
                    "source": current if kind == "verified-by" else resolved,
                    "target": resolved if kind == "verified-by" else current,
                }
            )
        for relation in relations_to.get(current, []):
            if relation.get("kind") != "verifies":
                continue
            verifier_id = str(relation["source"])
            resolved, issues = _resolve_executable(
                verifier_id,
                nodes,
                relations_from,
            )
            blockers.extend(issues)
            if resolved is None:
                continue
            execution_ids.add(resolved)
            queue.append(resolved)
            verification_by_node[current] = resolved
            edges.append(
                {
                    "kind": "verification",
                    "source": current,
                    "target": resolved,
                }
            )

    closure_ids = set(selected) | execution_ids
    for relation in graph.get("relations", []):
        source = str(relation["source"])
        target = str(relation["target"])
        if source not in closure_ids or target not in closure_ids:
            continue
        resolved_source = (
            source if source in execution_ids else selected_to_binding.get(source)
        )
        resolved_target = (
            target if target in execution_ids else selected_to_binding.get(target)
        )
        if relation["kind"] == "conflicts-with":
            condition = f" ({relation['condition']})" if relation.get("condition") else ""
            blockers.append(f"conflict: {source} vs {target}{condition}")
        elif relation["kind"] == "incompatible-with-version":
            condition = f" ({relation['condition']})" if relation.get("condition") else ""
            blockers.append(f"version incompatibility: {source} vs {target}{condition}")
        elif relation["kind"] == "alternative-to" and source in selected and target in selected:
            warnings.append(f"alternative modes selected together: {source}, {target}")
        elif (
            relation["kind"] == "hands-off-to"
            and resolved_source in execution_ids
            and resolved_target in execution_ids
        ):
            edges.append(
                {
                    "kind": "handoff",
                    "source": resolved_source,
                    "target": resolved_target,
                }
            )
        elif (
            relation["kind"] in {"verified-by", "verifies"}
            and resolved_source in execution_ids
            and resolved_target in execution_ids
        ):
            if relation["kind"] == "verified-by":
                verification_by_node[resolved_source] = resolved_target
            else:
                verification_by_node[resolved_target] = resolved_source

    execution_nodes: list[dict[str, Any]] = []
    for node_id in sorted(execution_ids):
        node = nodes[node_id]
        binding = dict(node["binding"])
        availability = str(binding["availability"])
        if availability in {"unbound", "dormant"}:
            blockers.append(f"{node_id}: binding availability is {availability} ({binding['ref']})")
        execution_nodes.append(
            {
                "id": node_id,
                "kind": node["kind"],
                "binding": binding,
                "owner": dict(node["owner"]),
                "inputs": list(node["abi"]["inputs"]),
                "outputs": list(node["abi"]["outputs"]),
                "effects": list(node["execution"]["effects"]),
                "verification": list(node["execution"]["verification"]),
                "termination": list(node["execution"]["termination"]),
                "availability": availability,
            }
        )

    normalized_external_inputs: list[dict[str, str]] = []
    for raw_input in external_inputs:
        item = dict(raw_input)
        target = item.get("target")
        port_name = item.get("port")
        if target is not None or port_name is not None:
            if not isinstance(target, str) or not isinstance(port_name, str):
                raise CapabilityContractError("targeted external input requires both target and port")
            target_node = nodes.get(target)
            if target_node is None or target_node.get("contract_level") != "executable":
                raise CapabilityContractError(f"targeted external input references unknown executable node: {target}")
            matches = [
                port
                for port in target_node.get("abi", {}).get("inputs", [])
                if port.get("name") == port_name
            ]
            if len(matches) != 1:
                raise CapabilityContractError(f"{target}: unknown or ambiguous input port '{port_name}'")
            item["type"] = str(matches[0]["type"])
        if not isinstance(item.get("type"), str) or not isinstance(item.get("ref"), str):
            raise CapabilityContractError("external input requires TYPE=REF or NODE::PORT=REF")
        normalized_external_inputs.append(item)

    global_supplied_types = {
        str(item["type"])
        for item in normalized_external_inputs
        if "target" not in item and "port" not in item
    }
    targeted_inputs = {
        (str(item["target"]), str(item["port"]))
        for item in normalized_external_inputs
        if "target" in item and "port" in item
    }
    providers: defaultdict[str, list[str]] = defaultdict(list)
    for node in execution_nodes:
        for output in node["outputs"]:
            providers[str(output["type"])].append(str(node["id"]))

    for node in execution_nodes:
        node_id = str(node["id"])
        required_type_counts: defaultdict[str, int] = defaultdict(int)
        for port in node["inputs"]:
            if port.get("required", False):
                required_type_counts[str(port["type"])] += 1
        for input_port in node["inputs"]:
            required = bool(input_port.get("required", False))
            artifact_type = str(input_port["type"])
            port_name = str(input_port["name"])
            if (node_id, port_name) in targeted_inputs:
                continue
            if artifact_type in global_supplied_types:
                if required_type_counts[artifact_type] > 1:
                    blockers.append(
                        f"{node_id}: global input type '{artifact_type}' is ambiguous across multiple required ports; target each port"
                    )
                continue
            candidates = sorted(provider for provider in providers.get(artifact_type, []) if provider != node_id)
            if not candidates:
                if not required:
                    continue
                blockers.append(
                    f"{node_id}: missing required input type '{artifact_type}' ({input_port['name']})"
                )
                continue
            if len(candidates) > 1:
                if not required:
                    warnings.append(
                        f"{node_id}: optional input '{artifact_type}' has multiple providers and was left unbound: {', '.join(candidates)}"
                    )
                    continue
                blockers.append(
                    f"{node_id}: ambiguous providers for '{artifact_type}': {', '.join(candidates)}"
                )
                continue
            edges.append(
                {
                    "kind": "data",
                    "source": candidates[0],
                    "target": node_id,
                    "artifact_type": artifact_type,
                }
            )

    edges = _dedupe_edges(edges)
    cycle = _topology_cycle(execution_ids, edges)
    if cycle:
        blockers.append(f"task-local dependency cycle: {', '.join(cycle)}")
    execution_stages = _execution_stages(execution_ids, edges)
    checkpoints = [
        {
            "node": str(node["id"]),
            **(
                {"verifier": verification_by_node[str(node["id"])]}
                if str(node["id"]) in verification_by_node
                else {}
            ),
            "criteria": list(node["verification"]),
        }
        for node in execution_nodes
    ]

    source_hash = str(graph.get("source", {}).get("content_hash", ""))
    normalized_source_graph_path = Path(source_graph_path).as_posix()
    identity = {
        "query": query,
        "selected": selected,
        "external_inputs": normalized_external_inputs,
        "source_graph_path": normalized_source_graph_path,
        "source_hash": source_hash,
    }
    plan_id = f"dag-{sha256_bytes(canonical_json(identity).encode('utf-8'))[:16]}"
    payload = {
        "schema_version": DAG_SCHEMA_VERSION,
        "authority": False,
        "plan_id": plan_id,
        "request": {"query": query},
        "source_graph": {
            "path": normalized_source_graph_path,
            "content_hash": source_hash,
        },
        "status": "blocked" if blockers else "ready",
        "selected_capabilities": selected,
        "nodes": execution_nodes,
        "edges": edges,
        "external_inputs": normalized_external_inputs,
        "execution_stages": execution_stages,
        "checkpoints": checkpoints,
        "terminal": {
            "lifetime": "task-local",
            "success_condition": "all selected nodes reached verified terminal conditions",
        },
        "warnings": sorted(set(warnings)),
        "blockers": sorted(set(blockers)),
    }
    return payload


def task_dag_structural_issues(
    payload: Mapping[str, Any],
    schema: Mapping[str, Any],
) -> list[str]:
    """Validate runtime-independent task-DAG structure for every owner."""

    issues = schema_issues(payload, schema)
    node_ids = {str(node["id"]) for node in payload.get("nodes", []) if isinstance(node, Mapping)}
    for edge in payload.get("edges", []):
        if not isinstance(edge, Mapping):
            continue
        if edge.get("source") not in node_ids:
            issues.append(f"edge source does not exist: {edge.get('source')}")
        if edge.get("target") not in node_ids:
            issues.append(f"edge target does not exist: {edge.get('target')}")
    cycle = _topology_cycle(node_ids, payload.get("edges", []))
    if cycle:
        issues.append(f"task-local DAG contains a cycle: {', '.join(cycle)}")
    if payload.get("status") == "ready" and payload.get("blockers"):
        issues.append("ready task-local DAG cannot contain blockers")
    if payload.get("status") == "blocked" and not payload.get("blockers"):
        issues.append("blocked task-local DAG must name at least one blocker")
    if payload.get("schema_version") == DAG_SCHEMA_VERSION:
        staged_ids = [
            str(node_id)
            for stage in payload.get("execution_stages", [])
            for node_id in stage
        ]
        if sorted(staged_ids) != sorted(node_ids):
            issues.append("execution stages must contain every execution node exactly once")
        stage_by_node = {
            str(node_id): stage_index
            for stage_index, stage in enumerate(payload.get("execution_stages", []))
            for node_id in stage
        }
        invalid_stage_edges = sorted(
            {
                (str(edge.get("source")), str(edge.get("target")))
                for edge in payload.get("edges", [])
                if isinstance(edge, Mapping)
                and str(edge.get("source")) in stage_by_node
                and str(edge.get("target")) in stage_by_node
                and stage_by_node[str(edge.get("source"))]
                >= stage_by_node[str(edge.get("target"))]
            }
        )
        for source, target in invalid_stage_edges:
            issues.append(
                "execution stage order violates edge "
                f"{source} -> {target}: source must precede target"
            )
        checkpoint_ids = [
            str(checkpoint.get("node"))
            for checkpoint in payload.get("checkpoints", [])
            if isinstance(checkpoint, Mapping)
        ]
        if sorted(checkpoint_ids) != sorted(node_ids):
            issues.append("checkpoints must cover every execution node exactly once")
    return issues


def validate_task_dag(repo_root: Path, payload: Mapping[str, Any]) -> list[str]:
    schema_path = (
        LEGACY_DAG_SCHEMA_PATH
        if payload.get("schema_version") == "aoa-task-local-dag-v1"
        else DAG_SCHEMA_PATH
    )
    schema = load_json(repo_root / schema_path)
    issues = task_dag_structural_issues(payload, schema)
    graph_path = repo_root / GRAPH_JSON_PATH
    if graph_path.is_file():
        current_graph = load_graph(repo_root)
        current_hash = current_graph.get("source", {}).get("content_hash")
        plan_hash = payload.get("source_graph", {}).get("content_hash")
        if plan_hash != current_hash:
            issues.append(
                f"task-local DAG source graph is stale: plan={plan_hash}, current={current_hash}"
            )
    return issues


def render_task_dag_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        f"# Task-local DAG `{payload['plan_id']}`",
        "",
        f"Status: **{payload['status']}**",
        "",
        f"Request: {payload['request']['query']}",
        "",
        "## Bindings",
        "",
        "| node | kind | owner | availability | effects |",
        "|---|---|---|---|---|",
    ]
    for node in payload["nodes"]:
        lines.append(
            f"| `{node['id']}` | {node['kind']} | {node['owner']['repo']} | {node['availability']} | {', '.join(node['effects'])} |"
        )
    lines.extend(["", "## Edges", ""])
    for edge in payload["edges"]:
        artifact = f" [{edge['artifact_type']}]" if edge.get("artifact_type") else ""
        lines.append(f"- `{edge['source']}` -> `{edge['target']}` ({edge['kind']}{artifact})")
    if payload.get("execution_stages"):
        lines.extend(["", "## Execution stages", ""])
        for index, stage in enumerate(payload["execution_stages"], start=1):
            lines.append(f"{index}. " + ", ".join(f"`{node_id}`" for node_id in stage))
    if payload.get("checkpoints"):
        lines.extend(["", "## Verification checkpoints", ""])
        for checkpoint in payload["checkpoints"]:
            verifier = (
                f" via `{checkpoint['verifier']}`"
                if checkpoint.get("verifier")
                else ""
            )
            lines.append(
                f"- `{checkpoint['node']}`{verifier}: "
                + "; ".join(checkpoint["criteria"])
            )
    if payload["blockers"]:
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {item}" for item in payload["blockers"])
    if payload["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in payload["warnings"])
    return "\n".join(lines) + "\n"
