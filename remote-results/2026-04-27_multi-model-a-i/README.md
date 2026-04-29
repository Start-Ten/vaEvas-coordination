# Remote Multi-Model A-I Evaluation Plan

Owner to assign: `shenbufan`

Date prepared: 2026-04-27

## Goal

Run the vaEvas model comparison matrix on additional model providers, including
MiniMax and Volcengine/Doubao-class models where credentials and adapters allow.

The core scientific question is not “which model is best in one shot”, but:

1. whether EVAS feedback improves each model over its own baseline;
2. whether checker/skill/contract feedback helps across model families;
3. whether failures are model-quality failures or infrastructure/provider
   failures;
4. whether the I path can be reproduced outside the current Kimi-focused local
   run.

## Current Reference Numbers

Use [EXPERIMENT_RESULT_LEDGER.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/EXPERIMENT_RESULT_LEDGER.md)
as the source of truth before comparing remote runs.  The local 2026-04-27
Kimi A/B/C current-regression rows are **not clean baselines** because their
generated roots contain dry-run placeholder artifacts.  Until Kimi A/B/C are
rerun in a fresh generated root, remote runs should compare against the clean
2026-04-25 baseline rows and treat 2026-04-27 Kimi H/I numbers as engineering
evidence only.

| Model | A | B | C | D | E | F | G | H | I-cold-start v0 | I-runner | I-final | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `kimi-k2.5` clean 2026-04-25 | 35/92 | 43/92 | 37/92 | 46/92 | 45/92 | 53/92 | 51/92 | N/R | N/R | N/R | N/R | clean-candidate historical baseline |
| `kimi-k2.5` current 2026-04-27 | invalid | invalid | invalid | 55/92 | 54/92 | 61/92 | 58/92 | 65/92 | provisional | 74/92 | 92/92 | A/B/C polluted; H/I are engineering evidence |
| `qwen3-max-2026-01-23` clean 2026-04-25 | 25/92 | 24/92 | 25/92 | 29/92 | 26/92 | 28/92 | 25/92 | N/R | N/R | N/R | N/R | clean-candidate, verify G sample count before final use |
| `qwen3-max-2026-01-23` current 2026-04-27 | 26/92 | 24/92 | 27/92 | 29/92 | 26/92 | 28/92 | provisional | N/R | N/R | N/R | N/R | G has only 36 generated samples |

Important interpretation:

1. `A-G` are the main cross-model conditions.
2. `H` is currently an incremental repair condition, not a fully standardized
   all-model condition.
3. The existing Kimi `I-cold-start v0` is now a pipeline smoke/provisional
   result because its A anchor was contaminated.  Rerun it only after clean
   A/B/C artifacts exist.
4. `I-runner` and `I-final` are engineering admission/closure evidence, not
   cold-start model-quality numbers.

## Assignment Table

| Priority | Owner | Model / Provider | Conditions | Split | Purpose | Acceptance Gate | Expected Output |
|---|---|---|---|---|---|---|---|
| P0 | shenbufan | `MiniMax-M2.5` or current MiniMax route via Bailian | API probe, then A on 3 tasks | smoke | Verify credential and routing before full92 | 3/3 calls return parseable candidates, no auth error | Update `PROVIDER_PROBES.md`; attach raw command log |
| P0 | shenbufan | Volcengine/Doubao model chosen from available account | API adapter probe | smoke | Confirm whether current runner can call it or needs adapter | One-task generation works through an explicit provider path | Update adapter section in `PROVIDER_PROBES.md` |
| P1 | shenbufan | any provider that passes P0 | A/B/C | full92 | Establish model baseline, checker transparency, skill impact | 92 generated samples per condition or explicit missing-count explanation | Fill `RESULT_MATRIX.md` and copy `model_results.json` paths |
| P2 | shenbufan | models with P1 return rate >= 80% | D/F | full92 | Test EVAS repair without skill, one-round and multi-round | D/F finish scoring; no stale generated roots mixed across models | Fill D/F rows and failure taxonomy |
| P2 optional | shenbufan | same models as P2 | E/G | full92 | Test skill during repair | E/G finish or clear blocked reason | Fill E/G rows |
| P3 | shenbufan + Bucketsran review | top 1-2 non-Kimi models | H-on-F or H-on-G | full92 or A-failure subset | See whether signature/contract repair generalizes | Only run after F/G artifacts are stable | Separate H report, not mixed into A-G table |
| P3 | shenbufan + Bucketsran review | top 1-2 non-Kimi models | I-cold-start v0 | A-failure subset + full92 materialization | Test I path from that model's A failures | A-failure subset scored, full92 materialized and re-scored | Separate I-cold-start report |

## Condition Definitions

| Condition | Meaning | Main Runner |
|---|---|---|
| A | raw prompt, no checker, no skill, no EVAS feedback | `run_experiment_matrix.py --condition A` |
| B | checker-visible prompt, no skill, no feedback | `run_experiment_matrix.py --condition B` |
| C | checker-visible prompt + skill, no feedback | `run_experiment_matrix.py --condition C` |
| D | one EVAS-guided repair, no skill | `run_experiment_matrix.py --condition D` |
| E | one EVAS-guided repair, with skill | `run_experiment_matrix.py --condition E` |
| F | three-round EVAS-guided repair, no skill | `run_experiment_matrix.py --condition F` |
| G | three-round EVAS-guided repair, with skill | `run_experiment_matrix.py --condition G` |
| H | signature/contract-guided repair from F/G residuals | `signature_guided_h.py` after F/G |
| I-cold-start v0 | contract/card repair from A raw failures | manual sequence from A score -> contract generation -> adaptive repair -> materialization |

