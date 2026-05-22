# vaBench Prompt 优化计划：基于 VerilogEval v2 与 CVDP

日期：2026-05-22

目标：优化 vaBench release prompts 的清晰度、可评测性和工程真实性，同时不泄露 gold
implementation，不把 prompt engineering 变成论文主贡献。

核心原则：

1. **benchmark prompt、runner wrapper、EVAS rules 分离**。
   - `forms/*/prompt.md` 是公开 benchmark contract。
   - model/baseline runner 可额外包 `Question/Answer`、rules、markers、ICL。
   - vaEVAS 独有的电压域、EVAS/Spectre 兼容、save columns、transient 约束集中维护在
     `vaBench_evas_rules.md`，由 wrapper 注入。
   - 不要把某个模型有效的 prompt trick 固化进 benchmark 本体。

2. **先审计，再改 prompt**。
   - 不能直接大规模改 prompt。
   - 先做小 slice，按 ambiguity、consistency、form match、behavioral match 打分。
   - prompt 改动会影响基准分母和可比性，必须记录版本。

3. **优化目标不是让任务变简单**。
   - VerilogEval v2 的规则和 extraction 是为了减少无意义格式错误。
   - CVDP 的 category contract 是为了减少任务模糊和 harness 不一致。
   - 不能把 hidden checker 或 gold control flow 写成自然语言答案。

## 1. 总体路线图

| 阶段 | 目标 | 主要动作 | 产物 | 验证 |
| --- | --- | --- | --- | --- |
| P0 | 建立审计基线 | 选 12-task slice；冻结原始 prompt；整理对应 gold/checker/harness | `prompt_audit_slice.md` | slice 覆盖 `dut/tb/bugfix/e2e`，包含 L1/L2 |
| P1 | 建立 failure taxonomy | 用已有失败样本或小模型 baseline 分类失败 | `prompt_failure_taxonomy.md` | 每个失败可归到 compile/interface/runtime/waveform/semantic |
| P2 | Prompt 质量评分 | 按 CVDP 四项评分：ambiguity、consistency、form match、behavioral match | `prompt_audit_scores.csv/md` | 低分项有具体原因和引用 |
| P3 | 设计公共 prompt scaffold | 为 `dut/tb/bugfix/e2e` 各写一个公共模板 | `prompt_scaffold_v2.md` | 不包含 gold leakage；覆盖 public checker-facing behavior |
| P4 | 设计 runner wrapper | 学 VerilogEval v2，把 role/EVAS rules/markers/ICL 放外层 | `runner_prompt_wrappers.md` + `vaBench_evas_rules.md` | wrapper 可开关，不改变 benchmark prompt |
| P5 | 小范围改 prompt | 只改 12-task slice 的低分 prompt | prompt patch | `diff --check`、prompt leak audit |
| P6 | 重跑验证 | 用同一 slice 跑 EVAS/Spectre，检查无新 mismatch | validation report | no EVAS PASS / Spectre FAIL regression |
| P7 | 扩展到全量 | 按类别批量推广模板与规则 | release prompt v2 manifest | score denominator 和 prompt version 更新 |

## 2. 可优化角度总表

