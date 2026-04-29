# G syntax-zero gate experiment

## Brief

Implement condition `G` as a reproducible runner mode on top of condition `F`.
The goal is not to add circuit knowledge. The goal is to force the repair loop
to clear syntax, interface, runtime, strict-preflight, and observable-artifact
errors before it starts changing behavior.

## KPI

- Primary: improve F failures whose first failure surface is compile, strict
  preflight, runtime artifact, or observability.
- Secondary: expose behavior-level EVAS feedback even when the task still does
  not pass.
- Guardrail: do not inject contract cards or task-specific circuit knowledge in
  this G run.

## Implementation

Changed:

- `behavioral-veriloga-eval/runners/run_adaptive_repair.py`

Added:

- CLI flag: `--syntax-zero-gate`
- Gate state recorded in each round `generation_meta.json`
- Prompt section: `# Syntax-Zero Gate (Condition G)`
- Gate issue extraction for:
  - DUT/TB compile not zero
  - `tran.csv missing`, `returncode=1`, timeout, `tb_not_executed`
  - strict-v3 markers such as `conditional_transition`,
    `conditional_cross`, `digital_verilog_syntax`,
    `dynamic_analog_vector_index`, embedded/strict preflight markers
  - observable-surface failures such as missing saved columns or too few edges
- Conservative preservation:
  - for `compile_tb` and `observable` layers, preserve the existing DUT and
    let the model repair the harness/testbench surface

G does not use contracts, mechanism cards, or gold harness behavior freezing in
this smoke run.

## Commands

First smoke batch:

```bash
python3 runners/run_adaptive_repair.py \
  --model kimi-k2.5 \
  --task adpll_ratio_hop_smoke \
  --task bbpd \
  --task d2b_4bit_smoke \
  --task flash_adc_3b_smoke \
  --task gray_counter_4b_smoke \
  --task nrz_prbs \
  --task adpll_timer_smoke \
  --task cppll_timer \
  --source-generated-dir generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun \
  --initial-result-root results/condition-F-strictv3-evasloop-kimi-full92-materialized-evas-2026-04-28-rerun \
  --generated-root generated-condition-G-syntax-zero-on-Ffail-kimi-2026-04-28 \
  --output-root results/condition-G-syntax-zero-on-Ffail-kimi-evas-2026-04-28 \
  --repair-public-spec-mode spectre-strict-v3 \
  --syntax-zero-gate \
  --no-repair-skill \
  --disable-contract-diagnosis \
  --max-rounds 3 \
  --patience 1 \
  --timeout-s 180 \
  --quick-maxstep 1n \
  --max-tokens 8192 \
  --workers 3 \
  --env-file .env.table2
```

Then extended to the remaining F compile/TB/infra-surface failures:

```bash
python3 runners/run_adaptive_repair.py \
  --model kimi-k2.5 \
  --task adpll_lock_smoke \
  --task bad_bus_output_loop \
  --task dwa_ptr_gen_no_overlap_smoke \
  --task cppll_freq_step_reacquire_smoke \
  --task sar_adc_dac_weighted_8b_smoke \
  --source-generated-dir generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun \
  --initial-result-root results/condition-F-strictv3-evasloop-kimi-full92-materialized-evas-2026-04-28-rerun \
  --generated-root generated-condition-G-syntax-zero-on-Ffail-kimi-2026-04-28 \
  --output-root results/condition-G-syntax-zero-on-Ffail-kimi-evas-2026-04-28 \
  --repair-public-spec-mode spectre-strict-v3 \
  --syntax-zero-gate \
  --no-repair-skill \
  --disable-contract-diagnosis \
  --max-rounds 3 \
  --patience 1 \
  --timeout-s 180 \
  --quick-maxstep 1n \
  --max-tokens 8192 \
  --workers 3 \
  --env-file .env.table2
```

## Results

Result root:

- `behavioral-veriloga-eval/results/condition-G-syntax-zero-on-Ffail-kimi-evas-2026-04-28/summary.json`
- Per-task best results are under
  `behavioral-veriloga-eval/results/condition-G-syntax-zero-on-Ffail-kimi-evas-2026-04-28/best/<task>/result.json`.
  The last runner invocation overwrote top-level `summary.json` with the
  second 5-task batch, so the 13-task aggregate below is computed from `best/`.

