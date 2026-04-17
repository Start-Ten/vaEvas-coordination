# Virtuoso + EVAS 团队上手参考（新成员版）

## 1. 文档目的

这份文档面向团队新成员，目标是让你在不了解 Virtuoso 的情况下，也能在 1~2 天内完成：

1. 连接远端 Virtuoso 与 Spectre
2. 理解最基础的 Virtuoso 使用方式
3. 跑通 EVAS 与 Spectre 双验证流程
4. 留下可复用、可交接的验证证据

本项目核心方向不是“只会用 Virtuoso”，而是“持续提高 EVAS 与 Virtuoso 的行为一致性，并建立有效 benchmark”。

---

## 2. 先理解三件事

### 2.1 这三者分别是什么

1. Virtuoso：Cadence 的设计环境，通常用于原理图、版图与仿真流程管理。
2. Spectre：Cadence 的仿真器，是我们当前 cross-check 的工业参考。
3. EVAS：本项目的事件驱动 Verilog-A 仿真器，是研发核心。

### 2.2 团队工作中的定位

1. EVAS 是主要研发对象。
2. Spectre 是行为对照基线。
3. 我们不追求“模型只在 EVAS 跑通”，而追求“EVAS 与 Spectre 在同一测试下行为一致”。

### 2.3 连接方式

团队目前采用 SSH bridge 方式（不是 GUI 自动化点击）：

1. 本地通过 bridge 调 Virtuoso/Spectre。
2. 远端仍由 Cadence 环境提供运行能力。
3. bridge 连通后，AI/脚本可以直接发起 SKILL、网表和 Spectre 任务。

---

## 3. 新成员环境准备清单

## 3.1 账号与网络

1. 你有可用的远端账号。
2. 你的机器可通过 SSH 登录跳板和目标主机。
3. SSH 密钥已经配置。

建议先验证：

```bash
ssh <your-host-alias>
```

## 3.2 本地目录

本项目常用目录：

1. ssh bridge：`<repo>/iccad/virtuoso-bridge-lite`
2. 研发仓库：`<repo>/vaEvas`
3. 协作仓库：`<repo>/vaEvas/coordination`

示例：`<repo>` 可以是 `/Users/<your-user>/Documents/TsingProject`。

如果你当前是在服务器上直接做环境接入，先不要假设这些目录已经存在。
应先确认：

1. 服务器上的团队共享目录在哪里
2. `vaEvas`、`behavioral-veriloga-eval`、`iccad/virtuoso-bridge-lite` 的实际路径分别是什么
3. 你应该直接进入共享目录，还是先 clone 到自己的 home 目录

常见误区不是 Cadence 没配好，而是已经连上机器了，但还不知道仓库究竟放在哪。

## 3.3 必读文档

1. `onboarding/ONBOARDING_CHECKLIST_TEAM.md`
2. `docs/benchmark/EVAS_VIRTUOSO_CLOSED_LOOP_BENCHMARK.md`
3. `onboarding/NEW_MEMBER_START.md`
4. `onboarding/SSH_TUNNEL_DAEMON_RUNBOOK.md`
5. `onboarding/AI_ONE_CLICK_TUNNEL_AND_LOOP_PROMPTS.md`

补充外部参考（在完整项目目录可用）：

1. `<repo>/sshConnect/Virtuoso桥接说明.md`
2. `<repo>/iccad/virtuoso-bridge-lite/README.md`

---

## 4. 第一次连接 Virtuoso 的标准流程

## 4.1 进入 bridge 目录

```bash
cd <repo>/iccad/virtuoso-bridge-lite
```

## 4.2 启动 bridge

```bash
zsh ./start_thu_bridge.sh
```

## 4.3 检查连接状态

```bash
zsh ./status_thu_bridge.sh
```

理想状态：

1. tunnel running
2. daemon OK
3. spectre 可用（或能定位失败原因）

## 4.4 做最小 SKILL 连通检查

