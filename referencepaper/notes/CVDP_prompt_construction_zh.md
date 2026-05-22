# CVDP Prompt 构造方式精读

日期：2026-05-21

本地与在线来源：

- 本地论文：`coordination/referencepaper/CVDP_2025.pdf`
- 官方代码仓库：`https://github.com/NVlabs/cvdp_benchmark`
- 官方 Hugging Face 数据集：`https://huggingface.co/datasets/nvidia/cvdp-benchmark-dataset`
- 本次抽样文件：
  - `/private/tmp/cvdp_nonagentic_codegen_no_commercial.jsonl`
  - `/private/tmp/cvdp_nonagentic_codegen_commercial.jsonl`
  - `/private/tmp/cvdp_agentic_codegen_no_commercial.jsonl`
  - `/private/tmp/cvdp_agentic_codegen_commercial.jsonl`

## 1. 核心结论

CVDP 的 prompt 构造确实和我们 vaBench 的形式很像，但它不是一套固定大模板，而是：

1. 用 task category 定义输入/输出契约。
2. 每个 datapoint 由专家手写或整理 prompt。
3. prompt 只暴露 public task/context，不暴露 hidden harness 和 reference solution。
4. 用 sanity check 与 LLM judge 过滤 prompt 质量。

所以它和 AnalogCoder 不同：AnalogCoder 是 prompt engineering + agent flow；CVDP 是 benchmark
datapoint construction。对 vaEVAS 更有直接参考价值。

## 2. 数据结构

### Non-Agentic

官方 README 给出的结构是：

```json
{
  "id": "cvdp_copilot_name_0001",
  "categories": ["category", "difficulty"],
  "input": {
    "prompt": "The task instruction here",
    "context": {
      "file_path.v": "file content here"
    }
  },
  "output": {
    "context": {
      "file_to_patch.v": "expected output content"
    }
  },
  "harness": {
    "files": {
      "docker-compose.yml": "test harness configuration"
    }
  }
}
```

这和我们 release task 的分层非常接近：

- `input.prompt` 类似 `forms/*/prompt.md`。
- `input.context` 类似给模型可见的 starter artifact/context。
- `output.context` 是 reference artifact，不给模型看。
- `harness.files` 是 evaluator 私有测试，不给模型看。

### Agentic

官方 README 给出的结构是：

```json
{
  "id": "cvdp_agentic_name_0001",
  "categories": ["category", "difficulty"],
  "system_message": "System instructions for the agent",
  "prompt": "The task instruction here",
  "context": {
    "file_path.v": "file content here"
  },
  "patch": {
    "file_to_patch.v": "expected changes in diff format"
  },
  "harness": {
    "files": {
      "docker-compose.yml": "test harness configuration"
    }
  }
}
```

Agentic 版本多了两点：

1. `system_message` 规定 agent 可用文件操作、编译、仿真、patch 输出格式。
2. `context` 在运行时变成 `/code/docs`、`/code/rtl`、`/code/verif`、`/code/prompt.json`。

这更像我们的 future repair/evaluation runner，而不是当前 prompt-only baseline。

## 3. CVDP 的 task category 与 vaBench form 对齐

| CVDP 类别 | 含义 | 和 vaBench 的关系 |
| --- | --- | --- |
| `cid002` | RTL code completion | 我们目前没有直接对应；类似给半成品 DUT 补全 |
| `cid003` | natural language spec to RTL | 最像我们的 `dut`，可类比 spec-to-Verilog-A DUT |
| `cid004` | RTL code modification | 类似修改已有 DUT/context，但不是 bugfix |
| `cid005` | spec-to-RTL with module reuse | 最像我们的 L2/E2E 组合任务 |
| `cid007` | lint/QoR improvement | 我们非目标，不适合放主线 |
| `cid012` | testbench stimulus generation | 类似我们的 `tb`，但 CVDP 更强调 stimulus-only |
| `cid013` | testbench checker generation | 我们 checker 是 benchmark 私有资产，不建议让模型生成作为主线 |
| `cid014` | assertion generation | RTL/SVA 特有；可作为 verification-task 参考，不直接照搬 |
| `cid016` | debugging / bug fixing | 最像我们的 `bugfix` |

本次本地统计：

| 数据子集 | 行数 | 类别分布 |
| --- | ---: | --- |
| non-agentic no-commercial | 302 | `cid002`:94, `cid003`:78, `cid004`:55, `cid007`:40, `cid016`:35 |
| non-agentic commercial | 187 | `cid012`:67, `cid013`:53, `cid014`:67 |
| agentic no-commercial | 92 | `cid003`:34, `cid004`:25, `cid005`:22, `cid016`:11 |
| agentic commercial | 68 | `cid003`:3, `cid005`:3, `cid012`:16, `cid013`:18, `cid014`:28 |

我们的 release prompt form 统计：

