# Closed-Loop Flow Example: ADC

This document demonstrates the layered closed-loop workflow on an ADC-flavored case.

Compared with the comparator example, this ADC example is more useful for showing:

1. why `compile + simulate` is not enough
2. why behavior validation needs task-specific checks
3. how a case can become benchmark-ready without immediately requiring full parity work

This example uses:

1. example path:
   `vaEvas/behavioral-veriloga-eval/examples/data-converter/adc_dac_ideal_4b`
2. related candidate cases:
   `adc_dac_ideal_4b`
   `sar_adc_dac_weighted_8b`

The simpler `adc_dac_ideal_4b` case is used as the main presentation example.

---

## 1. Why ADC Is A Better Mid-Complexity Example

ADC is a good demonstration case because it sits between simple logic-like blocks and heavy PLL closed-loop models.

It is more complex than comparator because it includes:

1. clocked sampling
2. quantization behavior
3. multi-bit output consistency
4. end-to-end signal reconstruction when paired with DAC

But it is still lighter than PLL closed-loop parity work because:

1. lock dynamics are not the main concern
2. parity metrics are not the only meaningful evaluation signal
3. task-specific correctness can already be strong at the EVAS-only level

So ADC is a good example for presenting:

1. `L0` minimal executable loop
2. `L1` behavior validation loop
3. optional `L2` parity extension
4. `L3` benchmark landing loop

---

## 2. The Four-Layer Flow

### L0: Minimal Executable Loop

Question:

`Can the ADC model and testbench run at all in EVAS?`

Expected outputs:

1. DUT compile success
2. testbench compile success
3. transient waveform output generated

### L1: Behavior Validation Loop

Question:

`Does the ADC behave like an ADC, rather than only producing waveforms?`

Expected outputs:

1. sampled/quantized behavior is visible
2. code output is consistent with stimulus trend
3. DAC reconstruction or related derived signals make sense

### L2: Parity Loop

Question:

`If this ADC case becomes a parity-sensitive benchmark, does EVAS match Spectre closely enough?`

For `adc_dac_ideal_4b`, this is optional in the first round.

### L3: Benchmark Landing Loop

Question:

`Can this ADC case be packaged and tracked as a benchmark asset?`

Expected outputs:

1. benchmark task or benchmark seed assets exist
2. runner checks are defined
3. result table row is filled
4. PR is submitted

---

## 3. L0 Example: Minimal Executable Loop

### Input

Use:

1. `adc_ideal_4b.va`
2. `tb_adc_dac_ideal_4b_ramp.scs`

Possible extension:

1. `tb_adc_dac_ideal_4b_sine.scs`

### What We Check

At `L0`, only ask:

1. can EVAS parse and compile the ADC
2. can EVAS compile the testbench
3. is `tran.csv` generated

### Pass Condition

The case passes `L0` if:

1. `dut_compile = pass`
2. `tb_compile = pass`
3. `tran_generated = pass`

### Why L0 Is Not Enough

For ADC-like cases, `L0` is useful but weak.

A model can pass `L0` while still being wrong in important ways:

1. output code may be stuck
2. code may not track the input ramp
3. DAC reconstruction may not correspond to ADC decisions

So ADC is a good example of why the project must go beyond compile-only evaluation.

---

## 4. L1 Example: Behavior Validation Loop

### Core Question

At `L1`, the key question becomes:

`Is the ADC behavior functionally meaningful under EVAS?`

### Example Checks For `adc_dac_ideal_4b`

Reasonable checks include:

1. output code spans multiple levels instead of staying constant
2. code increases in step-like fashion for ramp input
3. DAC output roughly follows the sampled and quantized input
4. no obvious mismatch between expected sampling behavior and observed transitions

### Stronger Than Comparator

This is where ADC becomes a more interesting demonstration than comparator:

1. the output is not just a binary decision
2. quantization correctness matters
3. temporal sampling correctness matters
4. reconstructed analog behavior can be examined

### Example Evidence

Useful evidence may include:

1. code trace over time
2. input vs reconstructed DAC output
3. pass/fail result from an analysis or validation script

### Pass Condition

The case passes `L1` if:

1. `L0` already passed
2. quantized code behavior is non-degenerate
3. task-specific validation reports acceptable behavior

### Typical Table Row

| owner | case_name | dut_compile | tb_compile | tran_generated | sim_correct | benchmark_seed |
| --- | --- | --- | --- | --- | --- | --- |
| `[owner]` | `adc_dac_ideal_4b` | `pass` | `pass` | `pass` | `pass` | `[candidate]` |

---

## 5. L2 Example: Optional Parity Loop

### Is L2 Required Immediately?

Not necessarily.

This ADC case helps illustrate an important workflow rule:

1. not every useful benchmark candidate needs full Spectre parity on day one
2. EVAS-only behavioral evidence can already justify benchmark-seed status
3. parity can be added later when the case becomes more timing-sensitive or benchmark-critical

### When L2 Becomes Valuable

For ADC-type cases, parity becomes more valuable when:

1. sampling-edge behavior becomes important
2. there is ambiguity in event semantics
3. reconstructed output differs suspiciously from expected behavior
4. the case is promoted into a stronger benchmark tier

### Possible ADC Parity Metrics

If dual validation is introduced later, useful metrics may include:

1. code mismatch rate
2. sampled output timing difference
3. reconstructed output RMSE
4. sampled value disagreement at decision instants

### Key Message

ADC shows that `L2` should be selective, not mandatory for all cases.

That keeps the workflow scalable.

---

## 6. L3 Example: Benchmark Landing Loop

### Goal

Turn the ADC case from a validated example into a benchmark asset.

### Expected Assets

A benchmark-ready ADC case should have:

1. `prompt.md`
2. `meta.json`
3. `checks.yaml`
4. runner-side validation logic if needed

### Team Tracking

At `L3`, the team must also record:

1. result path
2. current maturity stage
3. PR link
4. corresponding row in [BENCHMARK_RESULT_TABLE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md)

### Pass Condition

The case passes `L3` if:

1. assets are complete
2. benchmark checks pass on reference output
3. the team result table is filled
4. a PR is submitted

---

## 7. Why ADC Is A Good Workflow Showcase

ADC is a strong showcase because it highlights the middle of the stack:

1. it is clearly richer than smoke-only examples
2. it shows why `sim_correct` matters
3. it demonstrates why benchmark checks must be behavior-aware
4. it does not force every contributor into full parity work immediately

In other words:

1. comparator shows the light path
2. ADC shows the behavior-validation path
3. PLL shows the full parity-heavy path

This is a good progression for onboarding and for explaining the benchmark philosophy.

---

## 8. Suggested Result-Table Mapping

A practical first-pass row for this ADC case should include:

1. `owner`
2. `case_name = adc_dac_ideal_4b`
3. `category = data-converter`
4. `dut_compile`
5. `tb_compile`
6. `tran_generated`
7. `sim_correct`
8. `benchmark_seed`
9. `result_path`
10. `pr_link`

If parity is not run yet:

1. `evas_fb_hz = N/A`
2. `spectre_fb_hz = N/A`
3. `ppm_cross_delta = N/A`
4. `lock_time_delta_s = N/A`
5. `parity_status = single-sim`

---

## 9. Suggested Next Step

If this ADC presentation works well, the next useful trio would be:

1. comparator for lightweight validation
2. ADC for behavior-aware validation
3. CPPLL for parity-heavy validation

That three-case ladder would make the layered workflow easier to explain in both:

1. team onboarding
2. future paper writing
