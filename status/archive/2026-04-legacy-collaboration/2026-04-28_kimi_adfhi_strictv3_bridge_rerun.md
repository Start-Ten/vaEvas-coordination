# Kimi ADFHI strict-v3 bridge rerun

Start: 2026-04-28 14:34 CST

## Goal

Rebuild the Virtuoso bridge and rerun Kimi A/D/F/H/I under the same current
strict-v3 rules. Report EVAS pass rate first, then Spectre pass rate.

## Fixed Conditions

- Model: `kimi-k2.5`
- Task set: full92
- Public compatibility rule: `spectre-strict-v3`
- EVAS save policy: `contract`
- EVAS workers: `4`
- Spectre bridge env: `coordination/status/2026-04-28_virtuoso_bridge_sui.env`
- Spectre validation mode: `spectre`
- Spectre validation uses the same contract-pruned staging path as `score.py`.

## Bridge

- Rebuilt through `thu-sui -> thu-wei`.
- Tunnel status: running.
- Spectre probe: OK, Spectre 21.1.0 64bit 09/24/2022.
- CIW daemon: no response, not required for command-line Spectre validation.

## Conditions

| Condition | Meaning | EVAS result | Spectre result | Paths |
|---|---|---:|---:|---|
| A | prompt-only baseline | 25/92 (0.272) | 23/92 (0.250) | `generated-condition-A-strictv3-kimi-full92-2026-04-28-rerun`; `results/condition-A-strictv3-kimi-full92-evas-2026-04-28-rerun`; `results/condition-A-strictv3-kimi-full92-spectre-2026-04-28-rerun` |
| D | A + public Spectre/Verilog-A compatibility spec | 42/92 (0.457) | 43/92 (0.467) | `generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun`; `results/condition-D-strictv3-kimi-full92-evas-2026-04-28-rerun`; `results/condition-D-strictv3-kimi-full92-spectre-2026-04-28-rerun` |
| F | D + EVAS feedback repair loop, up to 3 rounds | 60/92 (0.652) | 58/92 (0.630) | `generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun`; `results/condition-F-strictv3-evasloop-kimi-full92-materialized-evas-2026-04-28-rerun`; `results/condition-F-strictv3-evasloop-kimi-full92-materialized-spectre-2026-04-28-rerun` |
| H | F + failure-signature/mechanism-guided repair | 61/92 (0.663) | 59/92 (0.641, synthesized from F full Spectre + 1-task delta) | `generated-condition-H-strictv3-signature-full92-materialized-kimi-2026-04-28-rerun`; `results/condition-H-strictv3-signature-full92-materialized-kimi-evas-2026-04-28-rerun`; `results/condition-H-strictv3-signature-full92-materialized-kimi-spectre-delta-2026-04-28-rerun` |
| I | H-style loop with functional-IR/contracts/mechanism cards | 62/92 (0.674) | 60/92 (0.652, synthesized from F full Spectre + 2-task delta) | `generated-condition-I-strictv3-functional-ir-full92-materialized-kimi-2026-04-28-rerun`; `results/condition-I-strictv3-functional-ir-full92-materialized-kimi-evas-2026-04-28-rerun`; `results/condition-I-strictv3-functional-ir-full92-materialized-kimi-spectre-delta-2026-04-28-rerun` |

## Command Log

Commands below are appended as each stage finishes.

### Bridge

```bash
/Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite/.venv/bin/virtuoso-bridge start \
  --env coordination/status/2026-04-28_virtuoso_bridge_sui.env
```

### A generation and EVAS

```bash
cd behavioral-veriloga-eval
set -a; source .env.table2; set +a
python3 runners/generate.py \
  --model kimi-k2.5 \
  --output-dir generated-condition-A-strictv3-kimi-full92-2026-04-28-rerun \
  --public-spec-mode prompt-only \
  --max-workers 4 \
  --max-tokens 8192 \
  --artifact-retry-on-truncation \
  --artifact-retry-max-tokens 8192

python3 runners/score.py \
  --model kimi-k2.5 \
  --generated-dir generated-condition-A-strictv3-kimi-full92-2026-04-28-rerun \
  --output-dir results/condition-A-strictv3-kimi-full92-evas-2026-04-28-rerun \
  --workers 4 \
  --timeout-s 180 \
  --save-policy contract

python3 runners/spectre_validate_baseline.py \
  --model kimi-k2.5 \
  --generated-dir generated-condition-A-strictv3-kimi-full92-2026-04-28-rerun \
  --evas-results-dir results/condition-A-strictv3-kimi-full92-evas-2026-04-28-rerun \
  --output-dir results/condition-A-strictv3-kimi-full92-spectre-2026-04-28-rerun \
  --env ../coordination/status/2026-04-28_virtuoso_bridge_sui.env \
  --spectre-mode spectre \
  --timeout-s 300 \
  --save-policy contract
```

A Spectre mismatches:

- `gain_extraction_smoke`: EVAS PASS, Spectre `FAIL_SPECTRE_RUN`
- `ramp_gen_smoke`: EVAS PASS, Spectre `FAIL_SPECTRE_RUN`

