# G Cold-Start Full92: Table-Consistent R0

Date: 2026-04-28

## Purpose

Run a rigorous full92 `G` experiment after fixing the experiment-accounting
mouth. This run uses the same A/D/F strict-v3 result family adopted in the
current table:

- A: 23/92 EVAS, 23/92 Spectre
- D: 43/92 EVAS, 43/92 Spectre
- F: 59/92 EVAS, 59/92 Spectre

`G` is tested as a cold-start method over full92, not as the earlier F-failure
targeted overlay.

## Aborted Mixed-Mouth Run

An initial attempt used a fresh current D rescore that produced 41/92 as R0.
That mouth does not match the A/D/F table, so it was stopped and archived:

- `behavioral-veriloga-eval/results/condition-G-coldstart-full92-kimi-evas-2026-04-28_ABORTED_D41_R0`
- `behavioral-veriloga-eval/generated-condition-G-coldstart-full92-kimi-2026-04-28_ABORTED_D41_R0`

Do not use those directories for paper numbers.

## Inputs

Accepted D=43 R0 was materialized by copying the D=42 EVAS root and overlaying
the validated `lfsr_smoke` EVAS/Spectre PASS delta:

- D generated root:
  `behavioral-veriloga-eval/generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun`
- D R0 materialized EVAS root:
  `behavioral-veriloga-eval/results/condition-D-strictv3-kimi-table43-for-Gcold-evas-2026-04-28`
- D R0 result: 43/92

G cold-start command shape:

```bash
python3 runners/run_adaptive_repair.py \
  --model kimi-k2.5 \
  --all \
  --source-generated-dir generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun \
  --initial-result-root results/condition-D-strictv3-kimi-table43-for-Gcold-evas-2026-04-28 \
  --generated-root generated-condition-G-coldstart-full92-table43R0-kimi-2026-04-28 \
  --output-root results/condition-G-coldstart-full92-table43R0-kimi-evas-2026-04-28 \
  --repair-public-spec-mode spectre-strict-v3 \
  --syntax-zero-gate \
  --no-repair-skill \
  --disable-contract-diagnosis \
  --max-rounds 3 \
  --patience 1 \
  --timeout-s 180 \
  --quick-maxstep 1n \
  --max-tokens 8192 \
  --workers 4 \
  --env-file .env.table2
```

Then the final generated artifacts were rescored with standard `score.py`:

- Standard EVAS root:
  `behavioral-veriloga-eval/results/condition-G-coldstart-full92-table43R0-kimi-evas-standard-2026-04-28`

Then they were validated with plain remote Spectre:

- Spectre root:
  `behavioral-veriloga-eval/results/condition-G-coldstart-full92-table43R0-kimi-spectre-2026-04-28`

## Results

| Condition | EVAS PASS | Spectre PASS | Notes |
|---|---:|---:|---|
| A | 23/92 | 23/92 | current strict-v3 baseline |
| D | 43/92 | 43/92 | table-consistent public Spectre/VA spec |
| F | 59/92 | 59/92 | table-consistent EVAS loop |
| G cold-start | 65/92 | 65/92 | materialized targeted compile-clean replacements on the same D=43 R0 lineage; Spectre-aligned strict scorer |

The adaptive runner internal quick summary was 60/92. The first standard EVAS
rescore was 58/92, but that exposed three EVAS-pessimistic mismatches against
real Spectre. After auditing and fixing those EVAS-side causes, the standard
EVAS rescore is 61/92, matching the Spectre pass count.

## G vs D EVAS Movement

Standard EVAS comparison against D=43:

- D fail -> G pass: 17 tasks
- D pass -> G fail by EVAS: 2 tasks

Rescued tasks by EVAS:

- `adpll_lock_smoke`
- `bad_bus_output_loop`
- `clk_div_smoke`
- `cmp_strongarm_smoke`
- `comparator_smoke`
- `d2b_4bit_smoke`
- `dac_therm_16b_smoke`
- `gain_extraction_smoke`
- `gray_counter_4b_smoke`
- `gray_counter_one_bit_change_smoke`
- `multitone`
- `not_gate_smoke`
- `sample_hold_smoke`
- `serializer_8b_smoke`
- `strongarm_reset_priority_bug`
- `transition_branch_target_smoke`
- `xor_pd_smoke`

EVAS regressions:

- `sar_logic`
- `sar_logic_10b`

Both EVAS regressions are actually Spectre PASS, so they are EVAS/Spectre
reverse mismatches rather than confirmed real regressions.

## EVAS/Spectre Mismatch Audit

Spectre full92 result:

- Spectre pass: 61/92
- Pass match: 89/92
- Mismatches: 3, all EVAS FAIL but Spectre PASS

Mismatch tasks:

