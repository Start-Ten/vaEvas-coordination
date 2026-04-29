# Benchmark-v2 Expanded to 400 Tasks

Date: 2026-04-29

## Summary

Benchmark-v2 has been expanded from the initial 30-task split to 400
materialized draft tasks.  The official 92-task tree was not modified; all new
tasks live under:

`behavioral-veriloga-eval/benchmark-v2/tasks/`

## Splits

| split | count | source | status |
|---|---:|---|---|
| `v2-small` | 30 | original 92 perturbation | EVAS 30/30, Spectre 30/30 |
| `v2-seed-perturbation-r1` | 30 | original 92 perturbation | EVAS validated |
| `v2-seed-perturbation-r2` | 120 | original 92 perturbation | EVAS validated |
| `v2-hard-negative-r1` | 100 | original 92 perturbation traps | EVAS validated |
| `v2-external-architecture-r1` | 120 | compact behavioral analog patterns | EVAS validated |
| total | 400 |  |  |

## Validation

| validation | result | root |
|---|---:|---|
| initial v2-small EVAS | 30/30 | `behavioral-veriloga-eval/results/benchmark-v2-gold-validation-2026-04-29-r2` |
| initial v2-small Spectre | 30/30 | `behavioral-veriloga-eval/results/benchmark-v2-gold-validation-spectre-2026-04-29-r1` |
| expanded new370 EVAS | 370/370 | `behavioral-veriloga-eval/results/benchmark-v2-new370-gold-evas-2026-04-29-r1` |
| expanded new370 Spectre | 370/370 | `behavioral-veriloga-eval/results/benchmark-v2-new370-gold-spectre-2026-04-29-r1` |
| expanded Spectre smoke | 12/12 | `behavioral-veriloga-eval/results/benchmark-v2-expanded400-gold-spectre-smoke-2026-04-29-r1` |

The expanded 370 tasks now have full EVAS and real Spectre gold validation.
Together with the initial `v2-small` split, benchmark-v2 has 400/400 EVAS gold
PASS and 400/400 Spectre gold PASS.

## What Changed

- Added manifest generator:
  `behavioral-veriloga-eval/runners/generate_benchmark_v2_expansion_manifests.py`
- Extended materializer:
  `behavioral-veriloga-eval/runners/materialize_benchmark_v2_tasks.py`
- Extended common checker:
  `behavioral-veriloga-eval/benchmark-v2/common_checker.py`
- Added three large manifests:
  - `v2-seed-perturbation-r2.json`
  - `v2-hard-negative-r1.json`
  - `v2-external-architecture-r1.json`

## Perturbation Coverage

The 400-task version now covers:

- semantic aliasing and port renaming
- width/ratio/timing parameter changes
- keyword removal
- negative constraints and template traps
- small system compositions
- external architecture patterns:
  - threshold detector
  - window detector
  - analog limiter
  - event pulse stretcher

## Next Step

Use this expanded split to evaluate whether grep/RAG/LEGO-style skill retrieval
generalizes beyond the original 92-task closed set.  Do not report teacher
materialization over these tasks as cold-start unless the generated artifact is
produced from the public prompt only.
