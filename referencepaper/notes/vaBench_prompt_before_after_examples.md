# vaBench Prompt 优化前后对比样例

日期：2026-05-22

目的：基于 VerilogEval v2 和 CVDP，把 vaBench prompt 优化落到可执行的前后对比。
本文件只给建议样例，不直接修改 release prompts。

参考原则：

- VerilogEval v2：把 task prompt 和 model runner wrapper 分开；用 `Question/Answer`、rules、
  output marker 解决模型输出格式和语言习惯问题。
- CVDP：把 task category、visible context、hidden evaluator boundary、behavioral match 写清楚；
  不把 reference solution 或 hidden harness 泄露给模型。
- vaEVAS：把电压域、EVAS/Spectre 兼容、save columns、transient testbench 约束单独维护为
  `vaBench_evas_rules.md`，由 runner wrapper 注入。

## 0. 公共优化：Prompt 本体与 Runner Wrapper 分离

### Before：当前常见写法

当前 release prompts 经常把任务说明、输出约束、少量语言规则都写在 `prompt.md` 里，例如：

```markdown
Return exactly the requested Verilog-A DUT artifact(s). Do not include
explanatory prose outside the source file contents.
```

这本身没有错，但它把两类事情混在一起：

1. benchmark public contract：任务是什么。
2. model invocation protocol：模型应该如何输出。

### After：建议改成两层

`forms/*/prompt.md` 保留 benchmark public contract：

```markdown
# Task: threshold_comparator_dut

Form: dut
Visible context: public task contract only
Target artifact: comparator.va
Hidden evaluator: deterministic checker with EVAS/Spectre validation

Implement a pure voltage-domain behavioral Verilog-A module named `comparator`.
...
```

baseline runner 外层再包 VerilogEval v2 风格 wrapper，并注入共享 EVAS rules：

```text
System:
You are a Verilog-A behavioral modeling engineer. Only write syntactically valid
Verilog-A and Spectre source artifacts.

Question:
<contents of forms/*/prompt.md>

EVAS rules:
<selected shared rules from vaBench_evas_rules.md>

Answer:
Return only the requested artifact contents.
```

### 为什么这样优化

VerilogEval v2 的一个关键经验是：`Question/Answer`、rules、`[BEGIN]/[DONE]` 属于生成流程，
不是 benchmark 数据本体。这样做的好处是：

- benchmark prompt 版本稳定，便于比较不同模型和不同 wrapper。
- runner 可以做 ablation，例如 no-rules / rules / ICL，而不改变 benchmark 本身。
- 避免把 prompt engineering 误写成 vaEVAS 的主贡献。

降低的失败类型：

- `artifact_missing`
- `veriloga_idiom_error`
- `module_interface_mismatch`
- 输出中混入解释文字或多余 markdown

## 1. DUT 样例：Threshold Comparator

当前文件：

`behavioral-veriloga-eval/benchmark-vabench-release-v1/tasks/vbr1_l1_threshold_comparator/forms/dut/prompt.md`

### Before：当前 prompt 摘要

```markdown
# Threshold comparator DUT

Write the Verilog-A DUT artifact(s) for `Threshold comparator`.

Reference artifact name(s): `comparator.va`.
Domain: pure voltage-domain behavioral Verilog-A.

## Module Contract

- Declaration: `comparator(vdd, vss, vinp, vinn, out_p)`

Ports:
- `vdd`, `vss`: electrical supply rails
- `vinp`, `vinn`: input electrical differential pair
- `out_p`: output electrical single-ended decision

## Behavioral Contract

- drive `out_p` high when `V(vinp) > V(vinn)` by a visible margin
- drive `out_p` low when `V(vinp) < V(vinn)` by a visible margin
- use rail-referenced output levels and finite `transition(...)` edges
```

### 问题

这个 prompt 已经不错，接口和 public observables 都清楚。但从 VerilogEval v2/CVDP 角度看，
它还可以更稳定：

1. “Write artifact(s)” 不如 “Implement a module named ...” 适合 instruction-tuned model。
2. 没显式写 `Form: dut`、visible context、hidden evaluator boundary。
3. “rail-referenced output levels” 对人清楚，但模型可能不稳定地理解为固定 0/1，而不是
   `V(vss)` / `V(vdd)`。
