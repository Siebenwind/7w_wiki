#!/usr/bin/env python3
"""
test_runner.py

Declarative test runner for CLI-level interoperability and clean-client-state checks.
All runtime execution stays on ./7w_wiki.py.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SUITES_DIR = PROJECT_ROOT / ".agent" / "tests" / "suites"
SYSTEM_TMP_DIR = Path(tempfile.gettempdir())
MSG_ID_RE = re.compile(r"^(MSG-\d{4}-\d{4})\b")
QUARANTINED_IN_ALL = {"rag-relevance-smoke", "pages-full-smoke"}


@dataclass
class CaseResult:
    case_id: str
    name: str
    status: str  # PASS, FAIL, SKIP
    command: list[str]
    exit_code: int | None
    reason: str
    stdout: str
    stderr: str
    duration_sec: float | None


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def load_suite(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Suite nicht gefunden: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if "cases" not in data or not isinstance(data["cases"], list):
        raise ValueError(f"Ungueltige Suite-Struktur (cases fehlt): {path}")
    return data


def run_cmd(cmd: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def collect_context(timeout: int) -> dict[str, str]:
    context: dict[str, str] = {}
    result = run_cmd(["./7w_wiki.py", "mail", "inbox", "--status", "OPEN"], timeout)
    for line in result.stdout.splitlines():
        m = MSG_ID_RE.match(line.strip())
        if m:
            context["first_open_message_id"] = m.group(1)
            break
    return context


def resolve_command(template: list[str], context: dict[str, str]) -> list[str]:
    resolved: list[str] = []
    for token in template:
        value = token
        for key, key_value in context.items():
            value = value.replace(f"{{{{{key}}}}}", key_value)
        resolved.append(value)
    return resolved


def _extract_markdown_links(raw: str) -> list[str]:
    # [label](target) but skip images ![...](...)
    matches = re.findall(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)", raw)
    return [m.strip() for m in matches]


def _resolve_local_link(source_file: Path, target: str) -> Path | None:
    cleaned = target.strip()
    if not cleaned:
        return None
    if cleaned.startswith(("http://", "https://", "mailto:", "#")):
        return None
    if cleaned.startswith("<") and cleaned.endswith(">"):
        cleaned = cleaned[1:-1].strip()
    cleaned = cleaned.split(" ", 1)[0]
    cleaned = cleaned.split("#", 1)[0]
    if not cleaned:
        return None
    if cleaned.startswith("file://"):
        # Explicitly keep as unresolved; this is prohibited in this repo.
        return Path("__INVALID_FILE_URI__")
    if cleaned.startswith("/"):
        return (PROJECT_ROOT / cleaned.lstrip("/")).resolve()
    return (source_file.parent / cleaned).resolve()


def check_links_in_files(files: list[str]) -> tuple[bool, str]:
    missing: list[str] = []
    for rel in files:
        source = (PROJECT_ROOT / rel).resolve()
        if not source.exists():
            missing.append(f"{rel} -> QUELLE_FEHLT")
            continue
        raw = source.read_text(encoding="utf-8")
        for target in _extract_markdown_links(raw):
            resolved = _resolve_local_link(source, target)
            if resolved is None:
                continue
            if resolved.name == "__INVALID_FILE_URI__":
                missing.append(f"{rel} -> {target} (file:// nicht erlaubt)")
                continue
            if not resolved.exists():
                missing.append(f"{rel} -> {target}")
    if not missing:
        return True, "ok"
    preview = "; ".join(missing[:5])
    extra = f" (+{len(missing)-5} weitere)" if len(missing) > 5 else ""
    return False, f"Broken links: {preview}{extra}"


def _expand_globs(patterns: list[str]) -> list[Path]:
    expanded: list[Path] = []
    for pattern in patterns:
        expanded.extend(sorted(PROJECT_ROOT.glob(pattern)))
    # Stable + unique
    unique = sorted(set(expanded))
    return [p for p in unique if p.is_file()]


def check_forbidden_patterns(
    include_globs: list[str],
    forbidden_regex: list[str],
    exclude_globs: list[str] | None = None,
) -> tuple[bool, str]:
    files = _expand_globs(include_globs)
    if not files:
        return False, f"Keine Dateien fuer include_globs gefunden: {include_globs}"

    excluded: set[Path] = set()
    for pattern in (exclude_globs or []):
        excluded.update(_expand_globs([pattern]))
    files = [p for p in files if p not in excluded]

    compiled = []
    for regex in forbidden_regex:
        try:
            compiled.append((regex, re.compile(regex)))
        except re.error as err:
            return False, f"Ungueltiger Regex {regex!r}: {err}"

    findings: list[str] = []
    for file_path in files:
        raw = file_path.read_text(encoding="utf-8")
        for line_no, line in enumerate(raw.splitlines(), start=1):
            for regex_text, regex in compiled:
                if regex.search(line):
                    rel = file_path.relative_to(PROJECT_ROOT)
                    snippet = line.strip()
                    if len(snippet) > 120:
                        snippet = snippet[:117] + "..."
                    findings.append(f"{rel}:{line_no} /{regex_text}/ -> {snippet}")

    if not findings:
        return True, "ok"

    preview = "; ".join(findings[:5])
    extra = f" (+{len(findings)-5} weitere)" if len(findings) > 5 else ""
    return False, f"Forbidden pattern hit: {preview}{extra}"


def check_required_patterns_by_file(requirements: list[dict]) -> tuple[bool, str]:
    missing: list[str] = []

    for req in requirements:
        rel_file = req.get("file")
        must_include = req.get("must_include_regex", [])
        if not rel_file:
            missing.append("INVALID_REQUIREMENT: file fehlt")
            continue
        if not isinstance(must_include, list) or not must_include:
            missing.append(f"{rel_file}: must_include_regex fehlt/leer")
            continue

        file_path = (PROJECT_ROOT / rel_file).resolve()
        if not file_path.exists():
            missing.append(f"{rel_file}: DATEI_FEHLT")
            continue

        raw = file_path.read_text(encoding="utf-8")
        for regex_text in must_include:
            try:
                regex = re.compile(regex_text)
            except re.error as err:
                missing.append(f"{rel_file}: ungueltiger Regex /{regex_text}/ ({err})")
                continue
            if not regex.search(raw):
                missing.append(f"{rel_file}: fehlt /{regex_text}/")

    if not missing:
        return True, "ok"

    preview = "; ".join(missing[:5])
    extra = f" (+{len(missing)-5} weitere)" if len(missing) > 5 else ""
    return False, f"Required pattern missing: {preview}{extra}"


def check_paths_absent(paths: list[str]) -> tuple[bool, str]:
    existing: list[str] = []
    for rel in paths:
        target = (PROJECT_ROOT / rel).resolve()
        if target.exists():
            existing.append(rel)

    if not existing:
        return True, "ok"

    preview = ", ".join(existing[:5])
    extra = f" (+{len(existing)-5} weitere)" if len(existing) > 5 else ""
    return False, f"Paths still exist: {preview}{extra}"


def check_json_unique_by_file(requirements: list[dict]) -> tuple[bool, str]:
    findings: list[str] = []

    for req in requirements:
        rel_file = req.get("file")
        array_path = req.get("array_path")
        key = req.get("key")
        if not rel_file or not array_path or not key:
            findings.append(f"Ungueltige JSON-Unique-Anforderung: {req!r}")
            continue

        file_path = (PROJECT_ROOT / rel_file).resolve()
        if not file_path.exists():
            findings.append(f"{rel_file}: DATEI_FEHLT")
            continue
        try:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as err:
            findings.append(f"{rel_file}: JSON nicht lesbar ({err})")
            continue

        current = payload
        for part in str(array_path).split("."):
            if not isinstance(current, dict) or part not in current:
                findings.append(f"{rel_file}: JSON-Pfad {array_path!r} fehlt")
                current = None
                break
            current = current[part]
        if current is None:
            continue
        if not isinstance(current, list):
            findings.append(f"{rel_file}: JSON-Pfad {array_path!r} ist keine Liste")
            continue

        seen: set[str] = set()
        duplicates: list[str] = []
        for item in current:
            if not isinstance(item, dict) or key not in item:
                findings.append(f"{rel_file}: Eintrag ohne Schluessel {key!r}")
                continue
            value = str(item[key])
            if value in seen:
                duplicates.append(value)
            else:
                seen.add(value)
        if duplicates:
            preview = ", ".join(sorted(set(duplicates))[:5])
            findings.append(
                f"{rel_file}: {len(duplicates)} doppelte Werte fuer {key!r}: {preview}"
            )

    if not findings:
        return True, "ok"
    preview = "; ".join(findings[:5])
    extra = f" (+{len(findings)-5} weitere)" if len(findings) > 5 else ""
    return False, f"JSON uniqueness violation: {preview}{extra}"


def check_command_inventory_files(files: list[str]) -> tuple[bool, str]:
    result = run_cmd(["./7w_wiki.py", "--help-json"], timeout=30)
    if result.returncode != 0:
        return False, f"--help-json failed with exit {result.returncode}"
    try:
        schema = json.loads(result.stdout)
    except json.JSONDecodeError as err:
        return False, f"--help-json returned invalid JSON: {err}"

    commands = [cmd.get("name", "") for cmd in schema.get("commands", []) if cmd.get("name")]
    missing: list[str] = []
    for rel in files:
        path = (PROJECT_ROOT / rel).resolve()
        if not path.exists():
            missing.append(f"{rel}: DATEI_FEHLT")
            continue
        raw = path.read_text(encoding="utf-8")
        for command in commands:
            pattern = rf"`{re.escape(command)}(?:[ `<\[]|`)"
            if not re.search(pattern, raw):
                missing.append(f"{rel}: fehlt `{command}`")

    if not missing:
        return True, "ok"

    preview = "; ".join(missing[:5])
    extra = f" (+{len(missing)-5} weitere)" if len(missing) > 5 else ""
    return False, f"Command inventory drift: {preview}{extra}"


def check_case_expectations(
    case: dict,
    proc: subprocess.CompletedProcess[str],
    duration_sec: float,
) -> tuple[bool, str]:
    parsed_json = None
    expected_exit_any = case.get("expect_exit_any")
    if expected_exit_any is not None:
        try:
            allowed = [int(x) for x in expected_exit_any]
        except Exception:
            return False, f"Ungueltiges expect_exit_any: {expected_exit_any!r}"
        if proc.returncode not in allowed:
            return False, f"Exitcode {proc.returncode} nicht in expect_exit_any {allowed}"
    else:
        expected_exit = int(case.get("expect_exit", 0))
        if proc.returncode != expected_exit:
            return False, f"Exitcode {proc.returncode} != erwartet {expected_exit}"

    stdout = proc.stdout or ""
    stderr = proc.stderr or ""

    for needle in case.get("expect_stdout", []):
        if needle not in stdout:
            return False, f"stdout enthaelt nicht: {needle!r}"

    for needle in case.get("expect_stderr", []):
        if needle not in stderr:
            return False, f"stderr enthaelt nicht: {needle!r}"

    for needle in case.get("forbid_stdout", []):
        if needle in stdout:
            return False, f"stdout enthaelt verbotenes Muster: {needle!r}"

    for needle in case.get("forbid_stderr", []):
        if needle in stderr:
            return False, f"stderr enthaelt verbotenes Muster: {needle!r}"

    if case.get("expect_valid_json", False):
        try:
            parsed_json = json.loads(stdout.strip())
        except json.JSONDecodeError as e:
            return False, f"stdout ist kein gueltiges JSON: {e}"
        required_keys = case.get("expect_json_keys", [])
        if required_keys and isinstance(parsed_json, dict):
            for k in required_keys:
                if k not in parsed_json:
                    return False, f"JSON fehlt erwarteter Key: {k!r}"
    elif case.get("expect_json_path_exists") or case.get("expect_json_path_in") or case.get("expect_json_path_equals") or case.get("expect_json_path_min"):
        try:
            parsed_json = json.loads(stdout.strip())
        except json.JSONDecodeError as e:
            return False, f"stdout ist kein gueltiges JSON fuer Path-Checks: {e}"

    def resolve_json_path(payload, path: str):
        current = payload
        for part in path.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                raise KeyError(path)
        return current

    for path in case.get("expect_json_path_exists", []):
        try:
            resolve_json_path(parsed_json, path)
        except KeyError:
            return False, f"JSON Pfad fehlt: {path!r}"

    for path, expected in case.get("expect_json_path_equals", {}).items():
        try:
            value = resolve_json_path(parsed_json, path)
        except KeyError:
            return False, f"JSON Pfad fehlt: {path!r}"
        if value != expected:
            return False, f"JSON Pfad {path!r} = {value!r}, erwartet {expected!r}"

    for path, allowed in case.get("expect_json_path_in", {}).items():
        try:
            value = resolve_json_path(parsed_json, path)
        except KeyError:
            return False, f"JSON Pfad fehlt: {path!r}"
        if value not in allowed:
            return False, f"JSON Pfad {path!r} = {value!r}, erwartet eine von {allowed!r}"

    for path, minimum in case.get("expect_json_path_min", {}).items():
        try:
            value = resolve_json_path(parsed_json, path)
        except KeyError:
            return False, f"JSON Pfad fehlt: {path!r}"
        try:
            numeric_value = float(value)
        except Exception:
            return False, f"JSON Pfad {path!r} ist nicht numerisch: {value!r}"
        if numeric_value < float(minimum):
            return False, f"JSON Pfad {path!r} = {numeric_value}, erwartet >= {minimum}"

    min_duration = case.get("min_duration_sec")
    if min_duration is not None and duration_sec < float(min_duration):
        return False, f"Laufzeit {duration_sec:.2f}s < min_duration_sec {float(min_duration):.2f}s"

    max_duration = case.get("max_duration_sec")
    if max_duration is not None and duration_sec > float(max_duration):
        return False, f"Laufzeit {duration_sec:.2f}s > max_duration_sec {float(max_duration):.2f}s"

    return True, "ok"


def run_suite(suite_name: str, timeout: int) -> tuple[list[CaseResult], Path]:
    suite_path = SUITES_DIR / f"{suite_name}.json"
    suite = load_suite(suite_path)
    context = collect_context(timeout)

    results: list[CaseResult] = []
    total_cases = len(suite["cases"])
    for idx, case in enumerate(suite["cases"], start=1):
        case_id = case.get("id", f"{suite_name}-{idx:03d}")
        name = case.get("name", case_id)
        print(f"[{suite_name}] case {idx}/{total_cases}: {case_id} - {name}", flush=True)
        skip_keys = case.get("skip_if_context_missing", [])
        if any(k not in context for k in skip_keys):
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="SKIP",
                    command=list(case.get("cmd", [])),
                    exit_code=None,
                    reason=f"Kontext fehlt: {', '.join([k for k in skip_keys if k not in context])}",
                    stdout="",
                    stderr="",
                    duration_sec=None,
                )
            )
            print(f"[{suite_name}] case {case_id}: SKIP ({results[-1].reason})", flush=True)
            continue

        link_files = case.get("link_check_files", [])
        if link_files:
            started = time.perf_counter()
            ok, reason = check_links_in_files(list(link_files))
            duration_sec = time.perf_counter() - started
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="PASS" if ok else "FAIL",
                    command=["link-check"] + list(link_files),
                    exit_code=0 if ok else 1,
                    reason=reason,
                    stdout="",
                    stderr="",
                    duration_sec=duration_sec,
                )
            )
            print(f"[{suite_name}] case {case_id}: {results[-1].status} ({results[-1].reason})", flush=True)
            continue

        pattern_globs = case.get("pattern_check_globs", [])
        forbidden_regex = case.get("forbid_regex", [])
        if pattern_globs and forbidden_regex:
            started = time.perf_counter()
            ok, reason = check_forbidden_patterns(
                include_globs=list(pattern_globs),
                forbidden_regex=list(forbidden_regex),
                exclude_globs=list(case.get("exclude_globs", [])),
            )
            duration_sec = time.perf_counter() - started
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="PASS" if ok else "FAIL",
                    command=["pattern-check"] + list(pattern_globs),
                    exit_code=0 if ok else 1,
                    reason=reason,
                    stdout="",
                    stderr="",
                    duration_sec=duration_sec,
                )
            )
            print(f"[{suite_name}] case {case_id}: {results[-1].status} ({results[-1].reason})", flush=True)
            continue

        required_by_file = case.get("required_regex_by_file", [])
        if required_by_file:
            started = time.perf_counter()
            ok, reason = check_required_patterns_by_file(list(required_by_file))
            duration_sec = time.perf_counter() - started
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="PASS" if ok else "FAIL",
                    command=["required-pattern-check"],
                    exit_code=0 if ok else 1,
                    reason=reason,
                    stdout="",
                    stderr="",
                    duration_sec=duration_sec,
                )
            )
            print(f"[{suite_name}] case {case_id}: {results[-1].status} ({results[-1].reason})", flush=True)
            continue

        absent_paths = case.get("paths_must_not_exist", [])
        if absent_paths:
            started = time.perf_counter()
            ok, reason = check_paths_absent(list(absent_paths))
            duration_sec = time.perf_counter() - started
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="PASS" if ok else "FAIL",
                    command=["path-absence-check"] + list(absent_paths),
                    exit_code=0 if ok else 1,
                    reason=reason,
                    stdout="",
                    stderr="",
                    duration_sec=duration_sec,
                )
            )
            print(f"[{suite_name}] case {case_id}: {results[-1].status} ({results[-1].reason})", flush=True)
            continue

        json_unique_requirements = case.get("json_unique_by_file", [])
        if json_unique_requirements:
            started = time.perf_counter()
            ok, reason = check_json_unique_by_file(list(json_unique_requirements))
            duration_sec = time.perf_counter() - started
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="PASS" if ok else "FAIL",
                    command=["json-unique-check"],
                    exit_code=0 if ok else 1,
                    reason=reason,
                    stdout="",
                    stderr="",
                    duration_sec=duration_sec,
                )
            )
            print(f"[{suite_name}] case {case_id}: {results[-1].status} ({results[-1].reason})", flush=True)
            continue

        command_inventory_files = case.get("command_inventory_files", [])
        if command_inventory_files:
            started = time.perf_counter()
            ok, reason = check_command_inventory_files(list(command_inventory_files))
            duration_sec = time.perf_counter() - started
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="PASS" if ok else "FAIL",
                    command=["command-inventory-check"] + list(command_inventory_files),
                    exit_code=0 if ok else 1,
                    reason=reason,
                    stdout="",
                    stderr="",
                    duration_sec=duration_sec,
                )
            )
            print(f"[{suite_name}] case {case_id}: {results[-1].status} ({results[-1].reason})", flush=True)
            continue

        cmd_template = case.get("cmd", [])
        if not cmd_template:
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="FAIL",
                    command=[],
                    exit_code=None,
                    reason="Keine cmd definiert",
                    stdout="",
                    stderr="",
                    duration_sec=None,
                )
            )
            print(f"[{suite_name}] case {case_id}: FAIL ({results[-1].reason})", flush=True)
            continue

        command = resolve_command(list(cmd_template), context)
        if not command[0].endswith("7w_wiki.py"):
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="FAIL",
                    command=command,
                    exit_code=None,
                    reason="Runtime-Verletzung: Testfall muss mit ./7w_wiki.py starten.",
                    stdout="",
                    stderr="",
                    duration_sec=None,
                )
            )
            print(f"[{suite_name}] case {case_id}: FAIL ({results[-1].reason})", flush=True)
            continue

        case_timeout = int(case.get("timeout_sec", timeout))
        run_timeout = case_timeout if case_timeout > 0 else timeout
        started = time.perf_counter()
        try:
            proc = run_cmd(command, run_timeout)
        except subprocess.TimeoutExpired:
            duration_sec = time.perf_counter() - started
            results.append(
                CaseResult(
                    case_id=case_id,
                    name=name,
                    status="FAIL",
                    command=command,
                    exit_code=None,
                    reason=f"Timeout nach {run_timeout}s",
                    stdout="",
                    stderr="",
                    duration_sec=duration_sec,
                )
            )
            print(f"[{suite_name}] case {case_id}: FAIL ({results[-1].reason})", flush=True)
            continue
        duration_sec = time.perf_counter() - started

        ok, reason = check_case_expectations(case, proc, duration_sec)
        status = "PASS" if ok else "FAIL"
        results.append(
            CaseResult(
                case_id=case_id,
                name=name,
                status=status,
                command=command,
                exit_code=proc.returncode,
                reason=reason,
                stdout=proc.stdout or "",
                stderr=proc.stderr or "",
                duration_sec=duration_sec,
            )
        )
        print(f"[{suite_name}] case {case_id}: {status} ({reason})", flush=True)

    return results, suite_path


def build_report(
    suite_name: str,
    suite_path: Path,
    results: list[CaseResult],
    report_path: Path,
) -> str:
    pass_count = sum(1 for r in results if r.status == "PASS")
    fail_count = sum(1 for r in results if r.status == "FAIL")
    skip_count = sum(1 for r in results if r.status == "SKIP")
    overall = "PASS" if fail_count == 0 else "FAIL"

    lines: list[str] = []
    lines.append("---")
    lines.append(f"uuid: {uuid.uuid4()}")
    lines.append(f"status: {overall}")
    lines.append(f"created_at: {now_iso()}")
    lines.append('epistemic: "#meta"')
    lines.append("---")
    lines.append("")
    lines.append(f"# Test Run Report: {suite_name}")
    lines.append("")
    lines.append(f"- Suite-Datei: `{suite_path.relative_to(PROJECT_ROOT)}`")
    lines.append(f"- Ergebnis: **{overall}**")
    lines.append(f"- PASS: {pass_count} | FAIL: {fail_count} | SKIP: {skip_count}")
    measured = [r.duration_sec for r in results if r.duration_sec is not None]
    if measured:
        total_runtime = sum(measured)
        avg_runtime = total_runtime / len(measured)
        lines.append(f"- Laufzeit (gemessen): Summe {total_runtime:.2f}s | Mittel {avg_runtime:.2f}s")
    lines.append("")
    lines.append("| ID | Name | Status | Exit | Laufzeit (s) | Hinweis |")
    lines.append("|---|---|---|---|---|---|")
    for r in results:
        exit_txt = "-" if r.exit_code is None else str(r.exit_code)
        duration_txt = "-" if r.duration_sec is None else f"{r.duration_sec:.2f}"
        lines.append(f"| `{r.case_id}` | {r.name} | {r.status} | {exit_txt} | {duration_txt} | {r.reason} |")
    lines.append("")

    for r in results:
        if r.status != "FAIL":
            continue
        lines.append(f"## FAIL: {r.case_id} - {r.name}")
        lines.append("")
        lines.append(f"- Kommando: `{' '.join(r.command)}`")
        if r.duration_sec is not None:
            lines.append(f"- Laufzeit: {r.duration_sec:.2f}s")
        lines.append(f"- Grund: {r.reason}")
        lines.append("")
        if r.stdout.strip():
            lines.append("```text")
            lines.append(r.stdout.strip())
            lines.append("```")
            lines.append("")
        if r.stderr.strip():
            lines.append("```text")
            lines.append(r.stderr.strip())
            lines.append("```")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def post_failure_mail(
    suite_name: str,
    results: list[CaseResult],
    report_path: Path,
    from_agent: str,
    to_agent: str,
    priority: str,
    timeout: int,
) -> tuple[bool, str]:
    failed = [r for r in results if r.status == "FAIL"]
    if not failed:
        return True, "Keine FAILs; kein Mail-Post notwendig."

    failed_ids = ", ".join([r.case_id for r in failed])
    subject = f"Test FAIL: {suite_name} ({len(failed)} Fehler)"
    body = (
        f"Suite `{suite_name}` ist fehlgeschlagen.\n\n"
        f"Fehlende Testfaelle: {failed_ids}\n"
        "Bitte uebernehmt den Defect per `mail claim` oder verlinktem Task und "
        "dokumentiert den Fix vor Re-Test."
    )
    cmd = [
        "./7w_wiki.py",
        "mail",
        "post",
        "--from",
        from_agent,
        "--to",
        to_agent,
        "--subject",
        subject,
        "--body",
        body,
        "--report-path",
        str(report_path.relative_to(PROJECT_ROOT)),
        "--priority",
        priority,
    ]
    proc = run_cmd(cmd, timeout)
    ok = proc.returncode == 0
    if ok:
        return True, (proc.stdout or "Dispatch-Meldung erstellt.").strip()
    err = (proc.stderr or proc.stdout or "").strip()
    return False, f"Dispatch-Post fehlgeschlagen (rc={proc.returncode}): {err}"


def discover_suites() -> list[str]:
    if not SUITES_DIR.exists():
        return []
    return sorted([p.stem for p in SUITES_DIR.glob("*.json")])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run declarative CLI interoperability test suites.")
    parser.add_argument(
        "--suite",
        default="clean-client-state",
        help="Suite-Name (Datei in .agent/tests/suites) oder 'all'.",
    )
    parser.add_argument("--list-suites", action="store_true", help="Nur verfuegbare Suiten ausgeben.")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout je Testkommando in Sekunden.")
    parser.add_argument("--post-failures", action="store_true", help="Bei FAIL automatisch Dispatch-Meldung posten.")
    parser.add_argument("--from-agent", default="Test-Waechter")
    parser.add_argument("--to-agent", default="ALL")
    parser.add_argument("--priority", default="HIGH", choices=["LOW", "NORMAL", "HIGH"])
    parser.add_argument(
        "--include-rag",
        action="store_true",
        help="Nimmt rag-relevance-smoke in --suite all auf (standardmaessig aus Sicherheitsgruenden ausgelassen).",
    )
    parser.add_argument("--allow-fail", action="store_true", help="Returncode 0 erzwingen trotz FAIL.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    suites = discover_suites()
    if args.list_suites:
        if not suites:
            print("Keine Suiten gefunden.")
            return 0
        for suite in suites:
            print(suite)
        return 0

    if args.suite == "all":
        selected = [suite for suite in suites if args.include_rag or suite not in QUARANTINED_IN_ALL]
        skipped = [suite for suite in suites if suite not in selected]
        if skipped:
            print(
                "[all] Hinweis: Standardlauf laesst aus Stabilitaetsgruenden aus: "
                f"{', '.join(skipped)} (Opt-in mit --include-rag)."
            )
    else:
        selected = [args.suite]

    unknown = [s for s in selected if s not in suites]
    if unknown:
        print(f"Unbekannte Suite(s): {', '.join(unknown)}")
        print("Verfuegbar:", ", ".join(suites) if suites else "(keine)")
        return 1

    if selected == ["rag-relevance-smoke"]:
        print("[rag-relevance-smoke] Warnung: Diese Suite ist instabil und nicht Teil von --suite all.", flush=True)

    test_run_tmp = Path(tempfile.mkdtemp(prefix="7w_test_"))
    overall_fail = False

    for suite_name in selected:
        results, suite_path = run_suite(suite_name, args.timeout)
        report_name = f"TEST_{suite_name}_{now_stamp()}.md"
        report_path = test_run_tmp / report_name
        report = build_report(suite_name, suite_path, results, report_path)
        try:
            report_path.write_text(report, encoding="utf-8")
            print(f"[{suite_name}] Report: {report_path}")
        except Exception as e:
            print(f"[{suite_name}] ⚠️ Konnte Report nicht schreiben ({e}). Fallback auf Stdout:")
            print(report)

        failed = [r for r in results if r.status == "FAIL"]
        if failed:
            overall_fail = True
        print(f"[{suite_name}] Report: {report_path}")
        print(f"[{suite_name}] PASS={sum(r.status == 'PASS' for r in results)} "
              f"FAIL={len(failed)} SKIP={sum(r.status == 'SKIP' for r in results)}")

        if args.post_failures and failed:
            ok, message = post_failure_mail(
                suite_name=suite_name,
                results=results,
                report_path=report_path,
                from_agent=args.from_agent,
                to_agent=args.to_agent,
                priority=args.priority,
                timeout=args.timeout,
            )
            print(f"[{suite_name}] Dispatch: {message}")
            if not ok:
                overall_fail = True

    if overall_fail and not args.allow_fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
