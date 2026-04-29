# Terminal B Prompt: R1/R2 Repair Lane

你是 Terminal B。本轮你负责 R1 和 R2，不负责 R0/R3，也不负责最终 full92 materialization。

请先阅读：

```text
/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/status/2026-04-26_codex-ab-collaboration.md
```

## Current Context

当前官方 full92：

```text
Pass@1 = 72/92 = 0.7826
generated_root = behavioral-veriloga-eval/generated-r22-r4-combined-admission-2026-04-27/
score_root = behavioral-veriloga-eval/results/latest-system-score-r22-r4-combined-admission-2026-04-27/
```

本轮你只处理：

```text
R1 edge/digital local: 0/4 PASS
R2 DWA/PFD/calibration: 0/4 PASS
```

相关报告：

```text
behavioral-veriloga-eval/results/CONTRACT_CARD_ABLATION_r22-r1-edge-digital-2026-04-27.md
behavioral-veriloga-eval/results/CONTRACT_CARD_ABLATION_r22-r2-dwa-pfd-cal-2026-04-27.md
behavioral-veriloga-eval/results/remaining20-triage-r22-r4-combined-admission-2026-04-27.md
behavioral-veriloga-eval/results/contract-check-remaining20-r22-r4-combined-admission-2026-04-27/
```

## Your Tasks

### Lane R1: Local State/Event Repair

目标任务：

```text
timer_absolute_grid_smoke
multimod_divider_ratio_switch_smoke
flash_adc_3b_smoke
cross_sine_precision_smoke
```

你要判断每个任务失败是卡在：

1. event 没触发；
2. counter/state 没更新；
3. output target 没保存；
4. analog contribution 写在错误位置；
5. reset/enable/sample window 让行为永远不可见。

优先选一个最容易局部修复的任务做 B-owned mini。

### Lane R2: Protocol-Level Contract Repair

目标任务：

```text
dwa_ptr_gen_no_overlap_smoke
dwa_wraparound_smoke
pfd_reset_race_smoke
bg_cal
```

你要重点解决“信号动了但协议不对”的问题：

1. DWA：activity 不够，必须检查 no-overlap、active-count、pointer wrap。
2. PFD：UP/DN 必须对称响应，不能只有 UP。
3. Calibration：不能只扫 code，必须有 freeze/settle/done。

优先补一个协议级 contract/card，使 `contract PASS but official FAIL` 的情况能被 contract 抓住。

## Write Scope

你可以自由写这些 B-owned 输出：

```text
behavioral-veriloga-eval/results/R1_R2_REPAIR_B_20260427.md
behavioral-veriloga-eval/results/R1_R2_CONTRACT_CARD_DRAFT_B_20260427.json
behavioral-veriloga-eval/results/r1-r2-terminal-b-2026-04-27/
behavioral-veriloga-eval/generated-r1-r2-terminal-b-2026-04-27/
behavioral-veriloga-eval/results/CONTRACT_CARD_ABLATION_r1-r2-terminal-b-*.md
refine-logs/R1_R2_B_LOG_20260427.md
refine-logs/R1_R2_B_REVIEW_20260427.md
```

如果必须改共享文件，先在协作文档追加 LOCK：

```text
coordination/status/2026-04-26_codex-ab-collaboration.md
```

共享文件包括：

```text
behavioral-veriloga-eval/docs/CONTRACT_REPAIR_CARDS.json
behavioral-veriloga-eval/docs/BEHAVIOR_CONTRACT_TEMPLATES.md
behavioral-veriloga-eval/runners/contract_check.py
behavioral-veriloga-eval/runners/generate_behavior_contracts.py
behavioral-veriloga-eval/runners/run_contract_card_ablation.py
behavioral-veriloga-eval/runners/build_repair_prompt.py
behavioral-veriloga-eval/runners/run_adaptive_repair.py
```

## Do Not Do

1. 不要改 gold、hidden checker、prompt 或官方 scoring 语义。
2. 不要覆盖 Terminal A 的 R0/R3/full92 结果目录。
3. 不要直接把 PASS artifact 手工合并进 combined tree。
4. 不要用任务名做一对一 hidden fix；contract/card 必须能解释为公开 prompt 机制或通用机制。
5. 不要把 `sar_logic_10b` / `spectre_port_discipline` 的 alias 映射当作官方 PASS。

## Expected Output

主报告：

```text
behavioral-veriloga-eval/results/R1_R2_REPAIR_B_20260427.md
```

报告必须包含：

1. R1 四个任务的失败定位表。
2. R2 四个任务的失败定位表。
3. 你选择的第一个 B-owned mini 任务和理由。
4. 至少一个 contract/card 草案，写到：

```text
behavioral-veriloga-eval/results/R1_R2_CONTRACT_CARD_DRAFT_B_20260427.json
```

5. 如果有 mini 结果，说明：
   - score root
   - generated root
   - 是否 PASS
   - 是否有 regression 风险
6. 如果没能 PASS，给出 stop reason：是模型没补对局部逻辑、contract 太弱、infra 阻塞，还是需要 A 改共享 runner。

## Preferred First Moves

建议先做两个小闭环：

1. R1 选 `multimod_divider_ratio_switch_smoke` 或 `timer_absolute_grid_smoke`，因为失败是输出边沿为 0，定位相对清楚。
2. R2 选 `dwa_ptr_gen_no_overlap_smoke`，因为它出现了 contract PASS 但 official FAIL，最适合检验协议级 contract 是否补强。