4. Verilog-A idiom rules 不应散落在每个 prompt，而应主要由 runner wrapper 注入。

### After：建议版 public prompt

````markdown
# Task: threshold_comparator_dut

Form: dut
Visible context: public task contract only
Target artifact: comparator.va
Hidden evaluator: deterministic waveform checker using the public observables below.
Domain: pure voltage-domain behavioral Verilog-A.

Implement a pure voltage-domain behavioral Verilog-A module named `comparator`.

## Interface Contract

Module declaration:

```verilog
module comparator(vdd, vss, vinp, vinn, out_p);
```

Ports, all `electrical`, exactly in this order:

- `vdd`: positive supply rail
- `vss`: reference supply rail
- `vinp`: positive input
- `vinn`: negative input
- `out_p`: single-ended voltage decision output

## Behavioral Contract

- Compare the differential input `V(vinp) - V(vinn)`.
- When the differential input is clearly positive, drive `out_p` toward `V(vdd)`.
- When the differential input is clearly negative, drive `out_p` toward `V(vss)`.
- Drive `out_p` with finite smoothed transitions.
- Do not introduce a clock, reset, hidden digital state, or current-domain behavior.

## Public Evaluation Observables

The companion validation testbench saves these waveform columns:

- `vinp`
- `vinn`
- `out_p`

## Output Contract

Return exactly one complete Verilog-A file named `comparator.va`.
Do not include explanatory prose outside the source file contents.
````

### 为什么这样优化

| 改动 | 来源 | 原因 |
| --- | --- | --- |
| 增加 `Form/Visible context/Hidden evaluator` | CVDP | 明确这是 DUT task，不是 TB 或 wrapper；也说明 checker 私有 |
| 用 “Implement a module named ...” 开头 | VerilogEval v2 spec-to-RTL | 更适合 chat/instruction 模型 |
| 把 rail behavior 写成 `V(vdd)` / `V(vss)` | CVDP behavioral match | 减少模型写固定 0/1 或不参考 supply rails |
| 明确不要 clock/reset/current-domain | VerilogEval v2 failure-driven rules | 防止模型把组合比较器写成时钟逻辑或电流贡献 |
| `artifact(s)` 改成 exact one file | VerilogEval output extraction | 减少多文件/解释文字/文件名错误 |

主要降低的失败类型：

- `module_interface_mismatch`
- `veriloga_idiom_error`
- `waveform_shape_error`
- `checker_behavior_gap`

## 2. TB 样例：Clocked Sample-and-Hold Testbench

当前文件：

`behavioral-veriloga-eval/benchmark-vabench-release-v1/tasks/vbr1_l1_clocked_sample_and_hold/forms/tb/prompt.md`

### Before：当前 prompt 摘要

```markdown
# Clocked sample-and-hold Testbench Companion

Write a Spectre transient testbench for the `Clocked sample-and-hold` behavioral
Verilog-A release task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the checker
- include or instantiate the Verilog-A behavioral module under test
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
```

### 问题

这是目前比较典型的弱点：对人来说知道要写 testbench，但对模型来说仍然太泛。

1. “public transient scenario” 没具体化，容易生成无效 stimulus。
2. “observable waveform or metric signals” 没列 exact save columns。
3. 没明确 `tb` 不是 checker generation。
4. 没明确 DUT file/module 和 instance port order。
5. CVDP 把 testbench stimulus 和 checker generation 拆成 `cid012/cid013`，我们这里应该更明确。

从 gold testbench 可见，该任务实际使用：

- `ahdl_include "sample_hold.va"`
- instance: `(vdd vss in clk out) sample_hold`
- transient: `tran tran stop=1u maxstep=2n`
- save: `in clk out`

### After：建议版 public prompt

