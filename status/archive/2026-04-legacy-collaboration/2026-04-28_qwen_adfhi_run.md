# Qwen A/D/F/H/I Run

## Brief

Run Qwen with the same cleaned experiment story currently used for Kimi:

- `A`: clean prompt-only baseline.
- `D`: one-shot public Spectre/Verilog-A strict-v3 rules.
- `F`: D plus EVAS-only adaptive repair loop, max 3 rounds.
- `H`: based on F failures, add failure-signature/mechanism-template repair guidance.
- `I`: based on F failures, add functional-IR contracts/cards in `VAEVAS_FUNCTIONAL_IR_ONLY=1` mode.

Model: `qwen3-max-2026-01-23`.

## KPI

- Produce full92 EVAS results for A/D/F/H/I.
- Keep H/I based on F failures and materialize full92 outputs from F plus verified pass repairs.
- Keep I-clean constraints: no gold save names in live prompt inference and no task-keyword card routing.
- Attempt Spectre delta validation if the remote bridge is available; otherwise record the infra blocker explicitly.

## Execution Log

- 2026-04-28: started Qwen A/D/F/H/I run setup.
- 2026-04-28: completed Qwen `A` prompt-only full92 EVAS.
  - Generated: `behavioral-veriloga-eval/generated-condition-A-clean-qwen-full92-2026-04-28`
  - Result: `behavioral-veriloga-eval/results/condition-A-clean-qwen-full92-evas-2026-04-28/model_results.json`
  - Score: `16/92`, `Pass@1=0.1739`
- 2026-04-28: completed Qwen `D` public strict-v3 one-shot full92 EVAS.
  - Generated: `behavioral-veriloga-eval/generated-condition-D-public-strictv3-qwen-full92-2026-04-28`
  - Result: `behavioral-veriloga-eval/results/condition-D-public-strictv3-qwen-full92-evas-2026-04-28/model_results.json`
  - Score: `39/92`, `Pass@1=0.4239`
- 2026-04-28: completed Qwen `F` from D-fail adaptive EVAS loop.
  - D-fail subset: `53` tasks.
  - F subset PASS: `17/53`.
  - Materialized generated tree: `behavioral-veriloga-eval/generated-condition-F-public-strictv3-evasloop-qwen-full92-materialized-2026-04-28`
  - Original workers=8 score: `55/92`, `Pass@1=0.598`
  - Fair rerun workers=4 score: `56/92`, `Pass@1=0.6087`
  - Fair rerun result: `behavioral-veriloga-eval/results/condition-F-public-strictv3-evasloop-qwen-full92-materialized-evas-2026-04-28-rerun2/model_results.json`
- 2026-04-28: completed Qwen `H` on F-fail set.
  - F-fail subset: `37` tasks.
  - H subset PASS: `0/37`.
  - Materialized generated tree: `behavioral-veriloga-eval/generated-condition-H-signature-full92-materialized-qwen-2026-04-28`
  - Original parallel score: `54/92`, affected by `cross_sine_precision_smoke` checker timeout under concurrent scoring load.
  - Fair rerun workers=4 score: `56/92`, `Pass@1=0.6087`
  - Fair rerun result: `behavioral-veriloga-eval/results/condition-H-signature-full92-materialized-qwen-evas-2026-04-28-rerun2/model_results.json`
- 2026-04-28: completed Qwen `I` functional-IR contract/card repair on F-fail set.
  - F-fail subset: `37` tasks.
  - I subset PASS: `2/37`: `cmp_delay_smoke`, `pfd_deadzone_smoke`.
  - Contracts: `behavioral-veriloga-eval/results/generated-behavior-contracts-I-clean-functional-ir-on-Ffail-qwen-2026-04-28`
  - Materialized generated tree: `behavioral-veriloga-eval/generated-condition-I-clean-functional-ir-full92-materialized-qwen-2026-04-28`
  - Original parallel score: `55/92`, affected by `cross_sine_precision_smoke` checker timeout under concurrent scoring load.
  - Fair rerun workers=4 score: `56/92`, `Pass@1=0.6087`
  - Fair rerun result: `behavioral-veriloga-eval/results/condition-I-clean-functional-ir-full92-materialized-qwen-evas-2026-04-28-rerun2/model_results.json`

## Current Result Table

Use the fair rerun rows for `F/H/I` when comparing repair methods, because the
first H/I full92 scores were run concurrently and exposed checker timeout
noise.

| Condition | Main idea | Official EVAS result |
| --- | --- | --- |
| `A` | Clean prompt-only baseline | `16/92`, `Pass@1=0.1739` |
| `D` | Add public Spectre/Verilog-A strict-v3 generation rules | `39/92`, `Pass@1=0.4239` |
| `F` | D + EVAS-only adaptive repair loop | `56/92`, `Pass@1=0.6087` |
| `H` | F-fail + failure-signature/mechanism repair prompts | `56/92`, `Pass@1=0.6087` |
| `I` | F-fail + functional-IR contracts/cards, no task-keyword routing | `56/92`, `Pass@1=0.6087` |

## Interpretation

- Qwen benefits strongly from public strict-v3 rules: `A -> D` improves from
  `16/92` to `39/92`.
- EVAS closed-loop repair is the main gain in this model run: `D -> F` improves
  from `39/92` to `56/92`.
- H did not add new stable passes over F on this Qwen run.
- I did repair `pfd_deadzone_smoke` in the F-fail subset, but the full92 total
  remains tied with F because `cmp_delay_smoke` is timeout-sensitive across
  repeated scoring runs.
- The run confirms that scoring/checker timeout noise must be controlled when
  reporting small deltas. For `F/H/I`, use the workers=4 rerun paths above.

## Spectre Validation Status

Attempted to start `virtuoso-bridge-lite` with:

```bash
../../iccad/virtuoso-bridge-lite/.venv/bin/virtuoso-bridge start \
  --env ../../iccad/virtuoso-bridge-lite/.env
```

The bridge did not start. The remote tunnel reports:

```text
No Python interpreter found on thu-wei. Detection output: ''
```

Therefore Qwen Spectre validation is currently `INFRA_BLOCKED`. This is a
remote environment/bridge setup issue, not an EVAS repair failure or generated
artifact failure.
