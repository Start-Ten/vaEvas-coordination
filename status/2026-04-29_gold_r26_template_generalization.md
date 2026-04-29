# Gold/R26 机制模板泛化实验

日期：2026-04-29

## 目的

这轮实验不是 cold-start LLM 成绩，也不是把历史修好的 artifact 直接拿来计入主表。

它验证一个更具体的问题：历史 R26 全闭合里学到的修复，是否能沉淀成“类型级机制模板”。如果一个模板只对原始 task_id 有效，换一点参数就失败，那它更像过拟合；如果换参数后仍然通过 EVAS checker，就说明它至少具备可迁移的电路写法价值。

## 方法

新增脚本：

- `behavioral-veriloga-eval/runners/gold_r26_template_generalization.py`

输入来源：

- `behavioral-veriloga-eval/generated-r26-dwa-pfd-combined-admission-2026-04-27/kimi-k2.5`

实验流程：

1. 从 R26 已验证 artifact 中选出一类代表性电路写法。
2. 把它抽象成机制模板，而不是 task_id 专用补丁。
3. 改变关键参数或激励条件。
4. 用原任务 checker 做 EVAS 验证。
5. 输出模板数据集与逐个变体结果。

输出位置：

- `behavioral-veriloga-eval/results/gold-r26-template-generalization-2026-04-29/gold_r26_mechanism_templates.json`
- `behavioral-veriloga-eval/results/gold-r26-template-generalization-2026-04-29/summary.json`
- `behavioral-veriloga-eval/results/gold-r26-template-generalization-2026-04-29/summary.md`

## 当前结果

总计 4 类机制模板、14 个参数扰动变体，EVAS 结果为 14/14 PASS。

| 机制模板 | 来源任务 | 扰动数 | PASS |
|---|---|---:|---:|
| PLL feedback cadence / lock | `adpll_timer_smoke` | 4 | 4 |
| DWA rotating pointer window | `dwa_ptr_gen_smoke` | 4 | 4 |
| PFD mutual-exclusion pulse windows | `pfd_reset_race_smoke` | 3 | 3 |
| ADC/DAC quantize-reconstruct | `adc_dac_ideal_4b_smoke` | 3 | 3 |

## 解释

这个结果说明：R26 里的经验不全是“对某个 benchmark 的死修”。至少在这 4 类上，它能被写成比较干净的机制模板，并在改变参考周期、分频比、DWA 输入码、PFD 脉宽、ADC/DAC VDD 和 ramp 条件后继续通过。

这给 H/I 后续优化的启发是：I 不应该只是“看到失败 task_id 后套补丁”，而应该把 R26/gold 中的经验整理成类型级机制卡片。机制卡片需要写清楚：

- 适用的功能关系，比如 PLL 的 ref/fb cadence、DWA 的 modulo pointer、PFD 的 UP/DN 互斥窗口、ADC/DAC 的单调量化重构。
- 可调参数，比如周期、分频比、码字、脉宽、VDD、ramp 时间。
- 约束输出方式，比如多路输出不要把 `transition()` 放进条件分支，避免仿真器状态不一致。
- 验证指标，比如 edge ratio、lock time、unique codes、overlap fraction、vout span。

## 边界

这还不能说明 cold-start I 一定提升，因为这里没有重新让 LLM 从 prompt 生成代码。

它能说明的是：历史全修复有工程闭合价值，可以作为 teacher dataset 的候选来源。下一步应该把这些模板转成 H/I 可注入的机制卡片，然后做 prompt 参数扰动或近邻 benchmark 的 cold-start 测试，检验 LLM 是否真的学会类型写法。
