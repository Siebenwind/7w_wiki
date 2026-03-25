#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from install_tool import build_manifest, load_config, should_exclude

REPO_ROOT = Path(__file__).resolve().parents[2]

DIST_DIR = REPO_ROOT / "dist"


def package_name(profile: str, platform: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"7w_wiki_{platform}_{profile}_{timestamp}.tar.gz"


def build_archive(manifest: dict, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / package_name(manifest["profile"], manifest["platform"])
    excludes = manifest.get("exclude_globs", [])

    def _filter(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo | None:
        candidate = REPO_ROOT / tarinfo.name
        if candidate.exists() and should_exclude(candidate, excludes):
            return None
        return tarinfo

    with tarfile.open(archive_path, "w:gz") as tar:
        for item in manifest["items"]:
            if not item["exists"]:
                continue
            source = REPO_ROOT / item["path"]
            tar.add(source, arcname=item["path"], filter=_filter)
        manifest_payload = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        temp_manifest = output_dir / "PACKAGE_MANIFEST.json"
        temp_manifest.write_text(manifest_payload, encoding="utf-8")
        tar.add(temp_manifest, arcname="PACKAGE_MANIFEST.json")
        temp_manifest.unlink()
    return archive_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build archive-first bundles for repo installation.")
    parser.add_argument("--platform", choices=["ubuntu", "debian", "macos", "wsl"], default="ubuntu")
    parser.add_argument("--profile", choices=["full", "agent-only"], default="full")
    parser.add_argument("--toolchain", choices=["system", "bundled", "auto"], default="auto")
    parser.add_argument("--output-dir", default=str(DIST_DIR), help="Output directory for bundle archives")
    parser.add_argument("--json", action="store_true", help="Output manifest JSON instead of status text")
    args = parser.parse_args()

    config = load_config()
    manifest = build_manifest(config, args.profile, args.platform, args.toolchain, None)
    archive_path = build_archive(manifest, Path(args.output_dir))
    archive_display = archive_path.resolve()
    try:
        manifest["archive"] = str(archive_display.relative_to(REPO_ROOT))
    except ValueError:
        manifest["archive"] = str(archive_display)

    if args.json:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    else:
        print(f"Package created at {archive_path}")
        print(f"Profile: {args.profile}")
        print(f"Platform target: {args.platform}")
        print(f"Toolchain mode: {manifest['toolchain']['selected_mode']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
