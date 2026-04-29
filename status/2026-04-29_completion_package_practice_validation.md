# Completion Package Practice Validation

Date: 2026-04-29

## What The Completion Package Contains

The completion package is the visible, reusable bundle needed to turn the current 92-task closed-set experience into a reproducible system artifact. It includes:

- `behavioral-veriloga-eval/docs/CLOSEDSET92_COMPLETION_LEDGER.json`: task-level 92/92 acceptance ledger and provenance.
- `behavioral-veriloga-eval/docs/VERIFIED_ARTIFACT_STORE.json`: accepted/teacher artifacts with claim boundaries.
- `behavioral-veriloga-eval/docs/CLOSEDSET_CIRCUIT_TEMPLATES.json`: reusable circuit-level templates distilled from the closed set.
- `behavioral-veriloga-eval/docs/CIRCUIT_MECHANISM_SKELETONS.json`: mechanism skeletons for ADC/DAC/DWA/PFD/divider/sample-hold style tasks.
- `behavioral-veriloga-eval/docs/SPECTRE_COMPATIBILITY_TEMPLATES.json`: Spectre/Verilog-A compatibility patterns discovered during EVAS-Spectre alignment.
- `behavioral-veriloga-eval/docs/CONTRACT_REPAIR_CARDS.json`: contract/repair cards used as structured repair hints.
- `behavioral-veriloga-eval/docs/COMPLETION_PACKAGE_MANIFEST.json`: package manifest and allowed claim boundary.
- `behavioral-veriloga-eval/runners/audit_completion_package.py`: closed-set audit runner.
- `behavioral-veriloga-eval/runners/completion_package_materialize_benchmark_v2.py`: public-prompt-to-artifact materializer for same-type new tasks.
- `behavioral-veriloga-eval/runners/validate_benchmark_v2_gold.py`: shared EVAS/Spectre validator for benchmark-v2 gold or generated candidates.

## Closed-Set 92 Verification

Command:

```bash
cd behavioral-veriloga-eval
python3 runners/audit_completion_package.py
```

Result:

- Package audit pass: `True`
- Accepted tasks: `92/92`
- Provenance split:
  - G strict anchor: `65`
  - H/I continuation: `4`
  - R26 teacher replay: `13`
  - R26 teacher Spectre-fix: `10`

Important boundary: this is a closed-set completion result, not a cold-start LLM result. The package records which entries are strict baseline anchors and which entries are teacher/replay continuations.

Output:

- `behavioral-veriloga-eval/results/completion-package-audit-2026-04-29/summary.json`
- `coordination/status/2026-04-29_completion_package_audit.md`

## Same-Type New Task Verification

The package was also tested on the 30-task `benchmark-v2` set. The materializer reads public `prompt.md` files and does not read benchmark-v2 gold DUT/testbench files.

Materialization command:

```bash
cd behavioral-veriloga-eval
python3 runners/completion_package_materialize_benchmark_v2.py \
  --output-dir generated-completion-package-benchmark-v2-2026-04-29-r1 \
  --model completion-package-v0
```

Result:

- Materialized tasks: `30/30`
- Generated files: `90`
- Generated root: `behavioral-veriloga-eval/generated-completion-package-benchmark-v2-2026-04-29-r1`

EVAS validation:

```bash
cd behavioral-veriloga-eval
python3 runners/validate_benchmark_v2_gold.py \
  --backend evas \
  --candidate-dir generated-completion-package-benchmark-v2-2026-04-29-r1 \
  --model completion-package-v0 \
  --output-dir results/completion-package-benchmark-v2-evas-2026-04-29-r1 \
  --timeout-s 180
```

Result: `30/30 PASS`, `pass_at_1=1.0`, with `dut_compile=1.0`, `tb_compile=1.0`, `sim_correct=1.0`.

Spectre validation:

```bash
cd behavioral-veriloga-eval
python3 runners/validate_benchmark_v2_gold.py \
  --backend spectre \
  --candidate-dir generated-completion-package-benchmark-v2-2026-04-29-r1 \
  --model completion-package-v0 \
  --output-dir results/completion-package-benchmark-v2-spectre-2026-04-29-r1 \
  --env ../coordination/status/local-private/virtuoso_bridge_sui.env \
  --spectre-mode spectre \
  --timeout-s 240
```

Result: `30/30 PASS`, `pass_at_1=1.0`, with `dut_compile=1.0`, `tb_compile=1.0`, `sim_correct=1.0`.

## Interpretation

This validates two different claims:

- Closed-set completion: the package can reproduce an accepted `92/92` state for the original task set, with explicit provenance.
- Same-type transfer: the package can materialize and pass 30 new same-type benchmark-v2 tasks from public prompts under both EVAS and Spectre.

It does not yet prove open-ended cold-start LLM generation. The benchmark-v2 result is stronger than pure replay because the materializer uses public prompts and slot binding, but it is still a template/materialization result rather than a fresh model-generation result.

## Next Check

The next fair comparison is to run A/D/F/G/I/RAG on benchmark-v2 under the same EVAS + Spectre validators and compare against this completion-package materializer line.
