# Benchmark92 Task-Form Optimization

日期：2026-04-30

## 核心观点

原始 92 不应该按“同一电路家族是否重复”来简单删减。更合理的分析方式是：

`核心电路功能 × 任务形态`

同一个电路功能可以同时出现在不同任务形态中，因为它们考察的是不同能力。例如 `d2b_4bit` 同时有 end-to-end 和 spec-to-VA 版本，并不是坏事；前者考 DUT+testbench 的完整闭环，后者考固定接口下的 DUT 实现。

## 当前 92 的任务形态分布

当前目录结构对应 4 个实际任务形态：

| task form | count | 当前含义 |
|---|---:|---|
| `end-to-end` | 55 | 同时生成 DUT 与 testbench，最终跑完整仿真 |
| `spec-to-va` | 18 | 从规格生成 Verilog-A DUT，评测器使用固定 harness |
| `tb-generation` | 11 | 给定 DUT，生成能暴露目标行为的 testbench |
| `bugfix` | 8 | 给定有缺陷的 Verilog-A，修复语法/接口/行为 bug |
| total | 92 |  |

这说明 benchmark92 目前明显偏向 `end-to-end`，而 `bugfix`、`tb-generation`、部分 DUT-only/spec-to-VA 覆盖偏少。

如果后续要把用户提到的 `DUT` 与 `spec-to-va` 分开，可以在 meta 中新增 `task_form`：

- `dut-only`: 接口和评测 harness 明确，主要考行为实现；
- `spec-to-va`: 输入规格更自然、更系统，主要考规格到模型的翻译。

目前仓库目录里二者大多都落在 `spec-to-va` 下，因此本轮先不重排目录，只在文档层建立分析框架。

## 功能 × 任务形态覆盖矩阵

下表按当前 `meta.json` 的 `category` 聚合。它不是最终命名体系，但足够暴露失衡点。

| core function/category | end-to-end | spec-to-va | tb-generation | bugfix | total |
|---|---:|---:|---:|---:|---:|
| digital-logic | 13 | 3 | 1 | 2 | 19 |
| comparator | 6 | 0 | 1 | 3 | 10 |
| data-converter | 6 | 0 | 2 | 0 | 8 |
| pll-clock | 4 | 4 | 0 | 0 | 8 |
| adc-sar | 1 | 5 | 0 | 1 | 7 |
| phase-detector | 5 | 0 | 1 | 1 | 7 |
| stimulus | 7 | 0 | 0 | 0 | 7 |
| sample-hold | 2 | 0 | 1 | 1 | 4 |
| calibration | 2 | 1 | 0 | 0 | 3 |
| measurement | 2 | 0 | 1 | 0 | 3 |
| signal-source | 1 | 2 | 0 | 0 | 3 |
| dac | 0 | 2 | 1 | 0 | 3 |
| pll-closed-loop | 2 | 0 | 0 | 0 | 2 |
| analog-events | 2 | 0 | 0 | 0 | 2 |
| pll | 1 | 0 | 1 | 0 | 2 |
| comms | 1 | 0 | 1 | 0 | 2 |
| amplifier-filter | 0 | 1 | 0 | 0 | 1 |
| testbench | 0 | 0 | 1 | 0 | 1 |

## 如何重新理解“近重复”

从这个角度看，之前标出的近重复并不一定要删：

| pair/group | 表面相似 | 更合理解释 |
|---|---|---|
| `d2b_4bit_smoke` vs `adc-sar/d2b_4bit` | 都是 4-bit analog-to-binary | 同一功能在 end-to-end 与 spec-to-VA/DUT-only 两种形态下出现 |
| `sar_logic` vs `sar_logic_10b` | 都是 10-bit SAR logic | 高度相近，但可以作为规格清晰度/接口约束强弱的对照 |
| `adpll_lock_smoke` vs `adpll_timer_smoke` | 都是 ADPLL lock | 一个允许 timer/idtmod，另一个限定 timer DCO，考约束收紧 |
| `cppll_tracking_smoke` vs `pll-clock/cppll_timer` | 都是 CPPLL timer | 一个 end-to-end，一个 spec-to-VA/DUT-only |
| PFD variants | 都是 `pfd_updn` | 分别测基础 UP/DN、deadzone、reset race、swapped output bug |
| comparator variants | 都是 comparator | 分别测基础比较、迟滞、延迟、StrongArm、offset search、bugfix |
| sample-hold variants | 都是 sample-hold | 分别测基本保持、droop、aperture testbench、wrong-edge bug |

因此优化目标不是删除这些任务，而是让 benchmark 结构更明确：同一核心功能可以覆盖多个任务形态，但每个形态需要有清楚理由。

## 当前最明显的空缺

从功能覆盖看，以下 4 个 benchmark-v2 外部架构候选值得加入主 benchmark：

| new core function | candidate task | 当前 92 是否等价覆盖 | 加入价值 |
|---|---|---|---|
| threshold detector | `v2_ext_threshold_detector_000` | 否；只有 comparator/above 近似任务 | 补单输入阈值决策功能 |
| window detector | `v2_ext_window_detector_000` | 否；有迟滞但没有 below/inside/above 三输出分类 | 补多输出互斥窗口分类 |
| analog limiter | `v2_ext_limiter_model_000` | 否；只有系统内部 clamp | 补独立模拟限幅传输曲线 |
| event pulse stretcher | `v2_ext_pulse_stretcher_000` | 否；有 PFD/clock pulse，但没有独立固定宽度 pulse stretcher | 补边沿触发、保持窗口、自动回落 |

