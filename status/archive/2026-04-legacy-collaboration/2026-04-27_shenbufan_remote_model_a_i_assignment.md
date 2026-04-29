# Shenbufan Remote Model A-I Assignment

Date: 2026-04-27

## One-Line Task

Run vaEvas A-I style model evaluation for additional providers, starting with
MiniMax and Volcengine/Doubao candidates, and report results in the remote
result pack:

```text
coordination/remote-results/2026-04-27_multi-model-a-i/
```

## Why This Matters

Our current paper story has Kimi/Qwen local evidence, but the result ledger now
marks the 2026-04-27 Kimi A/B/C current-regression rows as contaminated by
dry-run placeholder artifacts.  The goal is to rerun other providers cleanly
and test whether EVAS feedback and the contract/card direction improve other
model families too.

Before using any local reference number, read:

```text
coordination/docs/benchmark/EXPERIMENT_RESULT_LEDGER.md
```

## Scope

### Must Do First

1. Read:
   - `coordination/remote-results/2026-04-27_multi-model-a-i/README.md`
   - `coordination/remote-results/2026-04-27_multi-model-a-i/PROVIDER_PROBES.md`
   - `coordination/remote-results/2026-04-27_multi-model-a-i/RESULT_MATRIX.md`
2. Run provider smoke probes before full92 for MiniMax and Volcengine/Doubao.
3. Update `PROVIDER_PROBES.md` with the exact model string and result path.

### Main Run

For each provider that passes the smoke gate:

1. Run `A/B/C` full92.
2. If generated sample count is at least `80/92`, run `D/F`.
3. Run `E/G` only if the model is stable and there is enough time.
4. Do not run `H` or `I-cold-start v0` until A-G results are written and
   Bucketsran confirms the anchor condition.

## Recommended Model Order

| Order | Model/provider | Reason |
|---:|---|---|
| 1 | MiniMax via Bailian route | User-requested; current `generate.py` has a likely route but auth/model availability must be verified. |
| 2 | Volcengine/Doubao account model | User-requested; may need adapter work before full92. |
| 3 | `qwen3-coder-plus` | Stable secondary code model; useful if MiniMax/Volcengine blocks. |
| 4 | `qwen3.5-plus` | Secondary general model. |
| 5 | `glm-4.7` | Probe only unless response stability is good. |

## Acceptance Criteria

A remote run is complete only when:

1. `model_results.json` exists for every completed condition.
2. `RESULT_MATRIX.md` has aggregate pass count, pass rate, generated sample
   count, failure domains, and result paths.
3. API/provider errors are separated from model behavioral failures.
4. The exact commands are saved in a status note or run log.
5. No result is reported as paper-ready if generated samples are incomplete.

## Copy-Paste Prompt For Shenbufan

```text
请你接手 vaEvas 的 remote multi-model A-I evaluation。

入口文件：
/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/remote-results/2026-04-27_multi-model-a-i/README.md

先做 P0 provider smoke：
1. MiniMax 当前账号可用模型
2. 火山引擎/Doubao 当前账号可用模型

不要直接跑 full92，先把 3-task probe 结果写到：
/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/remote-results/2026-04-27_multi-model-a-i/PROVIDER_PROBES.md

通过 smoke 后，按 README 里的 A/B/C -> D/F -> E/G -> H/I-cold-start v0 顺序跑。
每个模型跑完后更新：
/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/remote-results/2026-04-27_multi-model-a-i/RESULT_MATRIX.md

注意：
1. H 和 I-cold-start v0 不要和 A-G 混在一起解释。
2. 当前本地 Kimi A/B/C 的 2026-04-27 数字已经标记为污染基线，不能作为 clean reference。
3. 新跑的所有 provider 都必须使用 fresh generated root，禁止 dry-run placeholder 进入正式评分。
```
