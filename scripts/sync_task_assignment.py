#!/usr/bin/env python3
"""Regenerate TASK_ASSIGNMENT.md from BENCHMARK_RESULT_TABLE.md."""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "benchmark" / "BENCHMARK_RESULT_TABLE.md"
OUTPUT = ROOT / "docs" / "project" / "TASK_ASSIGNMENT.md"

DEFAULT_COMMAND = "python coordination/scripts/sync_task_assignment.py"
CHECK_COMMAND = f"{DEFAULT_COMMAND} --check"

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
PRIORITY_LABEL = {"high": "高", "medium": "中", "low": "低"}
OWNER_ORDER = {"liangyuxuan": 0, "shenbufan": 1, "team": 2}


def normalize(value: str) -> str:
    return value.strip().strip("`").strip()


def lower(value: str) -> str:
    return normalize(value).lower()


def plain(value: str) -> str:
    return value.strip()


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_delimiter(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return False
    allowed = {"|", "-", " ", ":"}
    return all(ch in allowed for ch in stripped)


def parse_markdown_tables(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    tables: list[dict[str, object]] = []
    idx = 0

    while idx < len(lines) - 1:
        if not lines[idx].lstrip().startswith("|") or not is_table_delimiter(lines[idx + 1]):
            idx += 1
            continue

        header = split_markdown_row(lines[idx])
        rows: list[dict[str, str]] = []
        idx += 2

        while idx < len(lines) and lines[idx].lstrip().startswith("|"):
            cells = split_markdown_row(lines[idx])
            if len(cells) == len(header):
                rows.append(dict(zip(header, cells)))
            idx += 1

        tables.append({"header": header, "rows": rows})

    return tables


def classify_tables(tables: list[dict[str, object]]) -> tuple[list[dict[str, str]], ...]:
    case_rows: list[dict[str, str]] = []
    spec_rows: list[dict[str, str]] = []
    bugfix_rows: list[dict[str, str]] = []
    tb_rows: list[dict[str, str]] = []

    for table in tables:
        header = {normalize(name) for name in table["header"]}  # type: ignore[index]
        rows = table["rows"]  # type: ignore[index]
        if "case_name" in header:
            case_rows = rows  # type: ignore[assignment]
        elif "gold_answer_exists" in header:
            spec_rows = rows  # type: ignore[assignment]
        elif "gold_fix_exists" in header:
            bugfix_rows = rows  # type: ignore[assignment]
        elif "gold_tb_exists" in header:
            tb_rows = rows  # type: ignore[assignment]

    missing = []
    if not case_rows:
        missing.append("end-to-end/closed-loop table")
    if not spec_rows:
        missing.append("spec-to-va table")
    if not bugfix_rows:
        missing.append("bugfix table")
    if not tb_rows:
        missing.append("tb-generation table")
    if missing:
        raise SystemExit(f"Failed to locate required tables in {SOURCE}: {', '.join(missing)}")

    return case_rows, spec_rows, bugfix_rows, tb_rows


def format_code(value: str) -> str:
    text = normalize(value)
    if not text:
        return ""
    if text.startswith("`") and text.endswith("`"):
        return text
    return f"`{text}`"


def format_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    def sanitize(cell: str) -> str:
        return cell.replace("|", "\\|").replace("\n", " ").strip()

    lines = [
        "| " + " | ".join(sanitize(header) for header in headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(sanitize(cell) for cell in row) + " |")
    return lines


def priority_spec(row: dict[str, str]) -> str:
    category = lower(row["category"])
    task_name = normalize(row["task_name"])
    if category == "adc-sar" and task_name in {"sar_logic", "sar_12bit", "d2b_4bit"}:
        return "high"
    if category == "adc-sar":
        return "medium"
    if lower(row["owner"]) == "team":
        return "medium"
    return "medium"


def priority_bugfix(row: dict[str, str]) -> str:
    return "high" if lower(row["gold_fix_exists"]) == "yes" else "low"


def priority_tb(row: dict[str, str]) -> str:
    task_name = normalize(row["task_name"])
    if task_name in {"clk_div_min_tb", "comparator_offset_tb"}:
        return "medium"
    return "low"


def priority_case_issue(row: dict[str, str]) -> str:
    parity = lower(row["parity_status"])
    if parity == "spectre-idtmod-issue":
        return "medium"
    if lower(row["verification_status"]) != "passed":
        return "high"
    return "medium"


def next_action_spec(row: dict[str, str]) -> str:
    if lower(row["gold_answer_exists"]) != "yes":
        return "create gold DUT and automated check"
    return "run EVAS validation and backfill result row"


def next_action_bugfix(row: dict[str, str]) -> str:
    if lower(row["gold_fix_exists"]) == "yes":
        return "run EVAS validation and backfill result row"
    return "create gold dut_fixed.va and reference testbench"


def next_action_tb(row: dict[str, str]) -> str:
    if lower(row["gold_tb_exists"]) == "yes":
        return "run EVAS validation and backfill result row"
    return "create gold tb_*.scs and run EVAS"


def next_action_case_issue(row: dict[str, str]) -> str:
    parity = lower(row["parity_status"])
    if parity == "spectre-idtmod-issue":
        return "track known Spectre limitation; avoid treating as generic regression"
    if lower(row["verification_status"]) != "passed":
        return "close validation failure before promoting the row"
    return "review parity exception and decide if it needs dedicated closure work"


def sort_owner(name: str) -> tuple[int, str]:
    return OWNER_ORDER.get(lower(name), 99), lower(name)


def sort_by_priority(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(
        rows,
        key=lambda row: (
            PRIORITY_ORDER[row["derived_priority"]],
            sort_owner(row["owner"]),
            lower(row.get("category", "")),
            lower(row.get("task_name", row.get("case_name", ""))),
        ),
    )


def build_open_rows(
    rows: list[dict[str, str]],
    kind: str,
    priority_fn,
    next_action_fn,
    name_key: str,
) -> list[dict[str, str]]:
    open_rows: list[dict[str, str]] = []
    for row in rows:
        if lower(row["verification_status"]) == "passed":
            continue
        copied = dict(row)
        copied["derived_priority"] = priority_fn(row)
        copied["derived_next_action"] = next_action_fn(row)
        copied["derived_name"] = normalize(row[name_key])
        open_rows.append(copied)
    return sort_by_priority(open_rows)


def render_summary_section(
    case_rows: list[dict[str, str]],
    spec_rows: list[dict[str, str]],
    bugfix_rows: list[dict[str, str]],
    tb_rows: list[dict[str, str]],
) -> list[str]:
    dual_pass = sum(
        1
        for row in case_rows
        if lower(row["verification_status"]) == "passed" and lower(row["parity_status"]) == "dual-validated"
    )
    tracked_exceptions = sum(
        1
        for row in case_rows
        if lower(row["verification_status"]) == "passed" and lower(row["parity_status"]) not in {"dual-validated", "n/a"}
    )
    open_case_rows = sum(1 for row in case_rows if lower(row["verification_status"]) != "passed")

    spec_passed = sum(1 for row in spec_rows if lower(row["verification_status"]) == "passed")
    spec_pending_gold = sum(
        1 for row in spec_rows if lower(row["verification_status"]) != "passed" and lower(row["gold_answer_exists"]) != "yes"
    )
    spec_pending_validation = sum(
        1 for row in spec_rows if lower(row["verification_status"]) != "passed" and lower(row["gold_answer_exists"]) == "yes"
    )

    bugfix_pending_validation = sum(
        1 for row in bugfix_rows if lower(row["verification_status"]) != "passed" and lower(row["gold_fix_exists"]) == "yes"
    )
    bugfix_pending_gold = sum(
        1 for row in bugfix_rows if lower(row["verification_status"]) != "passed" and lower(row["gold_fix_exists"]) != "yes"
    )

    tb_pending_gold = sum(
        1 for row in tb_rows if lower(row["verification_status"]) != "passed" and lower(row["gold_tb_exists"]) != "yes"
    )
    tb_pending_validation = sum(
        1 for row in tb_rows if lower(row["verification_status"]) != "passed" and lower(row["gold_tb_exists"]) == "yes"
    )

    lines = ["## 当前状态概览", ""]
    lines.append("### benchmark / closed-loop 行")
    lines.extend(
        format_table(
            ["状态", "数量", "说明"],
            [
                ["已双验证通过", str(dual_pass), "verification_status=passed 且 parity_status=dual-validated"],
                ["特殊跟踪例外", str(tracked_exceptions), "passed 但 parity_status 不是 dual-validated"],
                ["未完成闭环", str(open_case_rows), "verification_status 仍非 passed"],
            ],
        )
    )
    lines.extend(["", "### spec-to-va 任务"])
    lines.extend(
        format_table(
            ["状态", "数量", "说明"],
            [
                ["已通过", str(spec_passed), "verification_status=passed"],
                ["待创建 gold", str(spec_pending_gold), "gold_answer_exists != yes"],
                ["待运行验证", str(spec_pending_validation), "gold_answer_exists=yes 但尚未 passed"],
            ],
        )
    )
    lines.extend(["", "### bugfix 任务"])
    lines.extend(
        format_table(
            ["状态", "数量", "说明"],
            [
                ["待运行验证", str(bugfix_pending_validation), "gold_fix_exists=yes 但 verification_status 尚未 passed"],
                ["待创建 gold", str(bugfix_pending_gold), "gold_fix_exists != yes"],
            ],
        )
    )
    lines.extend(["", "### tb-generation 任务"])
    lines.extend(
        format_table(
            ["状态", "数量", "说明"],
            [
                ["待创建 gold", str(tb_pending_gold), "gold_tb_exists != yes"],
                ["待运行验证", str(tb_pending_validation), "gold_tb_exists=yes 但 verification_status 尚未 passed"],
            ],
        )
    )
    return lines


def render_open_tasks_section(
    spec_rows: list[dict[str, str]],
    bugfix_rows: list[dict[str, str]],
    tb_rows: list[dict[str, str]],
) -> list[str]:
    spec_open = build_open_rows(spec_rows, "spec", priority_spec, next_action_spec, "task_name")
    bugfix_open = build_open_rows(bugfix_rows, "bugfix", priority_bugfix, next_action_bugfix, "task_name")
    tb_open = build_open_rows(tb_rows, "tb", priority_tb, next_action_tb, "task_name")

    owners = {
        normalize(row["owner"])
        for row in [*spec_open, *bugfix_open, *tb_open]
    }
    lines = ["## 当前需要推进的任务", ""]

    if not owners:
        lines.extend(["当前没有 `verification_status != passed` 的 open row。", ""])
        return lines

    for owner in sorted(owners, key=sort_owner):
        lines.append(f"### {owner}")
        lines.append("")

        owner_spec = [row for row in spec_open if normalize(row["owner"]) == owner]
        if owner_spec:
            lines.append("#### spec-to-va")
            lines.extend(
                format_table(
                    ["任务", "类别", "优先级", "当前状态", "下一步"],
                    [
                        [
                            format_code(row["task_name"]),
                            normalize(row["category"]),
                            PRIORITY_LABEL[row["derived_priority"]],
                            "pending",
                            row["derived_next_action"],
                        ]
                        for row in owner_spec
                    ],
                )
            )
            lines.append("")

        owner_bugfix = [row for row in bugfix_open if normalize(row["owner"]) == owner]
        if owner_bugfix:
            lines.append("#### bugfix")
            lines.extend(
                format_table(
                    ["任务", "问题类型", "优先级", "当前状态", "下一步"],
                    [
                        [
                            format_code(row["task_name"]),
                            plain(row["bug_type"]),
                            PRIORITY_LABEL[row["derived_priority"]],
                            "pending",
                            row["derived_next_action"],
                        ]
                        for row in owner_bugfix
                    ],
                )
            )
            lines.append("")

        owner_tb = [row for row in tb_open if normalize(row["owner"]) == owner]
        if owner_tb:
            lines.append("#### tb-generation")
            lines.extend(
                format_table(
                    ["任务", "优先级", "当前状态", "下一步"],
                    [
                        [
                            format_code(row["task_name"]),
                            PRIORITY_LABEL[row["derived_priority"]],
                            "pending",
                            row["derived_next_action"],
                        ]
                        for row in owner_tb
                    ],
                )
            )
            lines.append("")

    return lines


def render_exception_section(case_rows: list[dict[str, str]]) -> list[str]:
    special_rows = []
    for row in case_rows:
        parity = lower(row["parity_status"])
        if lower(row["verification_status"]) == "passed" and parity not in {"dual-validated", "n/a"}:
            copied = dict(row)
            copied["derived_priority"] = priority_case_issue(row)
            copied["derived_next_action"] = next_action_case_issue(row)
            special_rows.append(copied)

    lines = ["## 特殊跟踪项", ""]
    if not special_rows:
        lines.extend(["当前没有需要单独跟踪的 parity / simulator 例外。", ""])
        return lines

    lines.extend(
        format_table(
            ["案例", "优先级", "parity_status", "下一步", "result_path"],
            [
                [
                    format_code(row["case_name"]),
                    PRIORITY_LABEL[row["derived_priority"]],
                    normalize(row["parity_status"]),
                    row["derived_next_action"],
                    format_code(row["result_path"]),
                ]
                for row in sort_by_priority(special_rows)
            ],
        )
    )
    lines.append("")
    return lines


def render_priority_section(
    case_rows: list[dict[str, str]],
    spec_rows: list[dict[str, str]],
    bugfix_rows: list[dict[str, str]],
    tb_rows: list[dict[str, str]],
) -> list[str]:
    spec_open = build_open_rows(spec_rows, "spec", priority_spec, next_action_spec, "task_name")
    bugfix_open = build_open_rows(bugfix_rows, "bugfix", priority_bugfix, next_action_bugfix, "task_name")
    tb_open = build_open_rows(tb_rows, "tb", priority_tb, next_action_tb, "task_name")
    case_special = []
    for row in case_rows:
        parity = lower(row["parity_status"])
        if lower(row["verification_status"]) != "passed" or parity not in {"dual-validated", "n/a"}:
            copied = dict(row)
            copied["derived_priority"] = priority_case_issue(row)
            copied["derived_next_action"] = next_action_case_issue(row)
            case_special.append(copied)

    lines = ["## 优先级建议", "", "_这部分是根据结果表字段自动推导的启发式摘要，不再手工维护。_", ""]
    for priority in ("high", "medium", "low"):
        label = PRIORITY_LABEL[priority]
        lines.append(f"### {label}优先级")
        matched: list[str] = []

        for row in spec_open:
            if row["derived_priority"] == priority:
                matched.append(
                    f"- {normalize(row['owner'])}: {format_code(row['task_name'])} ({normalize(row['category'])}) -> {row['derived_next_action']}"
                )
        for row in bugfix_open:
            if row["derived_priority"] == priority:
                matched.append(
                    f"- {normalize(row['owner'])}: {format_code(row['task_name'])} -> {row['derived_next_action']}"
                )
        for row in tb_open:
            if row["derived_priority"] == priority:
                matched.append(
                    f"- {normalize(row['owner'])}: {format_code(row['task_name'])} -> {row['derived_next_action']}"
                )
        for row in case_special:
            if row["derived_priority"] == priority:
                matched.append(
                    f"- {normalize(row['owner'])}: {format_code(row['case_name'])} -> {row['derived_next_action']}"
                )

        if matched:
            lines.extend(matched)
        else:
            lines.append("- none")
        lines.append("")

    return lines


def render_completed_reference_section(spec_rows: list[dict[str, str]]) -> list[str]:
    passed_rows = sorted(
        [row for row in spec_rows if lower(row["verification_status"]) == "passed"],
        key=lambda row: (sort_owner(row["owner"]), lower(row["category"]), lower(row["task_name"])),
    )
    lines = ["## 已通过的 spec-to-va 参考行", ""]
    if not passed_rows:
        lines.extend(["当前没有 spec-to-va passed row。", ""])
        return lines

    lines.extend(
        format_table(
            ["owner", "任务", "类别", "pr_link", "result_path"],
            [
                [
                    normalize(row["owner"]),
                    format_code(row["task_name"]),
                    normalize(row["category"]),
                    format_code(row["pr_link"]),
                    format_code(row["result_path"]),
                ]
                for row in passed_rows
            ],
        )
    )
    lines.append("")
    return lines


def render_document(
    case_rows: list[dict[str, str]],
    spec_rows: list[dict[str, str]],
    bugfix_rows: list[dict[str, str]],
    tb_rows: list[dict[str, str]],
) -> str:
    today = dt.date.today().isoformat()
    lines = [
        "# vaEvas 任务分工表",
        "",
        f"> AUTO-GENERATED from `{SOURCE.relative_to(ROOT)}` by `{Path(__file__).relative_to(ROOT)}`.",
        "> Do not edit this file manually. Update the benchmark table, then rerun the syncer.",
        "",
        f"更新日期: {today}",
        "",
        "## 刷新命令",
        "",
        "```bash",
        DEFAULT_COMMAND,
        CHECK_COMMAND,
        "```",
        "",
    ]
    lines.extend(render_summary_section(case_rows, spec_rows, bugfix_rows, tb_rows))
    lines.extend(["", *render_open_tasks_section(spec_rows, bugfix_rows, tb_rows)])
    lines.extend(["", *render_exception_section(case_rows)])
    lines.extend(["", *render_priority_section(case_rows, spec_rows, bugfix_rows, tb_rows)])
    lines.extend(["", *render_completed_reference_section(spec_rows)])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Exit non-zero if TASK_ASSIGNMENT.md is stale.")
    parser.add_argument("--stdout", action="store_true", help="Print generated content to stdout.")
    args = parser.parse_args()

    text = SOURCE.read_text(encoding="utf-8")
    tables = parse_markdown_tables(text)
    case_rows, spec_rows, bugfix_rows, tb_rows = classify_tables(tables)
    rendered = render_document(case_rows, spec_rows, bugfix_rows, tb_rows)

    if args.stdout:
        sys.stdout.write(rendered)

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != rendered:
            sys.stderr.write(
                "TASK_ASSIGNMENT.md is stale. Run "
                f"`{DEFAULT_COMMAND}` from the vaEvas repo root.\n"
            )
            return 1
        sys.stdout.write("TASK_ASSIGNMENT.md is up to date.\n")
        return 0

    OUTPUT.write_text(rendered, encoding="utf-8")
    sys.stdout.write(f"Wrote {OUTPUT}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
