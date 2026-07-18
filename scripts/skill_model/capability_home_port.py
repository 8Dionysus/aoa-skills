"""Validate and project one repository-owned capability home."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, Sequence

from jsonschema import Draft202012Validator

from export import home_skill_port
from skill_model import capability_system


SCHEMA_VERSION = "aoa_capability_home_port_v1"
CONTRACT_REF = "aoa-skills:schemas/capability-home-port.schema.json"
DEFAULT_MANIFEST = Path("capabilities/port.manifest.json")
PORT_SCHEMA_PATH = Path("schemas/capability-home-port.schema.json")
FAMILY_SCHEMA_PATH = Path("schemas/capability_family.schema.json")
GRAPH_SCHEMA_PATH = Path("schemas/capability_graph.schema.json")
VALIDATOR_PATH = Path("scripts/validation/validate_capability_home_port.py")
CONTRACT_SOURCE_PATHS = (
    PORT_SCHEMA_PATH,
    FAMILY_SCHEMA_PATH,
    GRAPH_SCHEMA_PATH,
    capability_system.LEGACY_DAG_SCHEMA_PATH,
    capability_system.DAG_SCHEMA_PATH,
    Path("scripts/skill_model/capability_system.py"),
    Path("scripts/skill_model/capability_home_port.py"),
    Path("scripts/builders/build_capability_home_projection.py"),
    Path("scripts/runtime/capability_home.py"),
    VALIDATOR_PATH,
)
FORBIDDEN_PORTABLE_LITERALS = ("/srv/AbyssOS", "/home/", "~/.codex")
TRANSIENT_NAMES = {".DS_Store", "__pycache__", ".pytest_cache"}
COMPOSITION_RELATIONS = {
    "requires",
    "produces",
    "consumes",
    "composes-with",
    "conflicts-with",
    "alternative-to",
    "hands-off-to",
    "verifies",
    "specializes",
    "generalizes",
    "adapts",
    "supersedes",
    "incompatible-with-version",
    "guarded-by",
    "verified-by",
}
ABI_RELATIONS = {"produces", "consumes", "hands-off-to"}
MUTATING_EFFECTS = {
    "repo-write",
    "generated-write",
    "external-write",
    "runtime-mutation",
    "human-decision",
}
NETWORK_OR_INSTALL_COMMAND_RE = re.compile(
    r"(?im)^\s*(?:[$>]\s*)?(?:sudo\s+)?"
    r"(?:curl|wget|git\s+clone|pip(?:3)?\s+install|"
    r"python(?:3)?\s+-m\s+pip\s+install|npm\s+(?:install|ci)|"
    r"pnpm\s+(?:install|add)|yarn\s+(?:install|add))\b"
)
EXPLICIT_WRITE_MARKER_RE = re.compile(
    r"(?<![A-Za-z0-9_-])--(?:apply|write(?:-report)?|install|prune|repair)\b"
)
PROJECTION_FIELDS = ("graph_json", "graph_markdown", "router_markdown")
PROJECTION_SCHEMA_DEFS = {
    "graph_json": "projectionJsonPath",
    "graph_markdown": "projectionMarkdownPath",
    "router_markdown": "routerProjectionPath",
}


class CapabilityHomePortError(ValueError):
    """One owner capability source or projection violates the shared contract."""


@dataclass(frozen=True)
class CapabilityHomePort:
    contract_root: Path
    owner_root: Path
    manifest_path: Path
    manifest: dict[str, Any]

    @property
    def owner_repo(self) -> str:
        return str(self.manifest["owner_repo"])

    @property
    def family_root(self) -> Path:
        return Path(self.manifest["source"]["family_root"])

    @property
    def root_id(self) -> str:
        return str(self.manifest["source"]["root_id"])

    @property
    def graph_json(self) -> Path:
        return Path(self.manifest["projection"]["graph_json"])

    @property
    def graph_markdown(self) -> Path:
        return Path(self.manifest["projection"]["graph_markdown"])

    @property
    def router_markdown(self) -> Path:
        return Path(self.manifest["projection"]["router_markdown"])


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _graph_source_content_hash(payload: Mapping[str, Any]) -> str:
    source_identity = {
        key: value
        for key, value in payload["source"].items()
        if key != "content_hash"
    }
    package_identity = [
        {
            "id": str(node["id"]),
            "fingerprint": str(node["package"]["fingerprint"]),
        }
        for node in payload["nodes"]
        if isinstance(node.get("package"), Mapping)
    ]
    return _sha256(
        _canonical_json(
            {
                "source": source_identity,
                "skill_packages": package_identity,
            }
        ).encode("utf-8")
    )


def _inside(root: Path, relative: Path, *, label: str) -> Path:
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise CapabilityHomePortError(f"{label} must be a confined relative path: {relative}")
    root_resolved = root.resolve()
    candidate = root_resolved / relative
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise CapabilityHomePortError(f"{label} resolves outside owner root: {relative}") from exc
    current = root_resolved
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise CapabilityHomePortError(f"{label} path component is a symlink: {relative}")
    return candidate


def _schema_errors(payload: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for error in sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda item: list(item.absolute_path),
    ):
        location = "/".join(map(str, error.absolute_path)) or "<root>"
        errors.append(f"{location}: {error.message}")
    return errors


def _projection_output_paths(port: CapabilityHomePort) -> dict[str, Path]:
    """Resolve distinct confined read-model outputs before any builder work."""

    schema = capability_system.load_json(port.contract_root / PORT_SCHEMA_PATH)
    paths = {
        field: _inside(
            port.owner_root,
            Path(str(port.manifest["projection"][field])),
            label=f"projection.{field}",
        )
        for field in PROJECTION_FIELDS
    }
    relative_paths = {
        field: path.relative_to(port.owner_root.resolve()).as_posix()
        for field, path in paths.items()
    }
    for field, relative in relative_paths.items():
        pattern = schema["$defs"][PROJECTION_SCHEMA_DEFS[field]]["allOf"][1][
            "pattern"
        ]
        if re.fullmatch(str(pattern), relative) is None:
            raise CapabilityHomePortError(
                f"projection.{field} must be a generated/read-model path: "
                f"{relative}"
            )
    collisions: dict[str, list[str]] = {}
    for field, relative in relative_paths.items():
        collisions.setdefault(relative, []).append(field)
    duplicated = {
        relative: fields
        for relative, fields in collisions.items()
        if len(fields) > 1
    }
    if duplicated:
        details = "; ".join(
            f"{relative}: {', '.join(sorted(fields))}"
            for relative, fields in sorted(duplicated.items())
        )
        raise CapabilityHomePortError(
            f"projection outputs must be distinct read models: {details}"
        )
    return paths


def load_port(
    contract_root: str | Path,
    owner_root: str | Path,
    manifest_path: str | Path = DEFAULT_MANIFEST,
) -> CapabilityHomePort:
    contract = Path(contract_root).resolve()
    owner = Path(owner_root).resolve()
    manifest_relative = Path(manifest_path)
    manifest_file = _inside(owner, manifest_relative, label="capability manifest")
    if not manifest_file.is_file():
        raise CapabilityHomePortError(f"capability manifest is missing: {manifest_file}")
    payload = json.loads(manifest_file.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise CapabilityHomePortError("capability manifest must be a JSON object")
    schema = capability_system.load_json(contract / PORT_SCHEMA_PATH)
    issues = _schema_errors(payload, schema)
    if issues:
        raise CapabilityHomePortError("\n".join(issues))
    for field in ("owner_ref", "admission_ref", "skill_home_ref"):
        path = _inside(owner, Path(str(payload[field])), label=field)
        if not path.is_file():
            issues.append(f"{field} does not exist: {payload[field]}")
    eval_ref = payload.get("eval_port_ref")
    if isinstance(eval_ref, str):
        path = _inside(owner, Path(eval_ref), label="eval_port_ref")
        if not path.is_file():
            issues.append(f"eval_port_ref does not exist: {eval_ref}")
    if issues:
        raise CapabilityHomePortError("\n".join(issues))
    port = CapabilityHomePort(contract, owner, manifest_file, payload)
    _projection_output_paths(port)
    return port


def load_families(port: CapabilityHomePort) -> list[tuple[Path, dict[str, Any]]]:
    root = _inside(port.owner_root, port.family_root, label="source.family_root")
    if not root.is_dir():
        raise CapabilityHomePortError(f"capability family root is missing: {port.family_root}")
    paths = sorted(root.glob("*.yaml"))
    if not paths:
        raise CapabilityHomePortError("capability family root contains no YAML sources")
    schema = capability_system.load_json(port.contract_root / FAMILY_SCHEMA_PATH)
    families: list[tuple[Path, dict[str, Any]]] = []
    issues: list[str] = []
    for path in paths:
        payload = capability_system.load_yaml(path)
        for issue in capability_system.schema_issues(payload, schema):
            issues.append(f"{path.relative_to(port.owner_root).as_posix()}: {issue}")
        families.append((path, payload))
    if issues:
        raise CapabilityHomePortError("\n".join(issues))
    return families


def _package_snapshot(
    port: CapabilityHomePort,
    package_root: Path,
) -> tuple[list[dict[str, Any]], str, list[str]]:
    issues: list[str] = []
    rows: list[dict[str, Any]] = []
    generated_projection_paths = {
        str(port.manifest["projection"][field])
        for field in PROJECTION_FIELDS
    }
    if package_root.is_symlink() or not package_root.is_dir():
        return [], "", [f"skill package is missing or symlinked: {package_root}"]
    for path in sorted(package_root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(package_root)
        if path.is_symlink():
            issues.append(f"{package_root.name}: package contains symlink {relative}")
            continue
        if any(part in TRANSIENT_NAMES for part in relative.parts) or path.suffix == ".pyc":
            issues.append(f"{package_root.name}: package contains transient entry {relative}")
            continue
        if path.is_dir():
            continue
        if not path.is_file():
            issues.append(f"{package_root.name}: package contains non-regular entry {relative}")
            continue
        repo_relative = path.relative_to(port.owner_root).as_posix()
        if repo_relative in generated_projection_paths:
            continue
        raw = path.read_bytes()
        rows.append(
            {
                "path": repo_relative,
                "sha256": _sha256(raw),
                "bytes": len(raw),
                "executable": bool(path.stat().st_mode & 0o111),
            }
        )
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for forbidden in FORBIDDEN_PORTABLE_LITERALS:
            if forbidden in text:
                issues.append(
                    f"{repo_relative}: portable skill package contains host literal {forbidden!r}"
                )
    identity = [
        {
            "path": row["path"],
            "sha256": row["sha256"],
            "executable": row["executable"],
        }
        for row in rows
    ]
    return rows, _sha256(_canonical_json(identity).encode("utf-8")), issues


def _package_behavior_issues(
    port: CapabilityHomePort,
    node_id: str,
    node: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
) -> list[str]:
    issues: list[str] = []
    package_texts: list[str] = []
    for row in rows:
        path = port.owner_root / str(row["path"])
        try:
            package_texts.append(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
    package_text = "\n".join(package_texts)
    security = node.get("security", {})
    effects = set(node.get("execution", {}).get("effects", []))
    mutation = node.get("mutation")
    if (
        isinstance(security, Mapping)
        and security.get("network") == "forbidden"
        and NETWORK_OR_INSTALL_COMMAND_RE.search(package_text)
    ):
        issues.append(
            f"{node_id}: package contains a network or install command while network is forbidden"
        )
    if EXPLICIT_WRITE_MARKER_RE.search(package_text) and not effects.intersection(
        MUTATING_EFFECTS
    ):
        issues.append(
            f"{node_id}: package exposes an explicit write/apply marker but declares no mutating effect"
        )
    if effects.intersection(MUTATING_EFFECTS) and not isinstance(mutation, Mapping):
        issues.append(
            f"{node_id}: package mutation surface lacks preview/apply/recovery contract"
        )
    return issues


def _port_types(node: Mapping[str, Any], direction: str) -> set[str]:
    return {
        str(port["type"])
        for port in node.get("abi", {}).get(direction, [])
        if isinstance(port, Mapping) and isinstance(port.get("type"), str)
    }


def _dependency_cycle(
    node_ids: Iterable[str],
    relations: Sequence[Mapping[str, Any]],
) -> list[str] | None:
    edges: list[dict[str, str]] = []
    for relation in relations:
        kind = str(relation.get("kind"))
        if kind in {
            "requires",
            "guarded-by",
            "hands-off-to",
            "verified-by",
            "verifies",
        }:
            source = str(relation["source"])
            target = str(relation["target"])
            if kind in {"requires", "guarded-by", "verifies"}:
                source, target = target, source
            edges.append({"source": source, "target": target})
    return capability_system._topology_cycle(node_ids, edges)


def semantic_issues(
    port: CapabilityHomePort,
    families: Sequence[tuple[Path, Mapping[str, Any]]],
) -> list[str]:
    issues = capability_system.semantic_issues(
        port.owner_root,
        families,
        expected_root=port.root_id,
    )
    nodes = capability_system.node_map(families)
    relations = capability_system.relation_rows(families)
    for path, family in families:
        family_owner = family.get("owner", {})
        if family_owner.get("repo") != port.owner_repo:
            issues.append(
                f"{path.relative_to(port.owner_root)}: family owner must be {port.owner_repo!r}"
            )
    for node_id, node in sorted(nodes.items()):
        if node.get("owner", {}).get("repo") != port.owner_repo:
            issues.append(f"{node_id}: node owner must be {port.owner_repo!r}")
        if node.get("contract_level") != "executable":
            continue
        for field in ("classification", "procedure", "security"):
            if not isinstance(node.get(field), Mapping):
                issues.append(f"{node_id}: owner executable contract requires {field}")
        if not isinstance(node.get("purpose"), str) or not str(node["purpose"]).strip():
            issues.append(f"{node_id}: owner executable contract requires purpose")
        binding = node.get("binding", {})
        procedure = node.get("procedure", {})
        binding_ref = str(binding.get("ref", "")).split("#", 1)[0]
        if isinstance(procedure, Mapping) and procedure.get("ref") != binding_ref:
            issues.append(
                f"{node_id}: procedure.ref must equal the bound owner source {binding_ref!r}"
            )
        if binding_ref:
            procedure_path = _inside(
                port.owner_root,
                Path(binding_ref),
                label=f"{node_id}.procedure.ref",
            )
            if procedure_path.is_file() and isinstance(procedure, Mapping):
                text = procedure_path.read_text(encoding="utf-8")
                for section in procedure.get("required_sections", []):
                    if re.search(
                        rf"^#{{1,4}}\s+{re.escape(str(section))}\s*$",
                        text,
                        flags=re.MULTILINE | re.IGNORECASE,
                    ) is None:
                        issues.append(
                            f"{node_id}: required procedure section is missing: {section}"
                        )
        effects = set(node.get("execution", {}).get("effects", []))
        mutation = node.get("mutation")
        if effects & MUTATING_EFFECTS:
            if not isinstance(mutation, Mapping):
                issues.append(f"{node_id}: mutating executable requires mutation contract")
            elif mutation.get("explicit_apply_required") is not True:
                issues.append(f"{node_id}: mutating executable must require explicit apply")
        elif mutation is not None:
            issues.append(f"{node_id}: read-only executable must not declare mutation")
        security = node.get("security")
        if isinstance(security, Mapping):
            network = security.get("network")
            if network == "forbidden" and any(
                requirement in {"network", "internet", "http", "https"}
                for requirement in node.get("execution", {}).get("tool_requirements", [])
            ):
                issues.append(f"{node_id}: network requirement conflicts with forbidden posture")

    relation_pairs = {
        (str(row["kind"]), str(row["source"]), str(row["target"]))
        for row in relations
    }
    for relation in relations:
        kind = str(relation["kind"])
        source_id = str(relation["source"])
        target_id = str(relation["target"])
        if kind in COMPOSITION_RELATIONS and not str(relation.get("condition", "")).strip():
            issues.append(
                f"{relation['source_path']}: {kind} relation {source_id}->{target_id} requires a compatibility condition"
            )
        if source_id not in nodes or target_id not in nodes:
            continue
        source = nodes[source_id]
        target = nodes[target_id]
        if (
            kind in ABI_RELATIONS
            and source.get("contract_level") == "executable"
            and target.get("contract_level") == "executable"
        ):
            overlap = _port_types(source, "outputs") & _port_types(target, "inputs")
            if not overlap:
                issues.append(
                    f"{source_id}->{target_id}: {kind} relation has no output/input ABI intersection"
                )
        inverse = {
            "conflicts-with": "conflicts-with",
            "alternative-to": "alternative-to",
            "specializes": "generalizes",
            "generalizes": "specializes",
        }.get(kind)
        if inverse and (inverse, target_id, source_id) not in relation_pairs:
            issues.append(
                f"{source_id}->{target_id}: {kind} relation lacks inverse {inverse}"
            )
    cycle = _dependency_cycle(nodes, relations)
    if cycle:
        issues.append("hard dependency/handoff graph contains a cycle: " + ", ".join(cycle))

    physical_skills = {
        path.parent.name
        for path in (port.owner_root / "skills").glob("*/SKILL.md")
        if path.is_file()
    }
    skill_nodes: dict[str, Mapping[str, Any]] = {}
    for node_id, node in nodes.items():
        if node.get("kind") != "skill":
            continue
        ref = str(node.get("binding", {}).get("ref", "")).split("#", 1)[0]
        if ref.startswith("skills/") and ref.endswith("/SKILL.md"):
            skill_nodes[Path(ref).parent.name] = node
    if physical_skills != set(skill_nodes):
        missing = sorted(physical_skills - set(skill_nodes))
        extra = sorted(set(skill_nodes) - physical_skills)
        if missing:
            issues.append("skill packages missing capability nodes: " + ", ".join(missing))
        if extra:
            issues.append("capability skill nodes missing packages: " + ", ".join(extra))

    skill_port = home_skill_port.load_port_definition(
        port.owner_root,
        port.manifest["skill_home_ref"],
    )
    if skill_port.owner_repo != port.owner_repo:
        issues.append("skill home and capability home owner_repo differ")
    advertised_by_port = {bundle.name: bundle for bundle in skill_port.bundles}
    advertised_by_capability = {
        name: node
        for name, node in skill_nodes.items()
        if node.get("lifecycle", {}).get("visibility") == "advertised"
    }
    if set(advertised_by_port) != set(advertised_by_capability):
        issues.append(
            "advertised skill-home bundles and capability nodes differ: "
            f"port={sorted(advertised_by_port)}, capability={sorted(advertised_by_capability)}"
        )
    for name in sorted(set(advertised_by_port) & set(advertised_by_capability)):
        if (
            advertised_by_port[name].version
            != advertised_by_capability[name].get("lifecycle", {}).get("version")
        ):
            issues.append(f"{name}: skill-home and capability versions differ")

    parent_owner = str(port.manifest["federation"]["parent_owner"])
    parent_node = str(port.manifest["federation"]["parent_node"])
    central_graph_path = port.contract_root / capability_system.GRAPH_JSON_PATH
    if parent_owner == "aoa-skills" and central_graph_path.is_file():
        central_nodes = capability_system.graph_node_map(
            capability_system.load_graph(port.contract_root)
        )
        if parent_node not in central_nodes:
            issues.append(f"federation parent does not exist in aoa-skills graph: {parent_node}")

    return issues


def validate_sources(
    port: CapabilityHomePort,
) -> list[tuple[Path, dict[str, Any]]]:
    families = load_families(port)
    issues = semantic_issues(port, families)
    nodes = capability_system.node_map(families)
    for node_id, node in sorted(nodes.items()):
        if node.get("kind") != "skill":
            continue
        ref = str(node.get("binding", {}).get("ref", "")).split("#", 1)[0]
        if not ref.startswith("skills/"):
            continue
        rows, _, package_issues = _package_snapshot(
            port,
            port.owner_root / Path(ref).parent,
        )
        issues.extend(package_issues)
        issues.extend(
            _package_behavior_issues(
                port,
                node_id,
                node,
                rows,
            )
        )
    if issues:
        raise CapabilityHomePortError("\n".join(issues))
    return families


def _contract_source_metadata(port: CapabilityHomePort) -> dict[str, Any]:
    schema_path = port.contract_root / FAMILY_SCHEMA_PATH
    validator_path = port.contract_root / VALIDATOR_PATH
    contract_files = [
        {
            "path": path.as_posix(),
            "sha256": _sha256((port.contract_root / path).read_bytes()),
        }
        for path in CONTRACT_SOURCE_PATHS
    ]
    return {
        "port_manifest": {
            "path": port.manifest_path.relative_to(port.owner_root).as_posix(),
            "sha256": _sha256(port.manifest_path.read_bytes()),
        },
        "contract": {
            "owner_repo": "aoa-skills",
            "schema_path": FAMILY_SCHEMA_PATH.as_posix(),
            "schema_sha256": _sha256(schema_path.read_bytes()),
            "validator_path": VALIDATOR_PATH.as_posix(),
            "validator_sha256": _sha256(validator_path.read_bytes()),
            "contract_files": contract_files,
        },
    }


def build_graph(port: CapabilityHomePort) -> dict[str, Any]:
    families = validate_sources(port)
    payload = capability_system.build_graph_payload(
        port.owner_root,
        families=families,
        family_root=port.family_root,
        graph_schema_path=port.contract_root / GRAPH_SCHEMA_PATH,
        source_metadata=_contract_source_metadata(port),
        include_retrieval_depth_tokens=True,
    )
    referenced = {
        str(row["path"]): dict(row)
        for row in payload["source"]["referenced_files"]
    }
    retrieval = {
        str(row["id"]): row for row in payload["retrieval_documents"]
    }
    for node in payload["nodes"]:
        if node.get("kind") != "skill":
            continue
        ref = str(node.get("binding", {}).get("ref", "")).split("#", 1)[0]
        if not ref.startswith("skills/"):
            continue
        rows, fingerprint, issues = _package_snapshot(
            port,
            port.owner_root / Path(ref).parent,
        )
        if issues:
            raise CapabilityHomePortError("\n".join(issues))
        node["package"] = {
            "version": node["lifecycle"]["version"],
            "fingerprint": fingerprint,
            "files": rows,
        }
        supplemental: list[str] = []
        for row in rows:
            referenced[str(row["path"])] = {
                "path": str(row["path"]),
                "sha256": str(row["sha256"]),
            }
            path = port.owner_root / str(row["path"])
            if path.suffix.lower() in {".md", ".yaml", ".yml", ".json", ".txt"}:
                supplemental.append(path.read_text(encoding="utf-8"))
        document = retrieval.get(str(node["id"]))
        if document is not None:
            package_text = "\n".join(supplemental)
            document["search_text"] = document["search_text"] + "\n" + package_text
            document["package_tokens"] = capability_system.tokenize(package_text)
            document["tokens"] = capability_system.tokenize(document["search_text"])
    payload["source"]["referenced_files"] = sorted(
        referenced.values(),
        key=lambda item: str(item["path"]),
    )
    payload["source"]["content_hash"] = _graph_source_content_hash(payload)
    graph_schema = capability_system.load_json(port.contract_root / GRAPH_SCHEMA_PATH)
    issues = capability_system.schema_issues(payload, graph_schema)
    if issues:
        raise CapabilityHomePortError(
            "owner capability graph violates shared schema:\n" + "\n".join(issues)
        )
    return payload


def render_router_markdown(
    port: CapabilityHomePort,
    graph: Mapping[str, Any],
) -> str:
    rows = [
        node
        for node in graph["nodes"]
        if node.get("kind") == "skill"
    ]
    rows.sort(
        key=lambda node: (
            node.get("lifecycle", {}).get("visibility") != "advertised",
            str(node["id"]),
        )
    )
    lines = [
        f"# {port.owner_repo} capability router",
        "",
        "Generated from owner capability contracts. This card is a retrieval read model, not procedure or proof authority.",
        "",
        f"Source graph hash: `{graph['source']['content_hash']}`",
        (
            "Federation: "
            f"`{port.root_id}` {port.manifest['federation']['relation']} "
            f"`{port.manifest['federation']['parent_owner']}:{port.manifest['federation']['parent_node']}`."
        ),
        "",
        "| skill | visibility | use when | do not use when | version | fingerprint |",
        "|---|---|---|---|---|---|",
    ]
    for node in rows:
        applicability = node.get("applicability", {})
        use_when = "; ".join(applicability.get("use_when", []))
        do_not = "; ".join(applicability.get("do_not_use_when", []))
        package = node.get("package", {})
        lines.append(
            f"| `{str(node['id']).removeprefix('skill.')}` | "
            f"{node['lifecycle']['visibility']} | {use_when} | {do_not} | "
            f"{node['lifecycle']['version']} | `{str(package.get('fingerprint', ''))[:16]}` |"
        )
    lines.extend(
        [
            "",
            "Load the named `SKILL.md` for procedure. Use the full generated graph for ABI, effects, failures, relations, and composition; do not infer invocation or benefit from selection alone.",
            "",
        ]
    )
    return "\n".join(lines)


def build_outputs(port: CapabilityHomePort) -> dict[Path, str]:
    paths = _projection_output_paths(port)
    graph = build_graph(port)
    return {
        paths["graph_json"]: capability_system.dump_json(graph),
        paths["graph_markdown"]: capability_system.render_graph_markdown(graph),
        paths["router_markdown"]: render_router_markdown(port, graph),
    }


def generated_issues(port: CapabilityHomePort) -> list[str]:
    return [
        path.relative_to(port.owner_root).as_posix()
        for path, expected in build_outputs(port).items()
        if not path.is_file() or path.read_text(encoding="utf-8") != expected
    ]


def write_outputs(port: CapabilityHomePort) -> list[str]:
    written: list[str] = []
    for path, text in build_outputs(port).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        written.append(path.relative_to(port.owner_root).as_posix())
    return written


def load_owner_graph(port: CapabilityHomePort) -> dict[str, Any]:
    path = port.owner_root / port.graph_json
    if not path.is_file():
        raise CapabilityHomePortError(f"owner graph is missing: {port.graph_json}")
    payload = capability_system.load_json(path)
    schema = capability_system.load_json(port.contract_root / GRAPH_SCHEMA_PATH)
    issues = capability_system.schema_issues(payload, schema)
    if issues:
        raise CapabilityHomePortError("\n".join(issues))
    return payload


def validate_task_dag(
    port: CapabilityHomePort,
    graph: Mapping[str, Any],
    payload: Mapping[str, Any],
) -> list[str]:
    schema_path = (
        capability_system.LEGACY_DAG_SCHEMA_PATH
        if payload.get("schema_version") == "aoa-task-local-dag-v1"
        else capability_system.DAG_SCHEMA_PATH
    )
    schema = capability_system.load_json(port.contract_root / schema_path)
    issues = capability_system.task_dag_structural_issues(payload, schema)
    if payload.get("source_graph", {}).get("content_hash") != graph.get("source", {}).get(
        "content_hash"
    ):
        issues.append("task-local DAG source hash does not match owner graph")
    if payload.get("source_graph", {}).get("path") != port.graph_json.as_posix():
        issues.append("task-local DAG source path does not match owner graph")
    return issues
