#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

from pages_integrity import collect_pages_build_report, now_iso, write_pages_health_snapshot

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
REPO_CLI = os.path.join(REPO_ROOT, "7w_wiki.py")
VENV_MKDOCS = os.path.join(REPO_ROOT, ".venv", "bin", "mkdocs")


def _mkdocs_base_cmd():
    if os.path.exists(VENV_MKDOCS):
        return [VENV_MKDOCS], VENV_MKDOCS
    system_mkdocs = shutil.which("mkdocs")
    if system_mkdocs:
        return [system_mkdocs], system_mkdocs
    return None, None


def _run(cmd):
    return subprocess.run(cmd, cwd=REPO_ROOT).returncode


def _run_capture(cmd):
    return subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def _run_runtime(command_args):
    cmd = [sys.executable, REPO_CLI] + command_args
    print(f"[pages] runtime: {' '.join(command_args)}")
    return _run(cmd)


def _run_runtime_capture(command_args):
    cmd = [sys.executable, REPO_CLI] + command_args
    return _run_capture(cmd)


def cmd_status(args, silent=False):
    config_path = os.path.join(REPO_ROOT, args.config)
    if not silent:
        print(f"[pages] repo_root: {REPO_ROOT}")
        print(f"[pages] config: {config_path} ({'OK' if os.path.exists(config_path) else 'MISSING'})")
        print(f"[pages] docs_dir: {os.path.join(REPO_ROOT, 'docs')} ({'OK' if os.path.isdir(os.path.join(REPO_ROOT, 'docs')) else 'MISSING'})")
        print(f"[pages] site_dir: {os.path.join(REPO_ROOT, 'site')} ({'OK' if os.path.isdir(os.path.join(REPO_ROOT, 'site')) else 'MISSING'})")

    mkdocs_cmd, mkdocs_source = _mkdocs_base_cmd()
    if not mkdocs_cmd:
        if not silent:
            print("[pages] mkdocs: MISSING")
            print("[pages] hint: source .venv/bin/activate && pip install -r requirements.txt")
        return 1

    version_result = _run_capture(mkdocs_cmd + ["--version"])
    if version_result.returncode != 0:
        if not silent:
            print(f"[pages] mkdocs: FOUND at {mkdocs_source} but --version failed")
            print(version_result.stderr.strip())
        return version_result.returncode

    if not silent:
        print(f"[pages] mkdocs: {mkdocs_source}")
        print(f"[pages] {version_result.stdout.strip()}")
    return 0


def cmd_build(args):
    mkdocs_cmd, mkdocs_source = _mkdocs_base_cmd()
    if not mkdocs_cmd:
        print("[pages] mkdocs: MISSING")
        print("[pages] hint: source .venv/bin/activate && pip install -r requirements.txt")
        return 1

    config_path = os.path.join(REPO_ROOT, args.config)
    if not os.path.exists(config_path):
        print(f"[pages] config not found: {config_path}")
        return 1

    cmd = mkdocs_cmd + ["build", "-f", config_path]
    if not args.no_clean:
        cmd.append("--clean")
    if args.strict:
        cmd.append("--strict")

    print(f"[pages] mkdocs source: {mkdocs_source}")
    print(f"[pages] build: {' '.join(cmd)}")
    return _run(cmd)


def _run_validation_check(command_args, json_mode):
    started = time.perf_counter()
    if json_mode:
        result = _run_runtime_capture(command_args)
        parsed_json = None
        try:
            parsed_json = json.loads(result.stdout)
        except Exception:
            parsed_json = None
        return {
            "command": command_args,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "json": parsed_json,
            "duration_ms": round((time.perf_counter() - started) * 1000, 2),
        }
    rc = _run_runtime(command_args)
    return {
        "command": command_args,
        "exit_code": rc,
        "duration_ms": round((time.perf_counter() - started) * 1000, 2),
    }


