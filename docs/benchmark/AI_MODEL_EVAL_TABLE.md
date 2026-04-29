# AI Model Evaluation Table

This file is the team-wide table for comparing different AI models on `vaEvas` tasks.

Use it when testing:

1. closed-source models
2. open-source models
3. prompt variants
4. model-plus-workflow combinations

This table is different from [BENCHMARK_RESULT_TABLE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md):

1. `BENCHMARK_RESULT_TABLE.md` tracks task and benchmark asset status
2. `AI_MODEL_EVAL_TABLE.md` tracks model performance across tasks

---

## Recommended Evaluation Logic

For each model run, keep the evaluation staged:

1. `compile layer`
   `dut_compile`, `tb_compile`
2. `execution layer`
   `tran_generated`
3. `behavior layer`
   `sim_correct`
4. `parity layer`
   optional for parity-sensitive tasks
5. `benchmark-output layer`
   whether the model output is reusable as a benchmark seed candidate

This is meant to align with the layered closure idea:

1. `L0` minimal executable loop
2. `L1` behavior validation
3. `L2` parity validation
4. `L3` benchmark landing

---

## Required Columns

Each row should try to fill:

1. `run_id`
2. `model_name`
3. `provider`
4. `prompt_style`
5. `task_name`
6. `task_category`
7. `task_path`
8. `dut_compile`
9. `tb_compile`
10. `tran_generated`
11. `sim_correct`
12. `parity_status`
13. `benchmark_seed_candidate`
14. `result_path`
15. `notes`

Optional but recommended:

1. `temperature`
2. `attempt_index`
3. `pass_at_1_bucket`
4. `evas_fb_hz`
5. `spectre_fb_hz`
6. `ppm_cross_delta`
7. `lock_time_delta_s`

---

## Table

| run_id | model_name | provider | prompt_style | task_name | task_category | task_path | dut_compile | tb_compile | tran_generated | sim_correct | parity_status | benchmark_seed_candidate | temperature | attempt_index | pass_at_1_bucket | evas_fb_hz | spectre_fb_hz | ppm_cross_delta | lock_time_delta_s | result_path | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `[TODO]` | `GPT-5.4` | `OpenAI` | `default` | `comparator_smoke` | `comparator` | `behavioral-veriloga-eval/tasks/end-to-end/voltage/comparator_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `N/A` | `[TODO]` | `[TODO]` | `1` | `[TODO]` | `N/A` | `N/A` | `N/A` | `N/A` | `[TODO]` | baseline closed-source run |
| `[TODO]` | `GPT-5.4` | `OpenAI` | `default` | `adpll_lock_smoke` | `pll-closed-loop` | `behavioral-veriloga-eval/tasks/end-to-end/voltage/adpll_lock_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `1` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | parity-sensitive task |
| `[TODO]` | `Claude-[TODO]` | `Anthropic` | `default` | `comparator_smoke` | `comparator` | `behavioral-veriloga-eval/tasks/end-to-end/voltage/comparator_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `N/A` | `[TODO]` | `[TODO]` | `1` | `[TODO]` | `N/A` | `N/A` | `N/A` | `N/A` | `[TODO]` | compare against OpenAI |
| `[TODO]` | `Claude-[TODO]` | `Anthropic` | `default` | `adpll_lock_smoke` | `pll-closed-loop` | `behavioral-veriloga-eval/tasks/end-to-end/voltage/adpll_lock_smoke` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `1` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | parity-sensitive task |
| `[TODO]` | `Qwen-[TODO]` | `Alibaba` | `default` | `adc_dac_ideal_4b` | `data-converter` | `behavioral-veriloga-eval/examples/data-converter/adc_dac_ideal_4b` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `single-sim` | `[TODO]` | `[TODO]` | `1` | `[TODO]` | `N/A` | `N/A` | `N/A` | `N/A` | `[TODO]` | mid-complexity example |
| `[TODO]` | `Llama-[TODO]` | `Meta` | `default` | `lfsr` | `digital-logic` | `behavioral-veriloga-eval/examples/digital-logic/lfsr` | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` | `single-sim` | `[TODO]` | `[TODO]` | `1` | `[TODO]` | `N/A` | `N/A` | `N/A` | `N/A` | `[TODO]` | open-source baseline |

