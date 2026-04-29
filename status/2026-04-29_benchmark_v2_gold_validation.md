# Benchmark-v2 Gold Validation

Date: 2026-04-29

## Result

The first `benchmark-v2` split has been materialized and gold-validated.

| Item | Count / Result |
|---|---:|
| Draft tasks in `v2-small` | 30 |
| `prompt.md` files | 30 |
| gold Verilog-A DUTs | 30 |
| gold Spectre/EVAS testbenches | 30 |
| task-local `checker.py` files | 30 |
| EVAS gold pass | 30/30 |
| real Spectre gold pass | 30/30 |

## Locations

- Manifest: `behavioral-veriloga-eval/benchmark-v2/manifests/v2-small.json`
- Task root: `behavioral-veriloga-eval/benchmark-v2/tasks/`
- Common checker helper: `behavioral-veriloga-eval/benchmark-v2/common_checker.py`
- Materializer: `behavioral-veriloga-eval/runners/materialize_benchmark_v2_tasks.py`
- Gold validator: `behavioral-veriloga-eval/runners/validate_benchmark_v2_gold.py`
- EVAS result root: `behavioral-veriloga-eval/results/benchmark-v2-gold-validation-2026-04-29-r2`
- Spectre result root: `behavioral-veriloga-eval/results/benchmark-v2-gold-validation-spectre-2026-04-29-r1`

## What Was Added

The new split covers 6 mechanism groups with 5 perturbation tasks each:

- ADC-DAC shared-state quantize/reconstruct tasks
- binary weighted DAC tasks with thermometer distractors
- DWA rotating-window tasks
- PFD/reset/lock event-order tasks
- divider/counter ratio tasks
- sample-hold/calibration tasks

The perturbations include semantic aliases, keyword removal, negative constraints, parameter changes, and small system compositions. The point is to test whether RAG/I can identify a functional mechanism rather than only matching task names.

## Validation Note

During EVAS validation, the binary-DAC checker initially sampled during output `transition()` settling and produced false failures. The checker was corrected to evaluate only after input code stability. After that correction:

- EVAS: 30/30
- Spectre: 30/30

This means the benchmark gold artifacts are internally consistent across EVAS and real Spectre.

## Claim Boundary

These are benchmark authoring and gold-validation results. They do not show model success yet. The next experiment should run A/D/F/G/I or RAG-guided generation against this new split.
