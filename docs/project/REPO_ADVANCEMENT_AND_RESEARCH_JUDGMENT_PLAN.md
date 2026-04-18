# vaEvas 仓库推进与研究判断执行方案

更新日期：2026-04-18

---

## 1. 这份文件解决什么问题

当前 `vaEvas` 已经不处在“从零搭 benchmark”的阶段。

更准确地说，项目已经完成了 benchmark 主线的第一轮闭环，现在最重要的问题变成了两类：

1. 仓库还要怎么继续推进，才能更稳定、更干净、更容易维护。
2. 现有结果到底支持什么研究判断，哪些结论已经站稳，哪些还只能算工程直觉。

这份文件的目的，就是把接下来的工作明确分成两条主线：

1. `仓库推进`
2. `研究判断`

这样做的好处是：

1. 避免继续把所有问题都混成“再补几个 case”
2. 避免工程完成度和研究结论边界混在一起
3. 让后续使用 `vaevas-workflow`、`experiment-plan`、`research-review`、`result-to-claim` 时有共同参照

---

## 2. 当前基线

截至 2026-04-18，`vaEvas` 的项目状态可以先概括为：

1. `behavioral-veriloga-eval` 已形成四个 benchmark family 的可执行结构。
2. 当前 family 规模为：
   - `end-to-end`: 24
   - `spec-to-va`: 18
   - `bugfix`: 7
   - `tb-generation`: 7
3. benchmark / closed-loop 当前有 24 行 `dual-validated`。
4. 当前没有 `verification_status != passed` 的 open row。
5. 近期已经完成了一批关键工程收口：
   - `sync_task_assignment.py --check` 接入维护流程
   - bridge preflight 错误分类增强
   - `save` 语法回归保护
   - Spectre-safe PWL lint
   - bugfix / tb-generation 首轮扩展

因此，项目主线已不是“有没有 benchmark”，而是：

1. 这个 benchmark 仓库是否足够稳定、可追溯、可复用
2. 这套 benchmark 与工作流到底支撑到什么研究层级

---

## 3. 总体判断

### 3.1 目前已经成立的判断

下面这些判断，已经基本可以视为项目的稳定事实：

1. `vaEvas` 已经不是概念验证，而是有实际任务、gold、runner、result table、syncer、CI 守护的 benchmark 工作区。
2. EVAS-first 的定位已经站稳。
3. dual-suite 现在的价值主要是工程闭环与 parity 证据，而不是把项目目标改成“所有任务都做双 simulator 等价比赛”。
4. `bugfix` 和 `tb-generation` 不再只是象征性 family，已经有可继续扩展的真实骨架。

### 3.2 目前还不能过度下结论的地方

下面这些判断还不能说得太满：

1. 还不能仅凭当前结果就声称“vaEvas 已覆盖 behavioral Verilog-A benchmark 的主要代表空间”。
2. 还不能仅凭当前任务数就声称“benchmark 对 agent 质量已有充分区分度”。
3. 还不能只凭一轮工程闭环就声称“skill 改进会稳定提升 Pass@1”，因为这一层还缺更系统的前后对照。
4. 还不能把“repo 已经工程上可用”和“论文 claim 已经充足”混为一谈。

---

## 4. 主线 A：仓库推进

这一条线回答的问题是：

`仓库下一步还要做什么，才能让 benchmark 真正稳定下来？`

### A0. 原则

仓库推进阶段的默认原则：

1. 优先加固已有闭环，不优先追求任务数量。
2. 优先减少维护摩擦，不优先增加新概念。
3. 只在有明确评分语义时扩 benchmark。
4. 所有状态更新都以“结果表 -> syncer -> roadmap 文档”的顺序执行。

### A1. P0：必须优先收口的工程项

这些项的优先级最高，因为它们直接影响仓库是否“看起来完成但实际上还不够稳”。

#### A1.1 metadata 与文档治理

目标：

1. 补齐 `BENCHMARK_RESULT_TABLE.md` 中仍可确认但尚未填写的 `pr_link`
2. 清理过时 notes
3. 保证 `WORK_TODO.md`、结果表、`TASK_ASSIGNMENT.md` 的状态表达一致

完成标准：

1. 结果表里不再出现明显过时的 pending / parity / workaround 表述
2. `sync_task_assignment.py --check` 长期保持 clean
3. 新协作者不需要翻聊天记录才能知道项目状态

#### A1.2 bridge / dual-suite 工作流加固

目标：

1. 继续降低 dual-suite 的使用摩擦
2. 让 preflight 输出更接近“看到就知道先查什么”
3. 减少“实际能跑，但提示看起来像失败”的误导

完成标准：

1. `run_with_bridge.sh` 成为默认入口
2. preflight note / issue 的语义对使用者足够清楚
3. 关键桥接失败能按网络、SSH、daemon、Spectre 分层归因

#### A1.3 回归保护补齐

目标：

1. 把已经踩过的坑尽量转成自动化守护
2. 继续把“人肉记忆”改成“repo 规则”

当前已有：

1. `save` 语法检查
2. PWL lint
3. runner smoke tests

接下来建议补：

1. helper 脚本 smoke
2. 结果路径存在性或 manifest 检查
3. 新任务 authoring checklist 对应的自动检查

### A2. P1：高价值 benchmark 扩展

当前 benchmark 主线已经可用，但“能继续扩”的空间依然存在。

这里的关键不是多，而是准。

优先补哪些类型：

1. `bugfix`
   - 参数极性写反
   - reset 优先级错误
   - rail 饱和遗漏
   - edge / level 敏感混淆
