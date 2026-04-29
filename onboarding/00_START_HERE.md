# 00 Start Here（新人第一入口）

如果你只看一个文件，就先看这个。

## A. 你要先做什么（10 分钟）

1. 看协作者启动页：`./COLLABORATOR_START_HERE.md`
2. 看项目定位：`../README.md`
3. 看新人最短路径：`./QUICK_START.md`
4. 看仓库/分支可见性说明：`../status/2026-04-12_repo-visibility-note.md`
5. 看可执行 SSH + bridge 手册：`./SSH_TUNNEL_DAEMON_RUNBOOK.md`

## B. 按顺序执行（第一天）

1. 环境和 Git：`./ONBOARDING_CHECKLIST_TEAM.md`
2. Virtuoso + EVAS 最小理解：`./VIRTUOSO_EVAS_TEAM_GUIDE.md`
3. 闭环验证规范：`../docs/benchmark/EVAS_VIRTUOSO_CLOSED_LOOP_BENCHMARK.md`
4. 一键 AI 指令块：`./AI_ONE_CLICK_TUNNEL_AND_LOOP_PROMPTS.md`

## C. 你应该交付什么

1. 一次 tunnel + daemon 可用证据
2. 一次 EVAS-first 闭环结果（含 consistency_report 和 gate 结果）
3. 一段 8 行以内的执行结论

## D. 如果你卡住

1. 先看：`../docs/ops/UPLOAD_PACK_NOTE.md`
2. 再按：`./AI_ONE_CLICK_TUNNEL_AND_LOOP_PROMPTS.md` 的故障定位 Prompt

## E. 如果任务名在文档里，但你本地仓库里找不到

先不要直接判断自己拉错仓库。

按这个顺序做：

1. 看：`../status/2026-04-12_repo-visibility-note.md`
2. 看：`../docs/project/REPOSITORIES.md`
3. 确认自己当前的 `remote` 和 `branch`
4. 再向负责人确认当前建议使用的 source branch / fork
