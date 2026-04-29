# Combined Artifact Materialization Report

## Summary

- Base generated: `generated-condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-2026-04-28`
- Base score: `results/condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-evas-after-evasfix-full92-2026-04-28`
- Output generated: `generated-condition-I-clean-functional-ir-full92-materialized-kimi-2026-04-28`
- Base Pass@1 count: `62/92`
- Candidate pass tasks: `7`
- Replacements: `7`

## Replacements

| Task | Base | Candidate root | Notes |
|---|---|---|---|
| `bbpd_data_edge_alignment_smoke` | `FAIL_TB_COMPILE` | `results/condition-I-clean-functional-ir-on-Ffail-kimi-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; data_edges=8 lead_updn=4/0 lag_updn=0/4 overlap_frac=0.0000 |
| `cdac_cal` | `FAIL_SIM_CORRECTNESS` | `results/condition-I-clean-functional-ir-on-Ffail-kimi-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; vdac_activity col=VDAC_P range=0.308 |
| `comparator_hysteresis_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-I-clean-functional-ir-on-Ffail-kimi-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; rise_t=30.025ns fall_t=70.001ns |
| `dac_therm_16b_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-I-clean-functional-ir-on-Ffail-kimi-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; max_ones=16 max_vout=16.000 |
| `mux_4to1_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-I-clean-functional-ir-on-Ffail-kimi-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; all_4_select_windows_correct |
| `pfd_deadzone_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-I-clean-functional-ir-on-Ffail-kimi-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; streaming_checker:up_frac=0.0045 dn_frac=0.0000 up_pulses=15 |
| `segmented_dac` | `FAIL_SIM_CORRECTNESS` | `results/condition-I-clean-functional-ir-on-Ffail-kimi-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; diff_range=0.900 |

## Skipped

| Task | Reason |
|---|---|
