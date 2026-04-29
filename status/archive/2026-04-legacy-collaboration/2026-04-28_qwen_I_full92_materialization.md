# Combined Artifact Materialization Report

## Summary

- Base generated: `generated-condition-F-public-strictv3-evasloop-qwen-full92-materialized-2026-04-28`
- Base score: `results/condition-F-public-strictv3-evasloop-qwen-full92-materialized-evas-2026-04-28`
- Output generated: `generated-condition-I-clean-functional-ir-full92-materialized-qwen-2026-04-28`
- Base Pass@1 count: `55/92`
- Candidate pass tasks: `2`
- Replacements: `2`

## Replacements

| Task | Base | Candidate root | Notes |
|---|---|---|---|
| `cmp_delay_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-I-clean-functional-ir-on-Ffail-qwen-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; delays_ns=[0.025, 0.0, 0.0, 0.0] monotonic=True |
| `pfd_deadzone_smoke` | `FAIL_SIM_CORRECTNESS` | `results/condition-I-clean-functional-ir-on-Ffail-qwen-evas-2026-04-28/best` | spectre_strict:preflight_pass; returncode=0; streaming_checker:up_frac=0.0045 dn_frac=0.0000 up_pulses=15 |

## Skipped

| Task | Reason |
|---|---|
