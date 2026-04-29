# R26-To-Cold-Start Distillation Audit

Date: 2026-04-28

## Purpose

Answer the question:

> Which parts of the historical 92/92 engineering closure can be moved into a clean cold-start I pipeline, and which parts must remain engineering admission/materialization evidence only?

This audit separates:

- reusable infrastructure;
- reusable mechanism knowledge;
- reusable only after rewriting into prompt-derived / mechanism-level rules;
- non-cold-start artifact reuse.

Machine-readable table:

```text
coordination/status/2026-04-28_r26_to_coldstart_distillation_audit.json
```

## High-Level Answer

Yes, many historical mechanisms are transferable to cold-start, but not by copying the historical passing artifacts.

The transferable part is:

- mechanism families;
- failure signatures;
- prompt-derived functional IR;
- checker/runner infrastructure fixes;
- Spectre/EVAS compatibility rules;
- contract templates generated from public prompt/checker semantics.

The non-transferable part is:

- already-verified artifact materialization;
- task-id lookup;
- ref/gold filename aliases;
- hidden reference testbench reuse;
- task-specific patches that only work because the benchmark instance is known.

## Evidence Summary

From the historical closure/admission path:

| Source | Replacements | Audit decision |
|---|---:|---|
| I-runner local overlay | 9 | Do not directly enter cold-start; all 9 had ref/gold leakage flags in the no-leakage audit. Redistill only as generic mechanisms. |
| R22 runtime/interface | 2 | Can enter cold-start after mechanismization. |
| R23 ADPLL graph | 3 | Can enter cold-start as PLL feedback/cadence/lock graph mechanisms. |
| R24 CPPLL graph | 3 | Can enter cold-start as CPPLL feedback/reacquisition mechanisms. |
| R25 remaining mechanisms | 8 | Can enter cold-start as generic mechanism cards/templates. |
| R26 DWA/PFD closure | 4 | Can enter cold-start as DWA pointer/PFD pulse protocol mechanisms. |

Aggregate:

```text
29 historical replacements audited
20 eligible for cold-start after mechanismization
9 excluded from direct cold-start reuse
```

The 9 excluded replacements are still useful as design lessons, but only after removing ref/gold cues.

## What Can Enter Cold-Start Directly As Infrastructure

These are not method gains; they should be common infrastructure for A/D/F/H/I:

- EVAS parser/backend fixes;
- EVAS/Spectre sine/PWL/file-I/O compatibility fixes;
- Spectre mode correction: final strict gate should use plain `spectre` or validated `aps`, not `ax/cx` for maxstep-sensitive tasks;
- streaming checker refactors for large CSV tasks;
- transition/bus/checker sampling fixes;
- FAIL_INFRA vs functional failure attribution;
- prompt pollution cleanup;
- artifact truncation retry;
- strict v3 public Verilog-A/Spectre preflight.

These belong in the benchmark/runtime, not in H/I-specific prompt tricks.

## What Can Enter Cold-Start As Mechanism Knowledge

The following mechanism families are reusable and should be encoded in H/I:

| Mechanism family | Historical tasks | Cold-start form |
|---|---|---|
| PLL feedback cadence and lock window | `adpll_lock_smoke`, `adpll_ratio_hop_smoke`, `adpll_timer_smoke`, `cppll_freq_step_reacquire_smoke`, `cppll_timer`, `cppll_tracking_smoke` | Functional IR should detect ref/fb/vctrl/lock semantics and enforce ratio before lock. |
| Event ordering / final-step / timer grid | `final_step_file_metric_smoke`, `simultaneous_event_order_smoke`, `timer_absolute_grid_smoke` | Failure signature should distinguish event-order/timer-grid behavior from generic analog output mismatch. |
| Converter transfer / calibration / code coverage | `bg_cal`, `flash_adc_3b_smoke`, `dac_therm_16b_smoke`, `segmented_dac`, `cdac_cal`, `adc_dac_ideal_4b_smoke` | Mechanism cards should express monotonic transfer, code coverage, trim convergence, and analog span without task-specific thresholds. |
| Digital sequence / bus truth table / serialized frame | `bad_bus_output_loop`, `nrz_prbs`, `serializer_frame_alignment_smoke`, `gray_counter_one_bit_change_smoke`, `digital_basics_smoke` | Functional IR should recognize stable sampling windows, complement/swing, one-bit-change, and frame alignment. |
| DWA pointer and wraparound | `dwa_ptr_gen_no_overlap_smoke`, `dwa_ptr_gen_smoke`, `dwa_wraparound_smoke` | Contract templates should express pointer rotation, wrap split, one-hot/no-overlap active cells, and post-reset sample budget. |
| PFD/BBPD pulse protocol | `pfd_reset_race_smoke`, `bbpd_data_edge_alignment_smoke` | Failure signatures should map pulse polarity, up/dn exclusivity, reset race, and lead/lag windows to pulse-state repair. |
| Analog equation accuracy | `multitone`, `cross_sine_precision_smoke` | Use public stimulus/function semantics and EVAS/Spectre parity; avoid exact hidden expected waveform leakage. |

## What Must Not Enter Cold-Start Directly

The overfit guard found that the 9-task I-runner local overlay had ref/gold leakage flags:

