# vaEVAS Coordination

This repository is the lightweight coordination surface for the paper-facing
vaEVAS work. It should not duplicate runner source, raw simulator output, or
historical workflow experiments.

## Current Mainline

Date: 2026-05-21

`vaEVAS = vaBench benchmark + EVAS Spectre-aligned fast evaluator.`

The current paper-facing assets are:

1. `behavioral-veriloga-eval/benchmark-vabench-release-v1/`
2. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/`
3. `EVAS/`
4. `veriloga-skills/`

The current benchmark/evaluator claims must be sourced from release reports,
not from older coordination notes.

## Claim Boundaries

Allowed current wording:

1. The release package defines a 75-entry L1/L2 vaBench target.
2. The release has 75/75 materialized entries and 259 static-certified forms.
3. The score denominator is enabled for 74 certified content entries and 255 forms.
4. The imported EVAS/Spectre evidence has zero EVAS PASS / Spectre FAIL mismatches.
5. L0 EVAS/Spectre conformance is separate from scored L1/L2 benchmark tasks.

Blocked or gated wording:

1. Do not claim an EVAS release-wide speedup. Current same-slice timing is measured, but the release-wide speed claim is blocked because aggregate EVAS wall time is not faster than Spectre.
2. Do not claim model baselines until baseline runs are reported against the enabled score denominator.
3. Do not use bpack48, benchmark-v2, full92, b143, or historical MiMo/Kimi rows as the current paper-facing benchmark denominator.

## Source Of Truth

Read these first:

1. `behavioral-veriloga-eval/benchmark-vabench-release-v1/README.md`
2. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/claim_gate.md`
3. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/score_denominator_manifest.md`
4. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/dual_certification.md`
5. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/speed_debug_artifact.md`
6. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/paper_artifacts.md`
7. `coordination/referencepaper/README.md`

## Near-Term Work

1. Keep release reports consistent: `manifest`, `dual_certification`, `score_denominator_manifest`, `claim_gate`, and `paper_artifacts`.
2. Audit L2 checker strength; shallow companion checkers should not support strong benchmark claims.
3. Stratify EVAS/Spectre timing outliers before making any speed claim.
4. Run minimal model baselines only against counted release entries/forms.
5. Keep related work current: CVDP, RealBench, ProtocolLLM, ChipBench, VeriCoder, ACE-RTL, SiliconMind-V1, and synthesis/PPA-aware RTL evaluation.

## Directory Policy

1. `referencepaper/`: current related-work PDFs and reading map.
2. `status/`: current coordination snapshot only.
3. `docs/`: project overview, repository map, paper/claim notes, and operations notes that are still current.
4. `onboarding/`: minimal contributor entry points.
5. `skills/`, `templates/`: reusable helper material.

Old coordination experiment ledgers, benchmark-v2 expansion plans, remote model probes, raw result summaries, generated translations, and stale onboarding task packs should be deleted rather than treated as current evidence.
