# Benchmark Result Table

This file is the team-wide result table for benchmark-seed experiments.

Use it to collect data from:

1. example execution
2. benchmark conversion
3. closed-loop parity validation
4. PR-based benchmark integration

It is intended to support both:

1. weekly engineering tracking
2. later paper tables and summary statistics

Before using any row in this table as your immediate local task, confirm that the referenced case already exists in the branch you are currently using.

If `coordination` lists a case but your local `behavioral-veriloga-eval` does not contain it yet:

1. first read [REPOSITORIES.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/project/REPOSITORIES.md)
2. then read [2026-04-12_repo-visibility-note.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/status/2026-04-12_repo-visibility-note.md)
3. only after checking remote / branch should you decide whether the row is stale

---

## Required Columns

Every new case should try to fill these columns first:

1. `owner`
2. `case_name`
3. `category`
4. `source_path`
5. `dut_compile`
6. `tb_compile`
7. `tran_generated`
8. `sim_correct`
9. `tier` (`raw` / `verified`)
10. `verification_status` (`pending` / `passed` / `failed`)
11. `benchmark_seed`
12. `result_path`
13. `pr_link`
14. `notes`

For closed-loop or dual-validation cases, also fill:

1. `evas_fb_hz`
2. `spectre_fb_hz`
3. `ppm_cross_delta`
4. `lock_time_delta_s`
5. `parity_status`

---

## Table

