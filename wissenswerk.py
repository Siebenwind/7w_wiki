#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = REPO_ROOT / "wissenswerk.yaml"
DEFAULT_DESIGN = REPO_ROOT / "DESIGN.md"
DEFAULT_MANIFEST = REPO_ROOT / "project_manifest.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def load_json_like(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{path.name} must be JSON-compatible YAML for this dependency-light bootstrap slice: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must contain an object at the top level")
    return payload


def load_config(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    return load_json_like(path)


def repo_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_report(config: dict[str, Any], name: str, payload: dict[str, Any]) -> Path:
    reports_dir = repo_path(config.get("paths", {}).get("reports", "Logs/Wissenswerk"))
    ensure_dir(reports_dir)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_path = reports_dir / f"{stamp}_{name}.json"
    report_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report_path


def default_config_payload() -> dict[str, Any]:
    return {
        "schema_version": "wissenswerk.config.v1",
        "project": {
            "name": "Example Corpus",
            "product": "Wissenswerk",
            "language": "de",
            "tenant_id": "example",
        },
        "paths": {
            "sources": ["corpus"],
            "wiki": "docs/Wiki",
            "reports": "Logs/Wissenswerk",
            "ragprep_imports": ".agent/data/wissenswerk/ragprep_imports",
            "runtime_state": ".agent/data/wissenswerk/state",
        },
        "source_precedence": ["Primary Sources", "Derived Notes", "Wiki Pages"],
        "automation": {
            "auto_apply": True,
            "write_reports": True,
            "require_provenance": True,
            "rollback_hint": True,
        },
        "providers": {
            "chat": {
                "kind": "openai-compatible",
                "base_url": "https://api.openai.com/v1",
                "api_key_env": "OPENAI_API_KEY",
                "model": "gpt-5.4",
            },
            "summary": {
                "kind": "openai-compatible",
                "base_url": "https://api.openai.com/v1",
                "api_key_env": "OPENAI_API_KEY",
                "model": "gpt-5.4-mini",
            },
            "embedding": {
                "kind": "openai-compatible",
                "base_url": "https://api.openai.com/v1",
                "api_key_env": "OPENAI_API_KEY",
                "model": "text-embedding-3-large",
            },
        },
        "vector_store": {
            "kind": "pgvector",
            "dsn_env": "WISSENSWERK_DATABASE_URL",
            "schema": "wissenswerk",
            "collection": "example",
        },
        "ragprep": {
            "accepted_extensions": [".json", ".jsonl"],
            "required_fields": ["document_id", "chunk_id", "text", "source_path"],
            "optional_fields": ["title", "section", "language", "hash", "entities", "summary"],
        },
    }


def command_init(args: argparse.Namespace) -> int:
    target = repo_path(args.config)
    if target.exists() and not args.force:
        payload = {"status": "exists", "config": rel(target), "changed": False}
        json_print(payload) if args.json else print(f"{rel(target)} already exists")
        return 0
    target.write_text(json.dumps(default_config_payload(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    payload = {"status": "created", "config": rel(target), "changed": True}
    json_print(payload) if args.json else print(f"Created {rel(target)}")
    return 0


def provider_status(config: dict[str, Any]) -> dict[str, Any]:
    providers = config.get("providers", {})
    checks = []
    for name, provider in sorted(providers.items()):
        key_env = provider.get("api_key_env", "")
        checks.append(
            {
                "name": name,
                "kind": provider.get("kind", ""),
                "base_url": provider.get("base_url", ""),
                "model": provider.get("model", ""),
                "api_key_env": key_env,
                "env_present": bool(key_env and os.environ.get(key_env)),
                "status": "configured" if provider.get("base_url") and provider.get("model") else "incomplete",
            }
        )
    vector = config.get("vector_store", {})
    dsn_env = vector.get("dsn_env", "")
    return {
        "status": "ok",
        "providers": checks,
        "vector_store": {
            "kind": vector.get("kind", ""),
            "dsn_env": dsn_env,
            "env_present": bool(dsn_env and os.environ.get(dsn_env)),
            "schema": vector.get("schema", ""),
            "collection": vector.get("collection", ""),
        },
    }


def command_providers_check(args: argparse.Namespace) -> int:
    payload = provider_status(load_config(repo_path(args.config)))
    json_print(payload) if args.json else print_provider_status(payload)
    return 0


def print_provider_status(payload: dict[str, Any]) -> None:
    print("Wissenswerk provider status")
    for provider in payload["providers"]:
        env = "present" if provider["env_present"] else "missing"
        print(f"- {provider['name']}: {provider['kind']} {provider['model']} ({env})")
    vector = payload["vector_store"]
    env = "present" if vector["env_present"] else "missing"
    print(f"- vector_store: {vector['kind']} schema={vector['schema']} ({env})")


def parse_design_file(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError("DESIGN.md must start with YAML front matter")
    end = raw.find("\n---", 3)
    if end == -1:
        raise ValueError("DESIGN.md front matter is not closed")
    frontmatter = raw[3:end].strip()
    body = raw[end + 4 :].lstrip()
    try:
        tokens = json.loads(frontmatter)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "This bootstrap linter expects JSON-compatible YAML front matter in DESIGN.md"
        ) from exc
    if not isinstance(tokens, dict):
        raise ValueError("DESIGN.md front matter must contain an object")
    return tokens, body


def resolve_token(tokens: dict[str, Any], value: Any) -> Any:
    if not isinstance(value, str):
        return value
    match = re.fullmatch(r"\{([^}]+)\}", value.strip())
    if not match:
        return value
    current: Any = tokens
    for part in match.group(1).split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(match.group(1))
        current = current[part]
    return current


def _hex_to_rgb(value: str) -> tuple[float, float, float] | None:
    if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        return None
    return tuple(int(value[i : i + 2], 16) / 255.0 for i in (1, 3, 5))


def _linear(channel: float) -> float:
    return channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4


def contrast_ratio(fg: str, bg: str) -> float | None:
    fg_rgb = _hex_to_rgb(fg)
    bg_rgb = _hex_to_rgb(bg)
    if fg_rgb is None or bg_rgb is None:
        return None
    fg_lum = 0.2126 * _linear(fg_rgb[0]) + 0.7152 * _linear(fg_rgb[1]) + 0.0722 * _linear(fg_rgb[2])
    bg_lum = 0.2126 * _linear(bg_rgb[0]) + 0.7152 * _linear(bg_rgb[1]) + 0.0722 * _linear(bg_rgb[2])
    lighter = max(fg_lum, bg_lum)
    darker = min(fg_lum, bg_lum)
    return (lighter + 0.05) / (darker + 0.05)


def lint_design(path: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    try:
        tokens, body = parse_design_file(path)
    except Exception as exc:
        return {
            "status": "fail",
            "path": rel(path),
            "findings": [{"severity": "error", "message": str(exc)}],
            "summary": {"errors": 1, "warnings": 0, "info": 0},
        }

    required = ["name", "colors", "typography", "spacing", "components"]
    for key in required:
        if key not in tokens:
            findings.append({"severity": "error", "path": key, "message": f"Missing token section: {key}"})

    if "primary" not in tokens.get("colors", {}):
        findings.append({"severity": "warning", "path": "colors.primary", "message": "Missing primary color token"})

    section_order = [
        "Overview",
        "Colors",
        "Typography",
        "Layout",
        "Elevation & Depth",
        "Shapes",
        "Components",
        "Do's and Don'ts",
    ]
    positions = []
    for section in section_order:
        match = re.search(rf"^##\s+{re.escape(section)}\s*$", body, re.MULTILINE)
        if match:
            positions.append((section, match.start()))
    if positions != sorted(positions, key=lambda item: item[1]):
        findings.append({"severity": "error", "path": "sections", "message": "DESIGN.md sections are out of order"})

    seen_sections: set[str] = set()
    for match in re.finditer(r"^##\s+(.+?)\s*$", body, re.MULTILINE):
        section = match.group(1).strip()
        if section in seen_sections:
            findings.append({"severity": "error", "path": f"section.{section}", "message": "Duplicate section heading"})
        seen_sections.add(section)

    for component_name, component in tokens.get("components", {}).items():
        if not isinstance(component, dict):
            continue
        try:
            bg = resolve_token(tokens, component.get("backgroundColor"))
            fg = resolve_token(tokens, component.get("textColor"))
        except KeyError as exc:
            findings.append(
                {
                    "severity": "error",
                    "path": f"components.{component_name}",
                    "message": f"Broken token reference: {exc}",
                }
            )
            continue
        ratio = contrast_ratio(str(fg), str(bg))
        if ratio is not None and ratio < 4.5:
            findings.append(
                {
                    "severity": "warning",
                    "path": f"components.{component_name}",
                    "message": f"Contrast ratio {ratio:.2f}:1 is below WCAG AA.",
                }
            )

    findings.append(
        {
            "severity": "info",
            "path": "tokens",
            "message": (
                f"colors={len(tokens.get('colors', {}))}, "
                f"typography={len(tokens.get('typography', {}))}, "
                f"components={len(tokens.get('components', {}))}"
            ),
        }
    )
    errors = sum(1 for finding in findings if finding["severity"] == "error")
    warnings = sum(1 for finding in findings if finding["severity"] == "warning")
    info = sum(1 for finding in findings if finding["severity"] == "info")
    return {
        "status": "fail" if errors else "pass",
        "path": rel(path),
        "findings": findings,
        "summary": {"errors": errors, "warnings": warnings, "info": info},
    }


def command_design_lint(args: argparse.Namespace) -> int:
    payload = lint_design(repo_path(args.file))
    json_print(payload) if args.json else print_design_lint(payload)
    return 1 if payload["summary"]["errors"] else 0


def print_design_lint(payload: dict[str, Any]) -> None:
    print(f"DESIGN.md lint: {payload['status']}")
    for finding in payload["findings"]:
        print(f"- {finding['severity']}: {finding.get('path', '-')}: {finding['message']}")


def iter_ragprep_records(import_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    files = sorted([p for p in import_dir.rglob("*") if p.suffix.lower() in {".json", ".jsonl"}])
    for file_path in files:
        if file_path.suffix.lower() == ".jsonl":
            for line_no, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
                if not line.strip():
                    continue
                item = json.loads(line)
                if isinstance(item, dict):
                    item["_ragprep_file"] = rel(file_path)
                    item["_ragprep_line"] = line_no
                    records.append(item)
            continue
        payload = json.loads(file_path.read_text(encoding="utf-8"))
        items: list[Any]
        if isinstance(payload, dict) and isinstance(payload.get("chunks"), list):
            items = payload["chunks"]
        elif isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            items = [payload]
        else:
            items = []
        for item in items:
            if isinstance(item, dict):
                item["_ragprep_file"] = rel(file_path)
                records.append(item)
    return records


def normalize_chunk(record: dict[str, Any], default_language: str) -> dict[str, Any]:
    text = str(record.get("text") or record.get("content") or record.get("chunk_text") or "")
    source_path = str(record.get("source_path") or record.get("path") or record.get("source") or "")
    document_id = str(record.get("document_id") or record.get("doc_id") or source_path or record.get("_ragprep_file", ""))
    chunk_seed = str(record.get("chunk_id") or record.get("id") or hashlib.sha1(text.encode("utf-8")).hexdigest()[:16])
    chunk_id = str(chunk_seed)
    return {
        "document_id": document_id,
        "chunk_id": chunk_id,
        "text": text,
        "source_path": source_path,
        "title": str(record.get("title") or Path(source_path).stem or document_id),
        "section": str(record.get("section") or record.get("heading") or ""),
        "language": str(record.get("language") or default_language),
        "hash": str(record.get("hash") or hashlib.sha256(text.encode("utf-8")).hexdigest()),
        "entities": record.get("entities", []),
        "summary": str(record.get("summary") or ""),
        "ragprep_file": record.get("_ragprep_file", ""),
    }


def validate_chunks(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings = []
    for index, chunk in enumerate(chunks):
        missing = [field for field in ("document_id", "chunk_id", "text", "source_path") if not chunk.get(field)]
        if missing:
            findings.append({"index": index, "chunk_id": chunk.get("chunk_id", ""), "missing": missing})
    return findings


def command_ingest(args: argparse.Namespace) -> int:
    config = load_config(repo_path(args.config))
    import_dir = repo_path(args.from_ragprep)
    if not import_dir.exists():
        payload = {"status": "fail", "error": f"RagPrep import directory missing: {rel(import_dir)}"}
        json_print(payload) if args.json else print(payload["error"])
        return 2
    raw_records = iter_ragprep_records(import_dir)
    chunks = [normalize_chunk(record, config.get("project", {}).get("language", "de")) for record in raw_records]
    findings = validate_chunks(chunks)
    status = "fail" if findings else "ready"
    payload = {
        "status": status,
        "mode": "auto-apply" if args.apply else "dry-run",
        "source": rel(import_dir),
        "chunks_total": len(chunks),
        "documents_total": len({chunk["document_id"] for chunk in chunks if chunk.get("document_id")}),
        "validation_findings": findings,
        "vector_store": config.get("vector_store", {}),
        "report_path": "",
        "written": [],
    }
    if args.apply and not findings:
        state_dir = repo_path(config.get("paths", {}).get("ragprep_imports", ".agent/data/wissenswerk/ragprep_imports"))
        ensure_dir(state_dir)
        state_path = state_dir / f"ragprep_import_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
        state_path.write_text(json.dumps({"generated_at": now_iso(), "chunks": chunks}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        payload["written"].append(rel(state_path))
    report_path = write_report(config, "ragprep_ingest", payload)
    payload["report_path"] = rel(report_path)
    json_print(payload) if args.json else print(f"{status}: {len(chunks)} chunks; report {rel(report_path)}")
    return 1 if findings else 0


def command_wiki_build(args: argparse.Namespace) -> int:
    config = load_config(repo_path(args.config))
    wiki_root = repo_path(config.get("paths", {}).get("wiki", "docs/Wiki"))
    sources = [repo_path(path) for path in config.get("paths", {}).get("sources", [])]
    existing_sources = [path for path in sources if path.exists()]
    articles = sorted(wiki_root.rglob("*.md")) if wiki_root.exists() else []
    payload = {
        "status": "ready",
        "mode": "auto-apply" if args.apply else "dry-run",
        "wiki_root": rel(wiki_root),
        "source_roots": [rel(path) for path in existing_sources],
        "articles_seen": len(articles),
        "report_path": "",
        "written": [],
        "rollback_hint": "Revert the files listed in `written` and remove the report for this run.",
    }
    if args.apply:
        report_md = wiki_root / "Wissenswerk_Plattformstatus.md"
        ensure_dir(report_md.parent)
        report_md.write_text(
            "\n".join(
                [
                    "---",
                    f"uuid: {uuid.uuid4()}",
                    "title: Wissenswerk Plattformstatus",
                    "category: System",
                    "epistemic: \"#meta\"",
                    f"updated_at: {now_iso()}",
                    "---",
                    "",
                    "# Wissenswerk Plattformstatus",
                    "",
                    "Dieser Artikel dokumentiert den generischen Wissenswerk-Plattformkern fuer den Siebenwind-Referenztenant.",
                    "",
                    f"- Artikel im Wiki-Baum: {len(articles)}",
                    f"- Quellenwurzeln: {', '.join(rel(path) for path in existing_sources) or '[UNGEKLAERT]'}",
                    "- Retrieval-Default: pgvector",
                    "- Designvertrag: DESIGN.md",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        payload["written"].append(rel(report_md))
    report_path = write_report(config, "wiki_build", payload)
    payload["report_path"] = rel(report_path)
    json_print(payload) if args.json else print(f"wiki build {payload['mode']}: report {rel(report_path)}")
    return 0


def lexical_search(config: dict[str, Any], query: str, source: str, limit: int) -> list[dict[str, Any]]:
    roots = []
    if source in {"raw", "all"}:
        roots.extend(repo_path(path) for path in config.get("paths", {}).get("sources", []))
    if source in {"wiki", "all"}:
        roots.append(repo_path(config.get("paths", {}).get("wiki", "docs/Wiki")))
    terms = [term.lower() for term in re.findall(r"\w+", query) if len(term) > 2]
    hits = []
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for file_path in sorted(root.rglob("*.md")):
            if file_path in seen:
                continue
            seen.add(file_path)
            raw = file_path.read_text(encoding="utf-8", errors="ignore")
            haystack = raw.lower()
            score = sum(haystack.count(term) for term in terms)
            if score <= 0:
                continue
            snippet_start = min([haystack.find(term) for term in terms if haystack.find(term) >= 0] or [0])
            snippet = re.sub(r"\s+", " ", raw[snippet_start : snippet_start + 500]).strip()
            hits.append({"path": rel(file_path), "score": score, "snippet": snippet})
    hits.sort(key=lambda item: item["score"], reverse=True)
    return hits[:limit]


def command_search(args: argparse.Namespace) -> int:
    config = load_config(repo_path(args.config))
    hits = lexical_search(config, args.query, args.source, args.top)
    payload = {
        "status": "ok",
        "query": args.query,
        "source": args.source,
        "retrieval": "lexical-bootstrap",
        "vector_store": config.get("vector_store", {}).get("kind", ""),
        "hits": hits,
        "count": len(hits),
    }
    json_print(payload) if args.json else print_search(payload)
    return 0


def print_search(payload: dict[str, Any]) -> None:
    print(f"Wissenswerk search: {payload['query']} ({payload['source']})")
    for hit in payload["hits"]:
        print(f"- {hit['path']} score={hit['score']}: {hit['snippet'][:180]}")


def command_bot_discord(args: argparse.Namespace) -> int:
    config = load_config(repo_path(args.config))
    discord_cfg = config.get("bot", {}).get("discord", {})
    token_env = discord_cfg.get("token_env", "DISCORD_BOT_TOKEN")
    payload = {
        "status": "ready" if os.environ.get(token_env) else "missing_token",
        "adapter": "discord",
        "enabled": bool(discord_cfg.get("enabled", False)),
        "token_env": token_env,
        "token_present": bool(os.environ.get(token_env)),
        "command_prefix": discord_cfg.get("command_prefix", "!ww"),
        "run": bool(args.run),
        "note": "Bootstrap adapter. Use --run only after installing a Discord runtime package.",
    }
    if args.run and not payload["token_present"]:
        json_print(payload) if args.json else print("Discord token missing")
        return 2
    json_print(payload) if args.json else print(f"Discord adapter: {payload['status']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Wissenswerk corpus-to-wiki platform CLI")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to wissenswerk.yaml")
    sub = parser.add_subparsers(dest="command")

    init = sub.add_parser("init", help="Create a starter Wissenswerk tenant config")
    init.add_argument("--config", default="wissenswerk.yaml")
    init.add_argument("--force", action="store_true")
    init.add_argument("--json", action="store_true")

    ingest = sub.add_parser("ingest", help="Import RagPrep pre-chunked artifacts")
    ingest.add_argument("--from-ragprep", required=True)
    ingest.add_argument("--apply", action="store_true")
    ingest.add_argument("--json", action="store_true")

    wiki = sub.add_parser("wiki", help="Build or inspect generated wiki artifacts")
    wiki_sub = wiki.add_subparsers(dest="wiki_command")
    wiki_build = wiki_sub.add_parser("build", help="Build wiki artifacts")
    wiki_build.add_argument("--apply", action="store_true")
    wiki_build.add_argument("--json", action="store_true")

    search = sub.add_parser("search", help="Search the configured corpus/wiki")
    search.add_argument("query")
    search.add_argument("--source", choices=["raw", "wiki", "all"], default="wiki")
    search.add_argument("--top", type=int, default=5)
    search.add_argument("--json", action="store_true")

    providers = sub.add_parser("providers", help="Inspect configured model/vector providers")
    providers_sub = providers.add_subparsers(dest="providers_command")
    providers_check = providers_sub.add_parser("check", help="Check provider configuration")
    providers_check.add_argument("--json", action="store_true")

    design = sub.add_parser("design", help="Inspect the DESIGN.md contract")
    design_sub = design.add_subparsers(dest="design_command")
    design_lint = design_sub.add_parser("lint", help="Lint DESIGN.md")
    design_lint.add_argument("file", nargs="?", default=str(DEFAULT_DESIGN))
    design_lint.add_argument("--json", action="store_true")

    bot = sub.add_parser("bot", help="Run or inspect bot adapters")
    bot_sub = bot.add_subparsers(dest="bot_command")
    discord = bot_sub.add_parser("discord", help="Discord bot adapter")
    discord.add_argument("--run", action="store_true")
    discord.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init":
        return command_init(args)
    if args.command == "ingest":
        return command_ingest(args)
    if args.command == "wiki" and args.wiki_command == "build":
        return command_wiki_build(args)
    if args.command == "search":
        return command_search(args)
    if args.command == "providers" and args.providers_command == "check":
        return command_providers_check(args)
    if args.command == "design" and args.design_command == "lint":
        return command_design_lint(args)
    if args.command == "bot" and args.bot_command == "discord":
        return command_bot_discord(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
