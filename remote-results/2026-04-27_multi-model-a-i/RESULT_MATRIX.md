# Remote Multi-Model A-I Result Matrix

Fill this table after each remote run.  Use `N/R` for not run, `blocked` for a
real blocker, and always include the result path.

Check [EXPERIMENT_RESULT_LEDGER.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/EXPERIMENT_RESULT_LEDGER.md)
before using any local reference row.  The 2026-04-27 Kimi A/B/C rows are
currently invalid baselines due to dry-run placeholder contamination, and the
existing Kimi `I-cold-start v0` row is provisional.

## Aggregate Matrix

| Date | Owner | Model | Provider | API status | Split | A | B | C | D | E | F | G | H | I-cold-start v0 | Main result path | Notes |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 2026-04-25 | Bucketsran/Codex | `kimi-k2.5` | Bailian/Moonshot | pass | full92 | 35/92 | 43/92 | 37/92 | 46/92 | 45/92 | 53/92 | 51/92 | N/R | N/R | `behavioral-veriloga-eval/results/evas-scoring-condition-*-kimi-k2.5-full86-2026-04-25-overnight-kimi/model_results.json` | clean-candidate historical baseline; replace after clean current rerun |
| 2026-04-27 | Bucketsran/Codex | `kimi-k2.5` | Bailian/Moonshot | pass | full92 | invalid | invalid | invalid | 55/92 | 54/92 | 61/92 | 58/92 | 65/92 | provisional | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/summary.md`; `behavioral-veriloga-eval/results/i-cold-start-kimi-2026-04-27-full92-v2-score/model_results.json` | A/B/C generated roots contain dry-run placeholders; I-cold-start inherits that anchor; H/I-runner/I-final are engineering evidence |
| 2026-04-25 | Bucketsran/Codex | `qwen3-max-2026-01-23` | Bailian/Qwen | pass | full92 | 25/92 | 24/92 | 25/92 | 29/92 | 26/92 | 28/92 | 25/92 | N/R | N/R | `behavioral-veriloga-eval/results/evas-scoring-condition-*-qwen3-max-2026-01-23-full86-2026-04-25-overnight-qwen/model_results.json` | clean-candidate historical baseline |
| 2026-04-27 | Bucketsran/Codex | `qwen3-max-2026-01-23` | Bailian/Qwen | pass | full92 | 26/92 | 24/92 | 27/92 | 29/92 | 26/92 | 28/92 | provisional | N/R | N/R | `behavioral-veriloga-eval/results/current-experiment-regression-2026-04-27/summary.md` | local current reference; G has only 36 generated samples |
| TODO | shenbufan | `MiniMax-M2.5` or account-current MiniMax | Bailian/MiniMax | TODO | smoke -> full92 | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | P0 provider probe first |
| TODO | shenbufan | `doubao-<account-model>` | Volcengine | TODO | smoke -> full92 | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | needs adapter/provider probe first |
| TODO | shenbufan | `qwen3-coder-plus` | Bailian/Qwen | TODO | full92 | TODO | TODO | TODO | optional | optional | optional | optional | N/R | optional | TODO | secondary code-focused model |
| TODO | shenbufan | `qwen3.5-plus` | Bailian/Qwen | TODO | full92 | TODO | TODO | TODO | optional | optional | optional | optional | N/R | optional | TODO | secondary general model |
| TODO | shenbufan | `glm-4.7` | Bailian/GLM | TODO | smoke first | TODO | TODO | TODO | N/R | N/R | N/R | N/R | N/R | N/R | TODO | run only if return rate is acceptable |

## Required Per-Model Detail

For every completed model, add a subsection like this.

### `<MODEL_NAME>`

| Field | Value |
|---|---|
| Provider/account | TODO |
| Env vars used | TODO, do not paste secret values |
| Runner commit/branch | TODO |
| Start time / end time | TODO |
| Generated sample count A/B/C | TODO |
| Generated sample count D/E/F/G | TODO |
| Scoring timeout | TODO |
| Any scorer/checker changes | TODO |

| Condition | Pass@1 | Pass count | Generated samples | Failure domains | Result path | Notes |
|---|---:|---:|---:|---|---|---|
| A | TODO | TODO | TODO | TODO | TODO | TODO |
| B | TODO | TODO | TODO | TODO | TODO | TODO |
| C | TODO | TODO | TODO | TODO | TODO | TODO |
| D | TODO | TODO | TODO | TODO | TODO | TODO |
| E | TODO | TODO | TODO | TODO | TODO | TODO |
| F | TODO | TODO | TODO | TODO | TODO | TODO |
| G | TODO | TODO | TODO | TODO | TODO | TODO |
| H | TODO | TODO | TODO | TODO | TODO | only after review |
| I-cold-start v0 | TODO | TODO | TODO | TODO | TODO | only after review |

## Minimum Summary To Send Back

When a run is done, send:

```text
model:
provider:
conditions completed:
A/B/C sample counts:
D/F sample counts:
best cold-start condition:
delta over A:
delta over B:
main blocker:
result root:
one-sentence interpretation:
```