```markdown
# Task: clocked_sample_and_hold_tb

Form: tb
Visible context: companion DUT artifact `sample_hold.va`
Target artifact: tb_sample_hold_ref.scs
Hidden evaluator: external waveform checker; this task does not ask you to generate the checker.
Domain: Spectre transient testbench for pure voltage-domain behavioral Verilog-A.

Write one EVAS/Spectre-compatible transient testbench for the `sample_hold` behavioral DUT.

## DUT/Testbench Interface

- Include the generated DUT file: `sample_hold.va`
- Instantiate module `sample_hold` with positional ports:
  - `vdd`, `vss`, `in`, `clk`, `out`
- Use voltage sources only; do not instantiate transistor-level devices.

## Public Stimulus Contract

- Provide a 0.9 V supply `vdd` and 0 V reference `vss`.
- Drive `clk` with multiple clean rising edges during the transient run.
- Drive `in` with a changing voltage waveform so that consecutive samples differ.
- Leave enough time after clock edges for `out` to settle before the checker observes it.

## Public Output/Save Contract

- Include a transient analysis.
- Save these exact scalar names:
  - `in`
  - `clk`
  - `out`
- Use plain scalar save names; do not rely on instance-qualified or aliased names.

## Non-Goals

- Do not generate hidden checker logic.
- Do not use AC/noise analysis, current-domain solver assumptions, or transistor-level devices.

## Output Contract

Return exactly one Spectre file named `tb_sample_hold_ref.scs`.
Do not include explanatory prose outside the source file contents.
```

### 为什么这样优化

| 改动 | 来源 | 原因 |
| --- | --- | --- |
| 明确 `Form: tb` 和 “not checker” | CVDP `cid012/cid013` | 防止模型生成 checker 或断言逻辑，而不是 Spectre wrapper |
| 列出 include、module、port order | VerilogEval interface contract | 降低 DUT 实例化错误 |
| 列 exact save columns | vaEVAS checker boundary + CVDP behavioral match | 防止 `missing_observable` |
| 写 stimulus shape | CVDP testbench stimulus generation | 防止无有效边沿、无不同输入、checker 窗口无意义 |
| “plain scalar save names” | vaEVAS EVAS/Spectre artifact经验 | 避免 instance-qualified save 导致 `tran.csv` 列名不匹配 |

主要降低的失败类型：

- `missing_observable`
- `tb_stimulus_insufficient`
- `module_interface_mismatch`
- `checker_behavior_gap`

## 3. Bugfix 样例：One-Shot Timer

当前文件：

`behavioral-veriloga-eval/benchmark-vabench-release-v1/tasks/vbr1_l1_one_shot_timer/forms/bugfix/prompt.md`

### Before：当前 prompt 摘要

```markdown
# Task: vbm1_one_shot_timer_bugfix

The provided voltage-domain one-shot timer has a reset-priority bug: a reset
asserted while the output pulse is active does not immediately clear the pulse.
Fix the design so reset has priority over the pending one-shot timeout.

The fixed module must be named `one_shot_timer` and use electrical ports
`trig`, `rst_n`, and `pulse`. While `rst_n` is low, `pulse` must remain low and
any pending timeout must be disarmed. When `rst_n` is high, each rising `trig`
crossing should start one pulse of the configured width. If reset falls during
that pulse, the pulse should clear promptly rather than waiting for the timer.
```

### 问题

这个 prompt 对模型很友好，但有一点接近“把 bug 根因和修复方向说出来”。

CVDP 的 bugfix 更像工程 debug：给 faulty context、intended behavior、observed mismatch，让模型
定位并修。VerilogEval 的 bug tasks 也是展示 faulty implementation，而不是直接给 patch。

当前 prompt 的风险：

1. “reset-priority bug” 和 “reset has priority over pending timeout” 已经接近修复策略。
2. 没有以 observed-vs-expected 表示失败现象。
3. 没明确 visible context 是 faulty DUT，hidden evaluator 会检查 buggy fail/fixed pass。

### After：建议版 public prompt

