# Coordination Cleanup Manifest

Date: 2026-05-21

## Goal

Reduce `coordination/` to a current paper-facing coordination surface for:

1. vaBench release package status.
2. EVAS/Spectre claim gates.
3. Verilog-A/AMS-focused related work.
4. reusable onboarding, skills, scripts, and templates.

## Removed Classes

The cleanup removes stale coordination material that could mislead future paper
writing:

1. bpack48 / benchmark-v2 / full92 status fragments from April and early May.
2. old benchmark expansion plans and remote provider probe plans.
3. generated OpenLLM-RTL Chinese translation artifacts.
4. large historical experiment ledger and one-off audit datasets.
5. outdated onboarding pages that direct contributors to benchmark-v2 expansion.

## Exact Deleted Areas

1. `coordination/.github/`
2. `coordination/datasets/`
3. `coordination/docs/archive/`
4. `coordination/docs/architecture/`
5. `coordination/docs/benchmark/`
6. `coordination/docs/paper/`
7. stale files under `coordination/docs/ops/`
8. stale files under `coordination/docs/project/`
9. stale files under `coordination/onboarding/`
10. `coordination/remote-results/`
11. `coordination/scripts/`
12. `coordination/status/archive/`
13. stale dated files under `coordination/status/`
14. generated OpenLLM-RTL Chinese translation files and assets under `coordination/referencepaper/`
15. local ignored surfaces: `coordination/.claude/` and `coordination/status/local-private/`

## Preserved Classes

The cleanup preserves:

1. current source-of-truth pointer documents.
2. reference PDFs and reading map.
3. reusable repository, ops, skills, scripts, templates, and private-ignore policy.
4. archive directories already marked as historical.

## Current Source Of Truth

Use the release package reports instead of deleted coordination fragments:

```text
behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/claim_gate.md
behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/score_denominator_manifest.md
behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/dual_certification.md
behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/speed_debug_artifact.md
behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/paper_artifacts.md
```
