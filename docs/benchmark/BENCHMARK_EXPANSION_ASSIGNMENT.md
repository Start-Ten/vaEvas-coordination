# Benchmark Expansion Assignment

日期：2026-04-29

## 当前阶段目标

当前协作库分发给外部同学时，主任务不再是复盘历史闭环，而是：

`把 behavioral-veriloga-eval 中原始 92 个 benchmark 扩展成更大、更难、更能检验泛化能力的 Verilog-A benchmark。`

扩展来源有两条：

1. **原始 92 个 benchmark 的系统扰动**
   从已有任务出发，改变命名、参数、接口、描述方式、组合关系和负约束，生成同类型但不重复的新任务。
2. **公开资料/网络搜索得到的新 Verilog-A 架构**
   从公开 Verilog-A model、compact model、analog behavioral model、论文或开源项目中提炼可转成 EVAS-compatible Verilog-A 的行为任务，再叠加扰动。

最终目标不是堆数量，而是构建能回答这个问题的数据集：

`机制模板/RAG/闭环反馈到底是在记住原始 92，还是能迁移到同类新任务？`

## 存放位置

所有新任务先放在：

`behavioral-veriloga-eval/benchmark-v2/tasks/<new_task_id>/`

不要直接写入原始：

`behavioral-veriloga-eval/tasks/`

只有当新任务完成 gold、checker、EVAS 验证、Spectre 验证和人工审查后，才允许讨论是否提升为正式 benchmark。

## 每个新任务必须包含

每个 task 目录至少包含：

1. `prompt.md`
2. `gold/dut.va`
3. `gold/tb_ref.scs`
4. `checker.py`
5. `meta.json`

如果是 `tb-generation` 类型，可以把 DUT 作为给定文件，把 `gold/tb_ref.scs` 作为标准 testbench。

## meta.json 必填字段

```json
{
  "task_id": "v2_example_task",
  "source_type": "seed_92_perturbation | external_architecture",
  "source_seed": "original_92_task_id_or_url",
  "mechanism_family": "adc_dac | pfd | pll | dwa | sample_hold | divider | ...",
  "perturbation_axes": ["rename", "parameter", "keyword_removal"],
  "external_source_license": "MIT | BSD | paper-derived | unknown | not_applicable",
  "evas_compatible": true,
  "spectre_parity_required": true,
  "status": "draft | gold_ready | evas_pass | spectre_pass | reviewed_candidate",
  "review_notes": ""
}
```

## 路线 A：原始 92 的扰动扩展

### A1. 命名扰动

目的：验证系统能不能从功能角色识别端口，而不是死记名字。

例子：

1. `din` -> `dinp` / `input_level` / `sampled_quantity`
2. `ref_clk` -> `refclk` / `cadence` / `reference_event`
3. `vout` -> `held_level` / `reconstructed_level`

### A2. 参数扰动

目的：验证机制是否能绑定参数，而不是记固定数值。

可改：

1. 位宽：3/4/5/6/8 bit
2. 分频比：奇数/偶数/ratio hop
3. VDD、vref、offset、threshold
4. ramp time、dwell time、reset delay、pulse width
5. DWA window size、wrap count

### A3. 描述方式扰动

目的：验证从功能描述到机制的理解。

例子：

1. 不写 `ADC/DAC`，改写成“把连续输入映射成离散 decision code，并输出对应的 held reconstructed level”。
2. 不写 `DWA`，改写成“每次选择连续的一组 unit cell，并在边界处循环回绕”。
3. 不写 `PFD`，改写成“比较 reference event 和 feedback event 的先后，输出互斥 pulse，并在 reset window 后释放”。

### A4. 负约束扰动

目的：防止模型用常见但错误的模板糊过去。

例子：

1. binary DAC 明确不是 thermometer DAC。
2. binary counter 明确不是 Gray counter。
3. sample/hold 明确不是 continuous follower。
4. PFD 明确不是 XOR phase detector。
5. DWA 明确不是 random scramble。

### A5. 系统组合扰动

目的：让任务不再只是局部模块，而是检查模块之间的约束。

例子：

1. ADC decision code + DAC reconstruction 共享同一个采样状态。
2. PFD + reset race + lock detector。
3. divider + PFD + feedback ratio hop。
4. DWA pointer + segmented DAC glitch guard。
5. sample/hold + comparator/calibration settled flag。

