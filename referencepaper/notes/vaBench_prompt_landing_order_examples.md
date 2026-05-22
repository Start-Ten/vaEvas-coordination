# vaBench Prompt 修改落地顺序与前后对比例子

日期：2026-05-22

目的：说明哪些内容应该直接改 `forms/*/prompt.md`，哪些内容应该放到 runner wrapper
或 `vaBench_evas_rules.md`。本文件是修改方案示例，不直接修改 release prompts。

## 0. 总判断

public prompt 现在确实有问题，主要问题不是“缺少专家角色提示”，而是 benchmark contract
不够硬：form 边界、artifact 名、module/interface、public observables、stimulus/window、
composition objective 有些地方写得太泛或不一致。

修改原则：

| 内容 | 去哪里 |
| --- | --- |
| form、target artifact、module/interface、public behavior、public observables | 改 public prompt |
| checker 实际测了但 prompt 没公开的行为 | 改 public prompt 或修 checker |
| 电压域、EVAS/Spectre 兼容、通用 Verilog-A idiom、save scalar names | 放 `vaBench_evas_rules.md`，由 wrapper 注入 |
| `System/Question/Answer`、输出 marker、repair feedback、ICL | 放 runner wrapper |
| hidden checker 阈值、gold implementation control flow | 不写入 prompt/rules |

## 1. 落地顺序

1. **先定 public scaffold**：每个 prompt 至少包含 `Form / Target artifact / Visible context / Interface / Public behavior or stimulus / Public observables / Output contract`。
2. **建立 EVAS rules**：通用电压域和 EVAS/Spectre 兼容规则集中维护，不复制到每个 prompt。
3. **选 12-task slice 做 failure classification**：先判断失败属于 contract 缺失、EVAS 兼容、输出抽取、checker gap，还是 EVAS/Spectre parity。
4. **只改 public contract 缺失的 prompt**：例如 artifact 名不一致、observable 缺失、tb stimulus 太泛、bugfix 太直给。
5. **wrapper 只管模型调用协议**：baseline runner 注入 EVAS rules 和输出格式，不改变 benchmark prompt。
6. **改后重跑 changed slice**：prompt version 变化后，旧 baseline 不再直接可比。

## 2. 例子 A：TB prompt 太泛，应该直接改 public prompt

当前例子：

`vbr1_l1_clocked_sample_and_hold/forms/tb/prompt.md`

### Before 摘要

```markdown
Write a Spectre transient testbench for the `Clocked sample-and-hold` behavioral
Verilog-A release task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Reference testbench artifact names: `tb_sample_hold_ref.scs`.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the checker
- include or instantiate the Verilog-A behavioral module under test
```

### 问题

- `same behavioral DUT` 没写 module name 和 port order。
- `public transient scenario` 没写 stimulus shape。
- `public observables` 没列 exact save columns。
- checker 需要列名时，模型不知道该 save 什么。

对应 failure class：

- `missing_observable`
- `tb_stimulus_insufficient`
- `module_interface_mismatch`

### After 建议

```markdown
# Task: clocked_sample_and_hold_tb

Form: tb
Target artifact: `tb_sample_hold_ref.scs`
Visible context: public testbench contract only
Hidden evaluator: external deterministic checker; do not generate checker logic.

Write one Spectre transient testbench for the supplied Verilog-A DUT
`sample_hold.va`.

## DUT Instance Contract

- Include `sample_hold.va`.
- Instantiate module `sample_hold`.
- Positional ports, exactly in this order: `VDD`, `VSS`, `IN`, `CLK`, `OUT`.
- Use 0.9 V for `VDD` and 0 V for `VSS`.

## Public Stimulus Contract

- Drive `CLK` with multiple clean rising edges crossing 0.45 V.
- Drive `IN` through changing voltage levels or a ramp so successive clock edges
  sample different input values.
- Run long enough for several sample/hold intervals and settled output windows.

## Public Observables

Save these exact scalar waveform names:

- `in`
- `clk`
- `out`

## Output Contract

Return exactly one Spectre file named `tb_sample_hold_ref.scs`.
Do not include explanatory prose.
```

