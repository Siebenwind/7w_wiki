#!/usr/bin/env python3
"""
Archivar: Log rotation and compression for Siebenwind Wiki.
Compresses stale reports in Logs/Archive/ into dated .tar.gz bundles,
rotates DONE dispatches, and archives resolved Synapse Board tickets.
"""
import argparse
import datetime as dt
import os
import shutil
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_DIR = REPO_ROOT / "Logs" / "Archive"
COMPRESSED_DIR = ARCHIVE_DIR / "compressed"
DISPATCH_DIR = REPO_ROOT / "System" / "Synapse_Board" / "DISPATCH"
DISPATCH_ARCHIVE = DISPATCH_DIR / "_archive"
SYNAPSE_DIR = REPO_ROOT / "System" / "Synapse_Board"
SYNAPSE_RESOLVED = SYNAPSE_DIR / "_resolved"

# File categories for grouping into archives
CATEGORIES = {
    "audits": "Audit_*.txt",
    "tests": "TEST_*.md",
    "snapshots": "STATS_SNAPSHOT_*.json",
    "sessions": "SESSION_MEMORY_*.md",
}

BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def get_cutoff(keep_days: int) -> float:
    cutoff = dt.datetime.now() - dt.timedelta(days=keep_days)
    return cutoff.timestamp()


def find_stale_files(pattern: str, cutoff_ts: float) -> list[Path]:
    """Find files matching pattern that are older than cutoff."""
    stale = []
    for f in ARCHIVE_DIR.glob(pattern):
        if f.name.startswith(".") or f.name.endswith("_latest.json"):
            continue
        if f.stat().st_mtime < cutoff_ts:
            stale.append(f)
    return sorted(stale)


def compress_category(category: str, files: list[Path], dry_run: bool) -> Path | None:
    """Compress a list of files into a dated .tar.gz archive."""
    if not files:
        return None

    COMPRESSED_DIR.mkdir(parents=True, exist_ok=True)
    date_str = dt.datetime.now().strftime("%Y-%m-%d")
    archive_name = f"{category}_{date_str}.tar.gz"
    archive_path = COMPRESSED_DIR / archive_name

    # Don't overwrite existing archives
    counter = 1
    while archive_path.exists():
        archive_name = f"{category}_{date_str}_{counter}.tar.gz"
        archive_path = COMPRESSED_DIR / archive_name
        counter += 1

    if dry_run:
        total_size = sum(f.stat().st_size for f in files)
        print(f"  [DRY RUN] Would compress {len(files)} files ({total_size // 1024} KB) -> {archive_name}")
        return None

    with tarfile.open(archive_path, "w:gz") as tar:
        for f in files:
            tar.add(f, arcname=f.name)

    # Remove originals after successful compression
    for f in files:
        f.unlink()

    return archive_path


def rotate_dispatches(cutoff_ts: float, dry_run: bool) -> int:
    """Move DONE dispatches older than cutoff to _archive/."""
    import re

    if not DISPATCH_DIR.exists():
        return 0

    moved = 0
    for msg_file in sorted(DISPATCH_DIR.glob("MSG-*.md")):
        if msg_file.stat().st_mtime >= cutoff_ts:
            continue

        # Check if status is DONE
        try:
            text = msg_file.read_text(encoding="utf-8")
            if "status: DONE" not in text[:500]:
                continue
        except Exception:
            continue

        if dry_run:
            print(f"  [DRY RUN] Would archive dispatch: {msg_file.name}")
            moved += 1
            continue

        DISPATCH_ARCHIVE.mkdir(parents=True, exist_ok=True)
        shutil.move(str(msg_file), str(DISPATCH_ARCHIVE / msg_file.name))
        moved += 1

    return moved


def rotate_resolved_tickets(dry_run: bool) -> int:
    """Move resolved Conflict/Research tickets to _resolved/."""
    moved = 0

    for pattern in ["Conflict_*.md", "RESEARCH-*.md"]:
        for ticket in SYNAPSE_DIR.glob(pattern):
            # Check if resolved
            try:
                text = ticket.read_text(encoding="utf-8")
                # Research tickets that are resolved usually have [x] or "Abgeschlossen"
                is_resolved = (
                    "status: DONE" in text[:500]
                    or "status: Abgeschlossen" in text[:500]
                    or "Abgeschlossen" in text[:300]
                    or "[x]" in text[:500]
                )
                if not is_resolved:
                    continue
            except Exception:
                continue

            if dry_run:
                print(f"  [DRY RUN] Would archive resolved ticket: {ticket.name}")
                moved += 1
                continue

            SYNAPSE_RESOLVED.mkdir(parents=True, exist_ok=True)
            shutil.move(str(ticket), str(SYNAPSE_RESOLVED / ticket.name))
            moved += 1

    return moved


