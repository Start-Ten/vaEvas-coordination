# ADFG Same-Baseline Current Result

Date: 2026-04-28

This table uses the same strict-v3 / real-Spectre-compatible result lineage:

| Condition | EVAS PASS | Spectre PASS | Main root |
|---|---:|---:|---|
| A | 23/92 | 23/92 | `results/condition-A-strictv3-kimi-full92-spectre-2026-04-28-rerun` |
| D | 43/92 | 43/92 | `results/condition-D-strictv3-kimi-table43-for-Gcold-evas-2026-04-28` plus Spectre-validated `lfsr_smoke` overlay |
| F | 59/92 | 59/92 | table-consistent F strict-v3 EVAS loop |
| G | 65/92 | 65/92 | `results/condition-G-targeted-materialized-spectre-aligned-kimi-evas-2026-04-28` and `results/condition-G-targeted-materialized-spectre-aligned-kimi-spectre-combined-2026-04-28` |

G replacement details:

- Base G full92 Spectre result: 61/92.
- New Spectre-validated replacements: `d2b_4bit`, `pipeline_stage`,
  `cmp_delay_smoke`, `dwa_wraparound_smoke`.
- Final G full92 EVAS rescore: 65/92.
- Final G Spectre count: 65/92, from the existing full92 Spectre run plus the
  targeted changed-task Spectre deltas.

Final G non-pass classes under EVAS:

- `FAIL_SIM_CORRECTNESS`: 25
- `FAIL_TB_COMPILE`: 2