2. `tb-generation`
   - 更明确的测量型 bench
   - 建立时间 / 保持时间
   - 迟滞比较器
   - 锁定窗口观测
   - 频率 / 增益步进
3. `spec-to-va`
   - 更能体现行为结构而非纯模板补全的模块
4. `end-to-end`
   - 仅在评分语义足够清楚、gold 和检查容易维护时继续扩

扩展约束：

1. 不为凑数量引入难评分 case
2. 不把 benchmark 漂移成文档问答题
3. 不把 dual-suite 变成所有 family 的硬性负担

### A3. P2：skill 反哺

这一层不是“现在最急”，但价值很高。

目标：

1. 把 benchmark 中反复出现的失败模式回写到 `veriloga-skills`
2. 让后续 agent 首轮生成更贴近 benchmark 通过条件

优先回写的经验：

1. Spectre-safe testbench authoring
2. Cadence 兼容端口 / discipline 写法
3. `transition()` 使用边界
4. PLL 任务中的 task-aware parity 思路

---

## 5. 主线 B：研究判断

这一条线回答的问题是：

`我们现在到底知道了什么，还不知道什么？`

### B0. 原则

研究判断阶段要避免两种常见误差：

1. 把工程完成度误认为研究结论
2. 把“直觉上不错”误认为“结果已支持 claim”

因此这一条线的核心不是继续写代码，而是：

1. 明确问题
2. 对照证据
3. 划清边界

### B1. 现在最值得回答的四个研究问题

#### B1.1 family 覆盖是否已经足够平衡

要回答的问题：

1. 当前四个 family 是否都具有真实区分度
2. 是否仍有 family 因任务过少而显著偏弱
3. 当前任务分布是否过度偏向“容易做成 gold 的模块”

需要的证据：

1. family 数量分布
2. family 内任务类型分布
3. 各 family 的评分语义差异与维护成本

#### B1.2 EVAS-first 的定位是否已经有足够清晰的论证

要回答的问题：

1. 为什么项目不以 Spectre 作为统一评分基准
2. dual-suite 证据在项目里到底扮演什么角色
3. 哪些任务需要 parity，哪些只需要 execution evidence

需要的证据：

1. 当前 family 的 scoring policy
2. parity `required` / `not_required` 的具体案例
3. bridge / Spectre 工作流在工程层的真实摩擦

#### B1.3 benchmark 是否已经具备“有研究价值”的骨架

要回答的问题：

1. 项目是否只是内部工程整理
2. 还是已经形成“agent 评测 + failure attribution + workflow closure”的方法框架

需要的证据：

1. gold-backed tasks + executable checks
2. deterministic `Pass@1` 取向
3. failure attribution 与工程闭环
4. skill 反哺路径

#### B1.4 现有结果支持哪些 claim

要回答的问题：

1. 现在能 claim 的是“benchmark 建成”
2. 还是“某类 workflow 已经显著提升生成质量”
3. 或者仅能 claim “形成了一个可执行评测与闭环框架”

建议输出的判断层级：

1. `已支持`
2. `部分支持`
3. `仍缺关键证据`

### B2. 推荐的研究判断流程

这里不建议直接从聊天里即兴下结论。

更推荐的顺序是：

1. `research-review`
   - 让外部批判视角先指出风险点
2. `result-to-claim`
   - 再把结果和 intended claims 对齐
3. 如有必要，再回到 `experiment-plan`
   - 只补最有必要的新证据

### B3. 研究判断的停机条件

如果出现下面情况，说明应该暂停继续下结论，而不是继续往下说：

1. 同一个 claim 还没有对应的可执行证据
2. 结论依赖聊天记忆而不是结果路径 / 表格 / log
3. reviewer 风险已经指出，但还没有补证据就试图把表述写满

---

## 6. 接下来两周的推荐执行顺序

为了避免“什么都想做，结果都推进一点点”，建议顺序如下：

### 第 1 阶段：先把仓库收紧

1. 清理结果表旧 notes 与 `pr_link`
2. 保持 syncer 和 `WORK_TODO.md` 状态一致
3. 继续加固 bridge / dual-suite 的可解释性
4. 挑一小批高价值 benchmark 再扩一轮

输出物：

1. 更新后的结果表
2. clean 的 `TASK_ASSIGNMENT.md`
3. 新一轮 benchmark task 与结果路径

### 第 2 阶段：做正式研究判断

1. 对当前 benchmark 结构做一次 `research-review`
2. 对当前结果做一次 `result-to-claim`
3. 把“已支持 / 部分支持 / 仍缺证据”的边界写成项目内 memo

输出物：

1. reviewer 风险列表
2. claim 支持度矩阵
3. 下一轮补证据的最小计划

---

## 7. 推荐 skill 用法

对于当前阶段，推荐优先使用以下 skill：

### 仓库推进

1. `vaevas-workflow`
2. `experiment-plan`

推荐触发方式：

1. “请使用 `vaevas-workflow`，推进 behavioral-veriloga-eval 的下一轮收口”
2. “请使用 `experiment-plan`，围绕 benchmark 扩展与工作流加固给出具体计划”

### 研究判断

1. `research-review`
2. `result-to-claim`

推荐触发方式：

1. “请使用 `research-review`，评估 vaEvas 当前 benchmark 体系的研究质量和 reviewer 风险”
2. “请使用 `result-to-claim`，判断当前结果到底支持哪些项目结论”

---

## 8. 一句话总结

`vaEvas` 当前最重要的，不是马上写论文，而是先把 benchmark 仓库进一步收紧，并把“现有结果到底说明了什么”这件事说清楚。前者属于仓库推进，后者属于研究判断；两条线都做好了，后续无论是继续扩 benchmark，还是转入论文阶段，都会更稳。 