```python
from virtuoso_bridge import BridgeClient

c = BridgeClient()
print(c.execute_skill("1+2"))
```

成功返回后，说明 bridge 控制链路可用。

---

## 5. 从零理解 Virtuoso 最低知识

新成员不需要先学完整模拟 IC 设计，只要先掌握这些：

1. Library：工程库。
2. Cell：设计单元。
3. View：同一个 Cell 的不同视图（schematic、symbol、layout）。
4. Netlist：用于仿真的电路描述。
5. Corner/Model：工艺与模型条件。

你在团队前两周最常见工作是：

1. 看懂 testbench 结构。
2. 发起仿真并导出关键波形。
3. 和 EVAS 输出做同窗对比。

---

## 6. 新成员执行任务的最小闭环

每次任务至少完成以下步骤：

1. 明确输入模型与 testbench。
2. 先跑 EVAS 预检（保证可执行）。
3. 再跑 Spectre 对照（同刺激、同观察窗）。
4. 计算一致性指标。
5. 写出结论：通过/不通过、下一步修复点。

不要跳过第 2 步直接跑 Spectre，也不要只凭目测波形下结论。

---

## 7. 常见问题与排查

## 7.1 `spectre: Command not found`

通常是远端 Cadence 环境未被 source。

排查顺序：

1. 检查 `.env` 的 `VB_CADENCE_CSHRC` 是否正确。
2. 查看 bridge 日志中远端命令是否包含 `source <cadence cshrc>`。
3. 远端手工验证 `which spectre`。

## 7.2 bridge 启动但无法执行 SKILL

1. 检查 tunnel 与 daemon 状态。
2. 检查 Virtuoso 是否已启动。
3. 检查是否需要在 CIW 加载 `virtuoso_setup.il`。

## 7.3 EVAS 与 Spectre 结果偏差很大

1. 先确认 testbench、激励和观察窗完全一致。
2. 先排除统计口径问题（阈值、计边方式、采样窗）。
3. 进入 EVAS 语义修复闭环，不直接改底层矩阵求解原则。

---

## 8. 当前推荐分工（可直接分配）

更完整的流程见：

1. `docs/benchmark/EXAMPLE_TO_BENCHMARK_WORKFLOW.md`

本周建议直接按“跑 example -> 做闭环 -> 提炼 benchmark -> 提 PR”的方式推进。

## 8.1 shenbufan

建议先做稳定、容易补 check 的 example：

1. `lfsr`
2. `clk_burst_gen`
3. `digital_basics`

最低交付：

1. 跑通 EVAS
2. 给出最小行为检查
3. 转成 1 条 benchmark seed
4. 把结果填进统一实验表格
5. 提 1 个 PR

## 8.2 liangyuxuan

建议先做 data-converter / calibration 向的 example：

1. `dac_binary_clk_4b`
2. `adc_dac_ideal_4b`
3. `dwa_ptr_gen`

最低交付：

1. 跑通 EVAS
2. 明确 benchmark 价值
3. 转成 1 条 benchmark seed
4. 把结果填进统一实验表格
5. 提 1 个 PR

---

## 9. 交付物清单（必须）

每个任务至少提交：

1. 运行命令（可复现）
2. 关键结果文件路径
3. 一致性指标摘要
4. gate 判定结果
5. 统一实验表格中的对应数据行
6. 下一步 action（修 EVAS 语义 / 回看模型代码）

建议额外交付：

1. 1 页排查纪要
2. 失败样例清单
3. 已验证有效的修复模式

---

## 10. 与团队目标对齐

请始终围绕以下目标行动：

1. 让 EVAS 行为逐步逼近 Virtuoso/Spectre。
2. 把“这次修好了什么”沉淀成可复用 benchmark。
3. 让新成员也能重复跑通，而不是只靠个人经验。

如果你不确定该修 EVAS 还是改模型，先按项目闭环策略执行：

1. 先修 EVAS 语义层（不改矩阵求解底层原则）。
2. 多轮无效后再回看模型假设。
