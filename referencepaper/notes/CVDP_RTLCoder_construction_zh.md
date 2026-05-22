# CVDP 与 RTLCoder 构造方式精读

日期：2026-05-21

本地文件：

- `coordination/referencepaper/CVDP_2025.pdf`
- `coordination/referencepaper/RTLCoder_2024.pdf`
- `coordination/referencepaper/VerilogEval_v2_2025.pdf`

说明：原来的 `RTL-Coder_2024.pdf` 实际是 VerilogEval v2 论文，不是 RTLCoder
原文；已改名为 `VerilogEval_v2_2025.pdf`，并下载真正的 RTLCoder 论文为
`RTLCoder_2024.pdf`。

## 1. 一句话对比

CVDP 是 benchmark construction paper：让硬件工程师人工写真实 RTL/verification
任务，再用 harness 和质量过滤保证任务可评估。

RTLCoder 是 training-data/model paper：用 GPT 自动生成大量 RTL instruction-code
pairs，用语法检查过滤，再训练 7B 模型。

如果我们讨论 vaEVAS 的 prompt/benchmark 构造，CVDP 比 RTLCoder 更值得学；
如果讨论“小模型训练数据怎么来”，RTLCoder 才相关。

## 2. CVDP 是怎么构造的

CVDP 的构造路线是：

1. 约 35 名有 4 年以上 Verilog/verification 经验的硬件工程师人工写题。
2. 题目覆盖 13 个类别，包含 RTL generation、verification、debugging、assertion、
   code-spec alignment、Q&A 等。
3. 每个 datapoint 可以是 Non-Agentic 单轮，也可以是 Agentic 工具使用任务。
4. 每个 problem 是一个 evaluation-time extracted multi-file repository。
5. 正确性主要通过 test harness 检查，通常是 CocoTB；部分任务用 Icarus、Yosys、
   Verilator，cid12-14 还需要 commercial tools。
6. 模型/agent 可以看到 prompt、context、testbench 或 starter code，但看不到
   test harness 和 reference solution。
7. 1,313 个初始问题经过过滤后保留 783 个。

### CVDP 的类别设计

CVDP 的重要点不是单纯题目数量，而是覆盖真实硬件工作流：

1. RTL code completion。
2. natural language spec to RTL。
3. RTL code modification。
4. module reuse。
5. lint/QoR improvement。
6. testbench stimulus generation。
7. testbench checker generation。
8. assertion generation。
9. debugging/bug fixing。
10. RTL/testbench correspondence。
11. RTL/testbench Q&A。

这比 VerilogEval/RTLLM 的单一 code generation 更深，也更接近我们希望 vaBench
覆盖 DUT、TB、bugfix、E2E 的结构。

### CVDP 的质量过滤

CVDP 质量过滤分两层：

1. Sanity checks：
   - reference solution 必须通过 harness。
   - initial context 必须失败，保证任务确实需要模型解决。
   - 这一层排除了 78 个问题。

2. LLM-based judge：
   - ambiguity score。
   - consistency score。
   - category match score。
   - behavioral match score。
   - 阈值为 8.0，低分问题被过滤。

这个 judge 还能提出 prompt refinement，但论文没有正式使用自动改写结果，因为过度改写
可能让 prompt 变得太显式、太简单。

### CVDP 对 prompt 的态度

CVDP 的 prompt 不是越详细越好。论文指出未来 benchmark 要避免 overly descriptive
prompt：如果 prompt 把每根 wire 和 flip-flop 都说清楚，它只是 RTL 的自然语言复述，
不能测试 microarchitectural decision-making。

这点对 vaEVAS 很重要：我们应改善 prompt 的 construction scaffold，但不能把 gold 行为
写成可机械翻译的答案。

## 3. RTLCoder 是怎么构造的

RTLCoder 的核心是自动训练数据生成，分三阶段。

### Stage 1: RTL domain keywords preparation

它先用 GPT-3.5 生成 digital IC design 常用关键词。作者用树状查询方式：

1. 先让 GPT 给出 RTL design block 的类别和例子。
2. 再沿着类别继续追问更具体的关键词。
3. 例如从 multiplier 扩展到 Booth multiplier、Wallace tree multiplier。
4. 得到数百个 RTL design keywords。

