# Combined Artifact Materialization Report

## Summary

- Base generated: `generated-condition-D-public-strictv3-qwen-full92-2026-04-28`
- Base score: `results/condition-D-public-strictv3-qwen-full92-evas-2026-04-28`
- Output generated: `generated-condition-F-public-strictv3-evasloop-qwen-full92-materialized-2026-04-28`
- Base Pass@1 count: `39/92`
- Candidate pass tasks: `17`
- Replacements: `17`

## Replacements

| Task | Base | Candidate root | Notes |
|---|---|---|---|
| `bad_bus_output_loop` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; streaming_checker:mismatch_frac=0.0000 code_patterns=16 dout_patterns=16 uniform_frac=0.160 stable_rows=2041 |
| `bbpd` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; data_edges=150 up_edges=45 down_edges=45 overlap_frac=0.0000 |
| `bound_step_period_guard_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; guard_rises=4 wraps=4 phase_span=1.800 guard_hi_frac=0.220 |
| `cmp_delay_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; delays_ns=[0.002, 0.002, 0.002, 0.002] monotonic=True |
| `comparator_hysteresis_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; rise_t=30.025ns fall_t=70.001ns |
| `cross_interval_163p333_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; delay_ps=163.333 seen_hi=1.800 |
| `dac_therm_16b_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; max_ones=16 max_vout=16.000 |
| `dff_rst_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; streaming_checker:checks=10 q_mismatch=0 qb_mismatch=0 |
| `gray_counter_one_bit_change_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; streaming_checker:unique_codes=16 bad_transitions=0 |
| `multimod_divider_ratio_switch_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; streaming_checker:pre_div4=4.00;mid_div5=5.00;post_div4=4.00 |
| `mux_4to1_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; all_4_select_windows_correct |
| `pfd_updn_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; up_frac=0.198 dn_frac=0.000 up_pulses=30 |
| `sample_hold_droop_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; edges=9 sample_mismatch=0/6 droop_windows=2 |
| `sample_hold_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; edges=10 hold_ok |
| `sar_logic_10b` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; sim_correct not required by scoring |
| `serializer_8b_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; 0xA5_serialized_ok mode=edge_only mismatches=0 |
| `strongarm_reset_priority_bug` | `FAIL_DUT_COMPILE` | `results/condition-F-public-strictv3-evasloop-qwen-full92-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; reset_outp_max=0.000 reset_outn_max=0.000 high_outp=1.000 high_outn=1.000 low_outp=0.979 low_outn=0.979 |

## Skipped

| Task | Reason |
|---|---|
