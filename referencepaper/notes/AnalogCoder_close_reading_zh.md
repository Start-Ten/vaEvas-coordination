# AnalogCoder 中文精读笔记

日期：2026-05-21
论文：AnalogCoder: Analog Circuit Design via Training-Free Code Generation
本地 PDF：`coordination/referencepaper/AnalogCoder_AAAI2024.pdf`

## 0. 一句话判断

AnalogCoder 不是模型训练论文。它是一篇“模拟电路设计 agent + 仿真反馈闭环 +
小型 analog benchmark”的论文。它最值得我们吸收的是：如何把 LLM 输出接到可执行
仿真和功能检查上，而不是它的模型本身。

它和 vaEVAS 的关系是“方向相近，任务不同”：

1. AnalogCoder 生成 transistor-level circuit 的 PySpice 代码。
2. vaEVAS 面向 Verilog-A behavioral model 的 benchmark/evaluator。
3. AnalogCoder 用 PySpice/SPICE 反馈修复电路。
4. vaEVAS 用 EVAS 快速评估，并用 Spectre 做最终认证。

## 1. 摘要在说什么

摘要的逻辑很直接：

1. 模拟电路设计难，原因是要选 component、connectivity、parameters，并保证功能正确。
2. LLM 在 digital circuit design 上已有进展，但 analog circuitry 复杂且数据少。
3. AnalogCoder 提出一个 training-free LLM agent，通过生成 Python/PySpice 代码来设计模拟电路。
4. 方法有三件事：
   - feedback-enhanced flow：让 LLM 根据仿真和检查错误自动修复。
   - circuit tool library：把成功的基本电路保存成可复用子电路。
   - analog benchmark：用一组模拟电路任务评估方法。
5. 结果：AnalogCoder 成功设计 20 个 circuit，比标准 GPT-4o 多 5 个。

这里的关键词是 training-free。它不是训练一个 analog code model，而是围绕现有 LLM
搭了一个可执行设计循环。

## 2. Introduction 的真正动机

Introduction 先把已有 LLM-for-EDA 工作归为两类：

1. Verilog code generation/correction。
2. design flow script generation。

作者随后指出这些大多是 digital circuit design，而 analog design 更难。难点分三层：

1. **复杂性**：模拟电路有电压源、电流源、MOSFET、电阻、电容等多种组件，连线和参数轻微变化都可能改变功能。
2. **抽象层级低**：数字 Verilog 可以写高层功能，例如 adder；模拟电路必须显式构造物理组件和连接。
3. **语料少**：SPICE 在公开代码语料里更少，LLM 不容易直接学到 SPICE 规则。

因此他们的关键选择是：不让 LLM 直接写 SPICE，而是写 Python/PySpice。这个选择很重要，
因为它承认了目标语言/中间表示会显著影响 LLM 可用性。

对 vaEVAS 的启发：

1. 我们也面对低资源硬件语言问题，但我们不应该逃离 Verilog-A，因为我们的目标就是
   behavioral Verilog-A practice。
2. 我们可以把 AnalogCoder 作为“可执行反馈闭环”的 analog 先例。
3. 我们的差异在于：不是把任务转成 Python，而是围绕 Verilog-A 建 benchmark、checker、
   EVAS 和 Spectre certification。

## 3. Preliminary：它怎样定义 analog correctness

Preliminary 有两个作用。

第一，它解释 analog circuit 不是离散逻辑，而是连续信号变换。例如：

1. amplifier：输出是输入的放大。
2. op-amp：输出和差分输入相关。
3. integrator/adder/subtractor：可以通过 op-amp 结构实现连续信号运算。

第二，它解释三种表示：

1. circuit diagram。
2. SPICE netlist。
3. Python/PySpice code。

作者把 PySpice 作为 LLM 的主要生成表面，因为 Python 更熟悉，且 PySpice 仍能调用
SPICE 仿真。

这里有一个需要警惕的地方：它的 correctness 主要是 functional correctness，也就是
“输入刺激下输出行为满足任务检查”。这不是完整的工业模拟设计 signoff，不包括充分的
PVT、layout parasitic、corner、robustness、noise、yield 等。

## 4. Method 总览

AnalogCoder 的系统由三块组成：

1. prompt engineering。
2. feedback-enhanced design flow。
3. circuit tool library。

图 3 的核心流程可以理解为：