| Task | Decision |
|---|---|
| `adc_dac_ideal_4b_smoke` | Exclude direct artifact; redistill as converter quantize/reconstruct mechanism. |
| `bbpd_data_edge_alignment_smoke` | Exclude direct artifact; redistill as BBPD lead/lag pulse protocol. |
| `cdac_cal` | Exclude direct artifact; redistill as CDAC calibration/VDAC activity mechanism. |
| `dac_therm_16b_smoke` | Exclude direct artifact; redistill as thermometer-code coverage and output-span mechanism. |
| `digital_basics_smoke` | Exclude direct artifact; redistill as digital logic truth-table and output naming mechanism. |
| `gray_counter_one_bit_change_smoke` | Exclude direct artifact; redistill as Gray one-bit-change invariant. |
| `parameter_type_override_smoke` | Exclude direct artifact; redistill as parameter override/type compatibility rule. |
| `segmented_dac` | Exclude direct artifact; redistill as differential segmented-DAC transfer/span mechanism. |
| `serializer_frame_alignment_smoke` | Exclude direct artifact; redistill as frame pulse and serialized-bit alignment mechanism. |

Important: several of these mechanisms already reappeared in the 2026-04-28 clean H/I-on-F-fail runs without direct artifact copying:

- `bbpd_data_edge_alignment_smoke`: recovered by H-on-F-fail;
- `dac_therm_16b_smoke`: recovered by H and I;
- `segmented_dac`: recovered by I-on-F-fail;
- `serializer_frame_alignment_smoke`: recovered by H and I.

This is good evidence that at least part of the historical local overlay can be converted into legitimate cold-start mechanism knowledge.

## Mapping To Current H/I Results

Current clean anchors:

| Condition | Result |
|---|---:|
| A current clean R3 | 40/92 |
| D after EVAS fixes | 47/92 |
| F after EVAS fixes | 62/92 |
| H-on-F-fail subset | 6/30 |
| I-on-F-fail subset | 6/30 |
| H/I union over F-fail subset | 7 new tasks |

Overlay interpretation:

```text
F + H subset wins = 68/92
F + I subset wins = 68/92
F + H∪I subset wins = 69/92
```

This is not yet full cold-start I. It is evidence that mechanismization can recover historical local wins in a cleaner way.

## Proposed Cold-Start I Design After Distillation

### Layer 0: Common Infrastructure

Apply to all A/D/F/H/I:

- current EVAS/checker/parser fixes;
- strict v3 public Verilog-A/Spectre rules;
- Spectre/APS final-gate policy;
- failure attribution and infra/functional separation.

### Layer 1: Prompt Functional IR

From prompt only, infer:

- circuit family;
- required artifact shape;
- ports/observables;
- clock/reset/valid/window semantics;
- expected high-level mechanism, e.g. converter transfer, PLL feedback, DWA rotation.

No task-name primary matching.

### Layer 2: Failure Signature

From failed EVAS run, infer:

- compile/interface/runtime/behavior layer;
- symptom vector, e.g. too few edges, code span too small, no VDAC activity, ratio wrong, lock forced high, overlap pulses.

### Layer 3: Mechanism Cards

Select cards by:

- prompt functional IR;
- EVAS symptom vector;
- CSV metric families.

Do not select by task id except as a logging key.

### Layer 4: Contract Templates

Generate advisory/hard contracts from prompt/public checker semantics:

- edge count/window;
- monotonicity/code coverage;
- pulse exclusivity;
- feedback ratio before lock;
- pointer one-hot/no-overlap;
- frame alignment.

Avoid gold internal node names and hidden constants.

### Layer 5: Repair Prompt

Give LLM:

- original public task prompt;
- public strict v3 rules;
- current candidate files;
- EVAS failure notes;
- functional IR;
- selected mechanism card(s);
- contract pass/fail names and abstract hints.

Do not give:

- gold implementation;
- historical passing code;
- ref file names;
- task-specific exact patch recipe.

## Immediate Implementation Tasks

1. Add a trigger-provenance log to H/I repair prompts:
   - task id;
   - functional IR family;
   - selected mechanism card IDs;
   - evidence source: prompt phrase / EVAS note / CSV metric;
   - whether task id or gold path influenced selection.

2. Convert R23/R24 PLL graph patches into prompt-selected mechanism cards:
   - ratio before lock;
   - ref/fb edge cadence;
   - DCO/divider relation;
   - reacquisition after reference step.

3. Convert R26 DWA/PFD patches into prompt-selected mechanism cards:
   - DWA pointer one-hot/no-overlap;
   - wraparound split behavior;
   - PFD reset race and up/dn exclusivity.

4. Convert R25 remaining mechanisms:
   - bus truth-table stable sampling;
   - converter code coverage/span/monotonicity;
   - divider ratio switch;
   - differential sequence swing/complement;
   - timer grid/final-step event order.

5. Re-run:
   - H full92 from clean D after EVAS fixes;
   - I full92 with only mechanismized transferable knowledge;
   - prompt perturbation mini-set;
   - cross-model A/D/F/I on Qwen or another model.

## Paper Interpretation

Use three separate result types:

1. **Cold-start result**: A/D/F/H/I generated/repaired under clean rules.
2. **Distillation result**: historical R26 closure decomposed into transferable vs non-transferable mechanisms.
3. **Engineering closure result**: materialization/admission proves the benchmark can be fully closed, but is not itself cold-start pass rate.

The correct claim is not:

> I cold-start already equals 92/92.

The correct claim is:

> R26 shows that the failure space is largely covered by reusable mechanism families. A no-leakage audit identifies which parts can be distilled into cold-start H/I, and early clean H/I-on-F-fail runs recover 6-7 F failures without direct artifact reuse.