| owner | case_name | category | source_path | dut_compile | tb_compile | tran_generated | sim_correct | tier | verification_status | benchmark_seed | evas_fb_hz | spectre_fb_hz | ppm_cross_delta | lock_time_delta_s | parity_status | result_path | pr_link | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shenbufan | lfsr_smoke | digital-logic | `behavioral-veriloga-eval/tasks/end-to-end/voltage/lfsr_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; example: examples/digital-logic/lfsr |
| shenbufan | clk_burst_gen_smoke | stimulus | `behavioral-veriloga-eval/tasks/end-to-end/voltage/clk_burst_gen_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; example: examples/stimulus/clk_burst_gen |
| shenbufan | digital_basics_smoke | digital-logic | `behavioral-veriloga-eval/tasks/end-to-end/voltage/digital_basics_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; multi-module (AND/OR/NOT/DFF); example: examples/digital-logic/digital_basics |
| liangyuxuan | dac_binary_clk_4b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/dac_binary_clk_4b_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; example: examples/data-converter/dac_binary_clk_4b |
| liangyuxuan | adc_dac_ideal_4b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/adc_dac_ideal_4b_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; ADC+DAC chain; example: examples/data-converter/adc_dac_ideal_4b |
| liangyuxuan | dwa_ptr_gen_smoke | calibration | `behavioral-veriloga-eval/tasks/end-to-end/voltage/dwa_ptr_gen_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; example: examples/calibration/dwa_ptr_gen |
| team | noise_gen_smoke | stimulus | `behavioral-veriloga-eval/tasks/end-to-end/voltage/noise_gen_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; tests $rdist_normal semantic |
| team | dac_therm_16b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/dac_therm_16b_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; thermometer vs binary DAC contrast |
| team | sar_adc_dac_weighted_8b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/sar_adc_dac_weighted_8b_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; 8-bit SAR ADC — hardest data-converter task |
| team | gain_extraction_smoke | measurement | `behavioral-veriloga-eval/tasks/end-to-end/voltage/gain_extraction_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; multi-module dither-cross-correlation system |
| team | cppll_timer | pll-closed-loop | `vaEvas/testspace/cppll` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `seed` | `50e6` | `50e6` | `0.0` | `[TODO]` | `dual-validated` | `testspace/cppll/output/timer_full_while_fix` | `[TODO]` | while + timer parity closure |
| team | cppll_param_shift | pll-closed-loop | `vaEvas/testspace/cppll` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `seed` | `49e6` | `49e6` | `0.0` | `9.99e-08` | `dual-validated` | `testspace/cppll/output/timer_full_param_shift` | `[TODO]` | parameter robustness check |
| team | adpll_timer | pll-closed-loop | `vaEvas/testspace/adpll` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `seed` | `50e6` | `50e6` | `0.0` | `2.5e-11` | `dual-validated` | `testspace/adpll/output/adpll_full_tuned` | `[TODO]` | timer baseline |
| team | adpll_idtmod | pll-closed-loop | `vaEvas/testspace/adpll` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `seed` | `50e6` | `50e6` | `0.0` | `7.73e-12` | `dual-validated` | `testspace/adpll/output/adpll_idtmod_full` | `[TODO]` | idtmod compatibility path |
| team | adpll_lock_smoke | end-to-end-task | `behavioral-veriloga-eval/tasks/end-to-end/voltage/adpll_lock_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `formal-benchmark` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `task-check` | `[TODO]` | `[TODO]` | already formalized benchmark task |
| team | sample_hold_smoke | sample-hold | `behavioral-veriloga-eval/tasks/end-to-end/voltage/sample_hold_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; new category: sample-hold; example: examples/sample-hold/sample_hold |
| team | xor_pd_smoke | phase-detector | `behavioral-veriloga-eval/tasks/end-to-end/voltage/xor_pd_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; new category: phase-detector; XOR PD duty-cycle check |
| team | pfd_updn_smoke | phase-detector | `behavioral-veriloga-eval/tasks/end-to-end/voltage/pfd_updn_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; PFD with UP/DN reset logic; PLL-supporting |
| team | gray_counter_4b_smoke | digital-logic | `behavioral-veriloga-eval/tasks/end-to-end/voltage/gray_counter_4b_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; Gray code property check (1-bit change per step) |
| team | mux_4to1_smoke | digital-logic | `behavioral-veriloga-eval/tasks/end-to-end/voltage/mux_4to1_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; combinational 4-to-1 mux; all 4 select channels validated |
| team | flash_adc_3b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/flash_adc_3b_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; 3-bit flash ADC; all 8 codes + monotonicity check |
| team | serializer_8b_smoke | comms | `behavioral-veriloga-eval/tasks/end-to-end/voltage/serializer_8b_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `raw` | `pending` | `benchmark-seed` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | task assets created 2026-04-05; new category: comms; 8b P2S serializer bit-exact check |

---

## spec-to-va Results

Tracks AI-generated `.va` files evaluated against spec-to-va tasks.

### Required Columns

1. `owner`
2. `task_name`
3. `category`
4. `task_path`
5. `gold_answer_exists` (`yes` / `no`)
6. `dut_compile` (`pass` / `fail` / `[TODO]`)
7. `sim_correct` (`pass` / `fail` / `manual` / `[TODO]`)
8. `automated_check` (`yes` / `no` — whether `manual_review_expected_output` has been replaced)
9. `verification_status` (`pending` / `passed` / `failed`)
10. `result_path`
11. `pr_link`
12. `notes`

### Table

| owner | task_name | category | task_path | gold_answer_exists | dut_compile | sim_correct | automated_check | verification_status | result_path | pr_link | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shenbufan | clk_divider | digital-logic | `tasks/spec-to-va/voltage/digital-logic/clk_divider` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/clk_div_day1` | `origin/pr-2` | backfilled from `README_TASK_REPORT.md` (2026-04-07) and commits `d92479a`, `20e0fa4`, `c6f23a6`; branch not merged to `main` yet |
| shenbufan | prbs7 | digital-logic | `tasks/spec-to-va/voltage/digital-logic/prbs7` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/prbs7_day1` | `origin/pr-2` | backfilled from `README_TASK_REPORT.md` (2026-04-07) and commit `9608bfd`; branch not merged to `main` yet |
| shenbufan | therm2bin | digital-logic | `tasks/spec-to-va/voltage/digital-logic/therm2bin` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/therm2bin_day1` | `origin/pr-2` | backfilled from `README_TASK_REPORT.md` (2026-04-07) and commits `642b6e2`, `20e0fa4`, `c6f23a6`; branch not merged to `main` yet |
| shenbufan | bbpd | pll-clock | `tasks/spec-to-va/voltage/pll-clock/bbpd` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/bbpd_day1` | `origin/pr-2` | backfilled from `README_TASK_REPORT.md` (2026-04-07) and commit `aeb6f32`; branch not merged to `main` yet |
| shenbufan | multimod_divider | pll-clock | `tasks/spec-to-va/voltage/pll-clock/multimod_divider` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/multimod_divider_day1` | `origin/pr-2` | backfilled from `README_TASK_REPORT.md` (2026-04-07) and commit `49349b6`; branch not merged to `main` yet |
| liangyuxuan | sar_logic | adc-sar | `tasks/spec-to-va/voltage/adc-sar/sar_logic` | `no` | `[TODO]` | `[TODO]` | `no` | `pending` | `[TODO]` | `[TODO]` | needs gold .va + automated check |
| liangyuxuan | sar_12bit | adc-sar | `tasks/spec-to-va/voltage/adc-sar/sar_12bit` | `no` | `[TODO]` | `[TODO]` | `no` | `pending` | `[TODO]` | `[TODO]` | needs gold .va + automated check |
| liangyuxuan | d2b_4bit | adc-sar | `tasks/spec-to-va/voltage/adc-sar/d2b_4bit` | `no` | `[TODO]` | `[TODO]` | `no` | `pending` | `[TODO]` | `[TODO]` | needs gold .va + automated check |
| liangyuxuan | pipeline_stage | adc-sar | `tasks/spec-to-va/voltage/adc-sar/pipeline_stage` | `no` | `[TODO]` | `[TODO]` | `no` | `pending` | `[TODO]` | `[TODO]` | needs gold .va + automated check |
| liangyuxuan | segmented_dac | dac | `tasks/spec-to-va/voltage/dac/segmented_dac` | `no` | `[TODO]` | `[TODO]` | `no` | `pending` | `[TODO]` | `[TODO]` | needs gold .va + automated check |
| liangyuxuan | cdac_cal | dac | `tasks/spec-to-va/voltage/dac/cdac_cal` | `no` | `[TODO]` | `[TODO]` | `no` | `pending` | `[TODO]` | `[TODO]` | needs gold .va + automated check |
| team | sc_integrator | amplifier-filter | `tasks/spec-to-va/voltage/amplifier-filter/sc_integrator` | `no` | `[TODO]` | `[TODO]` | `no` | `pending` | `[TODO]` | `[TODO]` | switched-cap integrator; needs gold .va |
| team | bg_cal | calibration | `tasks/spec-to-va/voltage/calibration/bg_cal` | `no` | `[TODO]` | `[TODO]` | `no` | `pending` | `[TODO]` | `[TODO]` | background calibration; needs gold .va |