| 角度 | 来源 | 当前可能问题 | 优化动作 | 适用 form | 风险控制 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| Prompt vs wrapper 分离 | VerilogEval v2 | public prompt 混入模型调用协议，后续 baseline 不可比 | 保持 `prompt.md` 只写 task contract；runner 外层加 `Question/Answer`、rules、markers | 全部 | benchmark prompt 版本化；wrapper 作为 experiment config | P0 |
| 输出抽取边界 | VerilogEval v2 | 模型输出解释文字、多个文件边界不稳 | runner wrapper 使用 `[BEGIN file]...[DONE file]` 或现有 fenced block 解析；public prompt 保持 artifact contract | `dut/e2e/tb` | 不把 marker 强塞进 release prompt，除非评测器要求 | P1 |
| Form/category contract | CVDP | `tb`、`bugfix`、`e2e` 的任务边界可能混淆 | 每个 prompt 头部加 Form、Visible context、Target artifacts、Hidden evaluator boundary | 全部 | 只声明类别和可见边界，不泄露 checker | P1 |
| Interface contract | VerilogEval v1/v2 | module name、port order、artifact name 偶发不一致 | 统一写 module declaration、ports、parameters、artifact names；用表格或 bullet list | `dut/e2e/bugfix` | 不过度指定内部 implementation | P1 |
| EVAS/Verilog-A rules | VerilogEval v2 rules + vaEVAS | 模型使用 `reg/wire/always/initial`、错误贡献、缺 `analog begin`、不满足 EVAS/Spectre transient/save 约束 | runner wrapper 注入 `vaBench_evas_rules.md`；必要时 public prompt 加任务特定 domain/evaluator-facing constraint | 全部 | rules 是语言/仿真护栏，不是行为答案 | P1 |
| Behavioral contract completeness | CVDP behavioral match | prompt 没覆盖 checker 实际测的关键行为 | 审计 prompt vs checker；补 public behavior boundary、edge cases、reset/initial/settling | `dut/e2e/bugfix` | 不写 hidden thresholds 或 private checker logic | P1 |
| Bugfix observed-vs-expected | CVDP `cid016`、VerilogEval bug tasks | prompt 直接告诉 bug 根因，像修复提示而非 debug task | 改为 public intended behavior + representative observed mismatch 表 | `bugfix` | 避免给 gold patch control flow | P2 |
| TB stimulus/checker 边界 | CVDP `cid012/cid013` | `tb` 容易被理解为 checker generation | 明确 `tb` 是 Spectre transient wrapper/stimulus/save observables，不生成 hidden checker | `tb/e2e` | checker 仍为私有 benchmark asset | P1 |
| L2/E2E composition boundary | CVDP `cid005` | L2 prompt 只说综合目标，缺 public handoff | 加 public sub-behavior boundaries、handoff observables、composition objective | `e2e`，尤其 L2 | 不展开 gold state machine 或 exact equations | P2 |
| Failure classification loop | VerilogEval v2 | prompt 改进靠主观判断 | 建 vaEVAS failure taxonomy，按高频失败决定 rules/clarification | 全部 | 每次 prompt 修改绑定 failure class | P0 |
| Prompt quality scoring | CVDP LLM judge | prompt 是否模糊缺少量化标准 | 对每个 prompt 打 ambiguity/consistency/form match/behavioral match | 全部 | 可先人工评分，LLM judge 只做辅助 | P0 |
| ICL examples | VerilogEval v2 | 示例可能污染任务，复制 port/name | ICL 只作为 baseline variant；不放 benchmark prompt | baseline runner | 示例必须是非 gold、独立小题，且 A/B 测试 | P3 |
| Public evaluation contract | vaEVAS existing + CVDP | observables、tran setting、checker窗口不一致 | 统一 public observables、transient setting、valid sampling window 写法 | `tb/e2e/dut` | 只公开必要 evaluator-facing constraints | P1 |
| Prompt versioning | CVDP filtering + vaEVAS claim gates | prompt 修改后旧 baseline/score不可比 | 增加 prompt version manifest；记录变更原因和 affected rows | 全部 | 旧结果标注 historical；新结果重跑 | P0 |

## 3. 分 form 的具体优化计划

### 3.1 `dut`: spec-to-Verilog-A

参考：VerilogEval v2 `spec-to-RTL` + CVDP `cid003`。

| 子项 | 当前问题 | 优化方式 | 示例字段 |
| --- | --- | --- | --- |
| 开头任务句 | 有些 prompt 说 “Write artifact(s)” 不够像 instruction-tuned spec | 改成 “Implement a pure voltage-domain behavioral Verilog-A module named ...” | `I would like you to implement...` |
| Interface | 已有但格式不完全统一 | 统一 module declaration、port order、electrical ports、parameters | `Module: comparator(vdd, vss, vinp, vinn, out_p)` |
| Behavior | 有些只写 high-level behavior | 补 reset、event trigger、initial state、clamp、transition、settling | `On rising clk crossing...` |
| Idiom | 任务里不一定提醒 Verilog-A 写法 | 放入 runner wrapper rules；关键任务可保留 domain sentence | `Use voltage contributions and transition targets` |
| Observables | 已有但可统一 | 明确 companion testbench saves columns；DUT 不负责 save | `Public observables: vinp, vinn, out_p` |
| Output | 已有 | 统一 source-only contract | `Return exactly one Verilog-A file named ...` |

建议模板：

```markdown
I would like you to implement a pure voltage-domain behavioral Verilog-A module named `{module}`.

Interface:
- Ports, all `electrical`, exactly in this order: ...
- Parameters: ...

Behavior:
- ...

Public evaluation observables:
- The companion validation testbench saves: ...

Output:
- Return exactly `{artifact}` and no explanatory prose.
```

### 3.2 `tb`: Spectre transient wrapper/stimulus