Generated root:

- `behavioral-veriloga-eval/generated-condition-G-syntax-zero-on-Ffail-kimi-2026-04-28/`

## Surface-clean Closure Update

After the first 13-task run, we found one omitted runtime-artifact case:

- `adc_dac_ideal_4b_smoke`: F reported `returncode=1` and
  `tran.csv missing`.

We added it to G. G moved it to behavior-level feedback:

- `returncode=0`
- `streaming_checker:unique_codes=1 vout_span=0.844 vin_span=0.719`

Two residual non-behavior surfaces then remained:

- `flash_adc_3b_smoke`: TB/runtime failure from malformed PWL source syntax.
- `cppll_timer`: generic `tran.csv missing`, later found to be an EVAS
  runtime exception from division by zero inside the generated DUT.

To make G capable of closing these without task-specific circuit cards, we
added three generic diagnostics:

- `score.py`: strict preflight detects malformed Spectre PWL `wave=[...]`
  lists whose time/value tokens are not paired.
- `score.py`: strict preflight checks instance parameters passed by the actual
  staged testbench, including gold harnesses used by `spec-to-va`.
- `simulate_evas.py`: EVAS runtime exceptions such as
  `ZeroDivisionError: float division by zero` are preserved in `evas_notes`
  instead of being collapsed into only `tran.csv missing`.

Closure roots:

- `behavioral-veriloga-eval/results/condition-G-syntax-zero-closure-v2-kimi-evas-2026-04-28/`
- `behavioral-veriloga-eval/results/condition-G-syntax-zero-closure-v3-kimi-evas-2026-04-28/`

Final surface-clean aggregate over 14 F compile/TB/infra/runtime-surface cases:

| Condition | PASS | Average weighted score | Status mix | Residual compile/missing/runtime |
|---|---:|---:|---|---:|
| F source | 0/14 | 0.3333 approx | mixed compile/TB/infra/runtime | 14 |
| G surface-clean | 4/14 | 0.7619 | 4 `PASS`, 10 `FAIL_SIM_CORRECTNESS` | 0 |

The 4 PASS cases are:

- `d2b_4bit_smoke`
- `flash_adc_3b_smoke`
- `gray_counter_4b_smoke`
- `bad_bus_output_loop`

The remaining 10 cases all have DUT compile = 1, TB compile = 1,
`returncode=0`, and behavior-level metric feedback.

New Spectre checks after closure:

- `flash_adc_3b_smoke`: Spectre `1/1 PASS`, pass match `1/1`
  at
  `behavioral-veriloga-eval/results/condition-G-syntax-zero-closure-v2-kimi-spectre-flash-2026-04-28/`
- `cppll_timer`: Spectre `0/1 PASS`, pass match `1/1`
  at
  `behavioral-veriloga-eval/results/condition-G-syntax-zero-closure-v3-kimi-spectre-cppll-timer-2026-04-28/`

This is the intended G outcome: the syntax/runtime/CSV surface has been cleaned,
and the remaining failures are behavior failures suitable for H/I.

## Initial 13-task Smoke Before Closure

Aggregate on the first 13 F compile/TB/infra-surface failures:

| Condition | PASS | Average weighted score | Status mix |
|---|---:|---:|---|
| F source | 0/13 | 0.3077 | 9 `FAIL_DUT_COMPILE`, 2 `FAIL_INFRA`, 1 `FAIL_TB_COMPILE`, 1 `FAIL_SIM_CORRECTNESS` |
| G syntax-zero | 3/13 | 0.7180 | 3 `PASS`, 9 `FAIL_SIM_CORRECTNESS`, 1 `FAIL_TB_COMPILE` |

Remote Spectre cross-check for the three new G PASS artifacts:

- Output:
  `behavioral-veriloga-eval/results/condition-G-syntax-zero-on-Ffail-kimi-spectre-pass3-2026-04-28/`
- Mode: plain `spectre`
- Result: `3/3 PASS`, pass matches `3/3`
- Tasks: `d2b_4bit_smoke`, `gray_counter_4b_smoke`,
  `bad_bus_output_loop`

Remote Spectre cross-check for the ten remaining G FAIL artifacts:

- Output:
  `behavioral-veriloga-eval/results/condition-G-syntax-zero-on-Ffail-kimi-spectre-fail10-2026-04-28/`
