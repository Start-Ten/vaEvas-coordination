# R26 Teacher Replay Remaining Failure Packets

Date: 2026-04-29

These packets cover the 10 tasks that still fail after replaying R26 teacher artifacts through real Spectre. They are not treated as behavior failures until Spectre-compatible syntax and runner issues are removed.

## Summary

- Source root: `behavioral-veriloga-eval/results/r26-teacher-remaining23-spectre-2026-04-29`
- Total failures: `10`
- By label: `{'spectre_parameter_range_bound': 1, 'spectre_port_declaration_style': 7, 'malformed_pwl_wave': 2, 'interface_parameter_missing': 1, 'tb_syntax_unexpected_close_parenthesis': 1, 'embedded_declaration': 1}`
- By owner: `{'template_or_pipeline': 10}`

## Packets

| Task | Mechanism | Labels | Recommended Action |
|---|---|---|---|
| `bbpd` | `pll_feedback_cadence` | `spectre_parameter_range_bound` | Relax or remove incompatible parameter range constraints before hierarchy flattening. |
| `bbpd_data_edge_alignment_smoke` | `phase_detector_pulse_relation` | `spectre_port_declaration_style`, `malformed_pwl_wave` | Rewrite Verilog-A port declarations into separate direction and electrical declarations. |
| `bg_cal` | `calibration_search_settle` | `spectre_port_declaration_style`, `interface_parameter_missing` | Rewrite Verilog-A port declarations into separate direction and electrical declarations. |
| `cross_hysteresis_window_smoke` | `comparator_threshold_hysteresis` | `spectre_port_declaration_style` | Rewrite Verilog-A port declarations into separate direction and electrical declarations. |
| `pfd_deadzone_smoke` | `phase_detector_pulse_relation` | `spectre_port_declaration_style` | Rewrite Verilog-A port declarations into separate direction and electrical declarations. |
| `pfd_reset_race_smoke` | `phase_detector_pulse_relation` | `spectre_port_declaration_style` | Rewrite Verilog-A port declarations into separate direction and electrical declarations. |
| `phase_accumulator_timer_wrap_smoke` | `pll_feedback_cadence` | `spectre_port_declaration_style` | Rewrite Verilog-A port declarations into separate direction and electrical declarations. |
| `ramp_gen_smoke` | `generic_voltage_behavior` | `tb_syntax_unexpected_close_parenthesis` | Rewrite the Spectre instance line from multiline named-port style to positional instance syntax. |
| `sample_hold_droop_smoke` | `sample_hold_track_latch` | `malformed_pwl_wave`, `embedded_declaration` | Move block-local real declarations to module scope or a labeled analog block supported by Spectre. |
| `serializer_frame_alignment_smoke` | `serializer_frame_sequence` | `spectre_port_declaration_style` | Rewrite Verilog-A port declarations into separate direction and electrical declarations. |

## Claim Boundary

- These failures belong to the teacher-replay completion path, not cold-start A/D/F/G.
- A task should only move from this file into the accepted ledger after EVAS and real Spectre both pass.