def cmd_rotate(args: argparse.Namespace) -> int:
    cutoff_ts = get_cutoff(args.keep_days)
    cutoff_str = dt.datetime.fromtimestamp(cutoff_ts).strftime("%Y-%m-%d %H:%M")

    print(f"{BOLD}📦 Archivar: Log-Rotation{RESET}")
    print(f"   Cutoff: {cutoff_str} (keep_days={args.keep_days})")
    if args.dry_run:
        print(f"   {YELLOW}Mode: DRY RUN (keine Änderungen){RESET}\n")
    else:
        print()

    total_compressed = 0
    total_removed = 0

    # 1. Compress stale archive files by category
    print(f"{BOLD}Phase 1: Komprimiere veraltete Reports{RESET}")
    for category, pattern in CATEGORIES.items():
        stale = find_stale_files(pattern, cutoff_ts)
        if stale:
            size_kb = sum(f.stat().st_size for f in stale) // 1024
            result = compress_category(category, stale, args.dry_run)
            if result:
                print(f"  ✓ {category}: {len(stale)} Dateien ({size_kb} KB) -> {result.name}")
            total_compressed += len(stale)
            total_removed += len(stale)
        else:
            print(f"  — {category}: nichts zu archivieren")

    # 2. Rotate DONE dispatches
    print(f"\n{BOLD}Phase 2: Dispatch-Rotation{RESET}")
    dispatch_count = rotate_dispatches(cutoff_ts, args.dry_run)
    print(f"  {'→' if args.dry_run else '✓'} {dispatch_count} DONE-Nachrichten archiviert")

    # 3. Resolved tickets
    print(f"\n{BOLD}Phase 3: Board-Bereinigung{RESET}")
    ticket_count = rotate_resolved_tickets(args.dry_run)
    print(f"  {'→' if args.dry_run else '✓'} {ticket_count} abgeschlossene Tickets archiviert")

    # Summary
    print(f"\n{'='*50}")
    total = total_compressed + dispatch_count + ticket_count
    if total == 0:
        print(f"{GREEN}Nichts zu rotieren. Alles sauber.{RESET}")
    elif args.dry_run:
        print(f"{YELLOW}DRY RUN: {total} Dateien würden archiviert/komprimiert.{RESET}")
        print("Führe ohne --dry-run aus, um die Rotation durchzuführen.")
    else:
        print(f"{GREEN}✓ {total} Dateien verarbeitet.{RESET}")
        print(f"  Komprimiert: {total_compressed} | Dispatches: {dispatch_count} | Tickets: {ticket_count}")

    return 0


def cmd_unpack(args: argparse.Namespace) -> int:
    """Unpack a specific compressed archive back to Logs/Archive/."""
    archive_name = args.archive
    if not archive_name.endswith(".tar.gz"):
        archive_name += ".tar.gz"

    archive_path = COMPRESSED_DIR / archive_name
    if not archive_path.exists():
        print(f"{RED}Archive nicht gefunden:{RESET} {archive_path}")
        # List available archives
        available = sorted(COMPRESSED_DIR.glob("*.tar.gz")) if COMPRESSED_DIR.exists() else []
        if available:
            print(f"\nVerfügbare Archive:")
            for a in available:
                size_kb = a.stat().st_size // 1024
                print(f"  - {a.name} ({size_kb} KB)")
        return 1

    print(f"{BOLD}📦 Entpacke: {archive_name}{RESET}")
    with tarfile.open(archive_path, "r:gz") as tar:
        tar.extractall(path=ARCHIVE_DIR)
        members = tar.getnames()

    print(f"{GREEN}✓ {len(members)} Dateien nach Logs/Archive/ entpackt.{RESET}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Archivar: Log rotation & compression")
    sub = p.add_subparsers(dest="cmd", required=True)

    rotate = sub.add_parser("rotate", help="Compress stale logs and rotate dispatches")
    rotate.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    rotate.add_argument("--keep-days", type=int, default=7, help="Keep files newer than N days (default: 7)")
    rotate.set_defaults(fn=cmd_rotate)

    unpack = sub.add_parser("unpack", help="Unpack a compressed archive")
    unpack.add_argument("archive", help="Name of the archive to unpack (e.g. audits_2026-02-12)")
    unpack.set_defaults(fn=cmd_unpack)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
