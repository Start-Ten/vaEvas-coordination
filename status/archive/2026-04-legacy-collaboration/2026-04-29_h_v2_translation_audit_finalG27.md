# H-v1 Translation Audit For Final G Failures

Result root: `/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/condition-G-targeted-materialized-spectre-aligned-kimi-evas-2026-04-28`

## Summary

- Failed tasks audited: 27
- High confidence translations: 17
- Medium confidence translations: 10
- Low confidence translations: 0
- Uses task-id-specific focus text: 0
- Needs H-v2 rule improvement: 10

## Rows

| task | status | confidence | H-v1 rules | task-id focus | needs H-v2 | leading note |
|---|---|---|---|---:|---:|---|
| `adc_dac_ideal_4b_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `ADC_DAC_CODE_COVERAGE` | false | false | contract_save_pruned=removed:8,inserted:1,signals:8 |
| `adpll_ratio_hop_smoke` | `FAIL_SIM_CORRECTNESS` | `medium` | `GENERIC_METRIC_MISMATCH`, `GENERIC_METRIC_MISMATCH` | false | true | contract_save_pruned=removed:1,inserted:1,signals:6 |
| `adpll_timer` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `ADPLL_EDGE_RATIO` | false | false | contract_save_pruned=removed:1,inserted:1,signals:4 |
| `adpll_timer_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `ADPLL_EDGE_RATIO` | false | false | contract_save_pruned=removed:4,inserted:1,signals:4 |
| `bbpd` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `PFD_RESET_RACE` | false | false | contract_save_pruned=removed:1,inserted:1,signals:5 |
| `bbpd_data_edge_alignment_smoke` | `FAIL_SIM_CORRECTNESS` | `medium` | `GENERIC_METRIC_MISMATCH`, `GENERIC_METRIC_MISMATCH` | false | true | contract_save_pruned=removed:1,inserted:1,signals:5 |
| `bg_cal` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `GENERIC_METRIC_MISMATCH`, `CAL_CODE_SPAN` | false | false | contract_save_pruned=removed:1,inserted:1,signals:9 |
| `cdac_cal` | `FAIL_SIM_CORRECTNESS` | `medium` | `GENERIC_METRIC_MISMATCH`, `OBSERVABILITY_CONTRACT` | false | true | contract_save_pruned=removed:1,inserted:1,signals:5 |
| `clk_divider` | `FAIL_SIM_CORRECTNESS` | `medium` | `GENERIC_METRIC_MISMATCH` | false | true | contract_save_pruned=removed:1,inserted:1,signals:12 |
| `comparator_hysteresis_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `HYST_WINDOW` | false | false | contract_save_pruned=removed:4,inserted:1,signals:4 |
| `cppll_freq_step_reacquire_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `PLL_RELOCK_TIME` | false | false | contract_save_pruned=removed:1,inserted:1,signals:5 |
| `cppll_timer` | `FAIL_SIM_CORRECTNESS` | `medium` | `GENERIC_METRIC_MISMATCH`, `GENERIC_METRIC_MISMATCH`, `SIM_ARTIFACT`, `GENERIC_METRIC_MISMATCH` | false | true | contract_save_pruned=removed:1,inserted:1,signals:5 |
| `cppll_tracking_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `PLL_FREQ_RATIO` | false | false | contract_save_pruned=removed:4,inserted:1,signals:5 |
| `cross_hysteresis_window_smoke` | `FAIL_SIM_CORRECTNESS` | `medium` | `GENERIC_METRIC_MISMATCH`, `GENERIC_METRIC_MISMATCH` | false | true | contract_save_pruned=removed:1,inserted:1,signals:2 |
| `dwa_ptr_gen_no_overlap_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `DWA_NO_OVERLAP_WINDOW` | false | false | contract_save_pruned=removed:6,inserted:1,signals:35 |
| `dwa_ptr_gen_smoke` | `FAIL_TB_COMPILE` | `medium` | `GENERIC_METRIC_MISMATCH`, `SIM_ARTIFACT`, `GENERIC_METRIC_MISMATCH`, `SIM_ARTIFACT` | false | true | contract_save_pruned=removed:10,inserted:1,signals:34 |
| `multimod_divider` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `MULTIMOD_DIVIDER_COUNTS` | false | false | contract_save_pruned=removed:1,inserted:1,signals:7 |
| `multimod_divider_ratio_switch_smoke` | `FAIL_SIM_CORRECTNESS` | `medium` | `GENERIC_METRIC_MISMATCH`, `GENERIC_METRIC_MISMATCH` | false | true | contract_save_pruned=removed:1,inserted:1,signals:3 |
| `nrz_prbs` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `NRZ_PRBS_TRANSITIONS` | false | false | contract_save_pruned=removed:1,inserted:1,signals:2 |
| `pfd_deadzone_smoke` | `FAIL_TB_COMPILE` | `medium` | `GENERIC_METRIC_MISMATCH`, `GENERIC_METRIC_MISMATCH` | false | true | contract_save_pruned=removed:1,inserted:1,signals:4 |
| `pfd_reset_race_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `PFD_RESET_RACE` | false | false | contract_save_pruned=removed:1,inserted:1,signals:4 |
| `phase_accumulator_timer_wrap_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `PHASE_ACCUM_WRAP` | false | false | contract_save_pruned=removed:1,inserted:1,signals:2 |
| `prbs7` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `NRZ_PRBS_TRANSITIONS` | false | false | contract_save_pruned=removed:1,inserted:1,signals:11 |
| `ramp_gen_smoke` | `FAIL_SIM_CORRECTNESS` | `medium` | `GENERIC_METRIC_MISMATCH`, `GENERIC_METRIC_MISMATCH` | false | true | contract_save_pruned=removed:1,inserted:1,signals:6 |
| `sample_hold_droop_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `SAMPLE_HOLD_DROOP` | false | false | contract_save_pruned=removed:1,inserted:1,signals:3 |
| `sar_adc_dac_weighted_8b_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `ADC_DAC_CODE_COVERAGE` | false | false | contract_save_pruned=removed:3,inserted:1,signals:13 |
| `serializer_frame_alignment_smoke` | `FAIL_SIM_CORRECTNESS` | `high` | `GENERIC_METRIC_MISMATCH`, `SERIALIZER_FRAME_ALIGNMENT` | false | false | contract_save_pruned=removed:3,inserted:1,signals:12 |
