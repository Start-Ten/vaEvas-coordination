# Benchmark Expansion Plan

日期：2026-04-29

## 当前阶段定位

之前的 benchmark expansion 文档还停留在早期 46-task 阶段。现在项目已经进入新的阶段：

`以原始 92 个 benchmark 为 seed，构建更大的 perturbation + external architecture benchmark。`

执行细则以 [BENCHMARK_EXPANSION_ASSIGNMENT.md](BENCHMARK_EXPANSION_ASSIGNMENT.md) 为准。

## 为什么要扩展

原始 92 个任务太少，且已经被我们用于大量闭环调试、teacher replay、completion package 和 RAG 机制沉淀。

因此它适合回答：

1. EVAS 闭环能不能降低验证成本？
2. teacher/template 能不能完成闭集任务？
3. 哪些失败属于电路行为，哪些属于 checker/runner/infra？

但它不够回答：

1. 这些机制是否真正泛化？
2. RAG 是不是只记住了 task_id 或固定信号名？
3. 换参数、换接口、换描述后还能不能 pass？
4. 从公开 Verilog-A/analog behavioral model 中抽取的新架构能不能被纳入同一验证流程？

benchmark-v2 的任务就是补上这部分证据。

## 两条扩展路线

### 路线 A：92 seed perturbation

从原始 92 出发，做：

1. 命名扰动；
2. 参数扰动；
3. 接口顺序扰动；
4. 描述方式扰动；
5. 负约束扰动；
6. 系统组合扰动。

任务应先放入：

`behavioral-veriloga-eval/benchmark-v2/tasks/`

### 路线 B：external architecture intake

从公开资料中寻找能转成 Verilog-A benchmark 的机制，例如：

1. comparator / hysteresis / offset search；
2. sample-hold / aperture / droop；
3. oscillator / timer-based VCO / divider；
4. DAC / ADC / calibration；
5. PFD / lock detector；
6. nonlinear sensor / threshold detector；
7. simple stateful switching model。

外部来源必须记录 URL、许可证、转化方式和是否可公开。

## 验收标准

一个新任务只有满足以下条件，才算 benchmark candidate：

1. 有 `prompt.md`；
2. 有 `gold/dut.va`；
3. 有 `gold/tb_ref.scs`；
4. 有 `checker.py`；
5. 有 `meta.json`；
6. EVAS PASS；
7. Spectre PASS；
8. 没有 gold 泄漏；
9. 失败模式可自动分类。

## 近期目标

第一阶段目标不是直接扩到几百个，而是先做一批高质量样本：

| batch | source | target |
|---|---|---:|
| v2-seed-perturbation | 原始 92 扰动 | 60 |
| v2-external-architecture | 公开资料转化 | 20 |
| v2-hard-negative | 负约束/陷阱任务 | 20 |
| total |  | 100 |

每批都必须保留 EVAS/Spectre 验证摘要。

## 与论文关系

论文叙事应这样组织：

1. 原始 92：用于 A/D/F/G/I 和 closed-set completion。
2. benchmark-v2：用于证明机制模板/RAG/EVAS 闭环是否能迁移。
3. external architecture：用于说明 vaEvas 不只服务现有 92，而能支持持续构建 analog behavioral benchmark。