---

## bugfix Results

Tracks AI-generated bug fixes evaluated against bugfix tasks.

### Required Columns

1. `owner`
2. `task_name`
3. `bug_type`
4. `task_path`
5. `gold_fix_exists` (`yes` / `no`)
6. `dut_compile` (`pass` / `fail` / `[TODO]`)
7. `bug_fixed` (`pass` / `fail` / `[TODO]`)
8. `verification_status`
9. `notes`

### Table

| owner | task_name | bug_type | task_path | gold_fix_exists | dut_compile | bug_fixed | verification_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shenbufan | bad_bus_output_loop | wrong vector assignment `V(DOUT)<+` vs `V(DOUT[i])<+` | `tasks/bugfix/voltage/bad_bus_output_loop` | `yes` | `[TODO]` | `[TODO]` | `pending` | commit `7d97305` added `gold/dut_fixed.va` + `gold/tb_bad_bus_output_loop.scs` + automated EVAS check; run evidence not backfilled yet |
| shenbufan | missing_transition_outputs | output port missing `transition()` wrapper | `tasks/bugfix/voltage/missing_transition_outputs` | `yes` | `[TODO]` | `[TODO]` | `pending` | commit `7d97305` added `gold/dut_fixed.va` + `gold/tb_missing_transition_outputs.scs` + automated EVAS check; run evidence not backfilled yet |
| team | mixed_domain_cdac_bug | mixed `I()<+` and voltage-domain constructs | `tasks/bugfix/voltage/mixed_domain_cdac_bug` | `no` | `[TODO]` | `[TODO]` | `pending` | needs gold `dut_fixed.va` |
| team | spectre_port_discipline | `inout electrical A, B` sharing — Spectre rejects | `tasks/bugfix/voltage/spectre_port_discipline` | `no` | `[TODO]` | `[TODO]` | `pending` | needs gold `dut_fixed.va` |

---

## tb-generation Results

Tracks AI-generated testbenches evaluated against tb-generation tasks.

### Required Columns

1. `owner`
2. `task_name`
3. `task_path`
4. `gold_tb_exists` (`yes` / `no`)
5. `tb_compile` (`pass` / `fail` / `[TODO]`)
6. `tran_generated` (`pass` / `fail` / `[TODO]`)
7. `verification_status`
8. `notes`

### Table

| owner | task_name | task_path | gold_tb_exists | tb_compile | tran_generated | verification_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| liangyuxuan | clk_div_min_tb | `tasks/tb-generation/voltage/clk_div_min_tb` | `no` | `[TODO]` | `[TODO]` | `pending` | needs gold `tb_*.scs` + EVAS run |
| liangyuxuan | comparator_offset_tb | `tasks/tb-generation/voltage/comparator_offset_tb` | `no` | `[TODO]` | `[TODO]` | `pending` | needs gold `tb_*.scs` + EVAS run |
| liangyuxuan | dac_ramp_tb | `tasks/tb-generation/voltage/dac_ramp_tb` | `no` | `[TODO]` | `[TODO]` | `pending` | needs gold `tb_*.scs` + EVAS run |
| liangyuxuan | inl_dnl_probe | `tasks/tb-generation/voltage/testbench/inl_dnl_probe` | `no` | `[TODO]` | `[TODO]` | `pending` | needs gold `tb_*.scs` + EVAS run |

---

## Fill Rules

1. Use `pass` / `fail` / `N/A` where possible, not free-form wording.
2. Use absolute result paths or repository-relative result paths that others can reproduce.
3. If a case is not dual-validated, fill parity columns with `N/A`.
4. If a PR does not exist yet, keep `pr_link` as `[TODO]`.
5. If a result is provisional, say so in `notes`.
6. New rows default to `tier=raw` and `verification_status=pending`.
7. Only after passing the required validation gate can a row be promoted to `tier=verified` and `verification_status=passed`.

---

## Suggested Weekly Summary

At the end of each week, summarize:

1. how many rows were newly filled
2. how many cases are in `raw` vs `verified`
3. how many rows were promoted (`raw -> verified`)
4. how many cases reached `benchmark_seed`
5. how many cases reached `formal-benchmark`
6. how many rows are blocked by compile/runtime/check issues
7. top repeated failure modes
