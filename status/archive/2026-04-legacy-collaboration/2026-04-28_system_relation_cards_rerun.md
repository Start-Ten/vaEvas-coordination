# System Relation Mechanism Cards Rerun

Date: 2026-04-28

## Goal

Distill historical system-level repair knowledge into reusable mechanism cards and retest representative previous FAIL tasks without copying task-specific gold artifacts or deterministic R26 patches.

## Changes

- Added prompt functional-IR support for DWA rotating pointer/cell-enable systems:
  - `rotating_selection_window` claim in `behavioral-veriloga-eval/runners/infer_prompt_checker_specs.py`
  - `onehot_no_overlap` prompt checker template in `behavioral-veriloga-eval/runners/infer_prompt_checker_specs.py`
  - `onehot_no_overlap` contract generation in `behavioral-veriloga-eval/runners/generate_behavior_contracts.py`
- Added validation coverage for:
  - `dwa_ptr_gen_no_overlap_smoke`
  - `dwa_wraparound_smoke`
- Regenerated adopted prompt specs:
  - validated tasks: 61
  - validation matches: 61
  - adopted specs: 63
- Added system-level mechanism cards to `behavioral-veriloga-eval/docs/CONTRACT_REPAIR_CARDS.json`:
  - `pll_system_feedback_graph`
  - `dwa_system_rotating_window_graph`
  - `pfd_bbpd_system_edge_pulse_graph`
  - `adc_dac_system_quantize_reconstruct_graph`
  - `serializer_system_load_shift_frame_graph`
- Fixed `check_behavior_contracts.py` so `MISSING_CSV` reports retain prompt semantic source metadata. This makes offline contract-card auditing match the no-CSV repair-prompt path.

## Contract/Card Validation

Generated contracts:

```bash
python3 runners/generate_behavior_contracts.py \
  --result-root results/condition-F-strictv3-evasloop-kimi-full92-materialized-evas-2026-04-28-rerun \
  --out-root results/generated-behavior-contracts-I-system-cards-on-Ffail-kimi-2026-04-28 \
  --prompt-specs docs/PROMPT_CHECKER_SPECS_ADOPTED.json \
  --task adpll_lock_smoke --task cppll_freq_step_reacquire_smoke \
  --task dwa_ptr_gen_no_overlap_smoke --task dwa_wraparound_smoke \
  --task bbpd_data_edge_alignment_smoke --task pfd_reset_race_smoke \
  --task cdac_cal --task sar_adc_dac_weighted_8b_smoke \
  --task serializer_frame_alignment_smoke \
  --overwrite
```

Card matching with `VAEVAS_FUNCTIONAL_IR_ONLY=1` and `VAEVAS_RELAXED_CARD_SELECTOR=1`:

| Task | Selected system card |
|---|---|
| `adpll_lock_smoke` | `pll_system_feedback_graph` |
| `cppll_freq_step_reacquire_smoke` | `pll_system_feedback_graph` |
| `dwa_ptr_gen_no_overlap_smoke` | `dwa_system_rotating_window_graph` |
| `dwa_wraparound_smoke` | `dwa_system_rotating_window_graph` |
| `bbpd_data_edge_alignment_smoke` | `pfd_bbpd_system_edge_pulse_graph` |
| `pfd_reset_race_smoke` | `pfd_bbpd_system_edge_pulse_graph` |
| `cdac_cal` | `adc_dac_system_quantize_reconstruct_graph` |
| `sar_adc_dac_weighted_8b_smoke` | `adc_dac_system_quantize_reconstruct_graph` |
| `serializer_frame_alignment_smoke` | `serializer_system_load_shift_frame_graph` |

## Repair Rerun

Command:

```bash
VAEVAS_CONTRACT_ROOT=results/generated-behavior-contracts-I-system-cards-on-Ffail-kimi-2026-04-28 \
VAEVAS_ENABLE_REPAIR_CARDS=1 \
VAEVAS_FUNCTIONAL_IR_ONLY=1 \
VAEVAS_RELAXED_CARD_SELECTOR=1 \
VAEVAS_REPAIR_CARD_LIMIT=3 \
python3 runners/run_adaptive_repair.py \
  --model kimi-k2.5 \
  --task adpll_lock_smoke \
  --task cppll_freq_step_reacquire_smoke \
  --task dwa_ptr_gen_no_overlap_smoke \
  --task dwa_wraparound_smoke \
  --task bbpd_data_edge_alignment_smoke \
  --task pfd_reset_race_smoke \
  --task cdac_cal \
  --task sar_adc_dac_weighted_8b_smoke \
  --task serializer_frame_alignment_smoke \
  --workers 3 \
  --resume \
  --source-generated-dir generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun \
  --initial-result-root results/condition-F-strictv3-evasloop-kimi-full92-materialized-evas-2026-04-28-rerun \
  --generated-root generated-condition-I-system-cards-on-Ffail-kimi-2026-04-28 \
  --output-root results/condition-I-system-cards-on-Ffail-kimi-evas-2026-04-28 \
  --max-rounds 3 \
  --patience 1 \
  --timeout-s 180 \
  --max-tokens 8192 \
  --env-file .env.table2 \
  --repair-public-spec-mode spectre-strict-v3 \
  --no-repair-skill \
  --layered-only-repair
```

Result: `0/9 PASS`.

| Task | Final status | Main remaining issue |
|---|---|---|
| `adpll_lock_smoke` | `FAIL_SIM_CORRECTNESS` | compile fixed, but late `fb/ref` edge ratio is still 2.0 and lock never asserts |
| `cppll_freq_step_reacquire_smoke` | `FAIL_TB_COMPILE` | duplicate voltage sources still drive `ref_clk` |
| `dwa_ptr_gen_no_overlap_smoke` | `FAIL_DUT_COMPILE` | dynamic analog vector indexing and conditional `transition()` |
| `dwa_wraparound_smoke` | `FAIL_SIM_CORRECTNESS` | pointer/count/wrap behavior still wrong |
| `bbpd_data_edge_alignment_smoke` | `FAIL_SIM_CORRECTNESS` | lead/lag UP/DN response imbalance remains |
| `pfd_reset_race_smoke` | `FAIL_SIM_CORRECTNESS` | missing expected first/second UP/DN pulses |
| `cdac_cal` | `FAIL_SIM_CORRECTNESS` | no `vdac` differential activity |
| `sar_adc_dac_weighted_8b_smoke` | `FAIL_INFRA` | EVAS timeout after generated multi-file candidate |
| `serializer_frame_alignment_smoke` | `FAIL_SIM_CORRECTNESS` | frame activity insufficient |

## Interpretation

The system cards are now reusable and are actually injected into repair prompts, but they are not enough to reproduce the historical R26 closure. The historical 92/92 result included deterministic patch/materialization logic, checker/runtime fixes, and verified artifact reuse. The cold-start card-only path currently improves guidance and sometimes failure layer, but it does not yet synthesize robust implementations for the hard system cases.

The useful signal is `adpll_lock_smoke`: it moved from DUT compile failure to behavior failure, showing the new PLL relation card can help the model produce a runnable artifact. The negative signal is DWA: the card explains the right system relation, but the model still emits Spectre-incompatible dynamic analog vector access. That suggests the next reusable mechanism should combine system cards with a Spectre-safe implementation pattern for bus expansion and held-state output driving.
