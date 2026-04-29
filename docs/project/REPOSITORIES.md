# Repositories

## 协作原则

所有代码仓库统一采用：

1. `origin = 个人 fork 或自己的工作 remote`
2. `bucketsran = bucketsran 的 review/integration fork`
3. `upstream = Arcadia-1 等上游公共主仓`

默认工作方式是：

1. 从 `bucketsran/main` 或负责人指定分支同步当前团队基线
2. 在本地基于最新基线开任务分支
3. 推送到自己的 `origin/<branch>`
4. 通过 PR 合回 `BucketSran/*`
5. 经 bucketsran 复核后，再决定是否向 `upstream` 提 PR

所以从协作角度看：

1. 每个人维护的是自己的 fork
2. bucketsran fork 是当前协作 review 入口
3. upstream 是对外公共主仓，不是普通协作者第一提交目标
4. 中间层负责人主要复核进入 bucketsran fork 的改动，而不是替每个人直接维护他们的开发分支

---

## 代码仓库

先说明一件容易混淆的事：

1. `vaEvas` 在本地通常是一个工作目录，不是单独的 Git 仓库根
2. 真正参与协作的是它下面的多个独立仓库
3. 新成员如果只听到“去 vaEvas 目录”，还需要继续确认具体是其中哪一个仓库

### 1. EVAS

路径：

1. [EVAS](/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS)

Git：

1. `upstream`: `https://github.com/Arcadia-1/EVAS.git`
2. `bucketsran`: `https://github.com/BucketSran/EVAS.git`
3. `origin` 示例: `https://github.com/<your-account>/EVAS.git`

用途：

1. 模拟器能力
2. 示例与测试
3. 文档

### 2. behavioral-veriloga-eval

路径：

1. [behavioral-veriloga-eval](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval)

Git：

1. `upstream`: `https://github.com/Arcadia-1/behavioral-veriloga-eval.git`
2. `bucketsran`: `https://github.com/BucketSran/behavioral-veriloga-eval.git`
3. `origin` 示例: `https://github.com/<your-account>/behavioral-veriloga-eval.git`

用途：

1. benchmark 任务
2. runner
3. 评分与结果汇总

分支可见性说明：

1. `upstream/main` 可能只包含公开基线，不保证已经合入当前阶段全部 benchmark seed
2. `coordination` 中的分工、周报、结果表，可能引用团队 fork 或 feature branch 上尚未并回 `upstream/main` 的任务
3. 如果你在 `coordination` 里看到了某个任务名，但在自己本地的 `upstream/main` 里找不到：
   - 先不要默认是自己拉错仓库
   - 先确认自己当前看的 remote 和 branch
   - 再向负责人确认“当前任务对应的 source branch / fork”

当前已知例子：

1. `coordination` 中分配给 `liangyuxuan` 的若干 `end-to-end` case
   - 例如 `adc_dac_ideal_4b_smoke`
   - `dac_binary_clk_4b_smoke`
   - `dwa_ptr_gen_smoke`
2. 这些任务不在 `Arcadia-1/behavioral-veriloga-eval` 的当前 `upstream/main`
3. 它们来自团队后续扩展 benchmark 的分支；当前已知至少有一部分位于分支：
   - `feat/new-benchmark-seeds-2026-04-05`
4. 注意：
   - 分支名前的 remote 前缀在不同人机器上可能不同
   - 例如有人是 `origin/feat/...`
   - 也有人可能是 `team/feat/...` 或其他命名

遇到这种情况时，推荐同步顺序：

1. 先在本地执行 `git remote -v`
2. 再执行 `git branch -a`
3. 再确认任务是否存在于团队 fork / feature branch
4. 只有在确认所有团队分支都不存在时，才判断为文档过期或任务名写错

### 3. veriloga-skills

路径：

1. [veriloga-skills](/Users/bucketsran/Documents/TsingProject/vaEvas/veriloga-skills)

Git：

1. `upstream`: `https://github.com/Arcadia-1/veriloga-skills.git`
2. `bucketsran`: `https://github.com/BucketSran/veriloga-skills.git`
3. `origin` 示例: `https://github.com/<your-account>/veriloga-skills.git`

用途：

1. Verilog-A 生成规则
2. EVAS/OpenVAF 验证技能
3. prompt 与技能沉淀

### 4. 共享基础设施：virtuoso-bridge-lite

路径：

1. [virtuoso-bridge-lite](/Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite)

Git：

1. 团队主仓: `https://github.com/Arcadia-1/virtuoso-bridge-lite`
2. bucketsran fork 或团队指定 fork：按负责人提供的 remote 为准
3. 个人 fork 示例: `https://github.com/<your-account>/virtuoso-bridge-lite.git`

用途：

1. SSH bridge
2. Virtuoso / Spectre 远程联通
3. Agent 与脚本侧的 SKILL / 仿真调用入口

说明：

1. 它不是 `vaEvas` 专属代码仓
2. 当前全仓只保留一份，位于 `iccad/virtuoso-bridge-lite/`
3. 由 `iccad` 线维护和同步，但供 `TsingProject` 其他项目共享使用

## 顶层协作仓库

路径：

1. [coordination](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination)

Git：

1. bucketsran: `https://github.com/BucketSran/vaEvas-coordination.git`
2. 个人 fork 示例: `https://github.com/<your-account>/vaEvas-coordination.git`

用途：

1. 统一项目目标
2. 统一分工与协作规则
3. 统一进度同步与对上汇报

重要边界：

1. `coordination` 负责告诉你“当前应该做什么”
2. 它不天然保证你本地已经拿到了对应代码分支
3. 所以当 `coordination` 与 `upstream/main` 不一致时，应优先把“分支来源说明”补到 `coordination`，而不是只在私聊里口头同步

## Issue / PR 入口

当前协作约定：

1. 有问题先在 `BucketSran/*` 对应仓库提 issue。
2. 有改动提 PR 给 `BucketSran/*`。
3. 提完 PR 后微信通知 bucketsran。
4. bucketsran 复核后再决定是否向 `Arcadia-1/*` upstream 提交。

完整流程见：

1. [../ops/ISSUE_PR_WECHAT_WORKFLOW.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/ops/ISSUE_PR_WECHAT_WORKFLOW.md)

## 工作流文档所在位置

路径：

1. [worksche](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche)

重点文档：

1. [TEAM_PLAN.md](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/TEAM_PLAN.md)
2. [AI_WORKFLOW_OPTIMIZATION.md](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/AI_WORKFLOW_OPTIMIZATION.md)
3. [GIT_WORKFLOW.md](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/GIT_WORKFLOW.md)
4. [ONBOARDING_CHECKLIST.md](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/ONBOARDING_CHECKLIST.md)
