# VerilogEval Prompt 构造方式精读

日期：2026-05-22

本地与在线来源：

- 本地论文：`coordination/referencepaper/VerilogEval_2023.pdf`
- 本地后续论文：`coordination/referencepaper/VerilogEval_v2_2025.pdf`
- 官方仓库：`https://github.com/NVlabs/verilog-eval`
- v1 release 分支：`https://github.com/NVlabs/verilog-eval/tree/release/1.0.0`
- 本次抽样文件：
  - `/private/tmp/VerilogEval_Human_v1.jsonl`
  - `/private/tmp/VerilogDescription_Human_v1.jsonl`
  - `/private/tmp/ve_code_Prob006_prompt.txt`
  - `/private/tmp/ve_code_Prob006_ifc.txt`
  - `/private/tmp/ve_spec_Prob006_prompt.txt`
  - `/private/tmp/ve_code_Prob062_bug_prompt.txt`
  - `/private/tmp/ve_spec_Prob062_bug_prompt.txt`
  - `/private/tmp/verilog_eval_sv_generate`

## 1. 核心结论

VerilogEval 要学两件事：

1. v1 的经典设计：像 HumanEval 一样做 code completion，固定 module interface，hidden
   testbench 做功能正确性评估。
2. v2 的 prompt 改造：从 IDE-style completion 扩展到 chat-style specification-to-RTL，
   支持 in-context examples、prompt rules、`[BEGIN]`/`[DONE]` extraction 和 failure
   classification。

对 vaEVAS 来说，VerilogEval 比 CVDP 更基础：

- VerilogEval 教我们怎么把一个 benchmark prompt 写成“可稳定抽取、可稳定评测”的形式。
- CVDP 教我们怎么把任务类别扩成更真实的工程 workflow。

所以后续完善 vaBench prompt，应该先吸收 VerilogEval 的 prompt mechanics，再吸收 CVDP 的
workflow/category construction。

## 2. VerilogEval v1 的 prompt 方式

v1 论文给出的生成 prompt 由三块组成：

1. 可选 system prompt：
   - 约束模型只补全 syntax-correct Verilog。
   - 要求以 `endmodule` 结束。
   - 不要输出 module/input/output definition。
2. question prompt：
   - 要求根据描述实现 Verilog module。
   - 默认 clock/clk 信号为 positive-edge triggered，除非题目另说。
3. problem description：
   - 自然语言行为描述。
   - module header。
   - input/output definition。

v1 的官方 release 数据中，`data/VerilogEval_Human.jsonl` 的 `prompt` 字段主要是 module
header；自然语言描述在 `descriptions/VerilogDescription_Human.jsonl` 里。实际采样时会把
description 和 interface 组合成模型 prompt；评测时 hidden testbench 会把
`problem["prompt"] + completion` 拼成完整 Verilog 文件。

这是一种典型 code-completion benchmark：

```text
Description:
Given an 8-bit input vector, reverse its bit ordering.

module top_module (
  input [7:0] in,
  output [7:0] out
);

<model completes body only>
```

### v1 的优点

1. 接口无歧义：
   - module name 固定。
   - port name 固定。
   - bit width 固定。
   - output 是 wire 还是 reg 往往也由 header 决定。

2. 输出容易评测：
   - 模型只补 module body。
   - hidden testbench 直接拼接、编译、仿真。
   - pass@k 是功能正确性，不是 BLEU。

3. prompt 短：
   - 对 2023 年上下文较短的模型友好。
   - 很适合 HDLBits 这种小题。

### v1 的缺点

1. 它是 completion-style，不完全适合 chat/instruction 模型。
2. 模型容易违反“只补 body”：
   - 重复 module declaration。
   - 缺 `endmodule`。
   - 输出解释文字。
3. 固定 Verilog port 类型会引发 wire/reg 冲突：
   - 如果 output header 是 wire，模型却在 `always` 中赋值，会报 `Reg Declared as Wire`。
4. 任务主要是 self-contained module，缺少 module reuse、testbench、debug、agentic workflow。

这也是 v2 和 CVDP 后续扩展的出发点。

## 3. VerilogEval v2 的两种 prompt style

官方 main 分支把 156 个问题拆成两个 dataset：

| Dataset | 文件数量 | prompt style |
| --- | ---: | --- |
| `dataset_code-complete-iccad2023` | 156 prompt + 156 ifc + 156 ref + 156 test | code completion |
| `dataset_spec-to-rtl` | 156 prompt + 156 ref + 156 test | specification-to-RTL |

### 3.1 Code completion style

