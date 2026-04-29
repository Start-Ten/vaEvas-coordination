#!/usr/bin/env python3
"""Audit vaEvas git repositories against their tracking remotes."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


DEFAULT_REPOS = [
    "EVAS",
    "behavioral-veriloga-eval",
    "coordination",
    "veriloga-skills",
    "reference/verilog-eval",
    "reference/verilog-eval-v2",
]


def run(repo: Path, args: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]


def audit_repo(repo: Path, fetch: bool) -> dict:
    if fetch:
        run(repo, ["fetch", "--all", "--prune"])

    branch = run(repo, ["branch", "--show-current"]).stdout.strip()
    tracking = run(repo, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    tracking_name = tracking.stdout.strip() if tracking.returncode == 0 else ""

    ahead = behind = None
    if tracking_name:
        counts = run(repo, ["rev-list", "--left-right", "--count", "@{u}...HEAD"])
        if counts.returncode == 0:
            left, right = counts.stdout.strip().split()
            behind, ahead = int(left), int(right)

    status = lines(run(repo, ["status", "--porcelain=v1", "--untracked-files=all"]).stdout)
    ignored = lines(run(repo, ["status", "--porcelain=v1", "--ignored", "--untracked-files=no"]).stdout)
    head = run(repo, ["log", "-1", "--oneline"]).stdout.strip()

    tracked_changes = [s for s in status if not s.startswith("?? ")]
    untracked = [s[3:] for s in status if s.startswith("?? ")]
    ignored_paths = [s[3:] for s in ignored if s.startswith("!! ")]

    if ahead == 0 and behind == 0 and not tracked_changes:
        sync = "synced"
        if untracked:
            sync = "synced + untracked local files"
    elif ahead is None or behind is None:
        sync = "no tracking branch"
    elif ahead and behind:
        sync = f"diverged ahead={ahead} behind={behind}"
    elif ahead:
        sync = f"ahead {ahead}"
    elif behind:
        sync = f"behind {behind}"
    else:
        sync = "tracked changes present"

    return {
        "repo": str(repo),
        "branch": branch,
        "tracking": tracking_name,
        "ahead": ahead,
        "behind": behind,
        "sync": sync,
        "head": head,
        "tracked_change_count": len(tracked_changes),
        "untracked_count": len(untracked),
        "ignored_count": len(ignored_paths),
        "untracked_sample": untracked[:20],
        "ignored_sample": ignored_paths[:20],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="vaEvas root directory")
    parser.add_argument("--fetch", action="store_true", help="fetch all remotes before auditing")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    rows = []
    for rel in DEFAULT_REPOS:
        repo = root / rel
        if (repo / ".git").exists():
            rows.append(audit_repo(repo, args.fetch))

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0

    print("| repo | branch | tracking | sync | local residue |")
    print("|---|---|---|---|---|")
    for row in rows:
        residue = []
        if row["tracked_change_count"]:
            residue.append(f"tracked={row['tracked_change_count']}")
        if row["untracked_count"]:
            residue.append(f"untracked={row['untracked_count']}")
        if row["ignored_count"]:
            residue.append(f"ignored={row['ignored_count']}")
        residue_text = ", ".join(residue) if residue else "clean"
        print(
            f"| {Path(row['repo']).name} | {row['branch']} | "
            f"{row['tracking'] or '-'} | {row['sync']} | {residue_text} |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
