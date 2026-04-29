# Collaborator Start Here

这份文件给第一次拿到 `coordination` 的协作者看。

不要一上来直接做 benchmark。先用 15 分钟理解：

1. 我们在做什么；
2. 你需要拉哪些仓库；
3. 每个仓库负责什么；
4. 当前阶段为什么要扩展 benchmark；
5. 你的交付物应该放在哪里。

## 1. 项目一句话

`vaEvas` 的目标是构建一个面向 Verilog-A behavioral model 的可执行生成、验证、修复和 benchmark 系统。

我们关心的不只是“LLM 写出来像不像 Verilog-A”，而是：

1. 能不能编译；
2. 能不能仿真；
3. 波形/CSV 是否满足行为 checker；
4. EVAS 的快速验证结果是否能和 Spectre/Virtuoso 最终验收对齐；
5. EVAS 是否足够快，可以支持多轮 LLM repair 和大量 benchmark/teacher-data 构建。

## 2. 当前阶段在做什么

当前阶段的主要任务是：

`扩展 behavioral-veriloga-eval benchmark。`

原因是原始 92 个任务太少，而且已经被我们用于大量闭环调试、teacher replay、completion package 和 RAG/机制模板沉淀。现在需要更多新任务来验证这些机制是否真的能泛化。

新 benchmark 来源有两类：

1. 基于原始 92 个 benchmark 做系统扰动；
2. 从公开 Verilog-A/analog behavioral/compact-model 资料中提炼新架构，再转成 benchmark。

## 3. 你需要拉哪些仓库

`vaEvas` 本地通常是一个工作目录，不是单独的 Git 仓库。你需要分别拉下面这些仓库。

### 必须拉

```bash
mkdir -p vaEvas
cd vaEvas

git clone https://github.com/BucketSran/EVAS.git
git clone https://github.com/BucketSran/behavioral-veriloga-eval.git
git clone https://github.com/BucketSran/veriloga-skills.git
git clone https://github.com/BucketSran/vaEvas-coordination.git coordination
```

如果你要提交 PR，建议先 fork 这些仓库，然后把自己的 fork 设成 `origin`，把 bucketsran fork 设成 `bucketsran` 或 `upstream`。当前协作阶段的 PR 目标是 `BucketSran/*`；是否再投 upstream 由 bucketsran 复核后决定。

### 可能需要

如果你要做 Spectre/Virtuoso 交叉验证，还需要：

```bash
git clone https://github.com/Arcadia-1/virtuoso-bridge-lite.git
```

这个仓库通常放在共享的 `iccad/` 工作目录里，不一定放在 `vaEvas/` 下面。

## 4. 每个仓库是干什么的

| 仓库 | 作用 | 你通常会改哪里 |
|---|---|---|
| `coordination` | 项目说明、分工、benchmark 扩展任务、实验叙事 | 读文档，写任务报告 |
| `behavioral-veriloga-eval` | benchmark、runner、checker、结果汇总 | 新增 `benchmark-v2/tasks/...` |
| `EVAS` | 快速 Verilog-A behavioral simulator | 一般不改，除非发现 EVAS/Spectre 不一致 |
| `veriloga-skills` | Verilog-A 生成规则和电路机制知识 | 需要沉淀新机制时再改 |
| `virtuoso-bridge-lite` | 远程 Spectre/Virtuoso 调用 | 做最终验收时使用 |

## 5. 当前任务怎么开始

按这个顺序读：

1. `coordination/README.md`
2. `coordination/status/00_CURRENT_MAINLINE.md`
3. `coordination/docs/project/REPOSITORIES.md`
4. `coordination/docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md`
5. `coordination/docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md`
6. `coordination/docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md`
7. `coordination/skills/README.md`
8. `coordination/docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md`

读完以后，你应该能回答：

1. 为什么原始 92 不够；
2. benchmark-v2 为什么要单独放；
3. 一个新 task 需要哪些文件；
4. EVAS 和 Spectre 分别在流程里负责什么；
5. 你的任务是扰动已有 benchmark，还是引入外部架构。

## 6. 新 benchmark 放在哪里

所有新任务先放在：

```text
behavioral-veriloga-eval/benchmark-v2/tasks/<task_id>/
```

不要直接放进：

```text
behavioral-veriloga-eval/tasks/
```

一个新任务至少包含：

1. `prompt.md`
2. `gold/dut.va`
3. `gold/tb_ref.scs`
4. `checker.py`
5. `meta.json`

## 7. 推荐安装的 agent skills

如果你使用 Codex/agent 协作，建议先安装本仓库打包的 skills：

```bash
cd coordination
python3 skills/install_recommended_skills.py --all
```

安装后优先使用：

1. `vaevas-workflow`：规划 benchmark/runner/checker/EVAS 改动，记录 brief、KPI 和验证。
2. `vaevas-git-sync`：提交前检查 git 状态、避免误传 private 文件或大型实验噪声。

只查看 skill 列表：

```bash
python3 skills/install_recommended_skills.py --list
```

## 8. 你的最小交付

建议每位协作者先交一个小包：

1. 从原始 92 选 2 个 seed task；
2. 每个 seed 做 3 个扰动任务；
3. 从公开资料找 1 个新机制，转成 2 个任务；
4. 合计 8 个新任务；
5. 至少 6 个 EVAS PASS；
6. 至少 4 个 Spectre PASS；
7. 写 `EXPANSION_REPORT.md`。

模板见：

`coordination/docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md`

## 9. Issue / PR / 微信通知

协作时请遵守：

1. 发现问题先提 issue。
2. 有改动提 PR 给 `BucketSran/*` 对应仓库。
3. 提完 PR 后微信通知 bucketsran。

具体规则和模板见：

1. `coordination/docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md`
2. `coordination/templates/ISSUE_TEMPLATE_BENCHMARK.md`
3. `coordination/templates/PR_DESCRIPTION_TEMPLATE.md`
4. `coordination/templates/WECHAT_NOTIFY_TEMPLATE.md`

## 10. 不要做什么

1. 不要直接修改原始 92 个任务。
2. 不要把没有许可证说明的外部模型直接复制进 benchmark。
3. 不要只写 prompt，不写 gold/checker。
4. 不要只用 EVAS PASS 宣称最终通过；需要 Spectre 交叉验证。
5. 不要把 raw LLM response、巨大 CSV、临时日志提交到远端。

## 11. 你可以复制给 AI 的启动 Prompt

```text
请阅读 coordination/README.md、coordination/status/00_CURRENT_MAINLINE.md、
coordination/docs/project/REPOSITORIES.md、
coordination/docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md、
coordination/docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md、
coordination/skills/README.md、
coordination/docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md。

然后用新手能懂的话告诉我：
1. vaEvas 现在在做什么；
2. 我需要拉哪些仓库；
3. benchmark-v2 的任务应该放在哪里；
4. 我今天应该先认领什么类型的 benchmark 扩展任务；
5. 我不应该直接做什么。
```
