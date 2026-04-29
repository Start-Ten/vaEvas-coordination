# Other FAIL Cases After I Strict-v3

Date: 2026-04-28

Result root:

- `behavioral-veriloga-eval/results/condition-I-strictv3-functional-ir-full92-materialized-kimi-evas-2026-04-28-rerun`

Baseline:

- Kimi strict-v3 I full92 EVAS: `62/92 PASS`
- Total FAIL: `30`
- Excluded systemized representative cases: `9`
  - `adpll_lock_smoke`
  - `cppll_freq_step_reacquire_smoke`
  - `dwa_ptr_gen_no_overlap_smoke`
  - `dwa_wraparound_smoke`
  - `bbpd_data_edge_alignment_smoke`
  - `pfd_reset_race_smoke`
  - `cdac_cal`
  - `sar_adc_dac_weighted_8b_smoke`
  - `serializer_frame_alignment_smoke`
- Remaining other FAIL: `21`

## Remaining FAIL List

| Task | Status | Main observed issue |
|---|---|---|
| `adc_dac_ideal_4b_smoke` | `FAIL_SIM_CORRECTNESS` | compile/run clean; ADC/DAC ideal behavior still wrong |
| `adpll_ratio_hop_smoke` | `FAIL_DUT_COMPILE` | embedded declarations inside Verilog-A procedural region |
| `adpll_timer_smoke` | `FAIL_INFRA` | EVAS timeout after strict preflight |
| `bbpd` | `FAIL_DUT_COMPILE` | conditional `transition()` |
| `bg_cal` | `FAIL_SIM_CORRECTNESS` | trim code spans, but `settled_high=False` |
| `clk_divider` | `FAIL_SIM_CORRECTNESS` | not enough output clock edges |
| `cppll_timer` | `FAIL_SIM_CORRECTNESS` | `returncode=1`, `tran.csv missing`; likely runtime/artifact issue |
| `cppll_tracking_smoke` | `FAIL_SIM_CORRECTNESS` | compile/run clean; PLL tracking behavior still wrong |
| `cross_hysteresis_window_smoke` | `FAIL_SIM_CORRECTNESS` | compile/run clean; hysteresis/window behavior wrong |
| `d2b_4bit_smoke` | `FAIL_DUT_COMPILE` | unsupported `integer(...)` cast pattern |
| `flash_adc_3b_smoke` | `FAIL_DUT_COMPILE` | unsupported `integer(...)` cast pattern |
| `gray_counter_4b_smoke` | `FAIL_DUT_COMPILE` | conditional `@(cross())` |
| `lfsr_smoke` | `FAIL_SIM_CORRECTNESS` | compile/run clean; sequence behavior wrong |
| `multimod_divider` | `FAIL_SIM_CORRECTNESS` | ratio switch count mismatch: `base=4 pre_count=4 post_count=5` |
| `multimod_divider_ratio_switch_smoke` | `FAIL_SIM_CORRECTNESS` | compile/run clean; ratio-switch behavior wrong |
| `nrz_prbs` | `FAIL_DUT_COMPILE` | embedded declarations plus unsupported `integer(...)` cast |
| `phase_accumulator_timer_wrap_smoke` | `FAIL_SIM_CORRECTNESS` | compile/run clean; phase/timer wrap behavior wrong |
| `prbs7` | `FAIL_SIM_CORRECTNESS` | stuck output: `transitions=0 hi_frac=0.000` |
| `ramp_gen_smoke` | `FAIL_SIM_CORRECTNESS` | compile/run clean; ramp behavior wrong |
| `serializer_8b_smoke` | `FAIL_SIM_CORRECTNESS` | compile/run clean; serializer sequence behavior wrong |
| `transition_branch_target_smoke` | `FAIL_SIM_CORRECTNESS` | compile/run clean; transition/branch target behavior wrong |

## Grouping

### Compile/Syntax-Layer FAIL: 6

These are likely good next targets for the implementation-skeleton strategy because they are not yet behavior problems.

- `adpll_ratio_hop_smoke`: embedded declarations
- `bbpd`: conditional `transition()`
- `d2b_4bit_smoke`: unsupported `integer(...)`
- `flash_adc_3b_smoke`: unsupported `integer(...)`
- `gray_counter_4b_smoke`: conditional `@(cross())`
- `nrz_prbs`: embedded declarations and unsupported `integer(...)`

### Infra/Runtime-Layer FAIL: 2

- `adpll_timer_smoke`: timeout
- `cppll_timer`: `returncode=1`, missing `tran.csv`

`cppll_timer` is labeled `FAIL_SIM_CORRECTNESS` by the scorer, but the note shape is runtime/artifact-like.

### Behavior-Layer FAIL: 13

These compile and run, so they need mechanism-level or metric-gap repair rather than syntax repair.

- `adc_dac_ideal_4b_smoke`
- `bg_cal`
- `clk_divider`
- `cppll_tracking_smoke`
- `cross_hysteresis_window_smoke`
- `lfsr_smoke`
- `multimod_divider`
- `multimod_divider_ratio_switch_smoke`
- `phase_accumulator_timer_wrap_smoke`
- `prbs7`
- `ramp_gen_smoke`
- `serializer_8b_smoke`
- `transition_branch_target_smoke`

## Suggested Next Batch

The most efficient next batch is probably the 6 compile/syntax failures, because the repair objective is crisp and should not require deeper circuit reasoning:

1. `d2b_4bit_smoke`
2. `flash_adc_3b_smoke`
3. `gray_counter_4b_smoke`
4. `bbpd`
5. `nrz_prbs`
6. `adpll_ratio_hop_smoke`

If those move from compile failures to behavior failures, then the implementation-skeleton strategy is doing useful general work beyond the nine systemized cases.
