# Mechanism Skeleton Coverage

Date: 2026-04-29

This is a lightweight coverage report for the current 92-task closed set after the overnight update. It checks whether each major mechanism family has at least one reusable mechanism skeleton or compatibility template.

| Mechanism Family | Tasks | Current Skeleton / Template | Coverage Note |
|---|---:|---|---|
| `generic_voltage_behavior` | 26 | Spectre compatibility templates + public Verilog-A rules | Mostly syntax/interface/primitive analog behavior; not a single circuit mechanism |
| `converter_quantize_reconstruct_or_decode` | 16 | `adc_dac_quantize_reconstruct_skeleton`, `dac_decode_binary_thermometer_skeleton` | Covered, but needs negative constraints to avoid binary-vs-thermometer confusion |
| `pll_feedback_cadence` | 12 | `pll_feedback_cadence_skeleton` | Covered; system relation slots remain the hard part |
| `comparator_threshold_hysteresis` | 11 | `comparator_threshold_hysteresis_skeleton` | Covered |
| `phase_detector_pulse_relation` | 7 | `pfd_edge_pulse_window_skeleton` | Covered; distinguish PFD, BBPD, XOR phase detector in retrieval |
| `sample_hold_track_latch` | 5 | `sample_hold_track_latch_skeleton` | Covered |
| `counter_or_divider_sequence` | 5 | `divider_counter_ratio_skeleton` | Covered |
| `lfsr_prbs_sequence` | 4 | `lfsr_prbs_sequence_skeleton` | Covered |
| `dwa_rotating_pointer_window` | 3 | `dwa_pointer_window_skeleton` | Covered |
| `serializer_frame_sequence` | 2 | `serializer_frame_sequence_skeleton` | Covered |
| `calibration_search_settle` | 1 | `calibration_search_settle_skeleton` | Covered |

## Remaining Risk

Coverage is not the same as reliable retrieval. The earlier RAG audit still had dangerous false positives, especially:

- binary DAC vs thermometer DAC;
- PLL/divider/counter confusion;
- PFD/BBPD/XOR phase-detector confusion;
- spelling/port-name variants that require slot binding instead of keyword matching.

The next RAG iteration should therefore focus on reranking and negative constraints, not only adding more skeletons.

## Related Files

- Skeletons: `behavioral-veriloga-eval/docs/CIRCUIT_MECHANISM_SKELETONS.json`
- Spectre compatibility templates: `behavioral-veriloga-eval/docs/SPECTRE_COMPATIBILITY_TEMPLATES.json`
- Closed-set templates: `behavioral-veriloga-eval/docs/CLOSEDSET_CIRCUIT_TEMPLATES.json`
- Artifact store: `behavioral-veriloga-eval/docs/VERIFIED_ARTIFACT_STORE.json`
