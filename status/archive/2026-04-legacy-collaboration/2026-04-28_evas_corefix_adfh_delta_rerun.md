# EVAS Core Fix A/D/F/H Delta Rerun

Date: 2026-04-28

## Purpose

After repairing EVAS core Spectre-compatibility checks, rerun only the
previous EVAS/Spectre pass-mismatched tasks for Kimi A/D/F/H.

## EVAS Core / Checker Changes Being Validated

- Strict Spectre instance/source node-list syntax in EVAS parser.
- Strictly increasing PWL time points in EVAS waveform engine.
- Spectre-compatible preflight for runtime `transition()` placement.
- Supply-port hard-drive conflict detection against external voltage sources.
- Gray counter checker sampling changed from row-offset sampling to fixed
  physical settle-time sampling.

## Inputs

| Condition | Generated root | EVAS rerun root | Spectre rerun root |
|---|---|---|---|
| A | `generated-condition-A-strictv3-kimi-full92-2026-04-28-rerun` | `results/evas-core-align-A-delta-2026-04-28-rerun2` | `results/evas-core-align-A-delta-spectre-2026-04-28-rerun2` |
| D | `generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun` | `results/evas-core-align-D-delta-2026-04-28-rerun2` | `results/evas-core-align-D-delta-spectre-2026-04-28-rerun2` |
| F | `generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun` | `results/evas-core-align-F-delta-2026-04-28-rerun2` | `results/evas-core-align-F-delta-spectre-2026-04-28-rerun2` |
| H | `generated-condition-H-strictv3-signature-full92-materialized-kimi-2026-04-28-rerun` | `results/evas-core-align-H-delta-2026-04-28-rerun2` | `results/evas-core-align-H-delta-spectre-2026-04-28-rerun2` |

## Delta Results

| Cond | Task | EVAS status | Spectre status | Match |
|---|---|---|---|---|
| A | `gain_extraction_smoke` | `FAIL_SIM_CORRECTNESS` | `FAIL_SPECTRE_RUN` | yes |
| A | `ramp_gen_smoke` | `FAIL_DUT_COMPILE` | `FAIL_SPECTRE_RUN` | yes |
| D | `lfsr_smoke` | `PASS` | `PASS` | yes |
| F | `cmp_delay_smoke` | `FAIL_TB_COMPILE` | `FAIL_SPECTRE_RUN` | yes |
| F | `dwa_ptr_gen_smoke` | `FAIL_TB_COMPILE` | `FAIL_SPECTRE_RUN` | yes |
| F | `gray_counter_one_bit_change_smoke` | `PASS` | `PASS` | yes |
| F | `lfsr_smoke` | `PASS` | `PASS` | yes |
| H | `cmp_delay_smoke` | `FAIL_TB_COMPILE` | `FAIL_SPECTRE_RUN` | yes |
| H | `dwa_ptr_gen_smoke` | `FAIL_TB_COMPILE` | `FAIL_SPECTRE_RUN` | yes |
| H | `gray_counter_one_bit_change_smoke` | `PASS` | `PASS` | yes |
| H | `lfsr_smoke` | `PASS` | `PASS` | yes |
| H | `pfd_deadzone_smoke` | `PASS` | `PASS` | yes |

All rerun delta tasks now have EVAS/Spectre pass/fail agreement.

## Adjusted Full92 Pass Counts

These are synthesized by applying the delta changes to the previous full92
Kimi strict-v3 A/D/F/H table.

| Condition | Previous EVAS | Previous Spectre | Adjusted EVAS | Adjusted Spectre |
|---|---:|---:|---:|---:|
| A | 25/92 | 23/92 | 23/92 | 23/92 |
| D | 42/92 | 43/92 | 43/92 | 43/92 |
| F | 60/92 | 58/92 | 59/92 | 59/92 |
| H | 61/92 | 59/92 | 60/92 | 60/92 |

## Interpretation

- A's two previous EVAS false positives are now rejected by EVAS.
- D's `lfsr_smoke` reverse mismatch is fixed; EVAS and Spectre both pass.
- F's old false positives `cmp_delay_smoke` and `dwa_ptr_gen_smoke` are now
  rejected by EVAS; `gray_counter_one_bit_change_smoke` is now accepted by both
  after fixed-time checker sampling; `lfsr_smoke` is accepted by both.
- H inherits the same F alignment and keeps its own `pfd_deadzone_smoke`
  replacement as EVAS/Spectre PASS.