def _build_validate_report(args):
    started_total = time.perf_counter()
    status_rc = cmd_status(args, silent=args.json)
    if status_rc != 0:
        return {
            "generated_at": now_iso(),
            "mode": "fast" if args.fast else "full",
            "advisory_only": bool(args.fast),
            "status": "FAIL",
            "validation_timing_ms": {"total": round((time.perf_counter() - started_total) * 1000, 2)},
            "checks": [],
            "build": {"exit_code": status_rc},
            "pages_health": {
                "status": "FAIL",
                "canonical_wiki_root": "docs/Siebenwind_Wiki",
                "legacy_wiki_root": "Siebenwind_Wiki",
                "drift_status": "FAIL",
                "drift_counts": {
                    "docs_only_files": 0,
                    "legacy_only_files": 0,
                    "content_mismatches": 0,
                },
                "unresolved_total": 0,
                "allowlisted_total": 0,
                "planned_fix_total": 0,
                "unallowlisted_total": 0,
                "targets": [],
                "other_warnings": ["mkdocs status check failed"],
            },
        }, status_rc

    checks = []
    prechecks_started = time.perf_counter()
    if not args.skip_link_suite:
        checks.append(_run_validation_check(["test", "--suite", "interop-doc-links"], args.json))
    if not args.skip_source_hygiene:
        checks.append(_run_validation_check(["test", "--suite", "source-link-hygiene"], args.json))
    if not args.skip_process_governance:
        checks.append(_run_validation_check(["test", "--suite", "process-dispatch-curiosity"], args.json))
    if not args.skip_reader_stats_contract:
        checks.append(_run_validation_check(["test", "--suite", "reader-stats-contract"], args.json))
    if args.skip_audit:
        checks.append(_run_validation_check(["test", "--suite", "content-contract"], args.json))
        checks.append(_run_validation_check(["test", "--suite", "render-hygiene"], args.json))
    if not args.skip_audit:
        audit_args = ["audit"]
        if args.include_pages_audit:
            audit_args.append("--pages")
        if args.json:
            audit_args.append("--json")
        checks.append(_run_validation_check(audit_args, args.json))
    prechecks_duration_ms = round((time.perf_counter() - prechecks_started) * 1000, 2)

    for check in checks:
        if check["exit_code"] != 0:
            return {
                "generated_at": now_iso(),
                "mode": "fast" if args.fast else "full",
                "advisory_only": bool(args.fast),
                "status": "FAIL",
                "validation_timing_ms": {
                    "prechecks_total": prechecks_duration_ms,
                    "report_build": 0,
                    "total": round((time.perf_counter() - started_total) * 1000, 2),
                },
                "checks": checks,
                "build": {"exit_code": None},
                "pages_health": {
                    "status": "FAIL",
                    "canonical_wiki_root": "docs/Siebenwind_Wiki",
                    "legacy_wiki_root": "Siebenwind_Wiki",
                    "drift_status": "FAIL",
                    "drift_counts": {
                        "docs_only_files": 0,
                        "legacy_only_files": 0,
                        "content_mismatches": 0,
                    },
                    "unresolved_total": 0,
                    "allowlisted_total": 0,
                    "planned_fix_total": 0,
                    "unallowlisted_total": 0,
                    "targets": [],
                    "other_warnings": ["runtime pre-check failed"],
                },
            }, check["exit_code"]

    report_build_started = time.perf_counter()
    report = collect_pages_build_report(config=args.config, no_clean=args.no_clean, fast=args.fast)
    report_build_duration_ms = round((time.perf_counter() - report_build_started) * 1000, 2)
    report["generated_at"] = now_iso()
    report["checks"] = checks
    report["strict_requested"] = bool(args.strict)
    report["strict_links_requested"] = bool(args.strict_links)
    report["validation_timing_ms"] = {
        "prechecks_total": prechecks_duration_ms,
        "report_build": report_build_duration_ms,
        "total": round((time.perf_counter() - started_total) * 1000, 2),
    }

    pages_health = report["pages_health"]
    audit_check = next((check for check in checks if check["command"] and check["command"][0] == "audit"), None)
    contract_check = next((check for check in checks if check["command"] and check["command"][:3] == ["test", "--suite", "content-contract"]), None)
    if audit_check and audit_check.get("json"):
        report["drift_health"] = {
            "render_hygiene": audit_check["json"]["categories"].get("render_hygiene", {}),
            "contract_violations": audit_check["json"]["categories"].get("contract_violations", {}),
            "stub_inventory": audit_check["json"]["categories"].get("stub_inventory", {}),
            "bridge_inventory": audit_check["json"]["categories"].get("bridge_inventory", {}),
            "split_brain": audit_check["json"]["categories"].get("split_brain", {}),
            "traceability_gaps": audit_check["json"]["categories"].get("traceability_gaps", {}),
        }
    elif contract_check and contract_check.get("json"):
        contract_payload = contract_check["json"]
        report["drift_health"] = {
            "render_hygiene": contract_payload.get("render_hygiene", {}),
            "contract_violations": contract_payload.get("contract_violations", {}),
            "stub_inventory": contract_payload.get("stub_inventory", {}),
            "bridge_inventory": contract_payload.get("bridge_inventory", {}),
            "split_brain": contract_payload.get("split_brain", {}),
            "traceability_gaps": contract_payload.get("traceability_gaps", {}),
            "cache": contract_payload.get("cache", {}),
        }
    else:
        report["drift_health"] = {}
    non_roamlink_warning_count = len(pages_health.get("other_warnings", []))
    final_status = pages_health.get("status", report.get("status", "UNKNOWN"))
    exit_code = 0

    if not args.fast and report["build"]["exit_code"] != 0:
        final_status = "FAIL"
        exit_code = report["build"]["exit_code"]
    elif pages_health.get("drift_status") == "FAIL":
        final_status = "FAIL"
        exit_code = 1
    elif args.strict and not args.fast and non_roamlink_warning_count > 0:
        final_status = "FAIL"
        exit_code = 1
    elif args.strict_links and pages_health.get("unallowlisted_total", 0) > 0:
        final_status = "FAIL"
        exit_code = 1
    elif pages_health.get("status") == "WARN":
        final_status = "WARN"

    report["status"] = final_status
    pages_health["status"] = final_status
    if not args.fast:
        pages_health["last_validated_at"] = report["generated_at"]
        write_pages_health_snapshot(report)
    return report, exit_code


