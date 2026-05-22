# Coordination Structure Guide

Date: 2026-05-21

`coordination/` is now intentionally small. It should point to current
paper-facing evidence, not preserve every historical experiment note.

## Read Order

1. [README.md](README.md)
2. [status/00_CURRENT_MAINLINE.md](status/00_CURRENT_MAINLINE.md)
3. [docs/project/PROJECT_OVERVIEW.md](docs/project/PROJECT_OVERVIEW.md)
4. [referencepaper/README.md](referencepaper/README.md)
5. `behavioral-veriloga-eval/benchmark-vabench-release-v1/README.md`
6. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/claim_gate.md`
7. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/score_denominator_manifest.md`
8. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/speed_debug_artifact.md`

## Directory Roles

| Directory | Role |
| --- | --- |
| `referencepaper/` | Verilog-A/AMS-centered related-work PDFs and reading map. |
| `status/` | One current mainline snapshot. |
| `docs/project/` | Project overview and repository map. |
| `docs/ops/` | Remaining issue/PR/sync workflow notes. |
| `onboarding/` | Minimal contributor entry points. |
| `skills/`, `templates/` | Reusable helper material. |

## What Was Removed

Old coordination notes for bpack48, benchmark-v2, full92, b143, historical
provider probes, generated translations, and one-off experiment ledgers were
removed or left only in existing archive directories. They are not current
paper evidence.

## Current Evidence Rule

For paper claims, cite release reports under:

```text
behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/
```

Do not cite stale coordination summaries for score, speed, baseline, or
certification claims.
