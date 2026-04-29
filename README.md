# vaEvas Coordination

这个仓库只做项目协作和研究叙事管理，不放主产品代码。

它回答三个问题：

1. 现在主线是什么？
2. 哪些结果可以对外同步？
3. 协作者现在应该如何扩展 benchmark？

## 当前主线

截至 2026-04-29，主线已经从早期“多终端协作修 case”收敛为：

1. `EVAS`：修复与 Spectre/Verilog-A 行为一致性相关的内核和 preflight 问题。
2. `veriloga-skills`：沉淀可复用的电路机制知识和 Spectre 兼容写法。
3. `behavioral-veriloga-eval`：保留 A/D/F/G/I 结果线、closed-set completion package、benchmark-v2 和 RAG/contract runners。
4. `coordination`：只保留当前论文叙事、远端同步清单、最终实验摘要和后续计划。

一句话版：

`A/D/F/G 是同基线 cold-start/闭环结果线；H/I 是机制引导的有限延续；92/92 completion package 是闭集 teacher/template closure；benchmark-v2 用来验证同类任务迁移。`

## 当前协作目标

当前阶段的外部分工目标是：

`扩展 behavioral-veriloga-eval benchmark。`

协作者应该围绕两条路线工作：

1. 基于原始 92 个 benchmark 做系统扰动，生成更多同类但不重复的新任务。
2. 从公开 Verilog-A/analog behavioral model/compact-model 资料中提炼可转为 EVAS-compatible Verilog-A 的新架构，再叠加扰动。
3. 为新旧 benchmark 记录 EVAS vs Spectre 时间表，证明 EVAS 的闭环成本优势。

具体任务说明见：

1. [docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md](docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md)
2. [docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md](docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md)
3. [docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md](docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md)

## 先看哪里

只读 5 个文件就能理解现在状态：

1. [status/00_CURRENT_MAINLINE.md](status/00_CURRENT_MAINLINE.md)
2. [docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md](docs/benchmark/BENCHMARK_EXPANSION_ASSIGNMENT.md)
3. [docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md](docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md)
4. [docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md](docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md)
5. [status/2026-04-29_overnight_execution_summary.md](status/2026-04-29_overnight_execution_summary.md)

如果你是第一次加入项目，再看：

1. [onboarding/COLLABORATOR_START_HERE.md](onboarding/COLLABORATOR_START_HERE.md)
2. [onboarding/00_START_HERE.md](onboarding/00_START_HERE.md)
3. [onboarding/QUICK_START.md](onboarding/QUICK_START.md)
4. [docs/project/REPOSITORIES.md](docs/project/REPOSITORIES.md)

## 目录说明

1. `docs/`
   当前项目说明、benchmark 方案、论文草稿、架构和操作文档。
2. `status/`
   当前主线状态文件。旧协作记录已经移到 `status/archive/`。
3. `datasets/`
   从实验和 H/I 审计中提炼出的轻量数据集，不放完整原始结果。
4. `remote-results/`
   外部模型或远端机器跑出的结果摘要。
5. `referencepaper/`
   参考论文和翻译材料。
6. `onboarding/`
   新成员接入文档。
7. `scripts/`
   只保留 coordination 侧的数据整理脚本。

## 清理原则

主目录只保留“当前可复用、可上传、可引用”的文件。

旧文件不直接删除，而是归档到：

1. [status/archive/2026-04-legacy-collaboration/](status/archive/2026-04-legacy-collaboration/)
2. [docs/archive/](docs/archive/)

归档文件可以用于追溯历史讨论，但不再作为当前实验或论文主线依据。

## 相关代码仓库

第一次加入时，请先看 [onboarding/COLLABORATOR_START_HERE.md](onboarding/COLLABORATOR_START_HERE.md)，里面有需要 clone 的仓库清单和每个仓库的用途。

1. `EVAS`
   模拟器与 Spectre 对齐实现。
2. `behavioral-veriloga-eval`
   benchmark、runner、任务定义和评分。
3. `veriloga-skills`
   Verilog-A 生成和审查知识库。
4. `coordination`
   当前这个仓库，负责项目管理和研究叙事。

远端同步以 [status/2026-04-29_remote_sync_final_version_manifest.md](status/2026-04-29_remote_sync_final_version_manifest.md) 为准。