1. 对 basic circuit：任务描述进入 LLM，生成 PySpice 代码，进入反馈检查流。通过则加入 library，失败则带错误信息重试。
2. 对 composite circuit：先查询 library，取出需要的 subcircuit 调用方法，再让 LLM 拼成更复杂设计。
3. basic circuit 最多 3 次生成，composite circuit 最多 2 次生成。

这个设计不是“让 LLM 一次写对”，而是把 LLM 放进一个 bounded repair loop。

## 5. Prompt Engineering

Prompt 部分有三点：

1. **Programming language selection**：选择 Python/PySpice，而不是 raw SPICE。
2. **In-context learning**：给一个 two-stage amplifier 的详细例子。
3. **Chain-of-thought planning**：让 LLM 先列组件和连接计划，再写代码。

最重要的是第一点。作者不是单纯做 prompt trick，而是在重新选择 LLM 更擅长的中间语言。
这也是为什么这篇论文不能简单类比到 Verilog-A：我们不能只说“换成 Python 就行”，因为
我们的贡献正是让 Verilog-A behavioral model 变得可评估、可验证、可发布。

## 6. Feedback-Enhanced Design Flow

这是本文最有价值的部分。它不是只看 Python runtime error，而是按层级检查电路：

1. **Requirement Check**
   - 检查必要 input/output node 是否存在。
   - 检查基本拓扑约束，例如 common-drain amplifier 的输出应该接 source。
   - 检查是否缺少必要组件，例如 resistive load。

2. **Simulation and Operating Point Check**
   - 运行仿真，发现 floating nodes 等错误。
   - 检查 MOSFET 是否 active，例如 Vgs > Vth、Vds > Vgs - Vth。

3. **DC Sweep Check**
   - 扫 input voltage，看 output 是否随 input 变化。
   - 用 sweep 结果寻找更合适的 bias point。

4. **Function Check**
   - 根据 circuit type 做 DC/AC/transient 检查。
   - 例如 gain 是否足够、common-mode gain 是否小于 differential gain、oscillator 是否有足够 peaks。

这个层级很像我们做 benchmark checker 时应有的思想：先排除结构和执行错误，再看行为。
但 vaEVAS 要进一步区分：

1. L0 evaluator conformance：EVAS 和 Spectre 在语言/执行语义上对齐。
2. L1/L2 task correctness：具体 Verilog-A behavioral task 是否完成。

AnalogCoder 没有这个分层；它的检查主要服务于电路生成 agent。

## 7. Circuit Tool Library

tool library 的作用是把成功的 basic circuits 存成 reusable subcircuits。存储内容包括：

1. task description 和 circuit information 作为检索 key。
2. simulation specifications，例如 gain、phase difference。
3. code 和 call method 作为 value。

在 composite circuit 任务中，LLM 先检索需要的子电路，然后在 prompt 中获得这些子电路的
调用方式。例如 op-amp integrator 可以先检索 op-amp subcircuit，再把它接成 integrator。

这部分和我们最相关的是 L2 composition。AnalogCoder 的 composite tasks 本质是“已有基本模块
的组合”。我们在 vaBench 的 L2 里也应该强调组合行为，但不能只做浅层存在性检查；需要验证
完整 mixed-signal/behavioral flow。

## 8. Fine-tuning 部分为什么不是主线

论文也做了 GPT-3.5 fine-tuning：用 GPT-3.5、GPT-4o、Llama-3 成功生成的电路样本，
经过 TF-IDF 聚类，每类取样，再做交叉验证，保证 fine-tuning task 不在 test set。

但结果显示：fine-tuning 提高了某些任务的 success rate，却没有增加 solved task 的数量。
这和我们前面判断一致：对于这类 EDA 任务，单纯训练/微调不是最深的贡献点。更关键的是：

1. 任务定义是否真实。
2. checker 是否能抓住功能错误。
3. 仿真反馈是否可靠。
4. benchmark 是否可复现、可扩展、可认证。

## 9. Benchmark 设计

Benchmark 有 24 个 analog circuit design tasks：

1. 1-15 是 basic circuits，包括 amplifier、inverter、current mirror、op-amp。
2. 16-24 是 composite circuits，包括 oscillator、integrator、differentiator、adder、subtractor、Schmitt trigger、VCO、PLL。

