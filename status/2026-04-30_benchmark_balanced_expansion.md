# Benchmark Balanced Expansion

日期：2026-04-30

## 目的

本轮不是清理原始 92，也不是把 benchmark-v2 的扰动任务直接并入主集，而是建立一个更清楚的完整 split：

`核心电路功能 × 任务形态`

这样可以回答一个关键问题：同一个电路功能是否应该只出现一次？当前结论是“不应该”。同一功能在 end-to-end、DUT-only/spec-to-VA、testbench generation、bugfix 四种任务形态下考察的是不同能力。

## 位置

完整 split：

```text
behavioral-veriloga-eval/benchmark-balanced/
```

原始 92 没有被改动。

## 当前内容

当前 `benchmark-balanced` 共 143 个任务：

| source collection | count |
|---|---:|
| original92 | 92 |
| original92_taskform_completion_v1 | 35 |
| balanced_supplement_v1 | 16 |
| total | 143 |

任务形态分布：

| task form | count |
|---|---:|
| end-to-end | 62 |
| DUT-only/spec-to-VA | 33 |
| tb-generation | 23 |
| bugfix | 25 |

原始 92 的处理方式：

- 完整复制到 `benchmark-balanced/tasks/original92_*`；
- 不修改原始 `behavioral-veriloga-eval/tasks/`；
- 保留原始 `family/category/scoring/gold/prompt/checks`；
- 在复制后的 `meta.json` 中新增 `benchmark_split`、`source_collection`、`source_task_id`、`core_function`、`task_form`；
- 为复制任务补了 `checker.py` wrapper，使其后续可以调用原始 EVAS 行为 checker。

原始 92 核心功能补格：

- 先用原始 `category` 作为第一版 `core_function` 口径；
- 原始 92 共涉及 18 个核心功能族；
- 其中只有 `digital-logic` 已经四种任务形态都有；
- 本轮新增 35 个 `completion92_*` 任务，补齐其余缺失格子；
- 补齐后，原始 92 涉及的 18 个核心功能族都至少覆盖四种任务形态；
- 每个 completion 任务保留 `source_task_id`，说明它是由哪个原始任务派生出来的。

新增外部 balanced supplement：

4 个核心功能：

1. threshold detector
2. window detector
3. analog limiter
4. event pulse stretcher

4 种任务形态：

1. end-to-end
2. DUT-only/spec-to-VA
3. tb-generation
4. bugfix

共 16 个新增任务：

| core function | task forms |
|---|---|
| threshold detector | e2e, dut, tb, bugfix |
| window detector | e2e, dut, tb, bugfix |
| analog limiter | e2e, dut, tb, bugfix |
| event pulse stretcher | e2e, dut, tb, bugfix |

每个任务包含 `prompt.md`、gold Verilog-A、gold testbench、checker、checks 和 meta。

## 验证结果

| backend | result | output |
|---|---:|---|
| EVAS, supplement 16 | 16/16 PASS | `behavioral-veriloga-eval/results/benchmark-balanced-supplement-gold-evas-2026-04-30-r2/` |
| real Spectre, supplement 16 | 16/16 PASS | `behavioral-veriloga-eval/results/benchmark-balanced-supplement-gold-spectre-2026-04-30-r2/` |
| EVAS, completion smoke 4 | 4/4 PASS | `behavioral-veriloga-eval/results/benchmark-balanced-completion-smoke-evas-2026-04-30-r1/` |
| real Spectre, completion smoke 4 | 4/4 PASS | `behavioral-veriloga-eval/results/benchmark-balanced-completion-smoke-spectre-2026-04-30-r1/` |

说明：原始 92 是导入并补充结构化 metadata；35 个 completion 是结构性补格任务，已经做了 4 个跨形态 smoke 验证。本轮没有声称重新完成 full143 的 EVAS/Spectre 双后端验收。一次 full108/full143 风格的 EVAS 尝试在长尾事件精度任务上耗时较长，后续应单独拆成批处理验证。

## 复现命令

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval

python3 runners/materialize_benchmark_balanced_tasks.py

python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-balanced \
  --family benchmark-balanced \
  --backend evas \
  --output-dir results/benchmark-balanced-supplement-gold-evas-2026-04-30-r2 \
  --timeout-s 180 \
  --task balanced_threshold_detector_e2e \
  --task balanced_threshold_detector_dut \
  --task balanced_threshold_detector_tb \
  --task balanced_threshold_detector_bugfix \
  --task balanced_window_detector_e2e \
  --task balanced_window_detector_dut \
  --task balanced_window_detector_tb \
  --task balanced_window_detector_bugfix \
  --task balanced_analog_limiter_e2e \
  --task balanced_analog_limiter_dut \
  --task balanced_analog_limiter_tb \
  --task balanced_analog_limiter_bugfix \
  --task balanced_pulse_stretcher_e2e \
  --task balanced_pulse_stretcher_dut \
  --task balanced_pulse_stretcher_tb \
  --task balanced_pulse_stretcher_bugfix

python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-balanced \
  --family benchmark-balanced \
  --backend spectre \
  --output-dir results/benchmark-balanced-supplement-gold-spectre-2026-04-30-r2 \
  --timeout-s 180 \
  --spectre-mode spectre \
  --task balanced_threshold_detector_e2e \
  --task balanced_threshold_detector_dut \
  --task balanced_threshold_detector_tb \
  --task balanced_threshold_detector_bugfix \
  --task balanced_window_detector_e2e \
  --task balanced_window_detector_dut \
  --task balanced_window_detector_tb \
  --task balanced_window_detector_bugfix \
  --task balanced_analog_limiter_e2e \
  --task balanced_analog_limiter_dut \
  --task balanced_analog_limiter_tb \
  --task balanced_analog_limiter_bugfix \
  --task balanced_pulse_stretcher_e2e \
  --task balanced_pulse_stretcher_dut \
  --task balanced_pulse_stretcher_tb \
  --task balanced_pulse_stretcher_bugfix
```

## 当前结论

这个 split 已建立为 `benchmark-balanced` 的第一版。它的价值是把原始 92 纳入结构化矩阵，并补齐“原始 92 核心功能 × 四种任务形态”的缺失格子，同时用 16 个新增外部任务提供一组干净的核心功能 × 任务形态样板，而不是制造大量近似扰动。

注意：它仍然不等于“原始 92 的替代品”。更准确的使用方式是：

- 原始 92：保留为 legacy/main benchmark；
- benchmark-balanced：作为结构化任务形态覆盖 benchmark；
- benchmark-v2/v3：作为端口改名、参数扰动、语义改写等泛化压力测试。

下一步更适合做两件事：

1. 对 35 个 `completion92_*` 和 16 个外部 balanced supplement 分批跑 A/D/F/G/I，观察不同任务形态下闭环是否稳定；
2. 在 benchmark-v2/v3 中继续做端口改名、参数扰动、语义改写，验证 RAG/skill 是否真能泛化。