| vaBench form | 数量 |
| --- | ---: |
| `dut` | 57 |
| `tb` | 75 |
| `bugfix` | 52 |
| `e2e` | 75 |

所以你记得的“bugfix、spec-to-xxx、DUT 多种类型”这个印象基本对：CVDP 是按工程工作流拆
prompt 类型，vaBench 也是按 Verilog-A benchmark 工作流拆 form 类型。

## 4. CVDP prompt 的具体写法

### 4.1 Spec-to-RTL / 类比我们的 DUT

`cid003` prompt 通常包含：

1. 开头一句明确动作：Design/Create/Implement a module。
2. 模块名。
3. 参数表。
4. 输入输出表。
5. 行为定义。
6. timing/synchronization 约束。
7. 输出目标文件由 dataset 的 `output.context` 指定，而不是直接在 prompt 里作为可见答案。

典型例子是 QAM16 mapper：

- prompt 写清模块名 `qam16_mapper_interpolated`。
- 写清参数 `N`、`IN_WIDTH`、`OUT_WIDTH`。
- 写清 packed input/output 的位宽。
- 写清 mapping、interpolation、output arrangement。
- harness 用 Cocotb 检查随机与边界测试。

这和我们的 DUT prompt 相似：模块名、port order、参数、行为、public observables 都应可见。

区别是：CVDP 的 RTL prompt 往往比我们的 DUT prompt 更“规格书化”，表格更多、边界 case
更多；我们的 prompt 更强调 output contract 和 evaluator observables。

### 4.2 Code Modification / 类比已有上下文修改

`cid004` prompt 的结构是：

1. 指定已有 RTL 文件在 context 中。
2. 描述当前功能。
3. 描述新增/修改需求。
4. 要求保持已有接口、latency 或行为不变。
5. 输出修改后的同一文件。

这类任务对 vaEVAS 的启发是：如果我们未来想做“接口不变，扩展行为”的 Verilog-A 任务，
可以单独开一个 `modify` form；不要把它混到 `bugfix` 里。

### 4.3 Bugfix / 对应我们的 bugfix

`cid016` prompt 通常包含：

1. 有 bug 的 RTL 文件作为 context。
2. 自然语言说明设计原意。
3. 给出失败现象，常见形式是 expected vs actual 表。
4. 要求修复并保持模块接口。
5. hidden harness 验证修复。

这比我们的 bugfix prompt 多一个可学习点：失败现象可以更结构化。

我们现在的 bugfix prompt 通常会说明 bug 根因，例如 reset priority bug。这对模型友好，但
有时会太接近修复方向。CVDP 的方式更像工程 debug：给 observed mismatch，让模型定位并修。

对 vaEVAS 来说可折中：

- public prompt 可以给失败类别与代表性观测，例如 reset during pulse 后 `pulse` 没有及时清零。
- 不要直接给 gold patch 的控制流。
- bugfix form 可统一加入 “observed vs expected behavior” 小表。

### 4.4 Testbench Stimulus / 对应我们的 tb

`cid012` 是 stimulus generation，通常要求：

1. 完成或创建 SystemVerilog testbench。
2. 实例化 DUT/MUT。
3. 生成覆盖边界和随机场景的输入向量。
4. 重点是 stimulus，不要求完整 checker。

这和我们的 `tb` 不完全一样。我们 `tb` prompt 往往要求：

- 包含 transient analysis。
- 实例化 Verilog-A DUT。
- save public observables。
- 保持 EVAS/Spectre validation contract。

CVDP 对 `cid012` 和 `cid013` 的拆分提醒我们：如果我们说 `tb`，要明确它到底是 stimulus
companion、simulation wrapper、还是 checker companion。vaBench 当前 `tb` 更像 Spectre
testbench artifact，不是 checker generation。

### 4.5 Testbench Checker / 不建议作为 vaEVAS 主线 form

`cid013` 要求在已有 testbench 上加 checker/reference model。prompt 会提供：

1. DUT/testbench/spec context。
2. 要加入哪些 checker logic。
3. reference model 的行为要求。
4. 哪些输出要验证。

我们不应该直接照搬成 vaBench 的公开 form，因为 vaEVAS 的 checker 是 benchmark
可信度资产，应由我们控制并隐藏，而不是让被测模型生成。

但 `cid013` 对我们有一个重要启发：checker 行为应能反向审计 prompt。也就是说：

- prompt 声明的 public behavior 必须覆盖 checker 真正测的 behavior。
- checker 不应测试 prompt 从未公开的私有假设。

这正是 CVDP 的 `behavioral_match_score` 应用于 vaEVAS 的位置。

### 4.6 Agentic prompt / 类比 repair runner

CVDP agentic prompt 分成 `system_message` 和 task `prompt`。

`system_message` 不是任务规格，而是工具协议：

- 可以 `ls` / `tree`。
- 可以 `cat`。
- 可以写文件。
- 可以用 `iverilog` 编译。
- 可以用 `vvp` 仿真。
- 最后输出 Linux patch。

