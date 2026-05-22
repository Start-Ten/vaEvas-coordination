# vaEvas Skill Pack

这个目录用于分发 vaEvas 协作中常用的 Codex/agent skills。

目标不是把个人工作目录里的所有 skill 都塞进协作库，而是提供两类内容：

1. **bundled skills**：已经随 `coordination` 一起分发，协作者可以直接安装。
2. **optional external skills**：适合本项目的通用科研/实验管理技能，但来源在外部 skill 仓库或个人目录，需要按需获取。

## 1. 已打包 skills

当前随仓库分发：

| skill | 用途 | 适合什么时候用 |
|---|---|---|
| `vaevas-workflow` | 把 vaEvas 任务变成 brief/KPI/plan/validation/review 的执行闭环 | 做 release reports、checker audit、runner、EVAS、skills 或流程改动前 |
| `vaevas-git-sync` | 安全检查、提交、推送 vaEvas 多仓库改动 | 需要确认本地和 remote 是否同步、准备提交或 PR 时 |

安装到默认 Codex skill 目录：

```bash
cd /path/to/vaEvas/coordination
python3 skills/install_recommended_skills.py --all
```

只查看可用内容：

```bash
python3 skills/install_recommended_skills.py --list
```

预演安装：

```bash
python3 skills/install_recommended_skills.py --all --dry-run
```

默认安装位置是：

```text
~/.codex/skills/
```

如果你的 Codex skill 目录不同：

```bash
python3 skills/install_recommended_skills.py --all --codex-home /custom/codex/home
```

## 2. 推荐但未打包的外部 skills

`recommended-skills.json` 里列出了适合本项目的外部 skills，例如：

1. `experiment-plan`
2. `experiment-audit`
3. `experiment-queue`
4. `run-experiment`
5. `monitor-experiment`
6. `analyze-results`
7. `ablation-planner`
8. `paper-write`
9. `paper-compile`
10. `research-lit`

这些 skill 适合用来组织夜间实验、消融实验、结果审计、论文写作和文献调研。它们没有直接打包进本仓库，是为了避免把个人工具库和不相关资产整体复制进 coordination。

## 3. 使用原则

1. 对 release report、checker audit、EVAS/Spectre 对齐和 paper-facing validation 任务，优先使用 `vaevas-workflow`。
2. 对提交、同步、PR 前检查，优先使用 `vaevas-git-sync`。
3. 发现 benchmark、checker、EVAS、Spectre 对齐问题时，先按 issue/PR 流程记录，不要只在聊天里口头说明。
4. 任何包含 API key、bridge env、raw LLM response、大型仿真结果的文件都不要放进 skill 或 coordination。

协作流程见：

```text
docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md
```