---

## Full92 Aggregate Remote A-I Runs

For full benchmark A-I style runs, do not expand all 92 per-task rows here.
Use the remote result pack as the source of truth:

```text
coordination/remote-results/2026-04-27_multi-model-a-i/
```

Before copying any aggregate number into a paper table, check the result status
in [EXPERIMENT_RESULT_LEDGER.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/EXPERIMENT_RESULT_LEDGER.md).
The 2026-04-27 Kimi A/B/C current-regression rows are currently marked
`invalid-baseline` because their generated roots contain dry-run placeholder
artifacts.  The Kimi `I-cold-start v0=58/92` row is therefore provisional and
should not be used as an official cold-start result until A/B/C are rerun clean.

Aggregate rows currently planned:

| run_group | owner | model_name | provider | conditions | split | status | aggregate_result_path | notes |
|---|---|---|---|---|---|---|---|---|
| `remote-a-i-2026-04-27` | shenbufan | `MiniMax-M2.5` or account-current MiniMax | Bailian/MiniMax | P0 probe, then A-G; H/I only after review | full92 | planned | `coordination/remote-results/2026-04-27_multi-model-a-i/RESULT_MATRIX.md` | Smoke first because prior MiniMax route had credential/model availability uncertainty. |
| `remote-a-i-2026-04-27` | shenbufan | `doubao-<account-model>` | Volcengine | P0 adapter probe, then A-G if supported | full92 | planned | `coordination/remote-results/2026-04-27_multi-model-a-i/RESULT_MATRIX.md` | Current runner needs provider route confirmation before full92. |
| `remote-a-i-2026-04-27` | shenbufan | `qwen3-coder-plus` | Bailian/Qwen | A-C, optional D/F | full92 | backup planned | `coordination/remote-results/2026-04-27_multi-model-a-i/RESULT_MATRIX.md` | Stable secondary comparison if MiniMax/Volcengine blocks. |
| `remote-a-i-2026-04-27` | shenbufan | `qwen3.5-plus` | Bailian/Qwen | A-C, optional D/F | full92 | backup planned | `coordination/remote-results/2026-04-27_multi-model-a-i/RESULT_MATRIX.md` | Stable secondary comparison. |

Fill detailed per-condition numbers in the remote matrix first, then promote
paper-ready aggregate rows back into this file or the paper draft.

---

## Fill Rules

1. Use one row per `model x task x attempt`.
2. Use `pass` / `fail` / `N/A` where possible.
3. If parity is not run, fill parity columns with `N/A` and set `parity_status` to `single-sim` or `N/A`.
4. `benchmark_seed_candidate` means the generated output is strong enough to be considered for benchmark landing, not that it has already been merged.
5. Use `pass_at_1_bucket` to mark whether the row belongs to the counted first-attempt bucket for later paper statistics.

---

## Suggested Aggregate Metrics

These should be summarized after multiple rows are filled:

1. `dut_compile_rate`
2. `tb_compile_rate`
3. `tran_generation_rate`
4. `sim_correct_rate`
5. `parity_qualified_rate`
6. `benchmark_seed_candidate_rate`
7. deterministic `Pass@1`

---

## Suggested Comparison Slices

Useful slices for later analysis:

1. closed-source vs open-source
2. default prompt vs skill-guided prompt
3. simple tasks vs behavior-heavy tasks vs parity-heavy tasks
4. single-sim tasks vs dual-validation tasks

---

## Relationship To The Paper Draft

This table is intended to support later additions to:

1. [VAEVAS_OPENLLM_STYLE_DRAFT.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/paper/VAEVAS_OPENLLM_STYLE_DRAFT.md)
2. [PAPER_GAP_CHECKLIST.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/paper/PAPER_GAP_CHECKLIST.md)

It should eventually provide the raw data for:

1. model comparison tables
2. `Pass@1` summaries
3. failure analysis by model family
