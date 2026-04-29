#!/usr/bin/env python3
"""Export slim experiment ledgers and remove obsolete waveform payloads.

This script is intentionally conservative:

- It never deletes paths protected by
  `coordination/status/2026-04-29_cleanup_protect_manifest.json`.
- It exports JSONL ledgers before deleting payloads.
- It deletes only large regenerable waveform/simulator payloads by default:
  `tran.csv` files and Spectre `.raw` directories.

The remaining `result.json`, `model_results.json`, summaries, generated source,
repair prompts, and metadata are preserved for H/I dataset construction.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_ROOT = PROJECT_ROOT / "behavioral-veriloga-eval" / "results"
COORD_DATASETS = PROJECT_ROOT / "coordination" / "datasets"
PROTECT_MANIFEST = (
    PROJECT_ROOT / "coordination" / "status" / "2026-04-29_cleanup_protect_manifest.json"
)
FINAL_G_RESULT_ROOT = (
    PROJECT_ROOT
    / "behavioral-veriloga-eval"
    / "results"
    / "condition-G-targeted-materialized-spectre-aligned-kimi-evas-2026-04-28"
)


def rel(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def load_protected_prefixes() -> list[Path]:
    if not PROTECT_MANIFEST.exists():
        return []
    data = json.loads(PROTECT_MANIFEST.read_text(encoding="utf-8"))
    prefixes: list[Path] = []
    for item in data.get("protected_supporting_records", []):
        prefixes.append(PROJECT_ROOT / item)
    for entry in data.get("protected_mainline", {}).values():
        for item in entry.get("paths", []):
            prefixes.append(PROJECT_ROOT / item)
    return [p.resolve() for p in prefixes]


def is_protected(path: Path, protected: list[Path]) -> bool:
    rp = path.resolve()
    for prefix in protected:
        try:
            rp.relative_to(prefix)
            return True
        except ValueError:
            continue
    return False


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_json_error": str(exc), "_path": rel(path)}


def infer_run_root(result_path: Path) -> str:
    try:
        sub = result_path.resolve().relative_to(RESULTS_ROOT.resolve())
    except ValueError:
        return ""
    return sub.parts[0] if sub.parts else ""


def compact_result_record(result_path: Path) -> dict[str, Any]:
    result = read_json(result_path)
    task_id = result.get("task_id") or result_path.parent.name
    notes = result.get("evas_notes") or result.get("notes") or []
    return {
        "run_root": infer_run_root(result_path),
        "task_id": task_id,
        "result_path": rel(result_path),
        "status": result.get("status"),
        "scores": result.get("scores", {}),
        "metrics": result.get("metrics", {}),
        "notes": notes,
        "failure_domain": result.get("failure_domain"),
        "repair_owner": result.get("repair_owner"),
        "strict_preflight_status": result.get("strict_preflight_status"),
        "spectre_status": result.get("spectre_status"),
        "generated_artifacts": result.get("generated_artifacts"),
    }


def export_experiment_ledger(out_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with out_path.open("w", encoding="utf-8") as f:
        for path in sorted(RESULTS_ROOT.rglob("result.json")):
            rec = compact_result_record(path)
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def h_signature(notes: list[Any], metrics: dict[str, Any]) -> list[str]:
    text = " ".join(str(x).lower() for x in notes)
    text += " " + " ".join(f"{k}={v}".lower() for k, v in metrics.items())
    sigs: list[str] = []
    rules = [
        ("unique_codes=1", "code_coverage_failure"),
        ("vout_span=0", "output_activity_failure"),
        ("not_enough_edges", "edge_liveness_failure"),
        ("too_few_edges", "edge_liveness_failure"),
        ("transitions=0", "state_transition_liveness_failure"),
        ("lock_time=nan", "lock_failure"),
        ("late_edge_ratio", "feedback_ratio_failure"),
        ("freq_ratio", "frequency_ratio_failure"),
        ("up_edges=0", "pfd_or_bbpd_pulse_missing"),
        ("down_edges=0", "pfd_or_bbpd_pulse_missing"),
        ("max_active_cells=0", "dwa_cell_activation_failure"),
        ("no vdac activity", "dac_activity_failure"),
        ("sample_mismatch", "sample_hold_value_failure"),
        ("frame_rises=1", "serializer_frame_liveness_failure"),
        ("malformed_pwl_wave", "tb_pwl_syntax_failure"),
        ("conditional/event/loop/case", "conditional_transition_compile_failure"),
        ("tran.csv missing", "runtime_waveform_missing"),
    ]
    for needle, sig in rules:
        if needle in text and sig not in sigs:
            sigs.append(sig)
    return sigs


def export_current_g_hi_seed(out_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with out_path.open("w", encoding="utf-8") as f:
        for result_path in sorted(FINAL_G_RESULT_ROOT.glob("*/result.json")):
            rec = compact_result_record(result_path)
            if rec.get("status") == "PASS":
                continue
            rec["source"] = "final_G_65_failures"
            rec["h_signatures"] = h_signature(rec.get("notes", []), rec.get("metrics", {}))
            rec["i_seed_intent"] = "derive mechanism card and repair policy from prompt + notes"
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def path_size(path: Path) -> int:
    if path.is_file():
        try:
            return path.stat().st_size
        except OSError:
            return 0
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            p = Path(root) / name
            try:
                total += p.stat().st_size
            except OSError:
                pass
    return total


def cleanup_candidates(protected: list[Path]) -> list[tuple[Path, str, int]]:
    candidates: list[tuple[Path, str, int]] = []

    for path in sorted(RESULTS_ROOT.rglob("tran.csv")):
        if is_protected(path, protected):
            continue
        candidates.append((path, "tran_csv", path_size(path)))

    raw_dirs: list[Path] = []
    for path in sorted(RESULTS_ROOT.rglob("*.raw")):
        if not path.is_dir():
            continue
        if is_protected(path, protected):
            continue
        raw_dirs.append(path)
    # Avoid deleting nested raw dirs twice.
    filtered_raw_dirs: list[Path] = []
    for path in raw_dirs:
        if any(path.resolve().is_relative_to(parent.resolve()) for parent in filtered_raw_dirs):
            continue
        filtered_raw_dirs.append(path)
    for path in filtered_raw_dirs:
        candidates.append((path, "spectre_raw_dir", path_size(path)))

    return candidates


def remove_candidates(candidates: list[tuple[Path, str, int]]) -> tuple[int, int]:
    removed_count = 0
    removed_bytes = 0
    for path, _kind, size in candidates:
        if not path.exists():
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        removed_count += 1
        removed_bytes += size
    return removed_count, removed_bytes


def human_size(num: int) -> str:
    value = float(num)
    for unit in ("B", "K", "M", "G", "T"):
        if value < 1024 or unit == "T":
            return f"{value:.1f}{unit}"
        value /= 1024
    return f"{value:.1f}T"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Actually remove cleanup candidates.")
    ap.add_argument("--skip-ledger", action="store_true", help="Do not re-export JSONL ledgers.")
    args = ap.parse_args()

    stamp = datetime.now().strftime("%Y-%m-%d")
    ledger = COORD_DATASETS / f"experiment_ledger_slim_{stamp}.jsonl"
    hi_seed = COORD_DATASETS / f"hi_seed_final_G_failures_{stamp}.jsonl"

    if not args.skip_ledger:
        ledger_count = export_experiment_ledger(ledger)
        seed_count = export_current_g_hi_seed(hi_seed)
    else:
        ledger_count = seed_count = 0

    protected = load_protected_prefixes()
    candidates = cleanup_candidates(protected)
    total = sum(size for _path, _kind, size in candidates)

    summary = {
        "mode": "apply" if args.apply else "dry_run",
        "ledger_path": rel(ledger),
        "ledger_records": ledger_count,
        "hi_seed_path": rel(hi_seed),
        "hi_seed_records": seed_count,
        "protected_prefixes": [rel(p) for p in protected if p.exists()],
        "candidate_count": len(candidates),
        "candidate_bytes": total,
        "candidate_human": human_size(total),
        "candidate_breakdown": {},
    }
    for _path, kind, size in candidates:
        entry = summary["candidate_breakdown"].setdefault(kind, {"count": 0, "bytes": 0})
        entry["count"] += 1
        entry["bytes"] += size
    for entry in summary["candidate_breakdown"].values():
        entry["human"] = human_size(entry["bytes"])

    out_summary = COORD_DATASETS / f"cleanup_{'applied' if args.apply else 'dryrun'}_{stamp}.json"
    if args.apply:
        removed_count, removed_bytes = remove_candidates(candidates)
        summary["removed_count"] = removed_count
        summary["removed_bytes"] = removed_bytes
        summary["removed_human"] = human_size(removed_bytes)

    out_summary.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
