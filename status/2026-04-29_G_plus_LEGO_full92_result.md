# G + LEGO Full92 Result

Date: 2026-04-29

## Purpose

Run `G + LEGO` under the same table-consistent full92 baseline used by the
current Kimi A/D/F/G results.

This condition keeps G unchanged:

1. D=43 round-0 baseline.
2. strict-v3 public Spectre/Verilog-A rules.
3. syntax-zero gate.
4. 3-round EVAS repair loop.
5. no old repair-skill cards.
6. no contract diagnosis.

The only added condition is:

```bash
VAEVAS_ENABLE_LEGO_SKILLS=1
VAEVAS_LEGO_SKILL_TOP_K=3
```

## Command

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval

VAEVAS_ENABLE_LEGO_SKILLS=1 \
VAEVAS_LEGO_SKILL_TOP_K=3 \
python3 runners/run_adaptive_repair.py \
  --model kimi-k2.5 \
  --all \
  --source-generated-dir generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun \
  --initial-result-root results/condition-D-strictv3-kimi-table43-for-Gcold-evas-2026-04-28 \
  --generated-root generated-condition-G-lego-coldstart-full92-table43R0-kimi-2026-04-29-r1 \
  --output-root results/condition-G-lego-coldstart-full92-table43R0-kimi-2026-04-29-r1-evas \
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

## EVAS Result

Result root:

- `behavioral-veriloga-eval/results/condition-G-lego-coldstart-full92-table43R0-kimi-2026-04-29-r1-evas`

Generated root:

- `behavioral-veriloga-eval/generated-condition-G-lego-coldstart-full92-table43R0-kimi-2026-04-29-r1`

EVAS aggregate:

| Condition | EVAS PASS | Notes |
|---|---:|---|
| D baseline | 43/92 | Same R0 as current G |
| G current | 65/92 | Current table row |
| G + LEGO | 63/92 | Same G loop plus LEGO skill injection |

G + LEGO status mix:

| Status | Count |
|---|---:|
| `PASS` | 63 |
| `FAIL_SIM_CORRECTNESS` | 28 |
| `FAIL_TB_COMPILE` | 1 |

## Movement Against Current G

G fail -> G + LEGO pass:

1. `bbpd`
2. `cdac_cal`
3. `dwa_ptr_gen_smoke`

G pass -> G + LEGO fail:

1. `bad_bus_output_loop`
2. `dwa_wraparound_smoke`
3. `multitone`
4. `transition_branch_target_smoke`
5. `xor_pd_smoke`

Net movement against current G: `-2 PASS`.

## Spectre Delta Validation

All 20 tasks that were D-fail and became G + LEGO EVAS PASS were validated in
plain `spectre` mode.

Spectre root:

- `behavioral-veriloga-eval/results/condition-G-lego-coldstart-full92-table43R0-kimi-spectre-dfail-to-pass20-2026-04-29-r1`

Result:

```text
Spectre Pass@1 = 20/20
EVAS/Spectre pass match = 20/20
```

The 20 validated D-fail -> G + LEGO PASS tasks are:

1. `adpll_lock_smoke`
2. `bbpd`
3. `cdac_cal`
4. `clk_div_smoke`
5. `cmp_delay_smoke`
6. `cmp_strongarm_smoke`
7. `comparator_smoke`
8. `d2b_4bit`
9. `d2b_4bit_smoke`
10. `dac_therm_16b_smoke`
11. `dwa_ptr_gen_smoke`
12. `flash_adc_3b_smoke`
13. `gain_extraction_smoke`
14. `gray_counter_4b_smoke`
15. `gray_counter_one_bit_change_smoke`
16. `not_gate_smoke`
17. `pipeline_stage`
18. `sample_hold_smoke`
19. `serializer_8b_smoke`
20. `strongarm_reset_priority_bug`

## Interpretation

This is a useful but not yet winning condition.

Positive evidence:

1. LEGO injection does not break the Spectre compatibility of its newly
   accepted artifacts: all 20 D-fail -> G + LEGO PASS artifacts also pass real
   Spectre.
2. It rescues three tasks that current G does not pass, including
   `dwa_ptr_gen_smoke`, the prior multi-output transition/DWA hard case.
3. It confirms that the mechanism skills are executable repair guidance, not
   just retrieval labels.

Negative evidence:

1. Unconditional LEGO injection regresses five tasks that current G already
   passed.
2. The current repair prompt likely gives too much mechanism guidance even when
   syntax-zero or simple G feedback is already sufficient.
3. LEGO should not replace G globally; it should be gated by retrieval
   confidence, failure type, and round phase.

## Next Recommendation

Do not publish `G + LEGO` as a replacement for G.

Use it as an ablation showing that LEGO skills can rescue specific behavior and
system-mechanism failures, then implement a gated policy:

1. Do not inject LEGO while the failure layer is pure compile/TB/runtime unless
   the LEGO skill is a syntax-compatible structural skeleton.
2. Inject LEGO only after the syntax-zero gate is clear or when EVAS notes map
   strongly to a mechanism skill.
3. Use a conflict guard: if the top skill is unrelated to the checker metric,
   suppress it.
4. For already-passing G-style local compile repairs, keep the prompt smaller.

The next condition should be `G + gated-LEGO`, not another unconditional
full92 run.
