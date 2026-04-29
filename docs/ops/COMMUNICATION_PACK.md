# Communication Pack

## 发给新同学的最小材料包

建议发送：

1. [README.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/README.md)
2. [onboarding/COLLABORATOR_START_HERE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/onboarding/COLLABORATOR_START_HERE.md)
3. [docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md)
4. [docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md)
5. [docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md)
6. [skills/README.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/skills/README.md)
7. [docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md)

如果对方会使用 agent，再补：

1. [onboarding/AI_PROMPT_STARTER.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/onboarding/AI_PROMPT_STARTER.md)
2. [skills/recommended-skills.json](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/skills/recommended-skills.json)
3. [templates/PR_DESCRIPTION_TEMPLATE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/templates/PR_DESCRIPTION_TEMPLATE.md)

## 发给顶层管理者的最小材料包

建议发送：

1. [README.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/README.md)
2. [TEAM_PLAN.md](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/TEAM_PLAN.md)
3. [GIT_WORKFLOW.md](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/GIT_WORKFLOW.md)

如对方关心 AI 协作方式，再补：

1. [AI_WORKFLOW_OPTIMIZATION.md](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/AI_WORKFLOW_OPTIMIZATION.md)

## 给顶层的一段简短说明

可以直接概括为：

1. 当前项目目标已经明确为“Verilog-A 生成、EVAS 验证、benchmark 评分”的闭环系统。
2. 当前组织结构采用“顶层定目标、中间层控标准与质量、执行层产出任务和结果、agent 承担流程化执行”。
3. 当前中间层职责聚焦任务拆解、KPI、日志复核和标准沉淀，而不是长期承担所有执行细节。
4. 当前已补齐团队分工、AI 工作流、Git 协作规范和新成员接入清单，后续可支持多人并行协作。

## 给协作者的一段简短说明

可以直接发送：

```text
你先拉 coordination，然后读 README.md 和 onboarding/COLLABORATOR_START_HERE.md。

当前任务不是继续修旧 case，而是扩展 behavioral-veriloga-eval 的 benchmark-v2：
1. 基于原始 92 个 benchmark 做扰动；
2. 从公开 Verilog-A/analog behavioral model 资料中提炼新架构；
3. 每个新 task 都要有 prompt、gold、testbench、checker、meta；
4. 需要记录 EVAS 和 Spectre 的结果与耗时。

如果你用 Codex/agent，可以安装 coordination/skills 里的 vaevas-workflow 和 vaevas-git-sync。
发现问题先提 issue；有改动提 PR 到 BucketSran 对应仓库；提完 PR 后微信通知 bucketsran。
```
