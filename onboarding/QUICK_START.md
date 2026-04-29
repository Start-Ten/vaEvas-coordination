# Quick Start

## 你如果是第一次加入，只做这 9 步

1. 先确认服务器上的实际仓库路径，或者确认应该从哪里 clone 到自己的目录
2. 读 [COLLABORATOR_START_HERE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/onboarding/COLLABORATOR_START_HERE.md)
3. 按其中清单 clone `EVAS`、`behavioral-veriloga-eval`、`veriloga-skills`、`coordination`
4. 读 [00_START_HERE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/onboarding/00_START_HERE.md)
5. 读 [skills/README.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/skills/README.md)，如果使用 agent 就安装推荐 skills
6. 读 [ISSUE_PR_WECHAT_WORKFLOW.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md)
7. 读 [2026-04-12_repo-visibility-note.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/status/2026-04-12_repo-visibility-note.md)
8. 让 AI 用这些文档给你解释“项目目标 + 你的任务”
9. 按 [ONBOARDING_CHECKLIST_TEAM.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/onboarding/ONBOARDING_CHECKLIST_TEAM.md) 配好 Git 和本地环境

如果 Cadence 环境已经通，但还没找到仓库路径：

1. 先看 [REPOSITORIES.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/project/REPOSITORIES.md)
2. 再看 [2026-04-12_repo-visibility-note.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/status/2026-04-12_repo-visibility-note.md)
3. 再看 [2026-04-08_onboarding-path-blocker.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/status/2026-04-08_onboarding-path-blocker.md)
4. 不要继续在 VNC / SSH / Cadence 上反复试错

如果你已经有 `behavioral-veriloga-eval`，但 `WORK_ASSIGNMENT` 里的任务在你本地看不到：

1. 先不要默认是自己拉错
2. 先确认你看的是否只是 `Arcadia-1/upstream/main`
3. 再按 [2026-04-12_repo-visibility-note.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/status/2026-04-12_repo-visibility-note.md) 排查 remote / branch

## 先不要做什么

1. 不要直接改代码
2. 不要直接在 `main` 上开发
3. 不要还没看清任务边界就改 runner 或评分逻辑
4. 不要只让 AI 写代码，不让 AI 先解释任务
5. 不要只在微信里报告技术问题；需要先提 issue 或 PR，再微信提醒 bucketsran

## 你现在最需要知道的三件事

1. 项目目标不是“写点 Verilog-A”，而是做一个可执行、可评分、可回归的系统。
2. 当前阶段重点是扩展 benchmark-v2，并记录 EVAS/Spectre 结果和耗时。
3. 每个人平时维护的是自己的分支或 fork；有问题提 issue，有改动提 PR 给 `BucketSran/*`，提完微信通知 bucketsran。
4. 每个正式任务都应按 `brief -> kpi -> plan -> execute -> log -> review` 的流程走。

## 你今天可以直接复制给 AI 的一句话

```text
请先阅读 coordination 里的文档，用新手能懂的话告诉我：这个项目在做什么、我今天应该先做什么、我不应该直接做什么。
```