v2 的 code-complete prompt 文件仍然包含自然语言描述和 module interface，例如 vector reverse：

```text
Given an 8-bit input vector [7:0], reverse its bit ordering.

module TopModule (
  input [7:0] in,
  output [7:0] out
);
```

生成脚本会把 module declaration 前面的描述变成 Verilog comments，再把 module header 留在
prompt 里：

```verilog
// Implement the Verilog module based on the following description...
//
// Given an 8-bit input vector [7:0], reverse its bit ordering.

module TopModule (
  input [7:0] in,
  output [7:0] out
);
```

system message 仍然要求模型做 completion：

- 只输出 syntax-correct Verilog。
- 以 `endmodule` 结束。
- 不要包含 module/input/output definitions。

这个 style 和 vaBench 的 `dut` prompt 不完全一样，因为我们现在要求模型返回完整 Verilog-A
artifact，而不是只补 body。

### 3.2 Specification-to-RTL style

v2 额外引入更适合 chat 模型的 spec-to-RTL prompt。vector reverse 的 prompt 变成：

```text
I would like you to implement a module named TopModule with the following
interface. All input and output ports are one bit unless otherwise specified.

 - input  in  (8 bits)
 - output out (8 bits)

The module should reverse the bit ordering of the input port and write
the result to the output port.
```

生成脚本会包装成：

```text
Question:
<task prompt>

Enclose your code with [BEGIN] and [DONE]. Only output the code snippet
and do NOT output anything else.

Answer:
```

system message 则换成：

```text
You are a Verilog RTL designer that only writes code using correct Verilog syntax.
```

这个 style 对 vaEVAS 更有参考价值，因为我们的任务本质也是 specification-to-Verilog-A，而
不是 IDE 里续写已有 module body。

## 4. In-Context Learning 的用法与风险

v2 支持 0-shot 到多 shot。ICL example 是完整小模块：

1. combinational incrementer。
2. sequential incrementer with synchronous reset。
3. simple FSM。

这些 example 的作用不是给当前题答案，而是教模型：

- module declaration 到 `endmodule` 的完整边界。
- combinational logic 怎么写。
- sequential logic 怎么写。
- FSM 怎么组织 state、next-state、output logic。

但 v2 论文也指出 ICL 有风险：

1. 某些模型会从 example 复制错误 port name，例如把 `in_` 用到当前题。
2. 某些 example 会诱导模型过度使用 `begin/end`，反而漏掉 `endmodule`。
3. 1-shot 可能改善 combinational task，却伤害 sequential task。
4. prompt tuning 的效果高度 model/task dependent。

对 vaEVAS 的结论：

- 不应该把 ICL examples 固化到 benchmark public prompt 里。
- ICL 更适合作为 baseline runner 的 prompt prefix，在实验中作为一个 prompt variant。
- 如果加 Verilog-A example，必须非常小心，避免 example 的 port/name/state 被模型迁移到
  当前任务。

## 5. Prompt rules 的启发

v2 的 spec-to-RTL 生成脚本支持 rules suffix，例如：

- all ports/signals use `logic`，不要用 `wire`/`reg`。
- combinational always block 用 `always @(*)`。
- sized numeric constants size must be greater than zero。
- synchronous reset 不要把 reset 放进 sensitivity list。

这些 rules 不是某个题目的行为答案，而是语言/风格安全护栏。它们直接针对 failure
classification 里常见错误。

对 vaEVAS，这个思路非常有用。我们也应该有 Verilog-A rule suffix，但要注意它应该是
benchmark runner/prompt wrapper 的公共护栏，而不是每个任务重复写一遍。

候选 Verilog-A rules：

1. Use `electrical` ports and `analog begin ... end`.
2. Do not use digital Verilog `reg`, `wire`, `logic`, `always`, or `initial`.
3. Initialize state in `@(initial_step)`.
4. Use `@(cross(...))` for edge events and `@(timer(...))` only when periodic updates are needed.
5. Drive outputs with voltage contributions, normally `V(out) <+ transition(target, 0, trf)`.
6. Do not use current contributions, `ddt()`, `idt()`, AC/noise analysis, or transistor devices unless the task explicitly allows them.
7. Preserve exact module name, port order, saved waveform names, and requested artifact names.

这些 rules 不泄露 gold，但能减少无意义的语法/风格失败。

## 6. Failure classification 是 prompt tuning 的反馈机制

v2 不只是看 pass/fail，还把失败分类。典型失败包括：

- missing clock binding。
- module missing。
- reg/wire confusion。
- sensitivity list error。
- syntax error。
- reset issue。
- timeout。