参考：CVDP `cid012` 与 `cid013` 的拆分。

核心改动：明确 `tb` 不是 checker generation。

| 子项 | 当前问题 | 优化方式 |
| --- | --- | --- |
| 任务角色 | “testbench companion” 可能太泛 | 明确是 Spectre transient wrapper/stimulus/save observables |
| DUT 关系 | 有时只说 instantiate same DUT | 给 expected include/instance pattern 的 public constraints |
| Stimulus | 太泛可能导致无有效边缘或窗口 | 写 public stimulus shape：edges、levels、reset/enable windows、settling margin |
| Save columns | 已有但必须更硬 | 明确 plain scalar save names，不依赖 instance-qualified aliases |
| Checker 边界 | 容易生成额外 checker logic | 写 “Do not generate hidden checker logic; evaluator checker is external” |

建议 public sentence：

```markdown
This form asks for a Spectre transient testbench artifact: instantiate the public
behavioral DUT, drive the public stimulus scenario, and save the named observables.
Do not generate the hidden checker; the evaluator provides it separately.
```

### 3.3 `bugfix`: faulty Verilog-A repair

参考：CVDP `cid016` + VerilogEval bug tasks。

核心改动：少直接说 bug 根因，多给工程可见失败现象。

| 子项 | 当前问题 | 优化方式 |
| --- | --- | --- |
| Fault context | 已有 faulty DUT，但 prompt 可能直接暴露修复方向 | 给 intended behavior + observed mismatch |
| Observed table | 不稳定 | 加 `Scenario / Expected / Observed faulty behavior` 表 |
| Interface preservation | 已有但需统一 | 明确 module name、ports、parameters、artifact name 不变 |
| Fix scope | 可能引入 unrelated rewrite | 写 “preserve unrelated behavior” |
| Verification hint | 不能泄露 checker | 只说 public observable behavior，不写 hidden checker thresholds |

示例：

```markdown
Observed mismatch:

| Scenario | Expected | Observed faulty behavior |
| --- | --- | --- |
| `rst_n` falls while `pulse` is active | `pulse` clears promptly and pending timeout is disarmed | `pulse` remains high until the old timeout expires |
```

### 3.4 `e2e`: DUT + testbench integrated task

参考：VerilogEval v2 spec-to-RTL + CVDP `cid005` module reuse/composition。

| 子项 | 当前问题 | 优化方式 |
| --- | --- | --- |
| Artifact list | 多文件输出边界易乱 | 明确 file list、order、fenced block/marker requirements |
| Composition | L2 可能只写整体目标 | 写 public sub-behavior boundaries 和 handoff observables |
| Testbench | 可能忽略 save/tran | 将 Testbench Contract 单独列为硬约束 |
| DUT | 可能写成不可被 tb 实例化 | 将 module name/port order 与 tb instance 绑定 |
| Validation window | L2 最容易跑偏 | 写 final transient setting 和 checking-window public contract |

建议结构：

```markdown
Deliverables:
1. `{dut_file}.va`
2. `{tb_file}.scs`

DUT Contract:
- ...

Testbench Contract:
- ...

Composition-level objective:
- ...

Public handoff observables:
- ...
```

## 4. Runner wrapper 设计

VerilogEval v2 的一个关键点是：`Question/Answer`、rules、`[BEGIN]/[DONE]` 是生成脚本包装，不一定是数据集 prompt 本体。vaEVAS 应采用同样设计，并把电压域、EVAS/Spectre 兼容、save columns、transient testbench 约束集中到 `vaBench_evas_rules.md`。

### 4.1 Prompt-only baseline wrapper

```text
System:
You are a Verilog-A behavioral modeling engineer. Only write syntactically valid
Verilog-A and Spectre source artifacts.

Question:
<public prompt.md>

EVAS rules:
<selected shared rules from vaBench_evas_rules.md>

Output extraction:
Return only the requested artifact contents. If multiple files are requested,
wrap each file in a fenced block whose info string is the exact file name.

Answer:
```

### 4.2 EVAS-feedback repair wrapper

CVDP 的 agentic `system_message` 给工具协议；我们可以做 EVAS repair 版本：

```text
System:
You can inspect compile/runtime/checker feedback. Patch only the requested
artifact. Preserve public interface and output contract.

Failure summary:
- class: missing_column | syntax_error | waveform_shape | reset_priority | ...
- evidence: ...

Task:
<public prompt.md>

Answer:
<patched artifact only>
```

注意：repair wrapper 是 baseline 方法，不是 vaBench prompt 本体。

