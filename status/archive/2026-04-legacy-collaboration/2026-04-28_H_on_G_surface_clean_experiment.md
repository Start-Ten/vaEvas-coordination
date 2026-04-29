# H-on-G Surface-Clean Experiment

Date: 2026-04-28

## Purpose

This run tests condition H after condition G has already removed compile,
testbench, runtime, missing-artifact, and observable-noise failures.

Operational definition used here:

`H = G-stabilized artifacts + EVAS failure-signature/mechanism-guided behavior repair`

Excluded from this H run:

- contracts / functional IR
- mechanism-card skill injection
- task-local verified artifacts
- gold implementation copying

## Inputs

The input set is the 10 behavior-level failures remaining after the G
surface-clean closure:

- `adc_dac_ideal_4b_smoke`
- `adpll_ratio_hop_smoke`
- `bbpd`
- `nrz_prbs`
- `adpll_timer_smoke`
- `cppll_timer`
- `adpll_lock_smoke`
- `dwa_ptr_gen_no_overlap_smoke`
- `cppll_freq_step_reacquire_smoke`
- `sar_adc_dac_weighted_8b_smoke`

G source roots:

- `behavioral-veriloga-eval/results/condition-G-syntax-zero-on-Ffail-kimi-evas-2026-04-28/best`
- `behavioral-veriloga-eval/results/condition-G-syntax-zero-closure-v2-kimi-evas-2026-04-28/best`
- `behavioral-veriloga-eval/results/condition-G-syntax-zero-closure-v3-kimi-evas-2026-04-28/best`

## Signature-Guided H Prototype Check

First, the older bounded-template H prototype was run on materialized G anchors:

```bash
python3 runners/signature_guided_h.py \
  --g-result-root results/condition-G-syntax-zero-on-Ffail-kimi-evas-2026-04-28/best \
  --anchor-root generated-condition-G-surface-clean-anchors-for-H-kimi-2026-04-28 \
  --output-root results/condition-H-signature-on-G-surface-clean-kimi-evas-2026-04-28 \
  --generated-root generated-condition-H-signature-on-G-surface-clean-kimi-2026-04-28 \
  --timeout-s 180 \
  --workers 4 \
  --tasks adc_dac_ideal_4b_smoke adpll_ratio_hop_smoke bbpd nrz_prbs \
    adpll_timer_smoke cppll_timer adpll_lock_smoke \
    dwa_ptr_gen_no_overlap_smoke cppll_freq_step_reacquire_smoke \
    sar_adc_dac_weighted_8b_smoke
```

Result:

- `eligible=0/10`
- `rescued=0/10`
- `best_pass=3/10`, but those 3 are gold-harness replay effects, not H rescues.

Interpretation: the older H prototype is too narrow for this surface-clean
set. It is useful as evidence that H coverage must expand, but it is not the
right full end-to-end H runner for these remaining failures.

## Adaptive H-on-G Run

The main H run continued from G best artifacts using the adaptive repair loop,
with G's syntax-zero boundary preserved and contracts/skills disabled.

```bash
python3 runners/run_adaptive_repair.py \
  --model kimi-k2.5 \
  --task adc_dac_ideal_4b_smoke \
  --task adpll_ratio_hop_smoke \
  --task bbpd \
  --task nrz_prbs \
  --task adpll_timer_smoke \
  --task cppll_timer \
  --task adpll_lock_smoke \
  --task dwa_ptr_gen_no_overlap_smoke \
  --task cppll_freq_step_reacquire_smoke \
  --task sar_adc_dac_weighted_8b_smoke \
  --source-generated-dir generated-condition-G-syntax-zero-on-Ffail-kimi-2026-04-28 \
  --initial-result-root results/condition-G-syntax-zero-on-Ffail-kimi-evas-2026-04-28/best \
  --candidate-generated-dir generated-condition-G-syntax-zero-closure-v2-kimi-2026-04-28 \
  --candidate-result-root results/condition-G-syntax-zero-closure-v2-kimi-evas-2026-04-28/best \
  --candidate-generated-dir generated-condition-G-syntax-zero-closure-v3-kimi-2026-04-28 \
  --candidate-result-root results/condition-G-syntax-zero-closure-v3-kimi-evas-2026-04-28/best \
  --generated-root generated-condition-H-adaptive-on-G-surface-clean-kimi-2026-04-28-pat3 \
  --output-root results/condition-H-adaptive-on-G-surface-clean-kimi-evas-2026-04-28-pat3 \
  --repair-public-spec-mode spectre-strict-v3 \
  --syntax-zero-gate \
  --no-repair-skill \
  --disable-contract-diagnosis \
  --max-rounds 3 \
  --patience 3 \
  --timeout-s 180 \
  --quick-maxstep 1n \
  --max-tokens 8192 \
  --workers 3 \
  --env-file .env.table2
```

Result:

- EVAS PASS: `1/10`
- New H rescue over G: `bbpd`
- Remaining 9 tasks are still behavior failures.