指标是 Pass@1 和 Pass@5，另有 Number of solved，即多次采样中至少成功一次的任务数量。

附录 Table 6 给了各类电路的 correctness criteria。例如：

1. amplifier：gain > 0，drain current > 0。
2. op-amp：differential-mode gain > 0，且 differential-mode gain 大于 common-mode gain。
3. oscillator：有足够 peak、amplitude、period stability。
4. integrator/adder/subtractor：用输入输出波形和公式误差判断。

这些 criteria 是这篇论文的强点，因为它没有停留在 syntax/runtime pass。但也有明显边界：

1. 有些标准偏功能烟测，不等于严格 spec signoff。
2. 使用 Level-1 MOSFET model 降低了任务复杂度。
3. 主要验证功能是否出现，不验证工业级 robustness。

## 10. 实验结果

主表结论：

1. AnalogCoder 解决 20/24 个任务。
2. GPT-4o without tool library 解决 15/24 个任务。
3. Llama-3 解决 11/24 个任务。
4. GPT-3.5 解决 10/24 个任务。
5. AnalogCoder 平均 Pass@1/Pass@5 为 66.1/75.9。

Ablation 的信息更有价值：

1. GPT-3.5 直接生成 SPICE 比生成 Python/PySpice 弱。
2. 去掉 in-context example、CoT、feedback flow 都会降性能。
3. fine-tuning GPT-3.5 提升 pass rate，但不扩展 solved task 数量。

Attempt times 实验显示，多数成功发生在前三次尝试内；超过三次后成功概率下降而 token
成本继续上涨。这给我们做 repair-loop baseline 时提供了一个经验：反馈循环应有明确 budget，
不能无限修。

## 11. 批判性阅读

这篇论文的贡献是实在的，但边界也很清楚：

1. 它是 agent/system paper，不是单纯 benchmark paper。
2. benchmark 规模小，24 个任务，但在 analog LLM 方向已经有意义。
3. correctness 是 simulator-based functional checking，不是工业 signoff。
4. 它回避了 raw SPICE 生成难题，转为 PySpice 生成；这对它有效，但也说明它没有解决
   low-resource EDA DSL 本身的生成与验证问题。
5. composite circuit 的能力部分依赖 tool library，因此评价的是“LLM + library + feedback”的
   agent 系统，而不是纯模型能力。

## 12. 对 vaEVAS 的直接启发

我们应吸收三点：

1. **可执行反馈是 analog/AMS LLM 论文的共同趋势。**
   这支持我们把 EVAS/Spectre checker loop 放在论文核心，而不是把 LLM prompt 当主贡献。

2. **checker 的层级很重要。**
   AnalogCoder 从 requirement、operating point、DC sweep 到 function check。我们也应明确
   vaBench checker 不是 syntax-only，而是行为级功能检查，并且和 Spectre certification 对齐。

3. **benchmark 要服务于明确 artifact。**
   AnalogCoder benchmark 服务于 PySpice circuit generation。vaEVAS benchmark 应服务于
   Verilog-A behavioral model generation/evaluation，而不是泛化为所有 analog design。

## 13. 我们论文里的定位写法

可以这样写：

AnalogCoder demonstrates that simulator-grounded feedback can improve LLM-based analog
circuit construction by generating PySpice circuits and validating them with task-specific
checks. In contrast, vaEVAS targets behavioral Verilog-A models rather than transistor-level
circuit construction, and contributes a benchmark/evaluator package with deterministic
functional checkers and EVAS/Spectre certification.

中文理解：

AnalogCoder 证明了“仿真反馈闭环”在 analog circuit construction 中有效；但 vaEVAS 要补的是
另一个缺口：Verilog-A behavioral model 的可复现 benchmark、快速 evaluator，以及与 Spectre
对齐的认证证据。

## 14. 继续精读时要盯住的问题

1. 它的 function check 是否足够强，还是只覆盖了浅层现象？
2. 它的 benchmark task 是否有 gold/reference design，还是只判断生成结果是否满足 criteria？
3. 它的 Pass@k 更像是在评价模型采样能力，还是评价设计流程的鲁棒性？
4. 它的 tool library 是否让 composite task 变成“模块拼接”而不是真正复杂设计？
5. 它和 vaEVAS 的最大差别是否可以总结为：AnalogCoder 是 generator-centric，vaEVAS 是
   benchmark/evaluator/certification-centric？
