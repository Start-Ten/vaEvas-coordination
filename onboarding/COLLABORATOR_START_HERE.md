# Collaborator Start Here

This file is for someone joining the current vaEVAS paper effort.

## One-Sentence Project

vaEVAS builds a credible Verilog-A behavioral benchmark (`vaBench`) and a
Spectre-aligned fast evaluator (`EVAS`) so LLM-generated behavioral models can
be checked with public prompts, gold assets, deterministic checkers, score
denominators, and EVAS/Spectre certification.

## Current Work

The current work is not "add more benchmark-v2 tasks." It is:

1. maintain the clean release package in `benchmark-vabench-release-v1`.
2. keep claim-gated reports consistent.
3. strengthen L2 checker quality.
4. handle speed/debug claim blockers honestly.
5. prepare Verilog-A/AMS-focused related work and paper tables.

## Repositories

| Repository | Role |
| --- | --- |
| `behavioral-veriloga-eval` | vaBench release package, reports, runner, checkers, score denominator. |
| `EVAS` | fast Verilog-A evaluator and Spectre-alignment work. |
| `veriloga-skills` | Verilog-A generation/review knowledge. |
| `coordination` | current documentation, related work, and collaboration notes. |
| `virtuoso-bridge-lite` | shared Spectre/Virtuoso bridge infrastructure when needed. |

## Start Here

1. `coordination/README.md`
2. `coordination/status/00_CURRENT_MAINLINE.md`
3. `coordination/docs/project/PROJECT_OVERVIEW.md`
4. `coordination/referencepaper/README.md`
5. `behavioral-veriloga-eval/benchmark-vabench-release-v1/README.md`
6. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/claim_gate.md`
7. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/score_denominator_manifest.md`
8. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/speed_debug_artifact.md`

## Do Not Do

1. Do not use bpack48/full92/benchmark-v2 as the current benchmark denominator.
2. Do not claim EVAS speedup from the current release timing artifact.
3. Do not report model baselines outside the score-enabled release denominator.
4. Do not cite old coordination status files as current certification evidence.
5. Do not add large raw results or simulator scratch directories to coordination.