| Task | G status | G metric | H status | H metric | Delta |
|---|---:|---|---:|---|---|
| `adc_dac_ideal_4b_smoke` | FAIL_SIM_CORRECTNESS | `unique_codes=1 vout_span=0.844 vin_span=0.719` | FAIL_SIM_CORRECTNESS | `unique_codes=1 vout_span=0.844 vin_span=0.719` | same |
| `adpll_ratio_hop_smoke` | FAIL_SIM_CORRECTNESS | `pre_window_not_enough_edges num=0 den=80` | FAIL_SIM_CORRECTNESS | `pre_window_not_enough_edges num=0 den=80` | same |
| `bbpd` | FAIL_SIM_CORRECTNESS | `data_edges=150 up_edges=0 down_edges=0 overlap_frac=0.0000` | PASS | `data_edges=150 up_edges=30 down_edges=15 overlap_frac=0.0000` | new PASS |
| `nrz_prbs` | FAIL_SIM_CORRECTNESS | `transitions=0 complement_err=0.0023 swing=0.500` | FAIL_SIM_CORRECTNESS | `transitions=0 complement_err=0.0023 swing=0.500` | same |
| `adpll_timer_smoke` | FAIL_SIM_CORRECTNESS | `late_edge_ratio=0.580 lock_time=nan vctrl_range_ok=False` | FAIL_SIM_CORRECTNESS | `late_edge_ratio=0.580 lock_time=nan vctrl_range_ok=False` | same |
| `cppll_timer` | FAIL_SIM_CORRECTNESS | `freq_ratio=0.5082 fb_jitter_frac=0.1784 lock_time=nan` | FAIL_SIM_CORRECTNESS | `freq_ratio=0.5082 fb_jitter_frac=0.1784 lock_time=nan` | same |
| `adpll_lock_smoke` | FAIL_SIM_CORRECTNESS | `late_edge_ratio=1.000 lock_time=nan vctrl_range_ok=True` | FAIL_SIM_CORRECTNESS | `late_edge_ratio=1.000 lock_time=nan vctrl_range_ok=True` | same |
| `dwa_ptr_gen_no_overlap_smoke` | FAIL_SIM_CORRECTNESS | `sampled_cycles=17 bad_ptr_rows=0 max_active_cells=0 overlap_count=0` | FAIL_SIM_CORRECTNESS | `sampled_cycles=17 bad_ptr_rows=0 max_active_cells=0 overlap_count=0` | same |
| `cppll_freq_step_reacquire_smoke` | FAIL_SIM_CORRECTNESS | `pre_lock_edges=0 disturb_lock_low_frac=1.000 post_lock_edges=0 late_freq_ratio=1.1000` | FAIL_SIM_CORRECTNESS | `pre_lock_edges=0 disturb_lock_low_frac=1.000 post_lock_edges=0 late_freq_ratio=1.1000` | same |
| `sar_adc_dac_weighted_8b_smoke` | FAIL_SIM_CORRECTNESS | `unique_codes=1 avg_abs_err=0.0000 vout_span=0.000` | FAIL_SIM_CORRECTNESS | `unique_codes=1 avg_abs_err=0.0000 vout_span=0.000` | same |

## Spectre Cross-Validation

The only new H PASS was materialized into:

- `behavioral-veriloga-eval/generated-condition-H-adaptive-on-G-surface-clean-kimi-2026-04-28-pat3-best/`

Strict Spectre validation:

```bash
python3 runners/spectre_validate_baseline.py \
  --model kimi-k2.5 \
  --generated-dir generated-condition-H-adaptive-on-G-surface-clean-kimi-2026-04-28-pat3-best \
  --evas-results-dir results/condition-H-adaptive-on-G-surface-clean-kimi-evas-2026-04-28-pat3/best \
  --output-dir results/condition-H-adaptive-on-G-surface-clean-kimi-spectre-bbpd-ci-2026-04-28 \
  --env ../coordination/status/2026-04-28_virtuoso_bridge_sui.env \
  --spectre-mode spectre \
  --save-policy contract \
  --timeout-s 300 \
  --task bbpd
```

Result:

- Spectre PASS: `1/1`
- EVAS/Spectre pass match: `1/1`

An earlier validation attempt with `--profile sui` failed with
`Spectre executable not found`; this was a bridge-profile issue, not a circuit
or H result. The accepted validation uses the same default `ci` profile as the
prior strict-v3 reruns.

## Interpretation

H is useful but currently narrow:

- It can repair a clean behavior failure when the EVAS metric maps directly to
  a local mechanism. `bbpd` is the clear example: `up_edges=0` and
  `down_edges=0` became finite pulse counts.
- It did not fix the system-level PLL/ADPLL cases, ADC/SAR stuck-code cases,
  DWA no-activity case, or NRZ stuck-output case.
- The main bottleneck is no longer syntax or artifacts. It is missing
  mechanism specificity: the prompt tells the model the symptom family, but not
  enough internal system relations to reliably rebuild the correct behavior.

## Next

Use this result as the boundary between H and I:

1. Keep `bbpd` as a validated H rescue.
2. Do not claim H broadly solves the remaining behavior failures.
3. Move the 9 remaining failures to I, where prompt-derived functional IR,
   contracts, and mechanism cards can express the missing internal relations.
4. Expand H only when a new reusable template family has a clear trigger,
   interface condition, invariants, and Spectre-validated rescue evidence.