```markdown
# Task: one_shot_timer_bugfix

Form: bugfix
Visible context: faulty Verilog-A DUT `dut_buggy.va`
Target artifact: dut_fixed.va
Hidden evaluator: the provided faulty behavior must fail; the fixed artifact must pass the same public behavior contract.
Domain: pure voltage-domain behavioral Verilog-A.

The provided DUT is intended to implement a voltage-domain one-shot timer.
Repair the DUT while preserving the public interface and unrelated behavior.

## Interface Contract

The fixed module must be named `one_shot_timer`.
Ports, all `electrical`, exactly in this order:

- `trig`: trigger input
- `rst_n`: active-low reset input
- `pulse`: pulse output

## Intended Behavior

- While `rst_n` is low, `pulse` remains low and any pending output pulse is inactive.
- When `rst_n` is high, each rising crossing on `trig` starts one output pulse.
- The pulse should clear after the configured pulse width.
- A reset falling event during an active pulse should immediately return the observable output to the reset-low behavior.

## Observed Faulty Behavior

| Scenario | Expected behavior | Observed faulty behavior |
| --- | --- | --- |
| `rst_n` falls while `pulse` is active | `pulse` clears promptly and the pending pulse is disarmed | `pulse` remains high until the old timeout expires |

## Implementation Constraints

- Use voltage contributions and smoothed output transitions.
- Do not use current contributions, `ddt()`, or `idt()`.
- Preserve the module name, port order, and external behavior except for the repair.

## Output Contract

Return exactly one complete Verilog-A file named `dut_fixed.va`.
Do not include explanatory prose outside the source file contents.
```

### 为什么这样优化

| 改动 | 来源 | 原因 |
| --- | --- | --- |
| “reset-priority bug” 改成 observed mismatch | CVDP `cid016` | 更像真实 debug；降低直接泄露修复策略的风险 |
| 加 `Visible context: faulty DUT` | CVDP datapoint schema | 明确模型看到的是 faulty artifact，不是 hidden reference |
| 加 intended behavior + observed table | CVDP bugfix style | 让任务可理解但不过度给 patch |
| 写 “preserve unrelated behavior” | CVDP code modification/bugfix | 防止模型重写或改变非目标行为 |
| 保留 constraints | VerilogEval failure-driven rules | 仍减少 Verilog-A idiom 错误 |

主要降低的失败类型：

- `checker_behavior_gap`
- `initial_reset_error`
- `event_semantics_error`
- prompt leakage risk

## 4. E2E/L2 样例：Converter Front-End / Sample-Hold Droop

当前文件：

`behavioral-veriloga-eval/benchmark-vabench-release-v1/tasks/vbr1_l2_converter_front_end/forms/e2e/prompt.md`

### Before：当前 prompt 摘要

```markdown
Write a Verilog-A module named `sample_hold_droop_ref` and one minimal EVAS-compatible Spectre testbench.

# Task: sample_hold_droop_smoke

## Objective

Create a pure voltage-domain sample-and-hold model with observable hold droop. The testbench must
produce several sampling and hold windows so EVAS can measure droop behavior.

## DUT Contract

- Module name: `sample_hold_droop_ref`
- Ports, all `electrical`, exactly in this order: `vdd`, `vss`, `clk`, `vin`, `vout`
...

## Deliverables

Return exactly two fenced code blocks:

1. `sample_hold_droop_ref.va`
2. `tb_sample_hold_droop.scs`
```

### 问题

这个 prompt 已经接近我们想要的结构：DUT Contract、Testbench Contract、Public Evaluation
Contract 都有。但是它暴露了几个值得优化的点：

1. 这是 release entry `vbr1_l2_converter_front_end:e2e`，但 prompt 标题还是历史
   `sample_hold_droop_smoke`，缺少 release-level identity。
2. prompt deliverable 写 `tb_sample_hold_droop.scs`，而 release artifacts/gold 使用
   `tb_sample_hold_droop_ref.scs`。这是 consistency audit 应捕捉的问题。
3. L2/E2E 的 composition objective 可以更清楚：DUT behavior、TB stimulus、public handoff
   observables 应明确区分。
4. “Use final transient setting provided by injected Strict EVAS Validation Contract” 对 standalone
   release prompt 不够自洽；应直接列出 public transient setting。

### After：建议版 public prompt

````markdown
# Task: vbr1_l2_converter_front_end_e2e

Form: e2e
Level: L2
Visible context: public DUT/testbench contract only
Target artifacts:
1. sample_hold_droop_ref.va
2. tb_sample_hold_droop_ref.scs
Hidden evaluator: EVAS/Spectre-compatible waveform checker using the public columns below.
Domain: pure voltage-domain behavioral Verilog-A plus one Spectre transient testbench.

