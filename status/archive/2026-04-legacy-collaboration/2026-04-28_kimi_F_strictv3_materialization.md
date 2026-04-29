# Combined Artifact Materialization Report

## Summary

- Base generated: `generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun`
- Base score: `results/condition-D-strictv3-kimi-full92-evas-2026-04-28-rerun`
- Output generated: `generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun`
- Base Pass@1 count: `42/92`
- Candidate pass tasks: `18`
- Replacements: `18`

## Replacements

| Task | Base | Candidate root | Notes |
|---|---|---|---|
| `adpll_timer` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; streaming_checker:late_edge_ratio=1.040 lock_time=6.047e-08 vctrl_range_ok=True |
| `clk_div_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; edge_ratio=3.75 |
| `cmp_delay_smoke` | `FAIL_TB_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; delays_ns=[0.0, 0.001, 0.001, 0.001] monotonic=True |
| `cmp_strongarm_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; pre_high_frac=1.000 post_low_frac=1.000 |
| `comparator_hysteresis_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; rise_t=30.025ns fall_t=70.001ns |
| `comparator_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; output_mean_delta=1.231 |
| `d2b_4bit` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; dynamic monotonic code check samples=194 unique_codes=16 |
| `dac_therm_16b_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; max_ones=16 max_vout=16.000 |
| `dwa_ptr_gen_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; ptr_unique=14 max_cell_code=65279 |
| `gain_extraction_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; streaming_checker:diff_gain=16.90 |
| `gray_counter_one_bit_change_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; streaming_checker:unique_codes=16 bad_transitions=0 |
| `multitone` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; max_err=0.0000 |
| `not_gate_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; invert_match_frac=1.000 samples=144 |
| `pipeline_stage` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; vres_range=0.540 bounded=True d_active=True |
| `sample_hold_droop_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; edges=9 sample_mismatch=0/6 droop_windows=2 |
| `sample_hold_smoke` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; edges=10 hold_ok |
| `strongarm_reset_priority_bug` | `FAIL_DUT_COMPILE` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; reset_outp_max=0.000 reset_outn_max=0.000 high_outp=1.000 high_outn=1.000 low_outp=0.979 low_outn=0.979 |
| `xor_pd_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best` | spectre_strict:preflight_pass; returncode=0; duty=0.440 transitions=40 |

## Skipped

| Task | Reason |
|---|---|