### 为什么这是 public prompt 修改

这些不是模型技巧，而是 testbench task 的公开契约。没有这些信息，失败不能算模型能力差，
更像 benchmark task 模糊。

## 3. 例子 B：Bugfix 太直接，应该改成 observed-vs-expected

当前例子：

`vbr1_l1_clocked_sample_and_hold/forms/bugfix/prompt.md`

### Before 摘要

```markdown
Repair the supplied buggy Verilog-A implementation for `Clocked sample-and-hold`.

Bug to fix: The buggy sample-and-hold ignores the input sample and always holds zero.

Public behavior checks:

- samples_on_rising_clock_edge
- output_holds_between_edges
- sample_value_tracks_input_at_edge
```

### 问题

- “ignores the input sample and always holds zero” 已经接近直接告诉 bug 根因。
- bugfix task 更像 debug/repair，应该给工程可见现象，而不是 gold patch 方向。
- 仍然缺少 interface preservation 的硬字段。

对应 failure class：

- `bugfix_overdisclosure`
- `module_interface_mismatch`
- `behavioral_match_gap`

### After 建议

```markdown
# Task: clocked_sample_and_hold_bugfix

Form: bugfix
Target artifact: repaired `sample_hold.va`
Visible context: buggy source plus public intended behavior
Hidden evaluator: external waveform checker using the public behavior below.

Repair the supplied Verilog-A implementation of module `sample_hold`.
Preserve the module name, parameter names, electrical ports, and port order:
`VDD`, `VSS`, `IN`, `CLK`, `OUT`.

## Intended Public Behavior

- On each rising crossing of `CLK` through the public threshold, sample `V(IN)`.
- Between rising edges, hold the last sampled value at `OUT`.
- Drive `OUT` with finite transition edges.
- Preserve unrelated behavior and do not rewrite the public interface.

## Observed Mismatch From The Buggy Artifact

| Scenario | Expected behavior | Observed faulty behavior |
| --- | --- | --- |
| `IN` changes before successive rising `CLK` edges | `OUT` updates to the newly sampled input after each edge | `OUT` remains near the initial held level |
| `IN` is stable between clock edges | `OUT` holds the sampled value | `OUT` does not reflect the sampled input value |

## Output Contract

Return exactly the repaired Verilog-A artifact and no explanatory prose.
```

### 为什么这样改

它仍然告诉模型该修什么行为，但不直接说“代码里把 held 写成 0”。这更符合 CVDP/VerilogEval
bugfix prompt 的写法：给 intended behavior + observed mismatch，而不是给 patch answer。

## 4. 例子 C：E2E prompt artifact 名不一致，必须直接修 public prompt

当前例子：

`vbr1_l2_converter_front_end/forms/e2e/prompt.md`

### Before 摘要

```markdown
Write a Verilog-A module named `sample_hold_droop_ref` and one minimal EVAS-compatible Spectre testbench.

## Deliverables

Return exactly two fenced code blocks:

1. `sample_hold_droop_ref.va`
2. `tb_sample_hold_droop.scs`
```

但 release manifest/gold artifact 使用的是：

```text
sample_hold_droop_ref.va
tb_sample_hold_droop_ref.scs
```

### 问题

- target artifact 名不一致，这是 benchmark contract bug。
- 这种问题不能靠 wrapper 解决；wrapper 不应该猜哪个文件名才对。

对应 failure class：

- `artifact_missing`
- `artifact_name_mismatch`

### After 建议