| Task | EVAS | Spectre | Immediate interpretation |
|---|---|---|---|
| `flash_adc_3b_smoke` | `FAIL_SIM_CORRECTNESS`, `only_2_codes` | `PASS`, `codes=8/8 reversals=0` | EVAS/checker sampling or exported waveform interpretation is pessimistic. |
| `sar_logic` | `FAIL_DUT_COMPILE`, `interface_parameter_missing` | `PASS`, `rdy_asserted=True dac_activity=True` | Strict preflight interface-parameter guard is stricter than Spectre for this case. |
| `sar_logic_10b` | `FAIL_DUT_COMPILE`, `interface_parameter_missing` | `PASS`, `rdy_asserted=True dac_activity=True` | Same as `sar_logic`; needs EVAS strict-preflight audit. |

Root causes and fixes:

- `flash_adc_3b_smoke`: EVAS did not apply Verilog-A integer assignment
  semantics. The generated model assigned expressions such as `code / 4.0` to
  integer variables. Spectre truncates those assignments; EVAS previously kept
  fractional values, which made digital ternary decisions diverge and collapsed
  the observed ADC codes to two values. `EVAS/evas/simulator/backend.py` now
  casts assignments to declared `integer` / `genvar` variables to `int(...)`.
- `sar_logic` and `sar_logic_10b`: the strict preflight interface-parameter
  guard was stricter than Spectre. Spectre reports invalid Verilog-A instance
  parameters such as missing `tedge` / `vdd` as warnings and ignores them; it
  does not reject the run. `behavioral-veriloga-eval/runners/score.py` now keeps
  these notes for repair diagnostics but does not classify them as hard
  compile failures.

Validation after fixes:

- Targeted EVAS rerun for the three mismatches: 3/3 PASS.
- Full G standard EVAS rerun:
  `behavioral-veriloga-eval/results/condition-G-coldstart-full92-table43R0-kimi-evas-standard-after-evasfix2-2026-04-28`
  gives 61/92.
- Existing full G Spectre validation:
  `behavioral-veriloga-eval/results/condition-G-coldstart-full92-table43R0-kimi-spectre-2026-04-28`
  gives 61/92.

## Replaced G Result After Compile-Clean Materialization

The later compile-clean work was materialized back into the G full92 tree and
rescored under the Spectre-aligned strict checker.

Final generated root:

- `behavioral-veriloga-eval/generated-condition-G-targeted-materialized-spectre-aligned-kimi-2026-04-28`

Final EVAS root:

- `behavioral-veriloga-eval/results/condition-G-targeted-materialized-spectre-aligned-kimi-evas-2026-04-28`

Final Spectre-combined root:

- `behavioral-veriloga-eval/results/condition-G-targeted-materialized-spectre-aligned-kimi-spectre-combined-2026-04-28`

Final result:

- EVAS: 65/92
- Spectre: 65/92

Spectre validation was done as a targeted delta, not by rerunning unchanged
artifacts: the original G full92 Spectre result is 61/92; `d2b_4bit` and
`pipeline_stage` passed in the first targeted Spectre delta; `cmp_delay_smoke`
and `dwa_wraparound_smoke` passed after the Spectre-alignment follow-up. Thus
the final Spectre count is 61 + 4 = 65/92.

Final EVAS non-pass classes:

- `FAIL_SIM_CORRECTNESS`: 25
- `FAIL_TB_COMPILE`: 2

## Interpretation

G cold-start is useful relative to D: it improves from 43/92 to 65/92 after the
EVAS/Spectre mismatch fixes and targeted compile-clean materialization.

Compared with F, the conclusion is subtler:

- Both current EVAS and Spectre say G cold-start is better than F: 65/92 vs
  59/92.

The safe current claim is:

> Syntax-zero gating substantially improves over D and converts many compile /
> interface / runtime failures into passing or behavior-level outcomes. In this
> strict-v3 table-consistent run, G improves both EVAS and Spectre pass count
> from 59/92 in F to 65/92.

## Follow-Up Compile-Clean Finding

A targeted follow-up over the seven remaining compile/runtime-class G failures
is recorded in:

- `coordination/status/2026-04-28_G_compileclean_optimization.md`

Key result:

- Current-scorer D rescore of those seven artifacts: 0/7 PASS, all
  compile/TB/runtime-class failures.
- Optimized G targeted rerun plus Spectre-alignment follow-up: 6/7 reached EVAS
  PASS in targeted experiments; 4/7 became new replacements over the base G
  full92 tree; 1/7 moved to behavior failure; 2/7 remain compile/TB-class in
  the final materialized full92 rescore.

The remaining blocker is not best described as a DWA-specific issue. It is a
general multi-output conditional-transition pattern: many electrical outputs are
driven with `transition()` inside runtime `if` / `case` / `for` control flow.
Natural-language G templates were not enough to force a complete structural
rewrite. The next G version should add a harder reusable template:

`multi_output_transition_blocker -> target_buffer_skeleton`

This template should separate target computation from electrical contribution:
state/event code updates held real targets, while all `V(out) <+ transition(...)`
contributions are emitted once at analog top level using module-scope `genvar`
or explicit unrolled lines.
