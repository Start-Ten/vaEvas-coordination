# Experiment Result Ledger

Updated: 2026-04-28

This file is the small, citable index for vaEvas experiment results.  Raw
result directories remain under `behavioral-veriloga-eval/results/`, but not
every directory is paper-ready.  Use this ledger before copying numbers into
paper tables, remote assignments, or status summaries.

Condition definitions after cleanup live in
[CLEAN_EXPERIMENT_CONDITION_MATRIX.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/CLEAN_EXPERIMENT_CONDITION_MATRIX.md).

## Current Decision

The 2026-04-27 `current-experiment-regression` Kimi A/B/C rows are not clean
baselines.  Their generated roots contain dry-run placeholder artifacts:

```text
behavioral-veriloga-eval/generated-experiment/condition-A/kimi-k2.5/kimi-k2.5
behavioral-veriloga-eval/generated-experiment/condition-B/kimi-k2.5/kimi-k2.5
behavioral-veriloga-eval/generated-experiment/condition-C/kimi-k2.5/kimi-k2.5
```

Audit result:

```text
A/B/C Kimi placeholder files: 147 each
A/B/C Kimi dry_run generation_meta.json: 92 each
```

Therefore:

1. Do not cite Kimi `A=20/92`, `B=29/92`, or `C=29/92` as clean model
   performance.
2. Do not cite `I-cold-start v0=58/92` as official cold-start performance,
   because that replay started from the contaminated Kimi A baseline.
3. Keep `H-on-F`, `I-runner`, and `I-final` as engineering evidence only.
4. Clean current A reruns are now available; clean B/C, repeated-run
   uncertainty estimates, and downstream reruns are still required before the
   final paper table.

## Result Tiers

| Tier | Meaning | May Appear In Paper Main Table? |
|---|---|---|
| `clean-candidate` | No known placeholder/dry-run contamination; still may need final Spectre/Virtuoso acceptance. | Yes, with caveat if Spectre/Virtuoso is pending. |
| `superseded-clean` | Clean artifacts, but an older score pass has been replaced by a more accurate runner/checker version. | No; cite the newer clean-candidate row. |
| `engineering-evidence` | Demonstrates a repair/materialization/closure mechanism, but is not a cold-start baseline. | Appendix or method validation only. |
| `provisional` | Useful diagnostic result, but blocked by coverage, incomplete samples, or baseline uncertainty. | No, unless explicitly labeled. |
| `invalid-baseline` | Confirmed artifact contamination or stale/mixed generated roots. | No. |
| `scratch` | Local probe, ablation, or debugging run. | No. |

## Clean Candidate Baselines

Use these as the temporary baseline table until a clean 2026-04-27 rerun
replaces them.

| Date | Model | Conditions | Split | Result | Path | Status | Note |
|---|---|---|---|---:|---|---|---|
| 2026-04-25 | `kimi-k2.5` | A/B/C/D/E/F/G | full92 | A 35, B 43, C 37, D 46, E 45, F 53, G 51 | `behavioral-veriloga-eval/results/evas-scoring-condition-*-kimi-k2.5-full86-2026-04-25-overnight-kimi` | `clean-candidate` | Historical clean baseline; rerun with current guard before final paper. |
| 2026-04-28 | `kimi-k2.5` | A | full92 | A 40/92 | `behavioral-veriloga-eval/results/clean-A-r3-runnerfix-full92-2026-04-28` | `clean-candidate` | Same R3 generated artifacts as 2026-04-27, rescored after runner/checker fixes. Current clean A measurement: `dry_run=0`, `placeholder=0`, `tb-generation=11/11`, one infra from response truncation. |
| 2026-04-27 | `kimi-k2.5` | A | full92 | A 39/92 | `behavioral-veriloga-eval/results/clean-A-promptonly-kimi-2026-04-27-r3-genericprompt` | `superseded-clean` | Previous score of the same R3 artifacts before runner/checker fixes. Kept only for audit trail. |
| 2026-04-25 | `qwen3-max-2026-01-23` | A/B/C/D/E/F/G | full92 | A 25, B 24, C 25, D 29, E 26, F 28, G 25 | `behavioral-veriloga-eval/results/evas-scoring-condition-*-qwen3-max-2026-01-23-full86-2026-04-25-overnight-qwen` | `clean-candidate` | Qwen G was previously rate-limit flagged in the registry; verify sample count before final use. |
| 2026-04-27 | `kimi-k2.5` | D/E/F/H-on-F | full92 | D 55, E 54, F 61, H-on-F 65 | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/` | `clean-candidate` for D/E/F, `engineering-evidence` for H | These generated roots did not contain placeholder artifacts in the audit; H is incremental from F, not cold-start. |

## Engineering Evidence

| Date | Label | Result | Path | Status | Correct Interpretation |
|---|---|---:|---|---|---|
| 2026-04-27 | H-on-F Kimi | 65/92 | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/H-on-F-kimi` | `engineering-evidence` | Signature/contract-guided residual repair can improve over F. |
| 2026-04-27 | I-contract-runner Kimi | 74/92 | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/I-contract-runner-kimi` | `engineering-evidence` | Materialization/admission can replay independently verified PASS artifacts into full92. |
| 2026-04-27 | I-r26-final Kimi | 92/92 | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/I-r26-final-kimi` | `engineering-evidence` | Closure artifact set after R26 fixes; not a cold-start model result. |

## Invalid Or Provisional Results

| Date | Label | Reported Result | Path | Status | Reason |
|---|---|---:|---|---|---|
| 2026-04-27 | current Kimi A | 20/92 | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/A-kimi` | `invalid-baseline` | Scored dry-run placeholder artifacts mixed into the A generated root. |
| 2026-04-27 | current Kimi B | 29/92 | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/B-kimi` | `invalid-baseline` | Same placeholder/dry-run contamination. |
| 2026-04-27 | current Kimi C | 29/92 | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/C-kimi` | `invalid-baseline` | Same placeholder/dry-run contamination. |
| 2026-04-27 | I-cold-start v0 Kimi | 58/92 | `behavioral-veriloga-eval/results/i-cold-start-kimi-2026-04-27-full92-v2-score` | `provisional` | Started from contaminated A failures; keep as pipeline smoke only. |
| 2026-04-27 | G-qwen current regression | 24/92 | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/G-qwen` | `provisional` | Only 36 generated samples; not a full condition. |

## Required Cleanup Before Final Paper Numbers

1. Add scorer/generator guard: formal scoring must reject samples whose
   `generation_meta.json` has `dry_run: true`.
2. Rerun clean Kimi B/C in fresh generated roots with no placeholder files.
3. Repeat clean Kimi A enough times to estimate prompt-only trajectory
   variance; use mean/std/confidence intervals rather than a single A snapshot.
4. Rerun I-cold-start from the clean A failures.
5. Replace temporary clean-candidate rows with the clean current rerun matrix.
6. Run Spectre/Virtuoso acceptance on the final selected artifact set.
