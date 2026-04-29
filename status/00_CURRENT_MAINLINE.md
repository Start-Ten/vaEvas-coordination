# 当前主线快照

日期：2026-04-29

## 这个目录现在代表什么

`coordination/status/` 现在只记录 vaEvas 当前研究主线，不再平铺所有历史协作记录。

当前主线是：

1. 为原始 92 个任务建立 strict Spectre-compatible baseline。
2. 在同一 benchmark/evaluator 条件下比较 A/D/F/G。
3. 将 H/I 作为机制引导的有限延续，同时诚实报告其局限。
4. 通过 verified teacher/template artifacts 完成原始 92 个任务的闭集 completion。
5. 用 benchmark-v2 扰动任务验证这些 artifact 是否能迁移到同类新任务。
6. 让协作者扩展 benchmark：一部分来自原始 92 的系统扰动，一部分来自公开 Verilog-A/analog behavioral model 架构转化。
7. 补充 EVAS vs Spectre 时间表，证明 EVAS 不只是结果一致，也足够快，可以承担闭环内循环和 teacher-data 构建。

## 当前协作目标

现在分发 `coordination/` 给别人时，默认任务是扩展 benchmark，而不是复盘历史修复。

协作者应该阅读：

1. `docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md`
2. `docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md`
3. `docs/benchmark/BENCHMARK_EXPANSION_PLAN.md`
4. `docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md`

交付物应该进入 `behavioral-veriloga-eval/benchmark-v2/`，不要直接污染原始 92。

## 主结果文件

| 文件 | 用途 |
|---|---|
| `2026-04-28_ADFG_same_baseline_current.md` | 同基线 A/D/F/G 结果线。 |
| `2026-04-29_HI_sequence_results.md` | H/I 结果和局限总结。 |
| `2026-04-29_overnight_execution_summary.md` | 夜间总摘要，包含 92/92 闭集 completion 的边界。 |
| `2026-04-29_closedset92_completion_ledger.md` | 92 闭集 ledger 的中文摘要。 |
| `2026-04-29_completion_package_audit.md` | completion package 审计结果。 |
| `2026-04-29_completion_package_practice_validation.md` | completion package 在 benchmark-v2 上的实践验证。 |
| `2026-04-29_benchmark_v2_gold_validation.md` | benchmark-v2 gold 的 EVAS/Spectre 验证。 |
| `2026-04-29_circuit_mechanism_rag_audit.md` | 电路机制 RAG 审计。 |
| `2026-04-29_rag_upgrade_notes.md` | RAG-v2 当前结论和下一步。 |
| `2026-04-29_remote_sync_final_version_manifest.md` | 各仓库 remote 应上传的最终文件清单。 |
| `../docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md` | 当前外部协作的 benchmark 扩展任务说明。 |
| `../docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md` | EVAS vs Spectre 时间效率实验计划。 |

## 论文表述边界

可以这样说：

1. A/D/F/G 是干净的同基线结果线。
2. H/I 展示了机制引导闭环的延续能力，但还不能宣称解决 cold-start generation。
3. 92/92 是带有 teacher/template provenance 的闭集 completion package，不是纯 cold-start LLM 结果。
4. benchmark-v2 是后续验证迁移和泛化的关键测试。
5. 时间表应作为主线证据：Spectre 是最终裁判，EVAS 是高吞吐闭环反馈引擎。

不要这样说：

1. 不要说 cold-start 达到 92/92。
2. 不要说 R26/teacher artifacts 是新鲜模型生成。
3. 不要把 archive 里的 fail list 当成当前结果表引用。

## 归档规则

历史协作记录保存在：

1. `archive/2026-04-legacy-collaboration/`

这些文件仍然可以用于追溯，但当前主线应从上面列出的文件重建。