### Stage 2: instruction generation

它用两条路生成 instruction：

1. keyword-based：
   - 随机抽取 1-2 个关键词。
   - 结合 prompt template 让 GPT 生成 RTL design instruction。

2. source-code-based：
   - 从已有 Verilog source code 出发，让 GPT 根据代码反推相关设计问题。
   - 这样增加数据多样性。

然后它对 instruction pool 做 mutation：

1. single circuit variation。
2. circuits combining。
3. 新 instruction 通过 rule checker 后加入 pool。
4. 最后得到超过 50,000 条 instruction。

还会要求 GPT 生成 reasoning steps，增强 instruction 的细节信息。

### Stage 3: reference code generation

对每个 instruction，RTLCoder 让 GPT 生成 5 个 candidate Verilog reference codes。
然后用 automated syntax checker 过滤：

1. 只有 syntax-correct 的 code 会保留。
2. 如果 5 个候选全都 syntax fail，就丢弃该 instruction。
3. 最后得到超过 27,000 个 instruction-code pairs。

论文明确承认：理想情况下应该检查 RTL code 是否和 instruction 功能一致，但自动生成
testbench 做功能验证目前不可行。因此它只做了 syntax checking。

这就是 RTLCoder 的关键弱点：它的训练集不是 functionally certified dataset。

## 4. 二者对 vaEVAS 的启发

### 更应该学 CVDP

vaEVAS 的目标是发 Verilog-A practice，所以我们更像 CVDP：

1. 我们要强调 benchmark construction，而不是训练数据生成。
2. 我们要有 public prompt、gold artifact、checker、reference solution separation。
3. 我们要区分模型可见内容和 evaluator/harness 私有内容。
4. 我们要证明 gold/reference 通过，空/初始/坏例失败。
5. 我们要做 prompt ambiguity、behavioral match、category alignment 审计。

### 可以从 RTLCoder 学到什么

RTLCoder 对我们有两个间接启发：

1. 可以用关键词树和 mutation 扩展候选任务主题。
2. 但不能只用 syntax checker 过滤。Verilog-A 的关键不是 syntax pass，而是行为是否在
   EVAS/Spectre 下满足 checker。

因此 RTLCoder 适合放在 related work 的“training-data generation contrast”里，而不是
作为 prompt/benchmark 构造主参考。

## 5. 对 vaEVAS prompt 设计的修正建议

AnalogCoder 给我们 construction scaffold 的想法，但 CVDP 给了更稳的 benchmark 约束：

1. Prompt 应该补充构造提示，但不能变成 gold solution paraphrase。
2. 每个 task 应有 public contract 与 hidden checker 的边界。
3. Prompt 质量审计应看四项：
   - ambiguity：高级工程师能否不反复猜测就理解任务。
   - consistency：prompt、gold、checker、harness 是否一致。
   - category match：DUT/TB/bugfix/E2E 分类是否准确。
   - behavioral match：prompt 行为描述是否正好覆盖 checker 测的行为。
4. 对 L2 tasks，prompt 不能只说“组合系统”，还要给公共子行为边界和 observable
   handoff，但不要给内部 gold implementation。

## 6. 我们论文里可以怎么用

可以这样定位：

1. RTLCoder demonstrates that large synthetic RTL instruction-code datasets can
   improve small domain models, but its automated filtering is primarily syntax
   based and does not provide functional certification for each generated pair.

2. CVDP moves the benchmark direction toward human-authored, workflow-oriented,
   harness-backed hardware design and verification tasks with explicit
   quality filtering.

3. vaEVAS follows the benchmark/evaluator line rather than the synthetic
   training-data line: it targets Verilog-A behavioral models with public task
   contracts, deterministic checkers, EVAS/Spectre dual validation, and
   claim-gated release artifacts.

## 7. Practical Next Step

Before rewriting vaEVAS prompts, run a CVDP-style prompt audit over a small slice:

1. Choose 12 tasks:
   - 3 DUT.
   - 3 TB.
   - 3 bugfix.
   - 3 E2E/L2.
2. Score each prompt for ambiguity, consistency, category match, and behavioral match.
3. For low-score prompts, refine only the public prompt.
4. Re-run EVAS/Spectre on the same slice.
5. Require no EVAS PASS / Spectre FAIL regression.