```markdown
# Task: converter_front_end_e2e

Form: e2e
Target artifacts:
1. `sample_hold_droop_ref.va`
2. `tb_sample_hold_droop_ref.scs`

Visible context: public DUT and testbench contract
Hidden evaluator: external EVAS/Spectre-compatible waveform checker.

## DUT Contract

- Module name: `sample_hold_droop_ref`
- Ports, all `electrical`, exactly in this order: `vdd`, `vss`, `clk`, `vin`, `vout`
- Parameters:
  - `vth` real, default `0.45`
  - `tau` real, default `120n`
  - `dt` real, default `0.5n`
  - `trf` real, default `40p`
- Public behavior:
  - sample `V(vin)` on rising crossings of `clk`
  - hold the sampled value between clock edges
  - show bounded droop toward `V(vss)` during hold windows
  - keep `vout` within the supply range

## Testbench Contract

- Include `sample_hold_droop_ref.va`.
- Instantiate `sample_hold_droop_ref` by positional ports.
- Drive `clk` with several valid rising edges.
- Drive `vin` through distinct levels so multiple sample/hold windows are visible.
- Save these exact scalar names: `vin`, `clk`, `vout`.

## Output Contract

Return exactly two source artifacts named:

1. `sample_hold_droop_ref.va`
2. `tb_sample_hold_droop_ref.scs`
```

### 为什么这是 public prompt 修改

artifact 名、DUT contract、testbench contract、public observables 都是可见任务边界。它们不泄露
gold implementation，但能防止模型因为任务合同不清而失败。

## 5. 例子 D：DUT prompt 已经接近可用，只做 scaffold 统一

当前例子：

`vbr1_l1_threshold_comparator/forms/dut/prompt.md`

### Before 摘要

```markdown
# Threshold comparator DUT

Write the Verilog-A DUT artifact(s) for `Threshold comparator`.

Reference artifact name(s): `comparator.va`.
Domain: pure voltage-domain behavioral Verilog-A.

- Declaration: `comparator(vdd, vss, vinp, vinn, out_p)`
...
```

### 问题

这个 prompt 本身比前几个好。主要是格式没有完全和 scaffold 对齐，`visible margin` 这种词稍泛。

### After 建议

```markdown
# Task: threshold_comparator_dut

Form: dut
Target artifact: `comparator.va`
Visible context: public DUT contract only
Hidden evaluator: external waveform checker using the public observables below.

Implement one pure voltage-domain behavioral Verilog-A module named `comparator`.

## Interface Contract

- Ports, all `electrical`, exactly in this order: `vdd`, `vss`, `vinp`, `vinn`, `out_p`.

## Public Behavior

- Drive `out_p` toward the `vdd` rail when `V(vinp) > V(vinn)` by a clear analog margin.
- Drive `out_p` toward the `vss` rail when `V(vinp) < V(vinn)` by a clear analog margin.
- Use finite transition edges for output changes.
- Do not generate a Spectre testbench in this form.

## Public Observables

The evaluator testbench saves:

- `vinp`
- `vinn`
- `out_p`

## Output Contract

Return exactly one Verilog-A source file named `comparator.va`.
```

### 为什么不是大改

这个任务的问题主要是结构统一，不是行为缺失。不要为了“优化 prompt”把 checker 阈值或参考实现写进去。

## 6. EVAS rules：不要复制进每个 public prompt

这些内容不建议批量塞进每个 `prompt.md`：

```markdown
- Use `electrical` ports and `analog begin ... end`.
- Do not use digital Verilog `reg`, `wire`, `logic`, `always`, or `initial`.
- Use `@(initial_step)` for initialization when state is required.
- Use `@(cross(...))` for edge events.
- Use `transition(...)` for smoothed voltage outputs.
- Prefer plain scalar save names for required observables.
```

它们应该进入 `vaBench_evas_rules.md`，由 runner wrapper 注入。只有当某个任务需要任务特定约束
时才写进 public prompt，例如 comparator 必须保存 `vinp/vinn/out_p`，sample-and-hold TB 必须保存
`in/clk/out`。

## 7. Runner wrapper：示例

wrapper 是 baseline runner 调模型时的外层，不是 benchmark prompt：

```text
System:
You are a Verilog-A behavioral modeling engineer. Only write EVAS/Spectre-compatible
voltage-domain behavioral Verilog-A and Spectre transient artifacts.

Question:
<contents of forms/*/prompt.md>

EVAS rules:
<selected shared rules from vaBench_evas_rules.md>

Answer:
Return only the requested artifact contents.
```

这样 public prompt 负责 benchmark contract，EVAS rules 负责通用兼容性，wrapper 负责模型调用协议。