## 路线 B：公开资料/网络搜索扩展

协作者可以搜索公开 Verilog-A model、compact model、analog behavioral model、论文模型或开源 SPICE/AMS model。注意：我们的 benchmark 不是直接收集器件模型，而是把其中可执行、可检查、可扰动的行为机制转成小型 Verilog-A 任务。

### 推荐搜索入口

可从这些公开入口开始找候选机制：

1. OpenVAF examples：`https://openvaf.github.io/docs/getting-started/examples`
2. VA-Models：`https://github.com/dwarning/VA-Models`
3. ngspice OSDI/OpenVAF page：`https://ngspice.sourceforge.io/osdi.html`
4. Si2 Compact Model Coalition：`https://si2.org/compact-model-coalition/`
5. CMC Verilog-A coding guidelines：`https://si2.org/cmc-releases-coding-standard-guidelines-for-verilog-a-model-code/`

这些来源适合作为架构灵感和语法/建模风格参考；是否能直接使用代码取决于许可证和任务设计审查。

### 外部来源筛选标准

一个外部候选机制必须满足：

1. 能被压缩成小型行为任务，而不是完整 PDK/器件模型。
2. 能写出明确 checker，不依赖人工看图。
3. 能在 EVAS 支持的 voltage-domain 子集里表达。
4. 能用 Spectre 交叉验证。
5. 来源和许可证记录清楚。
6. 不要求 proprietary model、foundry PDK 或不可公开参数。

### 优先转化的外部机制

优先选择这些能转成 benchmark 的机制：

1. comparator / hysteresis / offset search
2. sample-hold / aperture / droop
3. oscillator / timer-based VCO / divider
4. DAC / ADC / calibration / thermometer-vs-binary coding
5. PFD / charge pump abstraction / lock detector
6. behavioral sensor / nonlinear transfer / threshold detector
7. simple memory or stateful switching model

暂不优先选择：

1. 大型 transistor compact model 全量移植；
2. 依赖 `ddt/idt/laplace/noise` 的模型；
3. 需要电流域 KCL 精确求解的模型；
4. 没有可自动 checker 的复杂模拟曲线拟合任务。

## 任务验收标准

每个新 benchmark 必须过四道门：

1. **Prompt 审查**
   不泄漏 gold 实现，不直接给代码答案；能清楚说明端口、行为和输出文件。
2. **Gold 审查**
   `gold/dut.va` 和 `gold/tb_ref.scs` 能运行，不依赖本地绝对路径。
3. **EVAS 验证**
   EVAS compile + simulate + checker PASS。
4. **Spectre 验证**
   Spectre run + checker PASS；如果 EVAS/Spectre 不一致，要先分类并回修 EVAS 或 checker。

通过后，`meta.json` 的 `status` 才能从 `draft` 提升到 `reviewed_candidate`。

## 分工建议

每位协作者一次认领一个机制 family，不要随机散做。

建议最小交付包：

1. 从原始 92 中选 2 个 seed task。
2. 每个 seed 做 3 个扰动任务。
3. 从公开资料找 1 个新机制，转成 2 个任务。
4. 合计 8 个新任务。
5. 至少 6 个完成 EVAS PASS。
6. 至少 4 个完成 Spectre PASS。
7. 写一个 `EXPANSION_REPORT.md`，说明哪些扰动有效、哪些失败、失败是否来自 prompt/gold/checker/EVAS/Spectre。

## EXPANSION_REPORT.md 模板

```markdown
# Benchmark Expansion Report

## Contributor

name:
date:

## Summary

- seed_92 perturbation tasks:
- external architecture tasks:
- EVAS PASS:
- Spectre PASS:

## Tasks

| task_id | source_type | source_seed/url | perturbation_axes | EVAS | Spectre | notes |
|---|---|---|---|---|---|---|

## Lessons

1.
2.
3.

## Promotion Recommendation

- promote now:
- needs repair:
- reject:
```

## 当前最重要的判断

这个阶段最重要的不是证明某个模型又多 pass 了几个，而是建立一个更有说服力的数据集：

1. 原始 92 的闭集 completion 说明机制模板有 teacher value。
2. benchmark-v2 扰动任务说明这些机制能否迁移。
3. 外部架构转化任务说明 vaEvas 是否能扩展到更真实、更广泛的 analog behavioral modeling 场景。
