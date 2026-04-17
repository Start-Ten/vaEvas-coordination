# 新成员接入清单（可单独随 coordination 上传）

## 1. 目标

本清单用于在只提供 `coordination` 的情况下，仍能让新成员完整开始工作。

第一天至少完成：

1. 理解项目目标与协作规则
2. 确认代码仓库实际路径或 clone 来源
3. 完成 Git remote 检查
4. 跑通一条最小双验证流程（EVAS 预检 + Spectre 对照）

---

## 2. 必读文档（都在本仓库内）

1. `README.md`
2. `onboarding/QUICK_START.md`
3. `onboarding/NEW_MEMBER_START.md`
4. `onboarding/VIRTUOSO_EVAS_TEAM_GUIDE.md`
5. `docs/benchmark/EVAS_VIRTUOSO_CLOSED_LOOP_BENCHMARK.md`
6. `docs/project/PROJECT_OVERVIEW.md`
7. `docs/project/REPOSITORIES.md`
8. `status/2026-04-12_repo-visibility-note.md`
9. `docs/benchmark/EXAMPLE_TO_BENCHMARK_WORKFLOW.md`

---

## 3. Git 初始化检查

## 3.0 先确认仓库路径

在做任何 `git remote -v` 或 `cd <repo>/...` 之前，先确认以下信息：

1. 服务器上是否已经有团队共享仓库目录
2. 这些目录的实际路径分别是什么
3. 如果没有现成目录，应该从哪个远端地址 clone
4. 是否要求先拷贝到自己的 home 目录再开发

至少要确认这几个路径中的一种真实来源：

1. `vaEvas`
2. `behavioral-veriloga-eval`
3. `iccad/virtuoso-bridge-lite`

如果环境已通但仓库未定位，直接参考：

1. [REPOSITORIES.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/project/REPOSITORIES.md)
2. [2026-04-12_repo-visibility-note.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/status/2026-04-12_repo-visibility-note.md)
3. [2026-04-08_onboarding-path-blocker.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/status/2026-04-08_onboarding-path-blocker.md)

## 3.1 Git 初始化检查

对你要参与的代码仓库（EVAS / eval / skills）逐一检查：

1. 是否已经 fork 到个人账号
2. `origin` 是否指向个人 fork
3. `upstream` 是否指向团队主仓

命令：

```bash
git remote -v
```

建议同步：

```bash
git checkout main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
```

---

## 4. 执行前置环境（必须先做）

在进入 bridge 和双仿真步骤前，先完成最小环境检查。
这里默认前一节已经确认了仓库路径，否则下面的 `cd <repo>/...` 没法执行：

1. Python 3 可用：`python3 --version`
2. EVAS 仓库依赖已安装（含 `.venv`）
3. bridge 仓库依赖已安装（含 `.venv`）

示例：

```bash
cd <repo>/vaEvas/EVAS
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

cd <repo>/iccad/virtuoso-bridge-lite
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

如果你的团队已准备统一环境，请遵循团队环境规范，不重复创建。

---

## 5. 先执行 SSH 隧道与 Daemon 对齐手册（推荐）

在执行 bridge 连通命令前，先跑通：

1. `onboarding/SSH_TUNNEL_DAEMON_RUNBOOK.md`

这一步能显著减少新人在 tunneling 和 daemon 端口不匹配上的反复试错。

---

## 6. Virtuoso bridge 最小连通检查

进入 bridge 目录（路径按你机器实际情况）：

```bash
cd <repo>/iccad/virtuoso-bridge-lite
zsh ./start_thu_bridge.sh
zsh ./status_thu_bridge.sh
```

最小 SKILL 烟测：

```python
from virtuoso_bridge import BridgeClient
c = BridgeClient()
print(c.execute_skill("1+2"))
```

---

## 7. EVAS-first 闭环最小执行

在 CPPLL 示例目录执行：

```bash
cd <repo>/vaEvas/testspace/cppll
python3 run_dual_verify.py --tb tb_cppll_lock_iter2.scs --va cppll_va.va --label first_run --evas-only
python3 run_dual_verify.py --tb tb_cppll_lock_iter2.scs --va cppll_va.va --label first_run
python3 ab_gate_decision.py --baseline output/baseline_no_idt_ppm/consistency_report.json --candidate output/first_run/consistency_report.json --primary ppm_cross_delta --max-abs 1000 --evas-fix-attempt 1 --max-evas-fix-attempts 3
```

---

## 8. 首周最低交付标准

每位新成员至少提交：

1. 一次完整命令记录
2. `consistency_report.json` 路径
3. gate 结果（含 `next_action`）
4. 文字结论：本轮是否通过、下一步做什么
5. 至少 1 条 benchmark seed 的 PR

---

## 9. 失败时统一动作

1. 不一致时先修 EVAS 语义层
2. 不改矩阵求解底层原理
3. 连续多轮无效后再回看模型代码
4. 每轮必须保留可复现实验标签和结果文件
