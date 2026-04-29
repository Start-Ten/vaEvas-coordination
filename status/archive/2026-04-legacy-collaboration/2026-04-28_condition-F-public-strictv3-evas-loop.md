# Condition F Public Strict v3 EVAS Loop

Date: 2026-04-28

## Definition

F is the clean public-rule EVAS repair condition:

- initial candidates come from D-style generation with public Spectre/Verilog-A strict v3 rules;
- repair uses EVAS feedback only, up to three rounds;
- repair skill cards, task-local contracts, functional IR, gold knowledge, and Spectre-in-the-loop feedback are disabled;
- Spectre is used only as a final gate for EVAS-passing candidates.

## Runner Changes

- `behavioral-veriloga-eval/runners/run_adaptive_repair.py`
  - Added `--workers` for task-level parallel repair.
  - Added `--resume` to skip already materialized best candidates.
  - Added `--repair-public-spec-mode spectre-strict-v3`.
  - Added `--no-repair-skill` and `--disable-contract-diagnosis` for clean F.
- `behavioral-veriloga-eval/runners/build_repair_prompt.py`
  - Repair prompts can now reuse the same public spec mode as initial generation.
  - Contract diagnosis can be explicitly disabled for F.
- `behavioral-veriloga-eval/runners/score.py`
  - strict v3 preflight now catches reversed Spectre source syntax such as `vsource vdd (...)`.
  - strict v3 preflight now catches `type=pulse` sources with `rise=0` or `fall=0`.
- `behavioral-veriloga-eval/specs/spectre_veriloga_public_rules.md`
  - Added the same public source-instantiation and positive pulse-edge rules.

## Main Results

| Condition | Gate | Pass |
|---|---:|---:|
| D public strict v3 one-shot | EVAS | 45/92 |
| F public strict v3 EVAS loop | EVAS | 60/92 |
| F public strict v3 EVAS loop | EVAS after EVAS-core/checker alignment fixes | 62/92 |
| F public strict v3 EVAS loop | Spectre final gate, `ax` preset | 59/92 |
| F public strict v3 EVAS loop | Spectre final gate, corrected mode by sole-mismatch retest | 60/92 |
| F public strict v3 EVAS loop | Spectre-known pass after EVAS alignment targeted retests | 62/92 |
| F public strict v3 generated tree | APS exploratory full92 gate | 62/92 |

The EVAS loop adds 15 net passes over D with no D-pass regressions under the final combined scoring run.
The later 60/92 to 62/92 change is not a new repair-loop gain. It fixes two EVAS-side false negatives already shown to pass real Spectre/APS:
`cross_sine_precision_smoke` and `dac_binary_clk_4b_smoke`.

## New F Passes Over D

- `bad_bus_output_loop`
- `clk_burst_gen_smoke`
- `cmp_strongarm_smoke`
- `comparator_offset_search_smoke`
- `cppll_timer`
- `dwa_ptr_gen_smoke`
- `gain_extraction_smoke`
- `gray_counter_4b_smoke`
- `gray_counter_one_bit_change_smoke`
- `noise_gen_smoke`
- `pipeline_stage`
- `prbs7`
- `sample_hold_smoke`
- `transition_branch_target_smoke`
- `xor_pd_smoke`

## Final Artifacts

- D EVAS baseline:
  `behavioral-veriloga-eval/results/condition-D-public-spectre-kimi-strict-v3-checker-r2-full92-existing-2026-04-28/`
- F combined generated tree:
  `behavioral-veriloga-eval/generated-condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-2026-04-28/`
- F final EVAS:
  `behavioral-veriloga-eval/results/condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-evas-2026-04-28/`
- F final EVAS after EVAS-core/checker alignment fixes:
  `behavioral-veriloga-eval/results/condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-evas-after-evasfix-full92-2026-04-28/`
- F final Spectre gate:
  `behavioral-veriloga-eval/results/condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-spectre-2026-04-28/`
