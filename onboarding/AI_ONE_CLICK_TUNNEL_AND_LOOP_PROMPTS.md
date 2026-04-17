# AI 一键执行指令块（Tunnel + Daemon + 闭环）

## 使用方式

把下面任一指令块完整复制给 AI（Copilot/Claude），并替换占位符：

1. `<repo>`：你的项目根目录
2. `<target-host>`：你在 `~/.ssh/config` 中的目标主机别名
3. `<cadence-cshrc>`：远端 Cadence 环境脚本路径

---

## Prompt 1：先做 SSH + bridge 连通

```text
请按以下步骤在终端执行，并逐步汇报结果。

目标：跑通 ssh tunneling + daemon，并确认二者匹配。

参数：
- REPO=<repo>
- HOST=<target-host>

步骤：
1) 验证 SSH 连通：
   - ssh ${HOST} 'echo ok_target && hostname'
   - ssh -o BatchMode=yes ${HOST} 'echo batch_ok'
2) 启动 bridge（优先脚本）：
   - cd ${REPO}/iccad/virtuoso-bridge-lite
   - zsh ./start_thu_bridge.sh
   - zsh ./status_thu_bridge.sh
3) 若脚本失败，使用手动兜底：
   - 终端A: ssh -N -L 5971:localhost:5971 ${HOST}
   - 终端B: cd ${REPO}/iccad/virtuoso-bridge-lite && source .venv/bin/activate && virtuoso-bridge start
   - 检查: virtuoso-bridge status
4) 做最小功能烟测（python）：
   - from virtuoso_bridge import BridgeClient
   - c = BridgeClient(); print(c.execute_skill("1+2"))

输出要求：
1) 每一步的命令和返回码
2) 最终是否确认 tunnel/daemon 可用
3) 如果失败，给出最可能原因和下一步命令
```

---

## Prompt 2：执行 EVAS-first 闭环（CPPLL）

```text
请按 EVAS-first 闭环执行 CPPLL 验证，并给出结构化结果。

参数：
- REPO=<repo>
- LABEL=<your-label>

步骤：
1) EVAS 预检：
   - cd ${REPO}/vaEvas/testspace/cppll
   - python3 run_dual_verify.py --tb tb_cppll_lock_iter2.scs --va cppll_va.va --label ${LABEL}_precheck --evas-only
2) EVAS + Spectre 全对照：
   - python3 run_dual_verify.py --tb tb_cppll_lock_iter2.scs --va cppll_va.va --label ${LABEL}
3) Gate 判定：
   - python3 ab_gate_decision.py --baseline output/baseline_no_idt_ppm/consistency_report.json --candidate output/${LABEL}/consistency_report.json --primary ppm_cross_delta --max-abs 1000 --evas-fix-attempt 1 --max-evas-fix-attempts 3

输出要求：
1) 关键指标：evas_fb_hz, spectre_fb_hz, ppm_cross_delta, rmse_vctrl_v, rmse_fb_v
2) gate decision 与 next_action
3) 一句话结论：通过/不通过 + 下一步
```

---

## Prompt 3：故障定位（只在失败时用）

```text
现在闭环失败，请做最小故障定位，不要大改。

目标：区分是环境问题、统计口径问题，还是 EVAS 语义问题。

请按顺序执行：
1) 环境：检查 bridge status、spectre 可达、输出文件是否为空
2) 数据：检查 consistency_report 是否有 NaN 或空波形
3) 口径：检查频率计边阈值和末窗设置是否一致
4) 语义：列出最可疑的 1~2 个 EVAS 事件/调度差异点

输出要求：
1) 证据化结论（含文件路径）
2) 只给一个最小修复建议
3) 修复后复跑命令
```

---

## Prompt 4：给负责人汇报（可直接发群）

```text
请将本轮结果整理成 8 行以内汇报：
1) 本轮目标
2) 执行命令（简写）
3) 关键指标
4) gate 结果
5) next_action
6) 风险
7) 需要协助
8) 下轮计划
```
