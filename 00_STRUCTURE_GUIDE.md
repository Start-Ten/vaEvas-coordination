# Coordination Structure Guide

这份文件解释当前 `coordination/` 的目录结构。旧协作记录已经被归档，主目录只保留现在论文和工程主线需要的内容。

## 1. 当前阅读顺序

1. [README.md](README.md)
2. [onboarding/COLLABORATOR_START_HERE.md](onboarding/COLLABORATOR_START_HERE.md)
3. [status/00_CURRENT_MAINLINE.md](status/00_CURRENT_MAINLINE.md)
4. [docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md](docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md)
5. [docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md](docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md)
6. [docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md](docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md)
7. [skills/README.md](skills/README.md)
8. [docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md](docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md)
9. [status/2026-04-29_remote_sync_final_version_manifest.md](status/2026-04-29_remote_sync_final_version_manifest.md)
10. [docs/00_DOC_MAP.md](docs/00_DOC_MAP.md)

## 2. 目录职责

### `status/`

当前阶段的结论和同步入口。

主目录只放当前主线文件；旧 A/B 协作、Terminal B prompt、早期 H/I 调试、fail 列表、旧 qwen/kimi 探索结果统一放到 `status/archive/2026-04-legacy-collaboration/`。

当前对外协作目标是 benchmark expansion。协作者优先看 `docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md`，而不是 archive 里的历史修复记录。

同时，后续 benchmark 扩展应记录 EVAS vs Spectre timing，支撑“EVAS 作为快速闭环反馈引擎”的论文主张。

### `onboarding/`

如果你是第一次拿到这个协作库，先看 `onboarding/COLLABORATOR_START_HERE.md`。它解释项目在做什么、需要 clone 哪些仓库、每个仓库用途是什么，然后才进入 benchmark 扩展任务。

### `docs/`

项目正式文档，包括：

1. `docs/project/`：仓库分工、项目概览、失败分类。
2. `docs/benchmark/`：A/D/F/G/I 条件、benchmark-v2、结果表。
3. `docs/architecture/`：RAG、硬编码 checker 风险等架构说明。
4. `docs/paper/`：论文草稿和图表计划。
5. `docs/ops/`：远端同步、沟通和上传口径。

### `datasets/`

只放从实验中提炼出的轻量数据，例如 H/I translation audit、failure seed、cleanup ledger。完整原始结果不放这里。

### `remote-results/`

用于放 shenbufan 或其他远端机器/模型返回的结果摘要。

### `referencepaper/`

外部论文、翻译稿和与论文有关的其他发现。这里不是 benchmark 主资产。

### `onboarding/`

新人接入和第一轮任务文档。它偏团队管理，不代表最新实验结论。

### `scripts/`

coordination 侧的数据整理脚本，不包含主 runner。

### `skills/`

可分发给协作者安装的 vaEvas skills。当前包含：

1. `vaevas-workflow`：把 benchmark/runner/EVAS 工作变成 brief、KPI、plan、validation、review 的闭环。
2. `vaevas-git-sync`：检查 vaEvas 多仓库 git 状态、避免上传 private 或大体积实验噪声。

### `templates/`

issue、PR、微信通知模板。协作者提交问题或改动时优先复用这些模板。

## 3. 什么算当前主线

当前主线必须同时满足：

1. 支撑论文叙事或远端同步。
2. 能指向可复现实验结果或正式代码仓库。
3. 不只是某一次失败调试的中间记录。

因此：

1. A/D/F/G/I 总表和最终 completion package 结果保留在主目录。
2. 早期 H/I、多终端协作、失败列表和参数试错记录归档。
3. 本地 bridge 配置放入 `status/local-private/`，不进入 git。

## 4. 上传规则

上传或同步 remote 时，优先看：

1. [status/2026-04-29_remote_sync_final_version_manifest.md](status/2026-04-29_remote_sync_final_version_manifest.md)
2. [status/2026-04-29_remote_sync_upload_recommendation.md](status/2026-04-29_remote_sync_upload_recommendation.md)

一句话规则：

`上传最终代码、最终 benchmark、最终知识资产和精简结果摘要；不要上传旧 generated/results 全量目录。`

## 5. Issue/PR/微信规则

1. 有问题先在对应 `BucketSran/*` 仓库提 issue。
2. 有改动提 PR 给 `bucketsran` 的 fork，不直接推 upstream。
3. 提完 PR 后微信通知 bucketsran，微信只做提醒，技术细节必须写在 issue/PR 里。

完整规则见 [docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md](docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md)。
