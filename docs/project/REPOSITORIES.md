# Repositories

`vaEvas` is a local workspace containing several independent repositories.

## Main Repositories

| Repository | Path | Current role |
| --- | --- | --- |
| `behavioral-veriloga-eval` | `/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval` | vaBench release package, runner, reports, checkers, score denominator, model baselines. |
| `EVAS` | `/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS` | Verilog-A evaluator and Spectre-alignment implementation. |
| `veriloga-skills` | `/Users/bucketsran/Documents/TsingProject/vaEvas/veriloga-skills` | Verilog-A generation and review knowledge. |
| `coordination` | `/Users/bucketsran/Documents/TsingProject/vaEvas/coordination` | Paper-facing coordination, related work, and collaboration notes. |
| `virtuoso-bridge-lite` | `/Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite` | Shared bridge for remote Virtuoso/Spectre runs. |

## Current Source Of Truth

For benchmark and paper claims, use:

```text
behavioral-veriloga-eval/benchmark-vabench-release-v1/
behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/
```

## Git Collaboration

Default remote convention:

1. `origin`: personal fork or local working remote.
2. `bucketsran`: bucketsran review/integration fork.
3. `upstream`: public upstream when applicable.

Open issues and PRs in the repository that owns the artifact:

| Change | Target repository |
| --- | --- |
| EVAS parser/kernel/preflight/parity | `EVAS` |
| benchmark release, runners, reports, checkers, baselines | `behavioral-veriloga-eval` |
| Verilog-A rule/skill updates | `veriloga-skills` |
| related work, coordination notes, collaboration docs | `coordination` |

Do not infer current tasks from old branch names or old coordination status
files. Use the release package and current mainline snapshot.