## Provider Notes

Current `generate.py` provider detection:

| Provider family | Current support | Required env |
|---|---|---|
| OpenAI-style `gpt-*`, `o*` | supported | `OPENAI_API_KEY` |
| Anthropic `claude-*` | supported | `ANTHROPIC_API_KEY` |
| Bailian/DashScope `qwen*`, `glm*`, `kimi*`, `minimax*`, `MiniMax*` | supported by current code path, but model/account may still fail auth | `BAILIAN_API_KEY` |
| Volcengine/Doubao | not confirmed in current runner | likely needs adapter or OpenAI-compatible base URL wiring |

Do not run Volcengine full92 until a one-task real API probe succeeds and the
provider path is written down in `PROVIDER_PROBES.md`.

## Standard Commands

Use `full86` for the current 92-task split.

### P0 Provider Smoke

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval

python3 runners/generate.py \
  --model <MODEL_NAME> \
  --output-dir generated-remote-probe-2026-04-27/<MODEL_SLUG> \
  --task and_gate_smoke \
  --task comparator_hysteresis_smoke \
  --task adpll_lock_smoke \
  --sample-idx 0 \
  --temperature 0 \
  --top-p 1 \
  --max-workers 1

python3 runners/score.py \
  --model <MODEL_SLUG> \
  --generated-dir generated-remote-probe-2026-04-27/<MODEL_SLUG> \
  --output-dir results/remote-probe-2026-04-27/<MODEL_SLUG> \
  --task and_gate_smoke \
  --task comparator_hysteresis_smoke \
  --task adpll_lock_smoke \
  --timeout-s 120 \
  --workers 1
```

### A-G Full92

Prefer one model per workspace when possible.  D-G generated roots are shared
by condition name and contain model subdirectories, so archive immediately after
each model run.

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval

python3 runners/run_experiment_matrix.py \
  --model <MODEL_NAME> \
  --split full86 \
  --condition all \
  --stage all \
  --sample-idx 0 \
  --temperature 0 \
  --top-p 1 \
  --max-tokens 4096 \
  --gen-workers 2 \
  --score-workers 4 \
  --timeout-s 180 \
  --score-save-policy contract \
  --date-tag remote-2026-04-27-<MODEL_SLUG>
```

After the run, copy the key result paths into `RESULT_MATRIX.md`:

```text
results/evas-scoring-condition-A-<MODEL_SLUG>-full86-remote-2026-04-27-<MODEL_SLUG>/model_results.json
results/evas-scoring-condition-B-<MODEL_SLUG>-full86-remote-2026-04-27-<MODEL_SLUG>/model_results.json
...
```

### H Follow-Up

Only run H after F/G finishes and after Bucketsran confirms which anchor to use.

```bash
python3 runners/signature_guided_h.py \
  --g-result-root results/evas-scoring-condition-F-<MODEL_SLUG>-full86-remote-2026-04-27-<MODEL_SLUG> \
  --anchor-root generated-table2-evas-guided-repair-3round/<MODEL_SLUG> \
  --output-root results/remote-H-on-F-2026-04-27-<MODEL_SLUG> \
  --generated-root generated-remote-H-on-F-2026-04-27-<MODEL_SLUG> \
  --timeout-s 120 \
  --workers 4
```

### I-cold-start v0 Follow-Up

Only run I-cold-start after the A result exists and the A failures are known.
Use the Kimi run as the reference pattern:

```text
results/i-cold-start-kimi-2026-04-27-final-score-subset
results/i-cold-start-kimi-2026-04-27-full92-v2-score
behavioral-veriloga-eval/refine-logs/I_COLD_START_REPLAY_20260427.md
```

The remote version must report:

1. A baseline pass count;
2. number of A failures;
3. generated contract coverage;
4. A-failure subset rescue count;
5. materialized full92 score;
6. whether any PASS candidates failed materialization and why.

## Result Update Rules

After each model:

1. update [RESULT_MATRIX.md](./RESULT_MATRIX.md);
2. update [PROVIDER_PROBES.md](./PROVIDER_PROBES.md) for API/provider status;
3. add a short entry to `coordination/status/YYYY-MM-DD_<model>_remote_ai_eval.md`;
4. if the run is paper-relevant, add one line to
   `behavioral-veriloga-eval/tables/RUN_REGISTRY.md`;
5. do not edit `coordination/docs/project/TASK_ASSIGNMENT.md` manually because
   it is auto-generated from benchmark construction rows.

## Stop Conditions

Stop and report instead of continuing if:

1. generated sample count is below 80/92 for A/B/C;
2. provider returns repeated auth/rate-limit errors;
3. D/F reuses stale B artifacts from a different model;
4. a model-specific prompt or task-name patch is required to make the method
   work;
5. scorer/checker code needs semantic changes.

Small tool fixes are allowed, but they must be documented separately from model
performance.
