# Original 92 Task-Form Audit

日期：2026-04-29

本文档审查 `behavioral-veriloga-eval/tasks/` 下原始 92 个任务中是否存在“表面相似但实际任务形态不同”的情况，以及 benchmark-v2 的 4 个外部架构候选是否已有等价覆盖。

结论先行：原始 92 中没有发现完全相同的 prompt 级重复；但存在若干机制高度相近的任务簇。这些任务大多不是严格重复，而是同一电路机制在不同任务形态或不同失效模式下的覆盖。因此本文档不是删除清单，而是帮助解释 benchmark92 的结构。

## 与 4 个新增外部架构的覆盖关系

| benchmark-v2 候选 | 原始 92 中的相近任务 | 是否已有等价覆盖 | 判断 |
|---|---|---|---|
| `v2_ext_threshold_detector_000` | `comparator_smoke`, `above_threshold_startup_smoke`, `inverted_comparator_logic_bug` | 部分相近，但不等价 | 原 92 有比较器和 `above()` 事件语义，但没有一个干净的单输入阈值检测器任务。建议加入。 |
| `v2_ext_window_detector_000` | `comparator_hysteresis_smoke`, `cross_hysteresis_window_smoke` | 不等价 | 原 92 有迟滞窗口，但没有 below/inside/above 三输出窗口分类器。建议加入。 |
| `v2_ext_limiter_model_000` | ADC/DAC clipping、PLL bounded monitor 等局部钳位行为 | 不等价 | 原 92 的 clamp 多是某个系统内部约束，没有独立的 analog limiter 传输曲线任务。建议加入。 |
| `v2_ext_pulse_stretcher_000` | `clk_burst_gen_smoke`, PFD pulse tasks, timer/cross tasks | 部分相近，但不等价 | 原 92 有事件和脉冲，但没有“输入上升沿触发固定宽度输出脉冲并自动回落”的独立 pulse stretcher。建议加入。 |

## 原始 92 中的近重复簇

这些簇不一定需要删除，但说明 92 本身并不是完全按“每个功能一个任务”构造的。

| 簇 | 任务 | 重复程度 | 建议 |
|---|---|---|---|
| static analog-to-binary | `end-to-end/voltage/d2b_4bit_smoke`, `spec-to-va/voltage/adc-sar/d2b_4bit` | 高 | 同一功能在 end-to-end 与 spec-to-VA/DUT-only 两种任务形态下出现，建议保留并标注 task form。 |
| 10-bit SAR logic | `spec-to-va/voltage/adc-sar/sar_logic`, `spec-to-va/voltage/sar_logic_10b` | 高 | 都是 10-bit SAR logic，可作为规格清晰度/约束强弱对照；不建议直接删除。 |
| timer-based ADPLL | `end-to-end/voltage/adpll_lock_smoke`, `end-to-end/voltage/adpll_timer_smoke` | 中高 | 目标都为 ADPLL lock；前者允许 timer 或 `idtmod()`，后者明确要求 timer DCO，代表约束收紧。 |
| CPPLL timer | `end-to-end/voltage/cppll_tracking_smoke`, `spec-to-va/voltage/pll-clock/cppll_timer` | 中高 | 同一 CPPLL timer 机制，但一个是 end-to-end，一个是 spec-to-VA/DUT-only，适合保留为任务形态对照。 |
| PFD variants | `pfd_updn_smoke`, `pfd_deadzone_smoke`, `pfd_reset_race_smoke`, `swapped_pfd_outputs_bug` | 中 | 都围绕 PFD UP/DN，但分别测基础行为、deadzone、reset race、bugfix。不是严格重复；适合保留部分代表。 |
| Gray counter variants | `gray_counter_4b_smoke`, `gray_counter_one_bit_change_smoke` | 中 | 都测 4-bit Gray counter one-bit-change；接口和 reset polarity 有差异，可作为约束表达差异的对照。 |
| comparator variants | `comparator_smoke`, `comparator_hysteresis_smoke`, `cmp_delay_smoke`, `cmp_strongarm_smoke`, `comparator_offset_search_smoke`, `strongarm_reset_priority_bug`, `inverted_comparator_logic_bug` | 低到中 | 同属 comparator 族，但分别覆盖 hysteresis、delay、StrongArm、offset search、bugfix，不建议简单删除。 |
| sample-hold variants | `sample_hold_smoke`, `sample_hold_droop_smoke`, `sample_hold_aperture_tb`, `sample_hold_step_tb`, `wrong_edge_sample_hold_bug` | 低到中 | 同属 sample-hold，但分别覆盖基本保持、droop、aperture、testbench generation、bugfix。不是严格重复。 |

## 对 benchmark 扩展的建议

1. 第一批只加入 4 个外部架构代表任务：
   - `v2_ext_threshold_detector_000`
   - `v2_ext_window_detector_000`
   - `v2_ext_limiter_model_000`
   - `v2_ext_pulse_stretcher_000`
2. 不把同机制的端口改名版本加入主 benchmark；这些留在 benchmark-v2 做泛化测试。
3. 不建议为了“去重”直接删除近重复簇；更好的做法是在 meta 中补充 `core_function` 与 `task_form`，让它们作为矩阵覆盖的一部分存在。
4. 不建议为了“去重”直接删除 PFD/comparator/sample-hold 变体，因为它们覆盖的是不同失效模式。
