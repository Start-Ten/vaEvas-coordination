# Project Overview

## Project In One Sentence

`vaEVAS` builds a credible Verilog-A behavioral benchmark (`vaBench`) and a
Spectre-aligned fast evaluator (`EVAS`) for executable, claim-gated evaluation
of generated behavioral models.

## Current North Star

Publish a compact paper-facing release package with public prompts, gold assets,
deterministic checkers, score-denominator manifests, EVAS/Spectre certification,
and carefully gated speed/baseline claims.

## Current Core Claims

| Claim | Current status | Evidence surface |
| --- | --- | --- |
| vaBench release target | 75 L1/L2 entries are defined and materialized. | `benchmark-vabench-release-v1/README.md`, `reports/claim_gate.md` |
| Scored denominator | 74 certified content entries and 255 forms are score-enabled. | `reports/score_denominator_manifest.md` |
| EVAS/Spectre parity | 259 certified forms have zero EVAS PASS / Spectre FAIL mismatches. | `reports/dual_certification.md` |
| L0 separation | L0 conformance diagnostics are excluded from benchmark scoring. | `reports/conformance_manifest.md` |
| EVAS speed/debug | Timing exists, but release-wide speedup is not currently allowed. | `reports/speed_debug_artifact.md` |
| Model baselines | Pending. | Future baseline reports against counted rows only. |

## Current Architecture

| Layer | Contents | Main risk |
| --- | --- | --- |
| Benchmark layer | release entries, forms, prompts, gold DUT/TB/checkers, score denominator | Overclaiming historical or unscored rows. |
| Validator layer | static checks, EVAS validation, Spectre validation, dual certification | Any EVAS PASS / Spectre FAIL mismatch. |
| Evaluator layer | EVAS runtime, Spectre bridge, timing/debug artifact | Speed claims without same-slice evidence or outlier analysis. |
| Paper layer | claim gate, paper tables, artifact index, related work | Using stale coordination notes instead of release reports. |

## Current Read Order

1. `coordination/README.md`
2. `coordination/status/00_CURRENT_MAINLINE.md`
3. `behavioral-veriloga-eval/benchmark-vabench-release-v1/README.md`
4. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/claim_gate.md`
5. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/score_denominator_manifest.md`
6. `behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/speed_debug_artifact.md`
7. `coordination/referencepaper/README.md`

## What Is No Longer Current

The following are historical development material, not current paper-facing
denominators:

1. bpack48 / benchmark-bpack-v1.
2. b143 / benchmark-balanced.
3. full92 and closed-set 92 repair loops.
4. benchmark-v2 perturbation expansion.
5. Historical MiMo/Kimi/provider probe tables.
