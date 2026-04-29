# Weekly Status — 2026-04-05

## Summary

This week completed the first full round of benchmark seed task asset creation.

---

## What Was Done

### behavioral-veriloga-eval: feat/new-benchmark-seeds-2026-04-05

Created 10 new benchmark task directories under `tasks/end-to-end/voltage/`:

**shenbufan ownership:**
1. `lfsr_smoke` — 31-bit LFSR, digital-logic
2. `clk_burst_gen_smoke` — clock burst generator, stimulus
3. `digital_basics_smoke` — AND/OR/NOT/DFF, digital-logic

**liangyuxuan ownership:**
4. `dac_binary_clk_4b_smoke` — 4-bit clocked binary DAC
5. `adc_dac_ideal_4b_smoke` — ideal 4-bit ADC + DAC chain
6. `dwa_ptr_gen_smoke` — DWA pointer rotation, calibration

**team:**
7. `noise_gen_smoke` — Gaussian noise generator (tests `$rdist_normal`)
8. `dac_therm_16b_smoke` — 16-bit thermometer DAC
9. `sar_adc_dac_weighted_8b_smoke` — 8-bit SAR ADC + weighted DAC (hardest)
10. `gain_extraction_smoke` — multi-module dither gain extraction (most complex)

Each task includes: `prompt.md`, `meta.json` (tier=raw, verification_status=pending), `checks.yaml`.

### Runner improvements (simulate_evas.py, run_examples_suite.py)

- Extended `CHECKS` dict in `simulate_evas.py` to cover all 10 new `_smoke` task IDs
- Extended `TASK_BY_EXAMPLE` in `run_examples_suite.py` to map all 14 examples to their task dirs
- Fixed fallback in `task_dir_for()` to raise a clear error instead of silently using a wrong default
- Fixed manifest.json: corrected all paths from `behavioral-va-eval/` to `behavioral-veriloga-eval/`

### coordination: main

- `BENCHMARK_RESULT_TABLE.md`: added 10 new rows (all `raw/pending/benchmark-seed`)
- Committed stale doc cleanup (old root-level docs deleted, META_JSON_MIN_TEMPLATE added)
- `status/2026-04-05_weekly-status.md`: this file

---

## Current Benchmark Coverage

| tier | count | notes |
|---|---|---|
| `verified` | 5 | cppll_timer, cppll_param_shift, adpll_timer, adpll_idtmod, adpll_lock_smoke |
| `raw/pending` | 10 | all newly created task assets |
| no task yet | 0 | all examples now covered |

---

## Late Session Update (same date)

### 7 new examples added (behavioral-veriloga-eval)

New circuit categories covering voltage-domain only, no idt/idtmod:

| example | category |
|---|---|
| `sample_hold` | sample-hold (new) |
| `xor_phase_detector` | phase-detector (new) |
| `pfd_updn` | phase-detector (new) |
| `gray_counter_4b` | digital-logic |
| `mux_4to1` | digital-logic |
| `flash_adc_3b` | data-converter |
| `serializer_8b` | comms (new) |

Each includes `.va` + `tb_*.scs` + `validate_*.py` + benchmark task stub. `manifest.json` updated to 21 entries.

### Benchmark structure clarified

Benchmark has **four task families**, not just end-to-end:

| family | current count |
|---|---|
| `end-to-end` | 26 |
| `spec-to-va` | 12 |
| `bugfix` | 4 |
| `tb-generation` | 4 |
| **total** | **46** |

`spec-to-va`, `bugfix`, `tb-generation` currently lack gold answers and automated checks — this is the next critical gap to close.

### Documents updated

- `WORK_ASSIGNMENT.md`: rewritten to cover all four task families; both students have end-to-end parity + spec-to-va gold answers + bugfix/tb-generation verification tasks
- `BENCHMARK_EXPANSION_PLAN.md`: updated to reflect 4-family structure, corrected current state (46 tasks), revised student assignment section
- `BENCHMARK_RESULT_TABLE.md`: added tracking tables for spec-to-va (13 rows), bugfix (4 rows), tb-generation (4 rows)

---

## Next Steps

### shenbufan
1. Run EVAS + Spectre parity for: `lfsr_smoke`, `clk_burst_gen_smoke`, `digital_basics_smoke`, `gray_counter_4b_smoke`, `mux_4to1_smoke`, `xor_pd_smoke`, `pfd_updn_smoke`
2. Write gold `.va` for: `clk_divider`, `prbs7`, `therm2bin`, `bbpd`, `multimod_divider` (spec-to-va)
3. Write gold fixes for: `bad_bus_output_loop`, `missing_transition_outputs` (bugfix)

### liangyuxuan
1. Run EVAS + Spectre parity for: `dac_binary_clk_4b_smoke`, `adc_dac_ideal_4b_smoke`, `dwa_ptr_gen_smoke`, `noise_gen_smoke`, `dac_therm_16b_smoke`, `sar_adc_dac_weighted_8b_smoke`, `sample_hold_smoke`, `flash_adc_3b_smoke`, `serializer_8b_smoke`
2. Write gold `.va` for: `sar_logic`, `sar_12bit`, `d2b_4bit`, `pipeline_stage`, `segmented_dac`, `cdac_cal` (spec-to-va)
3. Write gold `.scs` for: `clk_div_min_tb`, `comparator_offset_tb`, `dac_ramp_tb`, `inl_dnl_probe` (tb-generation)

### team
1. PR `feat/new-benchmark-seeds-2026-04-05` → upstream (Arcadia-1)
2. Run AI model evaluation on all four task families once gold answers exist
3. Fill `AI_MODEL_EVAL_TABLE.md`
4. Write related work section
5. Build 3 paper figures

---

## Blockers

None known. Infrastructure is ready; gold answers and parity runs are pending student action.
