# 2026-04 Pre-Paper-Pivot Archive

This archive keeps documents that were useful during earlier coordination and
benchmark-seed work, but are no longer part of the current paper-facing scan
path.

Archive date: 2026-04-26

Current paper narrative:

1. EVAS is behaviorally aligned with Spectre/Virtuoso.
2. EVAS is fast enough to serve as the inner loop for LLM Verilog-A repair.
3. The main condition ladder is A/D/F/H, with B/C/E/G treated as ablations.

Deletion rule:

1. Keep these files for at least one week after archive.
2. If no active paper, experiment, or coordination task references them during
   that period, they can be deleted in a later cleanup commit.
3. Do not delete them directly from this archive without first checking whether
   they contain unique experimental evidence.

Contents:

| Subdir | Files | Reason archived |
|---|---|---|
| `paper/` | `PAPER_STATS.md`, `paper_stats.json` | Historical 76-task paper stats; current paper uses the 92-task latest-system snapshot. |
| `benchmark/` | `CASE_SHOWCASE.md`, `CLOSED_LOOP_EXAMPLE_ADC.md`, `CLOSED_LOOP_EXAMPLE_COMPARATOR.md` | Older case-study notes; useful as appendix material, but not part of the current main scan path. |
| `project/` | `REPO_ADVANCEMENT_AND_RESEARCH_JUDGMENT_PLAN.md`, `WORK_ASSIGNMENT.md` | Older coordination/planning documents superseded by the current paper narrative and result snapshots. |

Not archived:

1. `docs/project/TASK_ASSIGNMENT.md` remains in place because the GitHub Actions
   sync check depends on it as a generated file.
2. `docs/benchmark/BENCHMARK_RESULT_TABLE.md` remains active because it is the
   source table for task-assignment synchronization.