- Mode: plain `spectre`
- Result: `0/10 PASS`, pass matches `10/10`
- Spectre failure taxonomy: 7 `FAIL_SIM_CORRECTNESS`,
  3 `FAIL_DUT_COMPILE` / `FAIL_SPECTRE_RUN`-style validation failures

This means the initial G pass/fail outcome was aligned with real Spectre on
all 13 targeted cases. The detailed failure surface was not always identical:
three cases that EVAS could stage as behavior/runtime failures become
Spectre-run/data-missing failures under plain Spectre.

Initial per-task comparison:

| Task | F status | G status | What changed |
|---|---|---|---|
| `d2b_4bit_smoke` | `FAIL_DUT_COMPILE` | `PASS` | strict digital/integer syntax fixed, behavior passes |
| `gray_counter_4b_smoke` | `FAIL_DUT_COMPILE` | `PASS` | conditional-cross style failure cleared, Gray behavior passes |
| `adpll_ratio_hop_smoke` | `FAIL_DUT_COMPILE` | `FAIL_SIM_CORRECTNESS` | compile/preflight cleared, now fails on edge-window behavior |
| `bbpd` | `FAIL_DUT_COMPILE` | `FAIL_SIM_CORRECTNESS` | conditional transition cleared, now exposes pulse behavior metrics |
| `nrz_prbs` | `FAIL_DUT_COMPILE` | `FAIL_SIM_CORRECTNESS` | embedded declarations/integer syntax cleared, now exposes transition/complement metrics |
| `adpll_timer_smoke` | `FAIL_INFRA` | `FAIL_SIM_CORRECTNESS` | runner reaches stable simulation and streaming checker metrics |
| `flash_adc_3b_smoke` | `FAIL_DUT_COMPILE` | `FAIL_TB_COMPILE` | DUT strict syntax cleared, but generated harness/runtime still fails |
| `cppll_timer` | `FAIL_SIM_CORRECTNESS` | `FAIL_SIM_CORRECTNESS` | no improvement; still `returncode=1` / `tran.csv missing` |
| `adpll_lock_smoke` | `FAIL_DUT_COMPILE` | `FAIL_SIM_CORRECTNESS` | strict syntax cleared, now exposes PLL lock metrics |
| `bad_bus_output_loop` | `FAIL_DUT_COMPILE` | `PASS` | dynamic analog vector index problem cleared, bus behavior passes |
| `dwa_ptr_gen_no_overlap_smoke` | `FAIL_DUT_COMPILE` | `FAIL_SIM_CORRECTNESS` | conditional/vector strict surface cleared, now exposes DWA activity metrics |
| `cppll_freq_step_reacquire_smoke` | `FAIL_TB_COMPILE` | `FAIL_SIM_CORRECTNESS` | TB compile/runtime surface cleared, now exposes PLL reacquire metrics |
| `sar_adc_dac_weighted_8b_smoke` | `FAIL_INFRA` | `FAIL_SIM_CORRECTNESS` | simulation reaches stable checker metrics |

## Interpretation

G helps most when F is blocked by syntax/strict-preflight/interface surfaces.
It is not yet a behavior repair strategy. Its main value is making later H/I
conditions more meaningful: after G, many tasks have stable DUT/TB compile,
strict preflight pass, `returncode=0`, and concrete behavior metrics.

After closure, the direct gain on the targeted surface set is `+4 PASS` over
the same F artifacts, and all 14 selected compile/TB/infra/runtime surfaces
were converted into either PASS or behavior-level failures.

## Remaining Risk

- This is a targeted 14-task compile/TB/infra/runtime-surface smoke, not a full92
  official row.
- Newly passing G artifacts were remote Spectre-cross-validated. The remaining
  behavior failures were not all re-cross-validated after closure.
- `cppll_timer` now reaches behavior-level feedback, but its PLL behavior is
  still wrong: `freq_ratio=0.5082`, `lock_time=nan`.

## Next

Use G as the official bridge between F and H:

1. Run G on all non-PASS F tasks, or at least all compile/runtime/observable
   failures.
2. Spectre-validate newly passing G artifacts.
3. Feed G-stabilized behavior failures into H, where failure signatures and
   mechanism cards can operate on concrete behavior metrics instead of syntax
   noise.