## 5. vaEVAS failure taxonomy 草案

| 类别 | 触发条件 | 可能 prompt 对策 |
| --- | --- | --- |
| `artifact_missing` | 未返回指定文件或多个文件边界不清 | 强化 output extraction wrapper |
| `module_interface_mismatch` | module name、port order、port type 不符 | 统一 Interface Contract |
| `veriloga_idiom_error` | 使用 `reg/wire/always/initial` 等数字 Verilog | runner rules 加 Verilog-A idiom |
| `spectre_syntax_error` | Spectre/OpenVAF parser error | 加 artifact-specific syntax rules |
| `missing_observable` | `tran.csv` 缺 save column | 强化 Public Observables / save scalar names |
| `event_semantics_error` | edge/cross/timer 行为不对 | 行为契约写清 threshold、direction、reset priority |
| `initial_reset_error` | 初值或 reset 窗口不对 | 加 initial condition/reset order |
| `waveform_shape_error` | transition/clamp/settling 不满足 | 写清 transition target、trf、clamp range |
| `tb_stimulus_insufficient` | tb 没提供有效 edges/levels/window | tb prompt 写 stimulus-shape requirements |
| `checker_behavior_gap` | checker 测了 prompt 未公开行为 | 修改 prompt 或 checker，优先公开必要 behavior |
| `evas_spectre_mismatch` | EVAS PASS / Spectre FAIL | prompt 不是首要修复对象，先查 evaluator/parity |

## 6. Prompt 审计表模板

每个被审计 prompt 一行：

| field | 含义 |
| --- | --- |
| `task_id` | vaBench task id |
| `form` | `dut/tb/bugfix/e2e` |
| `level` | L1/L2 |
| `ambiguity_score` | 1-10，prompt 是否清楚 |
| `consistency_score` | 1-10，prompt/gold/checker/harness 是否一致 |
| `form_match_score` | 1-10，form 是否准确 |
| `behavioral_match_score` | 1-10，prompt 是否覆盖 checker 行为 |
| `failure_classes_seen` | baseline 或历史失败类别 |
| `proposed_change` | 只写 public clarification 或 wrapper rule |
| `leakage_risk` | low/medium/high |
| `requires_rerun` | yes/no |

## 7. 建议的 12-task slice

先不要全量改，建议每类 3 个：

| form | 任务选择原则 |
| --- | --- |
| `dut` | 1 个纯组合/连续行为，1 个 event-driven，1 个带 reset/initial state |
| `tb` | 1 个简单 transient wrapper，1 个需要多边沿 stimulus，1 个 L2 companion |
| `bugfix` | 1 个 reset priority，1 个 event scheduling，1 个 output clamp/transition |
| `e2e` | 1 个 L1 integrated，2 个 L2 composition/measurement flow |

优先选已有 prompt 曾让我们感觉“不好”的任务，例如 sample/hold、one-shot、converter front-end、PLL/measurement flow 这类。

## 8. 里程碑与停止条件

| 里程碑 | 完成条件 |
| --- | --- |
| M1 审计基线 | 12-task slice 完成四项评分和 failure taxonomy |
| M2 模板定稿 | `dut/tb/bugfix/e2e` 四个 public scaffold + runner wrapper 草案 |
| M3 小范围改动 | 12-task prompt patch 完成，无 gold leakage |
| M4 重新验证 | changed slice EVAS/Spectre 通过，无 EVAS PASS / Spectre FAIL 回归 |
| M5 全量推广 | 全 release prompt 统一 form contract，更新 prompt version manifest |

停止条件：

- 如果低分主要来自 checker/gold 不一致，先修 checker/gold，不继续改 prompt。
- 如果 prompt 需要暴露 hidden checker 才能通过，说明 task/checker 边界有问题，不应靠 prompt 解决。
- 如果 prompt 改动改变 benchmark 难度，必须作为新 prompt version，不和旧 baseline 直接比较。

## 9. 论文写法上的收益

优化 prompt 后，论文可以更稳地写：

1. vaBench 的 public prompts follow a structured contract inspired by classic HDL benchmark design.
2. The prompt contract separates visible task specification from hidden deterministic checkers.
3. Prompt quality is audited using ambiguity, consistency, form match, and behavioral match criteria.
4. Verilog-A-specific idiom rules are part of evaluation harness wrappers, not the benchmark's scientific claim.
5. EVAS/Spectre dual validation remains the final judge; prompt design only reduces avoidable interface/syntax failures.
