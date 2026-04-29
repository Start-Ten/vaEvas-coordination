#!/usr/bin/env python3
"""Build an auditable H translation table from EVAS result.json files.

The table is intentionally separate from repair execution.  It lets us inspect
whether H is a faithful diagnostic translator before we count any PASS gain.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNERS = ROOT / "behavioral-veriloga-eval" / "runners"
sys.path.insert(0, str(RUNNERS))

from diagnosis_translation import translate_diagnosis  # noqa: E402


GENERIC_RULES = {"GENERIC_METRIC_MISMATCH", "SIM_ARTIFACT", "OBSERVABILITY_CONTRACT"}


def _notes(result: dict) -> list[str]:
    notes = result.get("evas_notes") or result.get("notes") or []
    if isinstance(notes, str):
        return [notes]
    return [str(item) for item in notes]


def _confidence(translations: list[dict]) -> str:
    rules = [item.get("matched_rule", "") for item in translations if item.get("matched_rule")]
    if not rules:
        return "low"
    non_generic = [rule for rule in rules if rule not in GENERIC_RULES]
    if non_generic:
        return "high"
    return "medium"


def _audit_one(path: Path) -> dict:
    result = json.loads(path.read_text(encoding="utf-8"))
    task_id = result.get("task_id") or path.parent.name
    translations: list[dict] = []
    for note in _notes(result):
        translated = translate_diagnosis(note, task_id)
        if not translated.get("diagnosis"):
            continue
        translations.append(
            {
                "note": note,
                "failure_type": translated.get("failure_type", ""),
                "matched_rule": translated.get("matched_rule", ""),
                "matched_keys": translated.get("matched_keys", []),
                "diagnosis": translated.get("diagnosis", ""),
                "repair_suggestions": translated.get("repair_suggestions", []),
                "has_task_id_specific_focus": bool(translated.get("circuit_specific")),
                "circuit_specific": translated.get("circuit_specific", ""),
            }
        )
    rules = [item["matched_rule"] for item in translations if item["matched_rule"]]
    task_specific = any(item["has_task_id_specific_focus"] for item in translations)
    return {
        "task_id": task_id,
        "status": result.get("status"),
        "scores": result.get("scores", {}),
        "failure_domain": result.get("failure_domain", ""),
        "notes": _notes(result),
        "h_v1_rules": rules,
        "h_v1_confidence": _confidence(translations),
        "h_v1_translation_count": len(translations),
        "h_v1_has_task_id_specific_focus": task_specific,
        "h_v1_needs_v2": (not translations) or all(rule in GENERIC_RULES for rule in rules),
        "translations": translations,
        "result_path": str(path),
    }


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")


def _write_markdown(path: Path, rows: list[dict], result_root: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for row in rows:
        key = row["h_v1_confidence"]
        counts[key] = counts.get(key, 0) + 1
    task_specific = sum(1 for row in rows if row["h_v1_has_task_id_specific_focus"])
    needs_v2 = sum(1 for row in rows if row["h_v1_needs_v2"])
    lines = [
        "# H-v1 Translation Audit For Final G Failures",
        "",
        f"Result root: `{result_root}`",
        "",
        "## Summary",
        "",
        f"- Failed tasks audited: {len(rows)}",
        f"- High confidence translations: {counts.get('high', 0)}",
        f"- Medium confidence translations: {counts.get('medium', 0)}",
        f"- Low confidence translations: {counts.get('low', 0)}",
        f"- Uses task-id-specific focus text: {task_specific}",
        f"- Needs H-v2 rule improvement: {needs_v2}",
        "",
        "## Rows",
        "",
        "| task | status | confidence | H-v1 rules | task-id focus | needs H-v2 | leading note |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for row in rows:
        rules = ", ".join(f"`{rule}`" for rule in row["h_v1_rules"][:4]) or "`none`"
        leading_note = ""
        for note in row["notes"]:
            if "returncode=" in note or "spectre_strict:preflight_pass" in note or note.startswith("generated_include="):
                continue
            leading_note = note
            break
        leading_note = leading_note.replace("|", "\\|")[:160]
        lines.append(
            f"| `{row['task_id']}` | `{row['status']}` | `{row['h_v1_confidence']}` | "
            f"{rules} | {str(row['h_v1_has_task_id_specific_focus']).lower()} | "
            f"{str(row['h_v1_needs_v2']).lower()} | {leading_note} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit H-v1 diagnosis translation on failed EVAS results.")
    parser.add_argument("--result-root", required=True)
    parser.add_argument("--output-jsonl", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    result_root = Path(args.result_root).resolve()
    rows = []
    for result_path in sorted(result_root.glob("*/result.json")):
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if result.get("status") == "PASS":
            continue
        rows.append(_audit_one(result_path))
    _write_jsonl(Path(args.output_jsonl), rows)
    _write_markdown(Path(args.output_md), rows, result_root)
    print(json.dumps({
        "failed_tasks": len(rows),
        "needs_v2": sum(1 for row in rows if row["h_v1_needs_v2"]),
        "task_id_specific_focus": sum(1 for row in rows if row["h_v1_has_task_id_specific_focus"]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
