# Daily Sync

## 每天第一件事

建议整个团队把每天的第一件事固定为：

1. 同步本仓库
2. 查看本周目标、状态、风险是否更新
3. 再同步当天涉及的代码仓库

## 推荐节奏

### Step 1: 同步顶层协作仓库

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/coordination
git checkout main
git pull
```

确认是否有更新：

1. `status/`
2. `risks/`
3. `docs/`
4. `templates/`

### Step 2: 阅读当天最相关的状态

重点看：

1. 本周目标是否变化
2. 哪些任务优先级提升
3. 是否有新的风险或依赖

### Step 3: 同步代码仓库

对当天要工作的仓库执行：

```bash
git checkout main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
```

### Step 4: 确认任务材料

开始任务前确认：

1. 是否已有 `brief`
2. 是否已有 `kpi`
3. 复杂任务是否已有 `plan`

### Step 5: 收工前做证据回填（四件套）

每天结束前，至少对当天推进的任务回填以下四项：

1. `branch + commit`：当天新增或更新的关键提交
2. `result_path`：可复核路径（例如 `results/...` 或 `testspace/...`）
3. `table_row_update`：在 `coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md` 更新对应行
4. `task_assignment_sync`：运行 `python coordination/scripts/sync_task_assignment.py` 刷新 `coordination/docs/project/TASK_ASSIGNMENT.md`

如果四项不齐：

1. 任务状态只记为 `in progress`
2. 不进入“已完成”统计
3. 次日优先补证据再开新任务

建议在收工前再跑一次：

```bash
python coordination/scripts/sync_task_assignment.py --check
```

这样可以尽早发现 `TASK_ASSIGNMENT.md` 是否仍然滞后于结果表。

## 为什么这样做

如果大家每天先同步顶层协作仓库，再进入代码仓库：

1. 目标变化会先被感知
2. 分工变化会先被感知
3. 任务优先级变化会先被感知
4. 不会出现“代码同步了，但人还在按旧目标做事”
