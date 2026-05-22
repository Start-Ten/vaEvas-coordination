# vaBench EVAS Rules：Prompt/Wrapper 的 EVAS 适配层

日期：2026-05-22

目的：把 vaEVAS 独有的电压域、EVAS/Spectre 双验证、可观测列、transient testbench
约束单独管理。`EVAS rules` 不是 benchmark 题目答案，也不是 hidden checker；它是一组
runner 可注入的公共兼容性规则，用来减少无意义的语法、接口、仿真环境错误。

## 1. 三层边界

| 层 | 内容 | 是否写入 `forms/*/prompt.md` |
| --- | --- | --- |
| Public benchmark prompt | 任务目标、公开 interface、target artifacts、公开 behavior boundary | 是 |
| Runner wrapper | system role、`Question/Answer`、output markers、可选 ICL/repair feedback | 否 |
| EVAS rules | EVAS/Spectre 兼容的 Verilog-A/Spectre 写法、保存列、transient 约束 | 主要否；只有任务特定公开约束才写入 |

原则：如果规则是所有任务通用的语言/仿真护栏，放进 runner wrapper 引用的 `EVAS rules`。
如果规则是某个任务的公开可评测行为，例如 exact port list、save column names、stimulus
window，则写进该任务的 public prompt。

## 2. 推荐公共规则

### 2.1 Verilog-A voltage-domain subset

- Use `electrical` ports for all public analog ports.
- Model signals through voltage contributions such as `V(out) <+ ...`.
- Stay in the voltage-domain behavioral subset; do not introduce current-domain,
  KCL/KVL topology, transistor-level devices, AC/DC analysis, or unsupported analog operators.
- Use `analog begin ... end` for behavior.
- Do not use digital Verilog constructs such as `reg`, `wire`, `logic`, `always`, or `initial`.

### 2.2 Event/state behavior

- Use `@(initial_step)` for initialization when state is required.
- Use `@(cross(expr, direction))` for threshold edge events.
- Preserve explicit reset/enable priority when the public task specifies it.
- Use `transition(value, delay, trise, tfall)` for smoothed voltage outputs when switching behavior is required.

### 2.3 Spectre testbench compatibility

- Testbenches should be transient wrappers/stimulus/save artifacts, not hidden checkers.
- Save the exact public observable names required by the task.
- Prefer plain scalar save names that the evaluator can map consistently.
- Provide enough stimulus edges, levels, and settling windows for the external checker to evaluate behavior.
- Keep DUT include/instance/module names consistent with the public artifact contract.

### 2.4 Output and artifact boundary

- Return only requested source artifacts.
- Preserve exact file names, module names, port order, parameter names, and saved waveform names.
- For multi-file tasks, use runner-level file markers or fenced blocks; do not bake model-specific markers
  into the public benchmark prompt unless the evaluator contract requires them.

## 3. 不应放进 EVAS rules 的内容

| 不应放入 | 原因 |
| --- | --- |
| Hidden checker thresholds or private sampling assertions | 会泄露 evaluator |
| Gold implementation control flow | 会把 benchmark 变成答案复述 |
| 某个模型专用措辞 | baseline 不可比 |
| ICL/few-shot examples | ICL 是 post-mainline baseline variant，不是当前主线 |
| EVAS/Spectre mismatch 的修复结论 | mismatch 优先查 evaluator/parity，不靠 prompt 遮盖 |

## 4. 与 failure taxonomy 的关系

`EVAS rules` 主要处理这些失败：

- `veriloga_idiom_error`
- `spectre_syntax_error`
- `missing_observable`
- `tb_stimulus_insufficient`
- 部分 `module_interface_mismatch`

如果失败是 `checker_behavior_gap`，应审计 public prompt 与 checker/gold 是否一致。
如果失败是 `evas_spectre_mismatch`，应优先修 EVAS/Spectre parity，不应把问题转嫁给 prompt。

## 5. Runner 注入方式

推荐 wrapper 结构：

```text
System:
You are a Verilog-A behavioral modeling engineer. Only write EVAS/Spectre-compatible
voltage-domain behavioral Verilog-A and Spectre transient artifacts.

Question:
<contents of forms/*/prompt.md>

EVAS rules:
<shared EVAS rules selected for this form>

Answer:
Return only the requested artifact contents.
```

这样可以统一管理 EVAS 适配，同时保持 public benchmark prompt 稳定、可版本化、可比较。