def cmd_validate(args):
    report, exit_code = _build_validate_report(args)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return exit_code

    print(f"[pages] pages_health: {report['pages_health']['status']}")
    print(
        "[pages] unresolved:"
        f" total={report['pages_health']['unresolved_total']}"
        f" allowlisted={report['pages_health']['allowlisted_total']}"
        f" planned_fix={report['pages_health']['planned_fix_total']}"
        f" unallowlisted={report['pages_health']['unallowlisted_total']}"
    )
    if report["pages_health"]["other_warnings"]:
        print(f"[pages] non-roamlinks warnings: {len(report['pages_health']['other_warnings'])}")
    return exit_code


def main():
    parser = argparse.ArgumentParser(description="GitHub Pages build and validation helper")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    status_parser = subparsers.add_parser("status", help="Show build prerequisites")
    status_parser.add_argument("--config", default="mkdocs.yml", help="mkdocs config path")

    build_parser = subparsers.add_parser("build", help="Run mkdocs build")
    build_parser.add_argument("--strict", action="store_true", help="Run mkdocs build in strict mode")
    build_parser.add_argument("--no-clean", action="store_true", help="Skip mkdocs --clean")
    build_parser.add_argument("--config", default="mkdocs.yml", help="mkdocs config path")

    validate_parser = subparsers.add_parser("validate", help="Run runtime checks and mkdocs build")
    validate_parser.add_argument("--fast", action="store_true", help="Use cached analysis plus the latest Pages snapshot as an advisory-only precheck")
    validate_parser.add_argument("--strict", action="store_true", help="Run mkdocs build in strict mode")
    validate_parser.add_argument("--strict-links", action="store_true", help="Fail if non-allowlisted unresolved internal links remain")
    validate_parser.add_argument("--no-clean", action="store_true", help="Skip mkdocs --clean")
    validate_parser.add_argument("--skip-link-suite", action="store_true", help="Skip interop doc link suite")
    validate_parser.add_argument("--skip-source-hygiene", action="store_true", help="Skip source-link hygiene suite")
    validate_parser.add_argument("--skip-process-governance", action="store_true", help="Skip process dispatch/curiosity governance suite")
    validate_parser.add_argument("--skip-reader-stats-contract", action="store_true", help="Skip reader stats contract suite")
    validate_parser.add_argument("--skip-audit", action="store_true", help="Skip register audit")
    validate_parser.add_argument("--include-pages-audit", action="store_true", help="Run audit --pages during validation")
    validate_parser.add_argument("--json", action="store_true", help="Output machine-readable validation report")
    validate_parser.add_argument("--config", default="mkdocs.yml", help="mkdocs config path")

    args = parser.parse_args()

    if args.subcommand == "status":
        sys.exit(cmd_status(args))
    if args.subcommand == "build":
        sys.exit(cmd_build(args))
    if args.subcommand == "validate":
        sys.exit(cmd_validate(args))

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
