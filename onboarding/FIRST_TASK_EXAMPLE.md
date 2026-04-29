# First Task Example

## 目标

这不是一个真实任务，而是一个给新成员跑通流程的示例。

目标是让你在第一周完成一次最小闭环：

`读文档 -> 问 AI -> 配 Git -> 选小任务 -> 产出 brief/kpi -> 执行 -> 写 log/review`

## 示例任务

建议新成员第一个任务选：

1. 文档类小任务
2. 模板类小任务
3. 一个最小 examples 回归检查

不要一开始就接：

1. 评分逻辑修改
2. runner 核心改动
3. 复杂 EVAS 行为修复

## 一个最小演练路径

### Step 1: 让 AI 先解释项目

复制 [AI_PROMPT_STARTER.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/onboarding/AI_PROMPT_STARTER.md) 里的 Prompt 1。

目标：

1. 先确认你知道项目在做什么
2. 先确认你今天不应该直接做什么

### Step 2: 检查 Git

进入你要参与的仓库，运行：

```bash
git remote -v
git status --short --branch
```

如果不确定对不对，复制 Prompt 2 给 AI。

### Step 3: 开一个最小任务分支

```bash
git checkout main
git fetch bucketsran
git merge --ff-only bucketsran/main
git push origin main
git checkout -b docs/my-first-task
```

### Step 4: 不要直接改，先做 brief 和 KPI

复制 Prompt 3 给 AI，让它先采访你，再帮你产出：

1. `brief`
2. `kpi`

文件位置一般放在：

1. `/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/briefs/`
2. `/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/kpis/`

### Step 5: 做一个最小改动

例如：

1. 补一段文档说明
2. 修一个模板命名问题
3. 补一个 onboarding 说明

### Step 6: 留下执行证据

按模板补：

1. `log`
2. `review`

至少记录：

1. 改了哪些文件
2. 用了哪些命令
3. 结果是什么
4. 还有什么没验证

### Step 7: 提交并准备 PR

```bash
git status
git add <files>
git commit -m "docs: complete first onboarding task"
git push -u origin docs/my-first-task
```

然后复制 Prompt 6 给 AI，让它帮你检查是否满足提交 PR 条件。

## 判断自己是否跑通了第一条链路

如果你完成了下面这些，就算成功：

1. 你能说清项目在做什么
2. 你的 Git remote 是对的
3. 你没有直接在 `main` 上开发
4. 你留下了 `brief/kpi/log/review`
5. 你能把改动推到自己的 fork