论文明确说，分类结果可以反过来指导 prompt tuning。例如 reg/wire 错误高，就可以改 prompt
rule，要求用 `logic` 或换到 spec-to-RTL 让模型自己生成 interface。

这对 vaEVAS 很关键。我们的 prompt 完善不应靠主观感觉，而应该有错误分类：

| VerilogEval failure | vaEVAS 类比 |
| --- | --- |
| Module Missing | module name / artifact missing |
| Reg Declared as Wire | 使用 `reg/wire/always` 等数字 Verilog 写法 |
| Unable to Bind Wire/Reg | port name、save column、instance node 名不匹配 |
| Sensitivity Problem | `cross/timer` event 触发错误 |
| Syntax Error | OpenVAF/Spectre parser error |
| Reset Issue | reset priority、initial condition、event ordering 错 |
| Timeout | EVAS/Spectre 仿真不收敛或运行过长 |
| General Runtime Error | waveform/checker semantic mismatch |

我们后续修 prompt 时，应该先跑小 slice，统计这些 failure class，再决定加哪些 prompt
rules，而不是凭直觉把 prompt 写长。

## 7. VerilogEval、CVDP、vaBench 的关系

| 维度 | VerilogEval | CVDP | vaBench/vaEVAS |
| --- | --- | --- | --- |
| 核心贡献 | 经典 Verilog code benchmark | workflow-oriented RTL/DV benchmark | behavioral Verilog-A benchmark + EVAS evaluator |
| prompt style | completion + spec-to-RTL | category-specific task prompt | DUT/TB/bugfix/E2E public prompt |
| 任务复杂度 | 多为 HDLBits self-contained module | 多文件、debug、TB、assertion、agentic | Verilog-A DUT/TB/L2 flow |
| hidden evaluator | Icarus hidden testbench | Cocotb/EDA hidden harness | deterministic checker + EVAS/Spectre |
| 对我们最有用 | prompt mechanics / output extraction / failure classification | category construction / quality filtering | 主线贡献 |

一句话：VerilogEval 是 prompt 与评测协议的基础样板；CVDP 是任务类别与工程真实性的扩展样板。

## 8. 对 vaEVAS prompt 的直接建议

### 8.1 区分 benchmark prompt 与 runner wrapper

VerilogEval v2 把 task prompt 和 generation wrapper 分开：

- task prompt：描述题目。
- wrapper：`Question:`、rules、`[BEGIN]`/`[DONE]`、`Answer:`。

vaEVAS 也应这样分：

1. `forms/*/prompt.md` 保持为 benchmark public contract。
2. baseline runner 可以在外层包一层：
   - role/system message。
   - Verilog-A idiom rules。
   - exact output extraction marker。

这样 benchmark prompt 本身不会被 prompt-engineering 实验污染。

### 8.2 DUT/E2E 可学习 spec-to-RTL 结构

建议 DUT/E2E prompt 采用类似结构：

```markdown
I would like you to implement a pure voltage-domain behavioral Verilog-A module named `{module}`.

Interface:
- electrical `{port}`: ...

Behavior:
- ...

Public evaluation observables:
- ...

Output:
- return exactly `{artifact}`.
```

这比 “Write the Verilog-A DUT artifact(s)” 更贴近 instruction-tuned model。

### 8.3 TB prompt 要避免误解为 checker generation

VerilogEval/CVDP 都提醒 testbench generation 和 checker generation 是不同任务。我们的 `tb`
prompt 应明确：

- generate Spectre transient wrapper/stimulus。
- instantiate DUT。
- save named observables。
- do not generate hidden checker logic。

### 8.4 Bugfix prompt 可采用 VerilogEval 的 bug example 风格

VerilogEval 的 bug tasks 会展示 faulty implementation，让模型“find the bug and fix”。我们可以
把 bugfix prompt 改成：

1. 给 faulty module/context。
2. 给 public intended behavior。
3. 给 representative observed mismatch。
4. 要求保留 interface 和 artifact name。

少直接说“这是 reset-priority bug”，多说“reset falls during active pulse, observed pulse remains high”。

### 8.5 Prompt 改动要和 failure taxonomy 绑定

后续 prompt 完善顺序建议：

1. 先选 12-task slice。
2. 对原始 prompt 运行模型 baseline 或已有失败样本。
3. 按 vaEVAS failure taxonomy 分类。
4. 只为高频失败增加 rules 或澄清。
5. 重新跑 EVAS/Spectre，确认没有把 prompt 改成 gold paraphrase。

这比一次性“把 prompt 写详细”更稳。