这些任务先作为 `end-to-end` 代表加入即可。同机制的端口改名版本、参数扰动版本继续留在 benchmark-v2 做泛化压力测试。

## 优化方案

### 阶段 1：结构化记录，不删除

1. 给原始 92 建立功能矩阵；
2. 不删除近重复任务；
3. 把近重复解释为同一功能在不同任务形态或不同失效模式下的覆盖；
4. 在论文/文档中避免说“重复”，改说“task-form coverage”。

### 阶段 2：加入 4 个功能代表任务

把 4 个外部架构任务作为候选加入 expanded official benchmark：

1. `v2_ext_threshold_detector_000`
2. `v2_ext_window_detector_000`
3. `v2_ext_limiter_model_000`
4. `v2_ext_pulse_stretcher_000`

注意：这会形成 `benchmark92+4` 或 `benchmark96`，不应再称为原始 92。

### 阶段 3：按矩阵补空格

后续新增任务不再盲目扩数量，而是优先补空格：

| core function | 优先补的任务形态 |
|---|---|
| threshold detector | spec-to-VA/DUT-only, bugfix |
| window detector | spec-to-VA/DUT-only, bugfix |
| analog limiter | spec-to-VA/DUT-only, bugfix |
| event pulse stretcher | spec-to-VA/DUT-only, bugfix |
| phase-detector | spec-to-VA/DUT-only |
| sample-hold | spec-to-VA/DUT-only |
| data-converter | bugfix |
| pll-clock | tb-generation, bugfix |

### 阶段 4：更新 meta，而不是移动目录

建议后续给每个任务的 `meta.json` 增加两个字段：

```json
{
  "core_function": "pfd",
  "task_form": "end-to-end"
}
```

这样不用重排目录，也能清楚表达 benchmark 结构。

## 当前建议

1. 先把 4 个外部架构代表任务作为 promotion candidates 保留，等待人工审核；
2. 不对原始 92 做删除或合并；
3. 后续如果要发布 expanded benchmark，用 `benchmark96` 或 `benchmark92+4` 命名；
4. benchmark-v2 继续承担泛化扰动测试，不进入精简主 benchmark。

## 2026-04-30 已落地扩展：benchmark-balanced

按照上面的矩阵思路，当前已经在 `behavioral-veriloga-eval/benchmark-balanced/` 新建了一个独立 benchmark split，不修改原始 92。

这个 split 的目标不是替代原始 92，而是把原始 92 放进统一的结构化矩阵里，同时补充一组干净的“同一个核心功能覆盖多种任务形态”的样板。

当前 `benchmark-balanced` 共 143 个任务：

| source collection | count |
|---|---:|
| imported original92 | 92 |
| original92 task-form completion v1 | 35 |
| balanced supplement v1 | 16 |
| total | 143 |

任务形态分布：

| task form | count |
|---|---:|
| end-to-end | 62 |
| DUT-only/spec-to-VA | 33 |
| tb-generation | 23 |
| bugfix | 25 |

其中 35 个 `completion92_*` 任务用于补齐原始 92 本身的核心功能矩阵：

- 使用原始 `category` 作为第一版 `core_function` 标签；
- 原始 92 共涉及 18 个核心功能族；
- 原始矩阵共有 35 个缺失单元；
- 补齐后，这 18 个核心功能族都至少覆盖四种任务形态；
- 每个 completion 任务记录 `source_task_id`，避免来源不透明。

其中新增 supplement 选了 4 个核心功能，每个核心功能各生成 4 种任务形态：

| core function | end-to-end | DUT-only/spec-to-VA | tb-generation | bugfix |
|---|---:|---:|---:|---:|
| threshold detector | 1 | 1 | 1 | 1 |
| window detector | 1 | 1 | 1 | 1 |
| analog limiter | 1 | 1 | 1 | 1 |
| event pulse stretcher | 1 | 1 | 1 | 1 |
| total | 4 | 4 | 4 | 4 |

对应新增任务数是 16 个。每个新增任务都包含：

- `prompt.md`
- `gold/dut.va`
- `gold/tb_ref.scs`
- `checker.py`
- `checks.yaml`
- `meta.json`

新增 supplement 的验证结果：

| backend | result |
|---|---:|
| EVAS gold validation | 16/16 PASS |
| real Spectre gold validation | 16/16 PASS |

completion 任务 smoke 验证：

| backend | result |
|---|---:|
| EVAS completion smoke | 4/4 PASS |
| real Spectre completion smoke | 4/4 PASS |

原始 92 在 `benchmark-balanced` 中的处理方式是导入并补齐 metadata：

- `task_id` 统一加 `original92_` 前缀，避免和新增任务冲突；
- `source_task_id` 保留原始任务名；
- `family` 保留原始值，用于兼容现有 scorer；
- 新增 `benchmark_split`、`source_collection`、`core_function`、`task_form`；
- 补了 `checker.py` wrapper，后续可调用原始 EVAS 行为 checker。

复现命令：

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

这一步的结论是：benchmark 完善应优先补“核心功能 × 任务形态”的空格，而不是简单叠加端口改名或参数扰动。当前 `benchmark-balanced` 已经把原始 92 的 18 个核心功能族补齐到四种任务形态；扰动任务仍然适合放在 benchmark-v2/v3 中，用来验证 RAG/skill/闭环方法的泛化能力。

因此当前 benchmark 体系建议表述为：

| split | role |
|---|---|
| original 92 | legacy/main benchmark |
| benchmark-balanced | structured task-form coverage benchmark |
| benchmark-v2/v3 | perturbation/generalization stress benchmark |