Implement an end-to-end converter-front-end slice: a clocked sample-and-hold behavioral model with finite hold droop,
plus a transient testbench that exercises multiple sample and hold windows.

## DUT Contract

- Module name: `sample_hold_droop_ref`
- Ports, all `electrical`, exactly in this order:
  - `vdd`
  - `vss`
  - `clk`
  - `vin`
  - `vout`
- Parameters:
  - `vth` real, default `0.45`
  - `tau` real, default `120n`
  - `dt` real, default `0.5n`
  - `trf` real, default `40p`

## DUT Behavioral Contract

- On each rising crossing of `clk`, sample `V(vin, vss)`.
- During hold intervals, keep the sampled output state while applying bounded droop toward `V(vss)`.
- Keep `vout` within the supply range.
- Use stable state variables and smoothed voltage contributions so the checker observes settled values after clock edges.

## Testbench Contract

- Provide a 0.9 V supply and 0 V reference.
- Drive `clk` with multiple rising edges within the final validation window.
- Drive `vin` through several distinct levels so consecutive held outputs differ.
- Instantiate the DUT by positional ports: `(vdd vss clk vin vout)`.
- Include the generated DUT file `sample_hold_droop_ref.va`.

## Public Evaluation Contract

Use this transient setting:

```spectre
tran tran stop=170n maxstep=0.1n
```

Save these exact scalar waveform names:

- `vin`
- `clk`
- `vout`

## Deliverables

Return exactly two fenced code blocks whose info strings are the exact file names:

1. `sample_hold_droop_ref.va`
2. `tb_sample_hold_droop_ref.scs`
````

### 为什么这样优化

| 改动 | 来源 | 原因 |
| --- | --- | --- |
| release-level task id + historical behavior name 分离 | CVDP category/datapoint identity | 避免历史 source task id 和 release row 混淆 |
| 修正 testbench artifact name | CVDP consistency score | prompt、manifest、gold artifact 必须一致 |
| DUT/Testbench/Public Evaluation 分开 | VerilogEval v2 + CVDP | 多文件任务边界更清楚，便于 extraction 和 audit |
| 写 public handoff observables | CVDP `cid005` composition | L2/E2E 的重点是组合行为和 observable handoff |
| 直接列 transient setting | VerilogEval self-contained prompt | prompt 不依赖外部“注入 contract”才能理解 |

主要降低的失败类型：

- `artifact_missing`
- `module_interface_mismatch`
- `missing_observable`
- `tb_stimulus_insufficient`
- `checker_behavior_gap`
- `consistency_score` 低分

## 5. 不应该做的优化

以下改动看似会提升模型通过率，但不建议放入 benchmark public prompt：

| 不建议动作 | 原因 |
| --- | --- |
| 把完整 Verilog-A idiom example 放入每个 prompt | 会变成 ICL，污染 benchmark prompt；应放 runner variant |
| 把 hidden checker 阈值和采样窗口全写出来 | 可能把 evaluator 变成可反向拟合答案 |
| 对 bugfix 直接描述 gold patch control flow | 降低 debug task 难度，像修复提示 |
| 为某个模型特化措辞 | baseline 不可比 |
| 大规模改 prompt 后沿用旧 baseline 结果 | prompt version 改变后必须重跑 |

## 6. 建议落地顺序

1. 先建立 runner wrapper 和共享 EVAS rules，而不是先批量改 prompt。
2. 选 12-task slice，按当前 prompt 跑或复用历史失败，分类 failure。
3. 对每个 prompt 做 CVDP 四项打分：
   - ambiguity
   - consistency
   - form/category match
   - behavioral match
4. 只改低分项：
   - filename/interface 不一致，优先修。
   - `tb` 缺 stimulus/save，补 public contract。
   - `bugfix` 太直给，改 observed-vs-expected。
   - `e2e/L2` 缺 composition boundary，补 public handoff observables。
5. 每个修改都记录：
   - 来源：VerilogEval v2 或 CVDP。
   - 目标 failure class。
   - leakage risk。
   - 是否需要重跑 EVAS/Spectre。
