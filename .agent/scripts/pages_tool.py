#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys


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


def cmd_status(args):
    config_path = os.path.join(REPO_ROOT, args.config)
    print(f"[pages] repo_root: {REPO_ROOT}")
    print(f"[pages] config: {config_path} ({'OK' if os.path.exists(config_path) else 'MISSING'})")
    print(f"[pages] docs_dir: {os.path.join(REPO_ROOT, 'docs')} ({'OK' if os.path.isdir(os.path.join(REPO_ROOT, 'docs')) else 'MISSING'})")
    print(f"[pages] site_dir: {os.path.join(REPO_ROOT, 'site')} ({'OK' if os.path.isdir(os.path.join(REPO_ROOT, 'site')) else 'MISSING'})")

    mkdocs_cmd, mkdocs_source = _mkdocs_base_cmd()
    if not mkdocs_cmd:
        print("[pages] mkdocs: MISSING")
        print("[pages] hint: source .venv/bin/activate && pip install -r requirements.txt")
        return 1

    version_result = _run_capture(mkdocs_cmd + ["--version"])
    if version_result.returncode != 0:
        print(f"[pages] mkdocs: FOUND at {mkdocs_source} but --version failed")
        print(version_result.stderr.strip())
        return version_result.returncode

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


def cmd_validate(args):
    status_rc = cmd_status(args)
    if status_rc != 0:
        return status_rc

    if not args.skip_link_suite:
        rc = _run_runtime(["test", "--suite", "interop-doc-links"])
        if rc != 0:
            return rc

    if not args.skip_source_hygiene:
        rc = _run_runtime(["test", "--suite", "source-link-hygiene"])
        if rc != 0:
            return rc

    if not args.skip_process_governance:
        rc = _run_runtime(["test", "--suite", "process-dispatch-curiosity"])
        if rc != 0:
            return rc

    if not args.skip_reader_stats_contract:
        rc = _run_runtime(["test", "--suite", "reader-stats-contract"])
        if rc != 0:
            return rc

    if not args.skip_audit:
        rc = _run_runtime(["audit"])
        if rc != 0:
            return rc

    return cmd_build(args)


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
    validate_parser.add_argument("--strict", action="store_true", help="Run mkdocs build in strict mode")
    validate_parser.add_argument("--no-clean", action="store_true", help="Skip mkdocs --clean")
    validate_parser.add_argument("--skip-link-suite", action="store_true", help="Skip interop doc link suite")
    validate_parser.add_argument("--skip-source-hygiene", action="store_true", help="Skip source-link hygiene suite")
    validate_parser.add_argument("--skip-process-governance", action="store_true", help="Skip process dispatch/curiosity governance suite")
    validate_parser.add_argument("--skip-reader-stats-contract", action="store_true", help="Skip reader stats contract suite")
    validate_parser.add_argument("--skip-audit", action="store_true", help="Skip register audit")
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