### D generation and EVAS

```bash
cd behavioral-veriloga-eval
set -a; source .env.table2; set +a
python3 runners/generate.py \
  --model kimi-k2.5 \
  --output-dir generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun \
  --public-spec-mode spectre-strict-v3 \
  --max-workers 4 \
  --max-tokens 8192 \
  --artifact-retry-on-truncation \
  --artifact-retry-max-tokens 8192

python3 runners/score.py \
  --model kimi-k2.5 \
  --generated-dir generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun \
  --output-dir results/condition-D-strictv3-kimi-full92-evas-2026-04-28-rerun \
  --workers 4 \
  --timeout-s 180 \
  --save-policy contract
```

D EVAS failed task list:
`coordination/status/2026-04-28_kimi_D_strictv3_rerun_fail50.txt`

D Spectre mismatch:

- `lfsr_smoke`: EVAS `FAIL_SIM_CORRECTNESS`, Spectre PASS.

### F repair and materialization

```bash
cd behavioral-veriloga-eval
TASK_ARGS=$(awk '{printf "--task %s ",$1}' ../coordination/status/2026-04-28_kimi_D_strictv3_rerun_fail50.txt)
set -a; source .env.table2; set +a
python3 runners/run_adaptive_repair.py \
  --model kimi-k2.5 $TASK_ARGS \
  --workers 4 \
  --resume \
  --source-generated-dir generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun \
  --initial-result-root results/condition-D-strictv3-kimi-full92-evas-2026-04-28-rerun \
  --generated-root generated-condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun \
  --output-root results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun \
  --max-rounds 3 \
  --patience 1 \
  --timeout-s 180 \
  --max-tokens 8192 \
  --env-file .env.table2 \
  --repair-public-spec-mode spectre-strict-v3 \
  --no-repair-skill \
  --disable-contract-diagnosis \
  --layered-only-repair

python3 runners/materialize_combined_artifacts.py \
  --base-generated generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun \
  --base-score results/condition-D-strictv3-kimi-full92-evas-2026-04-28-rerun \
  --candidate-score results/condition-F-strictv3-evasloop-kimi-full92-2026-04-28-rerun/best \
  --out-generated generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun \
  --model-slug kimi-k2.5 \
  --overwrite \
  --report-out ../coordination/status/2026-04-28_kimi_F_strictv3_materialization.md

python3 runners/score.py \
  --model kimi-k2.5 \
  --generated-dir generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun \
  --output-dir results/condition-F-strictv3-evasloop-kimi-full92-materialized-evas-2026-04-28-rerun \
  --workers 4 \
  --timeout-s 180 \
  --save-policy contract
```

F EVAS failed task list:
`coordination/status/2026-04-28_kimi_F_strictv3_rerun_fail32.txt`

F Spectre mismatches:

- `cmp_delay_smoke`: EVAS PASS, Spectre `FAIL_SPECTRE_RUN`
- `dwa_ptr_gen_smoke`: EVAS PASS, Spectre `FAIL_SPECTRE_RUN`
- `gray_counter_one_bit_change_smoke`: EVAS PASS, Spectre `FAIL_SIM_CORRECTNESS`
- `lfsr_smoke`: EVAS `FAIL_SIM_CORRECTNESS`, Spectre PASS

### H and I repair

H repaired the F failures with failure-signature/mechanism guidance and no
contract diagnosis. It generated one replacement over F:

- `pfd_deadzone_smoke`: EVAS PASS, Spectre PASS

I used functional-IR contracts/cards generated from the F failure set:

- Contract root:
  `results/generated-behavior-contracts-I-strictv3-functional-ir-on-Ffail-kimi-2026-04-28-rerun`
- Triage:
  `coordination/status/2026-04-28_kimi_I_strictv3_Ffail_triage.json`
- It generated two replacements over F:
  - `pfd_deadzone_smoke`: EVAS PASS, Spectre PASS
  - `bad_bus_output_loop`: EVAS PASS, Spectre PASS

For Spectre rates of H/I, the full92 value is synthesized from the F full92
Spectre result plus the validated replacement deltas, because H and I only
change 1 and 2 tasks respectively.

## Final Summary

| Condition | EVAS PASS | Spectre PASS | Notes |
|---|---:|---:|---|
| A | 25/92 | 23/92 | prompt-only baseline |
| D | 42/92 | 43/92 | public strict-v3 compatibility rules |
| F | 60/92 | 58/92 | 3-round EVAS repair loop from D failures |
| H | 61/92 | 59/92 | F + failure-signature/mechanism guidance |
| I | 62/92 | 60/92 | H-style loop + functional-IR contracts/cards |

KPI status:

- Bridge restored and Spectre batch validation usable: yes.
- EVAS A/D/F/H/I rerun: yes.
- Spectre A/D/F full92 validation: yes.
- Spectre H/I validation: targeted deltas only, then exact full92 synthesis from F.
