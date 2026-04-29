# EVAS vs Spectre Timing Plan

日期：2026-04-29

## 为什么要加入时间维度

vaEvas 的核心贡献不只是 EVAS 能在 voltage-domain behavioral tasks 上和 Spectre/Virtuoso 保持行为一致，还包括：

`EVAS 足够快，因此可以放进 LLM generate-simulate-repair 的内循环。`

Spectre/Virtuoso 仍然是最终验收参考，但如果每一轮候选生成、错误定位、修复尝试都调用 Spectre，闭环成本会过高。EVAS 的价值在于把大多数尝试放到快速、可批量执行的 verifier 上，最后再用 Spectre 做接受性验证。

因此论文主线应包含三条证据：

1. **Accuracy parity**
   EVAS 与 Spectre 在支持的 voltage-domain behavioral subset 上给出一致判断。
2. **Time efficiency**
   EVAS 单次验证和多轮闭环总耗时显著低于 Spectre。
3. **Feedback/data scalability**
   EVAS 的低成本验证支持多轮 repair、teacher artifact 构建、RAG/机制模板筛选和 benchmark-v2 扰动验证。

## 要回答的问题

1. 单个 task 上，EVAS 比 Spectre 快多少？
2. A/D/F/G/I 这类实验中，EVAS 内循环节省了多少总时间？
3. 如果把 Spectre 放进每一次 repair attempt，成本会高到什么程度？
4. benchmark-v2 gold validation 和 completion package validation 中，EVAS 的时间优势是否仍然存在？
5. 哪些任务 EVAS/Spectre 时间差距最大，是否与 CSV 大小、transition 数量、event density、checker 类型有关？

## 时间表模板

论文主表建议加入：

| Experiment | Scope | EVAS pass | Spectre pass | EVAS wall time | Spectre wall time | Speedup | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| A full92 validation | 92 | TBD | TBD | TBD | TBD | TBD | single-shot validation |
| D repair validation | A-fail tasks | TBD | TBD | TBD | TBD | TBD | one repair round |
| F/G repair loop | F/G attempts | TBD | TBD | TBD | TBD | TBD | multi-round inner loop |
| completion package audit | 92 | TBD | TBD | TBD | TBD | TBD | teacher/template closure |
| benchmark-v2 gold | 30 or more | TBD | TBD | TBD | TBD | TBD | transfer validation |

补充表建议加入 per-task timing：

| task_id | family | category | EVAS seconds | Spectre seconds | Speedup | CSV rows | checker type | agreement |
|---|---|---|---:|---:|---:|---:|---|---|

## 需要记录的字段

每次 EVAS 或 Spectre run 至少记录：

1. `task_id`
2. `condition`
3. `attempt_id`
4. `backend`: `evas` 或 `spectre`
5. `start_time`
6. `end_time`
7. `wall_seconds`
8. `status`: pass/fail/timeout/infra
9. `failure_class`
10. `csv_rows`
11. `checker_name`
12. `generated_root`
13. `result_root`
14. `machine`
15. `simulator_mode`: EVAS / Spectre / APS / SpectreX when relevant

## 测量原则

1. 同一个 task 的 EVAS 和 Spectre 应使用同一份 generated artifact。
2. wall time 统计应包含 compile、simulate、checker 三段，必要时额外拆分。
3. timeout 应单独统计，不要简单当成最大时间。
4. Spectre 最终验收可以只跑 EVAS PASS 或 paper-facing candidates；但时间优势估算要说明如果所有 attempts 都跑 Spectre 的反事实成本。
5. 对 repeated run，报告 median、p90 和 total，而不只报告 mean。

## 闭环成本估算

对于每个条件，记录：

```text
total_attempts = initial_generation + repair_attempts
evas_inner_loop_cost = sum(EVAS time for all attempts)
spectre_final_cost = sum(Spectre time for accepted/final candidates)
spectre_inner_loop_counterfactual = sum(Spectre time if every attempt used Spectre)
saved_time = spectre_inner_loop_counterfactual - (evas_inner_loop_cost + spectre_final_cost)
```

这能支持论文中的核心表述：

`EVAS does not replace Spectre as final acceptance; it makes the inner repair loop and teacher-data construction affordable.`

## 与 A/D/F/G/I 的关系

时间表不改变 A/D/F/G/I 的定义，但会改变论文解释方式：

1. `A`：单次生成后验证，记录 EVAS/Spectre 单次验证成本。
2. `D`：一轮 EVAS repair，证明一次反馈的收益和成本。
3. `F`：多轮 EVAS repair，重点展示 EVAS 快速内循环的必要性。
4. `G`：compile/interface/infra 类失败清理，记录减少无效 Spectre 调用的作用。
5. `H/I`：机制/RAG/contract 反馈，记录更复杂反馈是否值得额外开销。

## 与 benchmark-v2 的关系

benchmark-v2 扩展时，每个新任务除了 EVAS/Spectre pass，还要记录 timing。这样新 benchmark 不只是检验正确性，也能检验：

1. EVAS 的速度优势是否随任务复杂度保持；
2. 哪类任务适合 EVAS 内循环；
3. 哪类任务必须直接交给 Spectre；
4. RAG/机制模板是否减少 attempts，从而进一步降低总时间。

## 近期执行建议

第一轮不要追求所有历史结果补齐 timing。建议先做一个小而可信的 timing set：

1. 从原始 92 中选 20 个代表任务：
   - digital/simple：5
   - ADC/DAC：5
   - PFD/divider/PLL：5
   - sample-hold/calibration/system：5
2. 对每个任务运行同一 artifact 的 EVAS 和 Spectre。
3. 记录 compile/sim/checker wall time。
4. 汇总 median、p90、total、speedup。
5. 再扩展到 A/D/F/G 主结果线和 benchmark-v2。

这会给论文一个稳的时间证据入口，不需要等全部实验重跑完才开始写。