- F corrected Spectre-mode retest for the sole mismatch:
  `behavioral-veriloga-eval/results/condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-spectre-mode-spectre-comparator-2026-04-28/`
- F plain-Spectre retest for the two EVAS false negatives:
  `behavioral-veriloga-eval/results/condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-spectre-mode-spectre-evasfail-apspass2-2026-04-28/`
- F APS exploratory full92 gate:
  `behavioral-veriloga-eval/results/condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-spectre-mode-aps-2026-04-28/`
- F strict-r2 targeted repair for the two EVAS/Spectre mismatches:
  `behavioral-veriloga-eval/results/condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-targeted-2026-04-28/`

## Spectre Mode Correction

The previous final Spectre gate used the bridge default `ax` Spectre X preset. For the sole residual mismatch, `comparator_offset_search_smoke`, the Spectre log showed that Spectre X ignored/redefined the transient controls from the submitted netlist:

- EVAS note: `crossing_voltage=0.5076 low_frac=1.000 high_frac=1.000`
- `ax` Spectre note: `crossing_voltage=0.5153 low_frac=1.000 high_frac=1.000`
- `ax` log: `maxstep = 2 ns`, `Number of accepted tran steps = 55`

After adding `--spectre-mode` to `runners/spectre_validate_baseline.py` and rerunning the same generated artifact with plain `spectre` mode, the case passed:

- command mode: `--spectre-mode spectre`
- Spectre command omitted `+preset=ax`
- log: `maxstep = 100 ps`, `errpreset = conservative`, `Number of accepted tran steps = 1005`
- Spectre note: `spectre_csv_rows=1006 cols=4`, `crossing_voltage=0.5079 low_frac=1.000 high_frac=1.000`

Conclusion: the previous residual mismatch was a validation-backend mode issue, not an EVAS-loop repair failure. The corrected F Spectre-gated result is 60/92 by targeted retest of the only mismatched task.

## APS Exploratory Gate

We also ran the full F combined generated tree with `--spectre-mode aps`. APS preserved `maxstep` on inspected maxstep-sensitive tasks and produced:

- APS Spectre Pass@1: 62/92
- pass matches vs EVAS: 90/92
- mismatches:
  - `cross_sine_precision_smoke`: EVAS FAIL, APS PASS (`count_est=3.00 max_err_ps=0.9697`)
  - `dac_binary_clk_4b_smoke`: EVAS FAIL, APS PASS (`streaming_checker:levels=16 aout_span=0.835`)

This is an exploratory infrastructure result rather than the primary F metric. It suggests that APS can serve as a faster strict backend, and that EVAS may have a small number of simulator/backend false negatives. Details are recorded in `coordination/referencepaper/other_findings/spectre_backend_modes.md`.

## EVAS Alignment Fixes

After the APS/Spectre mismatch audit, we fixed the two EVAS false negatives rather than treating them as circuit failures:

- `EVAS/evas/netlist/runner.py`: Spectre sine sources now accept the common `dc`/`mag` aliases in addition to `sinedc`/`ampl`.
- `behavioral-veriloga-eval/runners/simulate_evas.py`: `dac_binary_clk_4b` now samples the reconstructed DAC output after `rdy` rising edges, matching the timing intent used by the Spectre checker instead of mixing transition rows into the level estimate.
- Regression coverage was added for comma-separated PWL waves and direct filename `$fstrobe(...)` handling, because these are EVAS compatibility behaviors that should not regress.

Validation:

- `PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_netlist.py EVAS/tests/test_engine.py -q`: 165 passed.
- targeted EVAS retest of `cross_sine_precision_smoke` and `dac_binary_clk_4b_smoke`: 2/2 PASS.
- full92 EVAS retest: 62/92, with `FAIL_INFRA` reduced to 0.

## Interpretation

F proves that public compatibility rules plus EVAS-only multi-round repair can substantially improve one-shot generation. The gains are concentrated in compile, testbench, source-instantiation, interface, and localized event/logic tasks. The remaining failures are mostly behavior-mechanism failures, motivating H/I-style contract and mechanism-guided repair.
