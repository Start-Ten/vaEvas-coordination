# VAEVAS Benchmark-v2 Perturbation Plan

Date: 2026-04-29

## Purpose

Benchmark-v2 is the generalization split for VAEVAS.  It is deliberately
separate from the original 92-task closed set so that RAG/materializer results
can be reported as perturbation transfer rather than closed-set replay.

The first draft split, `v2-small`, should stress mechanism understanding under
prompt and interface perturbations.  It is not a migrated benchmark yet: tasks
stay under `behavioral-veriloga-eval/benchmark-v2/` until gold artifacts,
checkers, and EVAS/Spectre parity are reviewed.

## Storage Boundary

Draft artifacts live only in:

- `behavioral-veriloga-eval/benchmark-v2/README.md`
- `behavioral-veriloga-eval/benchmark-v2/manifests/v2-small.json`
- future draft task roots under `behavioral-veriloga-eval/benchmark-v2/tasks/`

Do not copy draft tasks into `behavioral-veriloga-eval/tasks/` during design.
Do not write into active result roots.  Do not label any teacher-derived or
RAG-replayed artifact as cold-start success.

## Perturbation Axes

Each seed mechanism should receive variants along multiple axes.  A useful
variant changes the retrieval and slot-binding problem without changing the
underlying executable behavior contract.

### P1: Surface Rename

Rename ports and reorder declarations while preserving obvious keyword cues.
Examples:

- `din` -> `dinp`
- `ref_clk` -> `refclk`
- output vector order reversed in prompt text but not in electrical behavior

This is the easy control condition.  It should not dominate `v2-small`.

### P2: Semantic Alias

Replace common signal names with domain-neutral aliases:

- analog input: `sense_node`, `measured_level`, `external_drive`,
  `sampled_quantity`
- clock: `cadence`, `strobe`, `advance`
- phase detector inputs: `early_edge`, `late_edge`, `reference_event`,
  `feedback_event`
- DAC output: `held_level`, `reconstructed_level`, `drive_estimate`

The goal is to test whether RAG-v2 can infer functional IR from role semantics
instead of relying on literal names.

### P3: Keyword Removal

Remove canonical mechanism words and replace them with functional descriptions:

- no `ADC`, `DAC`, or `quantizer`; describe sampled decision codes and a held
  reconstructed level
- no `DWA`; describe rotating contiguous unit-cell selection and wrap behavior
- no `PFD`; describe event ordering, mutually exclusive pulses, and reset race
- no `PLL`; describe a loop made of event comparison, accumulated control, and
  divided feedback
- no `monotonic` or `thermometer`; describe ordering and active-cell count

These cases are the main test for query rewriting and HyDE mechanism
hypotheses in RAG-v2.

### P4: Negative and Distractor Constraints

Add explicit traps that block common but wrong templates:

- binary DAC, explicitly not thermometer or unary active-count coding
- binary counter, explicitly not Gray-coded
- arbitrary code ordering, explicitly not monotonic
- PFD reset race, explicitly not a generic XOR phase detector
- sample/hold, explicitly not continuously tracking input

The retrieval report should count forbidden-mechanism top-k rate for these
tasks.

### P5: Parameter and Checker Perturbation

Change numerical and checker assumptions:

- bit width: 3, 4, 5, 6, 8
- divider ratio: odd/even ratios, ratio hop, reset phase
- VDD/reference range and midscale offset
- pulse width, reset delay, race window
- ramp time, stimulus dwell time, tolerance bands
- DWA window size and wrap-count expectations

These variants test slot binding and checker-aware materialization.

### P6: System Composition

Combine mechanisms so that solving one local behavior is insufficient:

- ADC decision code plus DAC reconstruction with shared held state
- ADC-DAC plus background offset calibration and settled flag
- PFD plus reset race plus lock detector
- PLL loop with divider ratio hop and lock reacquisition
- DWA pointer plus segmented DAC glitch constraint
- sample/hold feeding a quantizer with hold-time checks

System tasks should be small enough for EVAS/Spectre parity review but should
force graph/structure retrieval instead of flat keyword matching.

## v2-small Scope

`v2-small` should contain 30 draft tasks:

- 6 mechanism groups
- 5 variants per group
- at least 18 tasks at perturbation level P3 or higher
- at least 6 explicit negative/distractor tasks
- at least 4 system-composition tasks

Proposed mechanism groups:

| group | purpose | seed source style |
|---|---|---|
| `adc_dac_chain` | shared quantized state, code outputs, reconstructed output | data-converter |
| `binary_vs_therm_dac` | distinguish binary-weighted from thermometer/unit-cell behavior | data-converter |
| `dwa_pointer` | rotating contiguous selection, no overlap, wrap accounting | calibration |
| `pfd_reset_lock` | event ordering, UP/DN exclusivity, reset race, lock windows | phase-detector |
| `divider_counter` | ratio math, reset phase, binary-vs-Gray distractors | digital-logic |
| `sample_cal_system` | sample/hold, calibration/search, settled flag, composed behavior | sample-hold/calibration |

## Required Manifest Fields

Each task entry must include:

- `task_id`
- `source_seed`
- `mechanism_family`
- `perturbation_level`
- `prompt_strategy`
- `gold_required`
- `checker_required`
- `spectre_parity_required`
- `split`
- `status`

The draft manifest may include additional descriptive fields such as
`negative_constraints`, `parameter_changes`, `expected_slots`, and
`review_notes`, but those fields are advisory until task files exist.

## Review Gates

1. Manifest review:
   - no task id conflicts with existing official tasks
   - no task path under `behavioral-veriloga-eval/tasks/`
   - perturbation mix matches the intended difficulty

2. Authoring review:
   - prompt is public and does not leak gold implementation
   - gold DUT and testbench exist under `benchmark-v2/tasks/...`
   - checker uses behavior-level assertions, not brittle waveform hashes

3. Parity review:
   - EVAS PASS on gold
   - Spectre PASS for parity-required tasks
   - EVAS/Spectre mismatch classified before promotion

4. Promotion review:
   - provenance recorded
   - manifest status moves from `draft_manifest` to `reviewed_candidate`
   - only then may a task be copied into the official `tasks/` tree

## Evaluation Metrics

Benchmark-v2 should report:

- EVAS PASS
- Spectre PASS
- EVAS/Spectre agreement
- mechanism recall@1/@3 for RAG-v2
- forbidden mechanism top-k rate
- slot coverage
- attempts per PASS
- parameter-binding failure rate
- closed-set leakage/provenance flags

The central claim is transfer under perturbation: RAG-v2 should retrieve and
bind the correct mechanism even when prompt keywords, port names, and numerical
settings differ from the original closed-set tasks.
