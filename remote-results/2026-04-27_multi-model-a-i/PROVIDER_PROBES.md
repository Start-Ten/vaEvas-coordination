# Provider Probe Log

Use this file before running full92 on a new model provider.

## Probe Rules

1. Never paste API keys here.
2. Record the model string exactly as passed to `generate.py`.
3. Record whether the current runner detected the expected provider.
4. Run a 3-task smoke before full92:
   `and_gate_smoke`, `comparator_hysteresis_smoke`, `adpll_lock_smoke`.
5. If a provider needs code changes, record them as adapter work, not as model
   performance.

## Probe Table

| Date | Owner | Model string | Provider | Env var | Probe tasks | Generated count | Score result | Status | Notes |
|---|---|---|---|---|---|---:|---|---|---|
| TODO | shenbufan | `MiniMax-M2.5` or actual account model | Bailian/MiniMax | `BAILIAN_API_KEY` | 3-task smoke | TODO | TODO | TODO | Current code path should route `minimax*`/`MiniMax*` through Bailian, but account auth/model availability must be verified. |
| TODO | shenbufan | `doubao-<account-model>` | Volcengine | TODO | 3-task smoke | TODO | TODO | TODO | Current runner does not have a confirmed Volcengine provider route. First confirm OpenAI-compatible endpoint or add adapter. |
| TODO | shenbufan | `qwen3-coder-plus` | Bailian/Qwen | `BAILIAN_API_KEY` | 3-task smoke or direct A/B/C | TODO | TODO | TODO | Secondary stable comparison candidate. |
| TODO | shenbufan | `qwen3.5-plus` | Bailian/Qwen | `BAILIAN_API_KEY` | 3-task smoke or direct A/B/C | TODO | TODO | TODO | Secondary stable comparison candidate. |
| TODO | shenbufan | `glm-4.7` | Bailian/GLM | `BAILIAN_API_KEY` | 3-task smoke | TODO | TODO | TODO | Probe only; do not run full repair if response timeout rate is high. |

## Probe Command Template

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

## Adapter Notes

If Volcengine/Doubao must be added to the runner, keep the change small:

1. add provider detection for the model string;
2. add env var and base URL handling;
3. keep prompt construction unchanged;
4. run the 3-task smoke;
5. only then run full92 A/B/C.
