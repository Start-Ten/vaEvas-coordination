# Current Mainline Snapshot

Date: 2026-05-21

## One-Line Mainline

`vaEVAS = vaBench benchmark + EVAS Spectre-aligned fast evaluator.`

The paper-facing work has moved past bpack48/benchmark-v2 coordination. The
current source of truth is the clean release package:

```text
behavioral-veriloga-eval/benchmark-vabench-release-v1/
behavioral-veriloga-eval/benchmark-vabench-release-v1/reports/
```

## Current Benchmark State

| Surface | Current role | Source of truth |
| --- | --- | --- |
| `benchmark-vabench-release-v1` | Paper-facing vaBench release package. | `benchmark-vabench-release-v1/README.md` |
| L1/L2 release entries | Scored benchmark target. | `reports/score_denominator_manifest.md` |
| L0 conformance | EVAS/Spectre diagnostic cases only. | `reports/conformance_manifest.md` |
| bpack48 / b143 / full92 / benchmark-v2 | Historical development material. | Do not use as current denominator. |

## Current Report Facts

| Claim surface | Current fact |
| --- | --- |
| Coverage target | 75 planned L1/L2 release entries. |
| Static/source completeness | 75/75 materialized entries and 259 static-certified forms. |
| Dual certification | 259 forms certified with zero dual failures and zero EVAS PASS / Spectre FAIL mismatches. |
| Score denominator | 74 certified content entries and 255 forms are score-enabled/scored. |
| L0 conformance | 4 diagnostic cases; 0 counted benchmark entries. |
| Speed/debug | Same-slice timing exists for all scored forms, but release-wide EVAS speed claim is blocked. |
| Model baselines | Pending; must report against counted release entries/forms only. |

## Current Priorities

1. Keep `manifest`, `dual_certification`, `score_denominator_manifest`, `claim_gate`, `paper_artifacts`, and Markdown exports consistent.
2. Audit L2 checker strength before using L2 rows for strong benchmark claims.
3. Investigate EVAS slow outliers before claiming any speed advantage.
4. Run minimal prompt-only / EVAS-feedback baselines after score-denominator gating.
5. Keep related work centered on recent benchmark/evaluator papers, not old model-training papers.

## Safe Wording

Use:

1. The release package defines the benchmark target and certification protocol.
2. The score denominator is enabled for certified content entries/forms.
3. The imported release evidence shows zero EVAS PASS / Spectre FAIL mismatches.
4. Speedup and model-baseline claims remain separately gated.

Avoid:

1. Claiming EVAS is faster than Spectre on the release package.
2. Treating bpack48/full92/benchmark-v2 as the current paper denominator.
3. Mixing historical provider/model rows with score-enabled release rows.
4. Treating static checks, dry-run imports, or partial historical summaries as certification evidence.
