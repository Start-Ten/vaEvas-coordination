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

After editing this table, rerun `python coordination/scripts/sync_task_assignment.py` so the derived task summary stays in sync.

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
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shenbufan | lfsr_smoke | digital-logic | `behavioral-veriloga-eval/tasks/end-to-end/voltage/lfsr_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/lfsr_smoke/lfsr_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation on 2026-04-17: transitions=196, hi_frac=0.478/0.472, max_nrmse=0.182 |
| shenbufan | clk_burst_gen_smoke | stimulus | `behavioral-veriloga-eval/tasks/end-to-end/voltage/clk_burst_gen_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/clk_burst_gen_smoke/clk_burst_gen_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation on 2026-04-17: clk_out_hi_frac=0.214/0.214, rising_edges=8, max_nrmse=0.0025 |
| shenbufan | digital_basics_smoke | digital-logic | `behavioral-veriloga-eval/tasks/end-to-end/voltage/digital_basics_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/digital_basics_smoke/digital_basics_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation on 2026-04-17: invert_match_frac=1.000, max_nrmse=0.01 |
| liangyuxuan | dac_binary_clk_4b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/dac_binary_clk_4b_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/dac_binary_clk_4b_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation via `run_gold_dual_suite.py` on 2026-04-16; p95/max_nrmse=0.0718 |
| liangyuxuan | adc_dac_ideal_4b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/adc_dac_ideal_4b_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/adc_dac_ideal_4b_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation on 2026-04-16; parity closed with digital-aware alignment update (p95/max_nrmse=0.1224) |
| liangyuxuan | dwa_ptr_gen_smoke | calibration | `behavioral-veriloga-eval/tasks/end-to-end/voltage/dwa_ptr_gen_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/dwa_ptr_gen_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation via `run_gold_dual_suite.py` on 2026-04-16; p95_nrmse=0.1323 max_nrmse=0.1825 |
| team | cmp_delay_smoke | comparator | `behavioral-veriloga-eval/tasks/end-to-end/voltage/cmp_delay_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-benchmark-expansion/cmp_delay_smoke` | `codex/upstream-complete-pr` | EVAS+Spectre dual validation on 2026-04-18 using the benchmark gold's explicit low-warning output style; both simulators preserve the four-phase monotonic delay trend with delays 0.08/0.09/0.10/0.11 ns and max_nrmse=0.1825. |
| team | comparator_hysteresis_smoke | comparator | `behavioral-veriloga-eval/tasks/end-to-end/voltage/comparator_hysteresis_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-expansion-2026-04-19/comparator_hysteresis_smoke` | `[TODO]` | EVAS+Spectre dual validation on 2026-04-19; hysteresis trip windows close with EVAS rise/fall times 30.025/70.075 ns, Spectre 30.065/70.065 ns, and max_nrmse=0.0017. |
| team | comparator_offset_search_smoke | comparator | `behavioral-veriloga-eval/tasks/end-to-end/voltage/comparator_offset_search_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `behavioral-veriloga-eval/results/gold-suite-p1-e2e-2026-04-19/comparator_offset_search_smoke` | `[TODO]` | Added on 2026-04-19 as a comparator offset-extraction benchmark. EVAS gold validation passes with `crossing_voltage=0.5050`, `low_frac=1.000`, and `high_frac=1.000`; bridge-backed dual validation is intentionally still pending under the current no-bridge queue rules. |
| team | cmp_strongarm_smoke | comparator | `behavioral-veriloga-eval/tasks/end-to-end/voltage/cmp_strongarm_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-benchmark-expansion/cmp_strongarm_smoke` | `codex/upstream-complete-pr` | EVAS+Spectre dual validation on 2026-04-18 using the benchmark gold's explicit low-warning output style; polarity swap behavior closes with EVAS pre/post fractions 0.444/1.000, Spectre 0.607/1.000, and max_nrmse=0.0175. |
| team | dwa_ptr_gen_no_overlap_smoke | calibration | `behavioral-veriloga-eval/tasks/end-to-end/voltage/dwa_ptr_gen_no_overlap_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-benchmark-expansion/dwa_ptr_gen_no_overlap_smoke` | `codex/upstream-complete-pr` | EVAS+Spectre dual validation on 2026-04-18 with no-overlap rotation checks enabled; both simulators pass sampled_cycles=17 with overlap_count=0, and parity is dominated only by analog clock-edge shape (max_nrmse=0.1802). |
| team | dwa_wraparound_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/dwa_wraparound_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `behavioral-veriloga-eval/results/gold-suite-p2-dwa-wraparound-2026-04-19/dwa_wraparound_smoke` | `[TODO]` | Added on 2026-04-19 as a P2 DWA pointer wraparound benchmark. EVAS gold validation passes with sampled_cycles=8, bad_ptr_rows=0, bad_count_rows=0, wrap_events=3, and split_wrap_rows=3; bridge-backed dual validation is intentionally deferred. |
| team | noise_gen_smoke | stimulus | `behavioral-veriloga-eval/tasks/end-to-end/voltage/noise_gen_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/noise_gen_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation via `run_gold_dual_suite.py` on 2026-04-16; p95/max_nrmse=0.1124 |
| team | dac_therm_16b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/dac_therm_16b_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/dac_therm_16b_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation via `run_gold_dual_suite.py` on 2026-04-16; p95/max_nrmse=0.0999 |
| team | sar_adc_dac_weighted_8b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/sar_adc_dac_weighted_8b_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final-v7/sar_adc_dac_weighted_8b_smoke` | `feat/liangyuxuan-pr-1` | Fixed on 2026-04-17: fin 1MHz→100kHz (slower sine gives finer vin resolution), stop 5us→10us (500 samples across one full sine cycle); unique_codes=224, avg_abs_err=0.0021, max_nrmse=0.006; commit 5dabc0d |
| team | gain_extraction_smoke | measurement | `behavioral-veriloga-eval/tasks/end-to-end/voltage/gain_extraction_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gain_extraction_smoke/gain_extraction_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation on 2026-04-17: diff_gain=11.14, max_nrmse=0.114 |
| team | cppll_timer | pll-closed-loop | `vaEvas/testspace/cppll` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `seed` | `50e6` | `50e6` | `0.0` | `[TODO]` | `dual-validated` | `testspace/cppll/output/timer_full_while_fix` | `[TODO]` | Timer-based CPPLL seed reference with 50 MHz EVAS/Spectre parity closure; benchmark-facing task rows now live under `cppll_timer` and `cppll_tracking_smoke`. |
| team | cppll_param_shift | pll-closed-loop | `vaEvas/testspace/cppll` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `seed` | `49e6` | `49e6` | `0.0` | `9.99e-08` | `dual-validated` | `testspace/cppll/output/timer_full_param_shift` | `[TODO]` | CPPLL parameter-robustness seed with 49 MHz EVAS/Spectre parity closure. |
| team | adpll_timer | pll-closed-loop | `vaEvas/testspace/adpll` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `seed` | `50e6` | `50e6` | `0.0` | `2.5e-11` | `dual-validated` | `testspace/adpll/output/adpll_full_tuned` | `[TODO]` | Timer-based ADPLL seed reference with 50 MHz EVAS/Spectre parity closure; benchmark-facing task rows now live under `adpll_timer` and `adpll_timer_smoke`. |
| team | adpll_idtmod | pll-closed-loop | `vaEvas/testspace/adpll` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `seed` | `50e6` | `50e6` | `0.0` | `7.73e-12` | `dual-validated` | `testspace/adpll/output/adpll_idtmod_full` | `[TODO]` | ADPLL `idtmod` seed reference retained for compatibility comparisons in PLL parity work. |
| team | adpll_lock_smoke | end-to-end-task | `behavioral-veriloga-eval/tasks/end-to-end/voltage/adpll_lock_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `formal-benchmark` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-adpll-lock-recheck-2026-04-18/adpll_lock_smoke` | `feat/adpll-lock-smoke-benchmark` | Revalidated on 2026-04-18 with task-aware PLL parity; EVAS and Spectre both lock at about 80 ns and late-window feedback frequency matches, while `vctrl_mon` remains informational because Spectre still reports 0 V in this idtmod path. |
| team | adpll_timer_smoke | pll-closed-loop | `behavioral-veriloga-eval/tasks/end-to-end/voltage/adpll_timer_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `formal-benchmark` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-pll-optimized-2026-04-18/adpll_timer_smoke` | `codex/upstream-complete-pr` | Task-aware PLL parity closed on 2026-04-18; late-window lock timing and feedback frequency agree, while `vctrl_mon` is informational because Spectre keeps it at 0 V in this path. |
| team | adpll_ratio_hop_smoke | pll-closed-loop | `behavioral-veriloga-eval/tasks/end-to-end/voltage/adpll_ratio_hop_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `formal-benchmark` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `behavioral-veriloga-eval/results/gold-suite-adpll-ratio-hop-2026-04-19/adpll_ratio_hop_smoke` | `[TODO]` | Added on 2026-04-19 as a PLL ratio-hop benchmark. EVAS gold validation passes with `hop_t=2.000e-06`, `pre_ratio=4.000`, `post_ratio=6.000`, and both pre/post lock windows asserted; bridge-backed dual validation is intentionally still pending under the current no-bridge queue rules. |
| team | multimod_divider_ratio_switch_smoke | pll | `behavioral-veriloga-eval/tasks/end-to-end/voltage/multimod_divider_ratio_switch_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `formal-benchmark` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `behavioral-veriloga-eval/results/gold-suite-p1-e2e-2026-04-19/multimod_divider_ratio_switch_smoke` | `[TODO]` | Added on 2026-04-19 as a ratio-switch divider benchmark. EVAS gold validation passes with `pre_div4=4.00`, `mid_div5=5.00`, and `post_div4=4.00`; bridge-backed dual validation is intentionally still pending under the current no-bridge queue rules. |
| team | cppll_freq_step_reacquire_smoke | pll-closed-loop | `behavioral-veriloga-eval/tasks/end-to-end/voltage/cppll_freq_step_reacquire_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `formal-benchmark` | `50182815.354` | `50208267.834` | `506.94` | `8.042e-11` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-cppll-initial-step-fix-v2/cppll_freq_step_reacquire_smoke` | `[TODO]` | Added on 2026-04-19 as a PLL relock benchmark. The old 292.5 ns gap was traced to an asymmetric relock anchor; the canonical initial-step-fix-v2 dual-suite closes task-aware PLL parity with relock_time_delta_s=8.04e-11, pre_lock_time_delta_s=6.72e-11, late_fb_freq_rel_delta=5.07e-4, and late_vctrl_mean_delta_v=1.81mV. Residual late-lock pulse tail differences remain tracked separately in the EVAS/Spectre alignment audit rather than as a benchmark blocker. |
| team | cppll_tracking_smoke | pll-closed-loop | `behavioral-veriloga-eval/tasks/end-to-end/voltage/cppll_tracking_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `formal-benchmark` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-pll-optimized-2026-04-18/cppll_tracking_smoke` | `codex/upstream-complete-pr` | Task-aware PLL parity closed on 2026-04-18 using late-window tracking metrics and bounded `vctrl_mon`, while free-running `dco_clk` phase remains intentionally informational. |
| team | sample_hold_smoke | sample-hold | `behavioral-veriloga-eval/tasks/end-to-end/voltage/sample_hold_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/sample_hold_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation via `run_gold_dual_suite.py` on 2026-04-16; p95/max_nrmse=0.0815 |
| team | xor_pd_smoke | phase-detector | `behavioral-veriloga-eval/tasks/end-to-end/voltage/xor_pd_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/xor_pd_fix_final/xor_pd_smoke` | `feat/new-benchmark-seeds-2026-04-05` | Fixed testbench delay=2.5ns→5ns (true 90° phase shift); EVAS+Spectre dual validation on 2026-04-17: duty=0.502, p95/max_nrmse=0.01 |
| team | pfd_deadzone_smoke | phase-detector | `behavioral-veriloga-eval/tasks/end-to-end/voltage/pfd_deadzone_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-expansion-2026-04-19/pfd_deadzone_smoke` | `[TODO]` | EVAS+Spectre dual validation on 2026-04-19 for near-deadzone short-pulse behavior; weighted UP duty closes at 0.0050 in both simulators with 15 pulses and max_nrmse=0.0008, and the pass also hardened the runner against adaptive-step duty mismeasurement. |
| team | pfd_reset_race_smoke | phase-detector | `behavioral-veriloga-eval/tasks/end-to-end/voltage/pfd_reset_race_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `formal-benchmark` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `behavioral-veriloga-eval/results/gold-suite-pfd-reset-race-2026-04-19/pfd_reset_race_smoke` | `[TODO]` | Added on 2026-04-19 as a near-simultaneous REF/FB race benchmark. EVAS gold validation passes with `up_first=0.0100`, `dn_second=0.0100`, `up_pulses_first=5`, `dn_pulses_second=5`, and `overlap_frac=0.0000`; bridge-backed dual validation is intentionally still pending under the current no-bridge queue rules. |
| team | pfd_updn_smoke | phase-detector | `behavioral-veriloga-eval/tasks/end-to-end/voltage/pfd_updn_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/pfd_updn_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation via `run_gold_dual_suite.py` on 2026-04-16; p95/max_nrmse=0.0586 |
| team | gray_counter_4b_smoke | digital-logic | `behavioral-veriloga-eval/tasks/end-to-end/voltage/gray_counter_4b_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/gray_counter_4b_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation via `run_gold_dual_suite.py` on 2026-04-16; p95/max_nrmse=0.0815 |
| team | gray_counter_one_bit_change_smoke | digital-logic | `behavioral-veriloga-eval/tasks/end-to-end/voltage/gray_counter_one_bit_change_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `behavioral-veriloga-eval/results/gold-suite-p1-e2e-2026-04-19/gray_counter_one_bit_change_smoke` | `[TODO]` | Added on 2026-04-19 as a Gray-code adjacency benchmark. EVAS gold validation passes with `unique_codes=16` and `bad_transitions=0`; bridge-backed dual validation is intentionally still pending under the current no-bridge queue rules. |
| team | mux_4to1_smoke | digital-logic | `behavioral-veriloga-eval/tasks/end-to-end/voltage/mux_4to1_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/mux_4to1_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation via `run_gold_dual_suite.py` on 2026-04-16; p95/max_nrmse=0.0182 |
| team | flash_adc_3b_smoke | data-converter | `behavioral-veriloga-eval/tasks/end-to-end/voltage/flash_adc_3b_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final/flash_adc_3b_smoke` | `feat/new-benchmark-seeds-2026-04-05` | EVAS+Spectre dual validation via `run_gold_dual_suite.py` on 2026-04-16; p95/max_nrmse=0.0815 |
| team | serializer_8b_smoke | comms | `behavioral-veriloga-eval/tasks/end-to-end/voltage/serializer_8b_smoke` | `pass` | `pass` | `pass` | `pass` | `verified` | `passed` | `benchmark-seed` | `N/A` | `N/A` | `N/A` | `N/A` | `dual-validated` | `behavioral-veriloga-eval/results/gold-dual-suite-final-v7/serializer_8b_smoke` | `feat/liangyuxuan-pr-1` | Fixed on 2026-04-17: (1) tb: LOAD width 15n→12.5n avoids race with CLK at t=20ns; (2) check: wait 1ns after CLK before sampling sout (transition settle time); 0xA5 serialized MSB-first correctly, max_nrmse=0.02; commit 91eeecb |

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
| shenbufan | clk_divider | digital-logic | `tasks/spec-to-va/voltage/digital-logic/clk_divider` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/clk_divider` | `origin/pr-2` | EVAS gold validation refreshed on 2026-04-18; dual validation also closed in the non-e2e refresh run for divide-by-5 behavior with lock assertion. |
| shenbufan | prbs7 | digital-logic | `tasks/spec-to-va/voltage/digital-logic/prbs7` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/prbs7` | `origin/pr-2` | EVAS gold validation refreshed on 2026-04-18 after widening serial column matching; dual validation also closed in the non-e2e refresh run with `transitions=53` and `hi_frac=0.529`. |
| shenbufan | therm2bin | digital-logic | `tasks/spec-to-va/voltage/digital-logic/therm2bin` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/therm2bin` | `origin/pr-2` | EVAS gold validation refreshed on 2026-04-18 after accepting `bin_*` outputs in the automated check; dual validation also closed in the non-e2e refresh run with `all_bits_high_final_window=True`. |
| shenbufan | bbpd | pll-clock | `tasks/spec-to-va/voltage/pll-clock/bbpd` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/bbpd` | `origin/pr-2` | EVAS gold validation refreshed on 2026-04-18; dual validation also closed in the non-e2e refresh run with `data_edges=150`, `up_edges=60`, and `down_edges=60`. |
| shenbufan | multimod_divider | pll-clock | `tasks/spec-to-va/voltage/pll-clock/multimod_divider` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/multimod_divider` | `origin/pr-2` | EVAS gold validation refreshed on 2026-04-18; dual validation also closed in the non-e2e refresh run with `base=4`, `pre_count=9`, and `post_count=9`. |
| liangyuxuan | sar_logic | adc-sar | `tasks/spec-to-va/voltage/adc-sar/sar_logic` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/sar_logic` | `feat/liangyuxuan-pr-1` | Gold DUT and automated check validated under EVAS on 2026-04-18; dual validation also closed in the non-e2e refresh run with `rdy_asserted=True` and `dac_activity=True`. |
| liangyuxuan | sar_12bit | adc-sar | `tasks/spec-to-va/voltage/adc-sar/sar_12bit` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/sar_12bit` | `feat/liangyuxuan-pr-1` | Gold DUT and automated check validated under EVAS on 2026-04-18; dual validation also closed in the non-e2e refresh run with `rdy_asserted=True` and `dac_activity=True`. |
| liangyuxuan | d2b_4bit | adc-sar | `tasks/spec-to-va/voltage/adc-sar/d2b_4bit` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/d2b_4bit` | `feat/liangyuxuan-pr-1` | Gold DUT and automated check validated under EVAS on 2026-04-18; dual validation also closed in the non-e2e refresh run with the dynamic monotonic code check passing under Spectre. |
| liangyuxuan | pipeline_stage | adc-sar | `tasks/spec-to-va/voltage/adc-sar/pipeline_stage` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/pipeline_stage` | `feat/liangyuxuan-pr-1` | EVAS validation passed on 2026-04-18; the refreshed dual run also closes parity with `vres_range=0.140`, `bounded=True`, and `d_active=True`. |
| liangyuxuan | segmented_dac | dac | `tasks/spec-to-va/voltage/dac/segmented_dac` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/segmented_dac` | `feat/liangyuxuan-pr-1` | Added reference testbench and validated under EVAS on 2026-04-18; the refreshed dual run also closes parity with `diff_range=0.400`. |
| liangyuxuan | cdac_cal | dac | `tasks/spec-to-va/voltage/dac/cdac_cal` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/cdac_cal` | `codex/upstream-complete-pr` | Gold DUT/reference testbench validate under EVAS on 2026-04-18; the non-e2e refresh run also closes dual validation with `VDAC_N` activity range `0.150`. |
| team | sc_integrator | amplifier-filter | `tasks/spec-to-va/voltage/amplifier-filter/sc_integrator` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/sc_integrator` | `codex/upstream-complete-pr` | Gold DUT/reference testbench validate under EVAS on 2026-04-18; the non-e2e refresh run also closes dual validation with `monotonic=True` and `total_step=0.480`. |
| team | bg_cal | calibration | `tasks/spec-to-va/voltage/calibration/bg_cal` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/bg_cal` | `codex/upstream-complete-pr` | Gold DUT/reference testbench validate under EVAS on 2026-04-18; convergence was tuned so `settled` asserts, and the non-e2e refresh run closes dual validation with `code_span=8` and `settled_high=True`. |
| team | adpll_timer | pll-clock | `tasks/spec-to-va/voltage/pll-clock/adpll_timer` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-suite-pll-2026-04-18/adpll_timer` | `codex/upstream-complete-pr` | EVAS gold validation passes, and the PLL-optimized dual run closes task-aware parity in `results/gold-dual-suite-pll-optimized-2026-04-18/adpll_timer`. |
| team | cppll_timer | pll-clock | `tasks/spec-to-va/voltage/pll-clock/cppll_timer` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-suite-pll-2026-04-18/cppll_timer` | `codex/upstream-complete-pr` | EVAS gold validation passes, and the PLL-optimized dual run closes task-aware parity with retryable Spectre upload handling in `results/gold-dual-suite-pll-optimized-2026-04-18/cppll_timer`. |
| team | multitone | signal-source | `tasks/spec-to-va/voltage/signal-source/multitone` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/multitone` | `codex/upstream-complete-pr` | Gold DUT/reference testbench validate waveform samples under EVAS on 2026-04-18; the non-e2e refresh run also closes dual validation with `max_err=0.0002`. |
| team | nrz_prbs | signal-source | `tasks/spec-to-va/voltage/signal-source/nrz_prbs` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/nrz_prbs` | `codex/upstream-complete-pr` | Gold DUT/reference testbench validate under EVAS on 2026-04-18 after increasing the testbench data rate; the non-e2e refresh run also closes dual validation with `transitions=16`, `complement_err=0.0000`, and `swing=0.600`. |
| team | sar_logic_10b | adc-sar | `tasks/spec-to-va/voltage/sar_logic_10b` | `yes` | `pass` | `pass` | `yes` | `passed` | `behavioral-veriloga-eval/results/gold-dual-suite-non-e2e-refresh-2026-04-18/sar_logic_10b` | `feat/liangyuxuan-pr-1` | EVAS gold validation completed on 2026-04-18 via `run_gold_suite.py`; dual validation also closed in the non-e2e refresh run with `rdy_asserted=True` and `dac_activity=True`. |

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
| shenbufan | bad_bus_output_loop | wrong vector assignment `V(DOUT)<+` vs `V(DOUT[i])<+` | `tasks/bugfix/voltage/bad_bus_output_loop` | `yes` | `pass` | `pass` | `passed` | EVAS gold validation refreshed on 2026-04-18 using the benchmark gold's explicit supply-scaled transition style; dual validation also closed in the non-e2e refresh run with `mismatch_frac=0.0000` and `code_patterns=16`. |
| shenbufan | missing_transition_outputs | output port missing `transition()` wrapper | `tasks/bugfix/voltage/missing_transition_outputs` | `yes` | `pass` | `pass` | `passed` | EVAS gold validation refreshed on 2026-04-18 using the benchmark gold's explicit supply-scaled transition style; dual validation also closed in the non-e2e refresh run with `mismatch_frac=0.0000`, `flag_span=0.900`, and `stable_samples=50`. |
| team | mixed_domain_cdac_bug | mixed `I()<+` and voltage-domain constructs | `tasks/bugfix/voltage/mixed_domain_cdac_bug` | `yes` | `pass` | `pass` | `passed` | Gold fix and reference testbench validate under EVAS; dual validation also closed in the non-e2e refresh run with `max_err=0.0000`. |
| team | spectre_port_discipline | `inout electrical A, B` sharing — Spectre rejects | `tasks/bugfix/voltage/spectre_port_discipline` | `yes` | `pass` | `pass` | `passed` | Gold fix and reference testbench validate under EVAS; dual validation also closed in the non-e2e refresh run (`spectre:ok`). |
| team | strongarm_reset_priority_bug | reset does not override StrongArm latch outputs | `tasks/bugfix/voltage/strongarm_reset_priority_bug` | `yes` | `pass` | `pass` | `passed` | Gold bug/fix pair plus reset-priority reference testbench validate under EVAS in `behavioral-veriloga-eval/results/gold-suite-p1-bugfix-2026-04-19/strongarm_reset_priority_bug`; reset window holds both outputs low and post-reset comparator polarity is restored. |
| team | inverted_comparator_logic_bug | comparator output polarity inverted against `vinp > vinn` intent | `tasks/bugfix/voltage/inverted_comparator_logic_bug` | `yes` | `pass` | `pass` | `passed` | Gold fix plus comparator-polarity regression testbench pass under EVAS and in `behavioral-veriloga-eval/results/gold-dual-suite-expansion-clean-2026-04-18/inverted_comparator_logic_bug`. |
| team | swapped_pfd_outputs_bug | PFD `up` / `dn` outputs swapped | `tasks/bugfix/voltage/swapped_pfd_outputs_bug` | `yes` | `pass` | `pass` | `passed` | Gold fix restores pulse direction; EVAS and clean dual-suite validation both pass in `behavioral-veriloga-eval/results/gold-dual-suite-expansion-clean-2026-04-18/swapped_pfd_outputs_bug`. |
| team | wrong_edge_sample_hold_bug | sample/hold updates on the wrong clock edge | `tasks/bugfix/voltage/wrong_edge_sample_hold_bug` | `yes` | `pass` | `pass` | `passed` | Gold fix now samples on the intended edge; EVAS and clean dual-suite validation both pass in `behavioral-veriloga-eval/results/gold-dual-suite-expansion-clean-2026-04-18/wrong_edge_sample_hold_bug`. |

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
| liangyuxuan | clk_div_min_tb | `tasks/tb-generation/voltage/clk_div_min_tb` | `yes` | `pass` | `pass` | `passed` | Gold DUT plus minimal reference testbench validate under EVAS; a dual-suite rerun also confirmed EVAS+Spectre execution in `behavioral-veriloga-eval/results/gold-dual-suite-tb-generation-2026-04-18/clk_div_min_tb`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family. |
| liangyuxuan | comparator_offset_tb | `tasks/tb-generation/voltage/comparator_offset_tb` | `yes` | `pass` | `pass` | `passed` | Gold DUT plus offset-oriented reference testbench validate under EVAS; a dual-suite rerun also confirmed EVAS+Spectre execution in `behavioral-veriloga-eval/results/gold-dual-suite-tb-generation-2026-04-18/comparator_offset_tb`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family. |
| liangyuxuan | dac_ramp_tb | `tasks/tb-generation/voltage/dac_ramp_tb` | `yes` | `pass` | `pass` | `passed` | Gold DUT plus ramp-oriented reference testbench validate under EVAS; a dual-suite rerun also confirmed EVAS+Spectre execution in `behavioral-veriloga-eval/results/gold-dual-suite-tb-generation-2026-04-18/dac_ramp_tb`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family. |
| liangyuxuan | inl_dnl_probe | `tasks/tb-generation/voltage/testbench/inl_dnl_probe` | `yes` | `pass` | `pass` | `passed` | Gold probe module, fixture DUT, and reference testbench with `final_step` file output validate under EVAS; a dual-suite rerun also confirmed EVAS+Spectre execution in `behavioral-veriloga-eval/results/gold-dual-suite-tb-generation-2026-04-18/inl_dnl_probe`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family. |
| team | dco_gain_step_tb | `tasks/tb-generation/voltage/dco_gain_step_tb` | `yes` | `pass` | `pass` | `passed` | Gold DCO plus gain-step reference testbench validate under EVAS in `behavioral-veriloga-eval/results/gold-suite-tb-expansion-2026-04-19/dco_gain_step_tb`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family, and bridge-backed execution is intentionally still pending under the current no-bridge queue rules. |
| team | gain_step_tb | `tasks/tb-generation/voltage/gain_step_tb` | `yes` | `pass` | `pass` | `passed` | Gold DUT plus gain-step reference testbench pass under EVAS and in `behavioral-veriloga-eval/results/gold-dual-suite-expansion-clean-2026-04-18/gain_step_tb`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family. |
| team | segmented_dac_glitch_tb | `tasks/tb-generation/voltage/segmented_dac_glitch_tb` | `yes` | `pass` | `pass` | `passed` | Gold segmented-DAC fixture plus glitch-oriented reference testbench validate under EVAS in `behavioral-veriloga-eval/results/gold-suite-p1-tb-2026-04-19/segmented_dac_glitch_tb`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family, and bridge-backed execution is intentionally still pending under the current no-bridge queue rules. |
| team | sample_hold_aperture_tb | `tasks/tb-generation/voltage/sample_hold_aperture_tb` | `yes` | `pass` | `pass` | `passed` | Gold sample/hold plus aperture-aware reference testbench validate under EVAS in `behavioral-veriloga-eval/results/gold-suite-tb-expansion-2026-04-19/sample_hold_aperture_tb`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family, and bridge-backed execution is intentionally still pending under the current no-bridge queue rules. |
| team | sample_hold_step_tb | `tasks/tb-generation/voltage/sample_hold_step_tb` | `yes` | `pass` | `pass` | `passed` | Gold DUT plus sample/hold capture testbench pass under EVAS and in `behavioral-veriloga-eval/results/gold-dual-suite-expansion-clean-2026-04-18/sample_hold_step_tb`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family. |
| team | xor_phase_tb | `tasks/tb-generation/voltage/xor_phase_tb` | `yes` | `pass` | `pass` | `passed` | Gold DUT plus XOR phase-detector testbench pass under EVAS and in `behavioral-veriloga-eval/results/gold-dual-suite-expansion-clean-2026-04-18/xor_phase_tb`. Benchmark scoring remains EVAS-primary because `sim_correct` is not required for this family. |

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