这和 vaEVAS 的 EVAS-feedback repair runner 非常像。对我们来说，prompt-only benchmark 不应
混入这些 agent 工具协议；但 repair baseline 可以单独有一套 agent system prompt：

- read task assets。
- run EVAS。
- inspect logs/waveform summary。
- patch DUT/TB。
- final answer only source artifacts or patch。

## 5. CVDP 的 prompt 质量过滤

CVDP 的 LLM judge 对每个 datapoint 打四类分：

1. `ambiguity_score`：原 prompt 是否清楚，模型能否不反复猜测就解题。
2. `consistency_score`：prompt、input、output/reference、harness 是否一致。
3. `category_match_score`：category tag 是否准确。
4. `behavioral_match_score`：prompt 描述的行为是否匹配 reference solution 与 harness 检查。

它还允许生成 refined prompt，但论文没有正式采用自动改写结果，因为过度改写会让 prompt
变成 reference solution 的自然语言复述，削弱 benchmark 难度。

这点对 vaEVAS 很关键：我们可以做 prompt audit，但不能把 prompt 改成 gold 的逐句说明。

## 6. 对 vaEVAS 的具体改法

### 6.1 保留现有四类 form，但补强边界

当前四类 form 不需要推倒：

- `dut` 对应 spec-to-Verilog-A。
- `tb` 对应 Spectre testbench companion。
- `bugfix` 对应 faulty Verilog-A repair。
- `e2e` 对应 DUT + testbench integrated task。

应补强的是每类 form 的 public contract 结构。

### 6.2 给每类 prompt 一个 category contract

参考 CVDP，建议每个 prompt 头部加入或统一保留这些字段：

```markdown
- Form: dut | tb | bugfix | e2e
- Visible context: none | starter DUT | faulty DUT | companion DUT | docs
- Target artifact(s): ...
- Hidden evaluator: deterministic checker + EVAS/Spectre validation
- Public behavior boundary: ...
```

这个不是给模型“答案”，而是让类别边界稳定，便于审计。

### 6.3 给 bugfix 加 observed-vs-expected

bugfix prompt 可以从：

> reset-priority bug; fix it

变成：

| Scenario | Expected | Observed faulty behavior |
| --- | --- | --- |
| `rst_n` falls while pulse active | `pulse` clears promptly and pending timeout is disarmed | `pulse` remains high until the old timeout expires |

这样比直接给实现建议更像 CVDP 的 debug task，也更能体现 benchmark 的工程真实性。

### 6.4 明确 tb 不是 checker generation

我们的 `tb` prompt 应该明确：

- 这是 Spectre transient testbench artifact。
- 必须 drive public scenario。
- 必须 save public observables。
- 不要求生成 hidden checker。
- checker 是 evaluator 私有部分。

这可以避免模型把 `tb` 当成“写一堆检查逻辑”的任务。

### 6.5 L2/E2E 学 `cid005`

CVDP 的 `cid005` 是 module reuse/composition。对我们的 L2/E2E，应该显式给：

1. public sub-behavior boundaries。
2. required handoff observables。
3. composition-level objective。
4. exact artifact list。

但不能把每个内部状态如何写都铺成 gold。

## 7. 我们论文可以怎么写

可以把 CVDP 放在 related work 里作为最接近的 RTL benchmark 构造参考：

> CVDP expands hardware-code evaluation beyond single-turn RTL generation by
> organizing expert-authored tasks into workflow categories such as
> specification-to-RTL, code modification, testbench generation, checker
> generation, assertions, and debugging, with hidden harnesses and prompt
> quality filtering. vaEVAS follows the same benchmark-construction direction
> but targets behavioral Verilog-A practice: public DUT/TB/bugfix/E2E task
> contracts, deterministic checkers, and EVAS/Spectre dual validation.

要强调的差异：

1. CVDP 是 digital RTL/SystemVerilog；vaEVAS 是 behavioral Verilog-A。
2. CVDP hidden harness 多是 CocoTB/EDA 工具；vaEVAS hidden harness 是 deterministic
   checker + EVAS/Spectre dual validation。
3. CVDP 包含 checker/assertion generation；vaEVAS 把 checker 作为 benchmark 可信资产隐藏。
4. CVDP 的 agentic task 侧重 Docker agent + EDA 工具；vaEVAS 的 agent/repair 只能作为 baseline，
   主贡献仍是 vaBench + EVAS。

## 8. 下一步建议

下一步不应直接大规模改 prompts。建议先做 12 个任务的小审计：

1. 3 个 `dut`。
2. 3 个 `tb`。
3. 3 个 `bugfix`。
4. 3 个 `e2e`，优先 L2。

每个 prompt 打四项分：

- ambiguity。
- consistency。
- form/category match。
- behavioral match。

然后只改低分项，并用同一 slice 重新跑 EVAS/Spectre，要求不引入 EVAS PASS / Spectre FAIL
回归。
