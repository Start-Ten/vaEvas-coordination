#!/usr/bin/env python3
"""Install bundled vaEvas skills into a local Codex skill directory."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


SKILLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SKILLS_DIR.parent
MANIFEST_PATH = SKILLS_DIR / "recommended-skills.json"


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def codex_skills_dir(codex_home: str | None) -> Path:
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def copy_skill(name: str, source: Path, target_root: Path, dry_run: bool) -> None:
    target = target_root / name
    print(f"{name}: {source} -> {target}")
    if dry_run:
        return
    if not source.exists():
        raise FileNotFoundError(f"missing bundled skill source: {source}")
    target_root.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def list_skills(manifest: dict) -> None:
    print("Bundled skills:")
    for item in manifest.get("bundled", []):
        print(f"  - {item['name']}: {item.get('description', '')}")
    print("\nOptional external skills:")
    for item in manifest.get("optional_external", []):
        print(f"  - {item['name']}: {item.get('why', '')}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="install all bundled skills")
    parser.add_argument("--skill", action="append", default=[], help="install one bundled skill by name")
    parser.add_argument("--list", action="store_true", help="list bundled and optional skills")
    parser.add_argument("--dry-run", action="store_true", help="show install actions without copying")
    parser.add_argument("--codex-home", help="custom Codex home directory; default is ~/.codex")
    args = parser.parse_args()

    manifest = load_manifest()
    if args.list:
        list_skills(manifest)

    selected = set(args.skill)
    if args.all:
        selected.update(item["name"] for item in manifest.get("bundled", []))

    if not selected:
        if not args.list:
            parser.error("choose --list, --all, or --skill NAME")
        return 0

    bundled = {item["name"]: item for item in manifest.get("bundled", [])}
    missing = sorted(selected - set(bundled))
    if missing:
        raise SystemExit(f"unknown bundled skill(s): {', '.join(missing)}")

    target_root = codex_skills_dir(args.codex_home)
    for name in sorted(selected):
        source = REPO_ROOT / bundled[name]["source"]
        copy_skill(name, source, target_root, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
