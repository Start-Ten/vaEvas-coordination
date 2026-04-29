# Remote Results

This directory stores coordination-facing plans, result indexes, and handoff
templates for experiments that are expected to run on another machine or by
another teammate.

Do not put large generated artifacts here.  Keep this directory small:

1. assignment brief
2. command log
3. aggregate result table
4. links or relative paths to the actual `behavioral-veriloga-eval/results/...`
   and `behavioral-veriloga-eval/generated...` artifacts
5. known blockers and rerun notes

Current active remote experiment:

1. [2026-04-27_multi-model-a-i](./2026-04-27_multi-model-a-i/README.md)

Before using local reference numbers, check:

```text
coordination/docs/benchmark/EXPERIMENT_RESULT_LEDGER.md
```

The 2026-04-27 Kimi A/B/C current-regression rows are currently marked
`invalid-baseline` because of dry-run placeholder contamination.
