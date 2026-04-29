# Clean Experiment Condition Matrix

Updated: 2026-04-27

This file defines which experiment conditions should remain in the paper-facing
vaEvas matrix after result hygiene cleanup.

The goal is to avoid an overgrown condition alphabet.  A condition is kept only
if it answers a distinct paper question.

## Paper Narrative

The paper should tell one clean story:

1. single-shot LLM Verilog-A generation is unreliable even under a fair public
   task specification;
2. EVAS execution feedback turns generation into a repair loop and produces the
   main performance gain;
3. structured failure feedback, contracts, and mechanism cards can improve the
   remaining behavior failures, but must be evaluated with no-leak clean
   anchors;
4. engineering admission/closure results are useful, but they are not model
   baselines.
5. timing evidence is part of the main claim: Spectre/Virtuoso remains the
   final acceptance reference, while EVAS is fast enough to serve as the
   inner repair loop and teacher-data construction engine.

## Official Conditions To Keep

| Condition | Keep? | Paper role | Definition | Question Answered |
|---|---|---|---|---|
| `A` | yes | primary baseline | Fair public-spec single-shot baseline: original prompt plus public interface/output/Verilog-A syntax/observable requirements. No checker source, no skill, no EVAS feedback, no gold implementation. | How well does the model do when the task is specified fairly enough to be executable? |
| `D` | yes | main method step | One EVAS-guided repair round starting from clean `A` artifacts, repairing only A-failed tasks and preserving A-pass tasks. | Does one executable feedback round help? |
| `F` | yes | main method result | Multi-round EVAS-guided repair starting from clean `A` artifacts, with best-so-far/admission gates. | Does fast EVAS enable better iterative repair? |
| `I` | yes, when ready | contract method result | No-leak functional-IR/contract/card repair starting from clean `A` failures. | Do public contracts and mechanism cards improve a true cold-start loop? |
| `H-on-F` | yes, secondary | residual repair evidence | Signature/contract-guided repair from clean `F` residual failures. | Can structured failure feedback rescue what ordinary EVAS repair misses? |

## Fair Public-Spec Baseline

`A` is not an intentionally underspecified raw prompt.  It should give the
model the public information that a human engineer would need to produce an
executable answer, while withholding hidden evaluator implementation details.

`A` may include:

1. required module name and public port/interface names;
2. required output file types and whether a testbench is expected;
3. pure Verilog-A and Spectre syntax constraints;
4. public observable signal/CSV names needed to judge the task;
5. natural-language behavior requirements, such as monotonic transfer,
   quantization range, pulse direction, lock window, or code coverage.

`A` must not include:

1. gold Verilog-A implementation;
2. hidden checker source;
3. private threshold constants extracted only from hidden checker internals;
4. task-specific repair patches;
5. standard answer waveforms;
6. trial-and-error knowledge obtained from repeatedly querying the checker.

Example shape:

```text
Write module adc_dac_ideal_4b.
Inputs/outputs are ...
Use pure Verilog-A.
Expose code_0..code_3 and vout.
Behavior: quantize vin into 4-bit code and reconstruct vout monotonically.
Do not use hidden state that prevents code coverage.
```

## Statistical Reporting For Prompt-Only Runs

Prompt-only `A` is a stochastic generation observation, not a deterministic
property of a single run. Even with `temperature=0`, provider-side decoding,
tie-breaking, truncation boundaries, and batching can change the generated code
trajectory.

Paper-facing `A` numbers should therefore be reported as:

1. a clean snapshot result for traceability;
2. a repeated-run estimate when finalizing claims: preferably `N>=5`, and
   `N>=10` for the main `A` baseline if budget permits;
3. `mean +/- std` over full92 pass count;
4. a 95% bootstrap or Wilson confidence interval;
5. per-task flip rate across repeated runs;
6. a targeted prompt-defect table separating true prompt fixes from unrelated
   trajectory variance.

Prompt-cleanup claims must be phrased as prompt/spec hygiene unless repeated
runs on the same frozen prompt show a statistically stable aggregate result.
A delta between different prompt snapshots is an audit signal, not a controlled
model-variance measurement.

## Appendix Or Ablation Conditions

| Condition | Keep? | Role | Why Not Main |
|---|---|---|---|
| `B` | appendix only | `A + checker source/transparent checker information`, no feedback | Useful to test checker transparency, but too close to evaluator internals for a clean main baseline. |
| `C` | appendix only | `A + skill`, no feedback | Tests static circuit knowledge. Keep only if we want a skill ablation; not central to the EVAS feedback thesis. |
| `D-B` / `F-B` | appendix only | EVAS repair starting from checker-visible `B` artifacts | Previous D/F behaved like this. Useful diagnostic, but not the clean cold-start main method. |
| `E` / `G` | appendix only | skill + EVAS repair | Keep only if skill injection becomes a paper claim. Otherwise it complicates the story. |
| `I-on-F` | appendix only | contract/card repair from `F` residuals | Good mechanism ablation, but not a cold-start result. |

## Freeze Or Remove From Main Tables

| Label | Status | Reason |
|---|---|---|
| current 2026-04-27 Kimi `A/B/C` | invalid baseline | Generated roots contain dry-run placeholder artifacts. |
| `I-cold-start v0` | provisional smoke | Started from contaminated A anchor; keep only as pipeline smoke evidence. |
| `I-runner` | engineering evidence | Materialization/admission result, not a model baseline. |
| `I-final` / R26 final admission | engineering closure | Demonstrates full92 closure artifact set, not cold-start model performance. |
| historical scratch/probe directories | archive only | Useful for audit, but should not be read by clean rerun scripts. |

## Minimal Paper Tables

### Main Performance Table

Only these rows should appear in the main pass-rate table:

```text
A
D
F
I   if clean no-leak run is complete
```

`H-on-F` can appear in the same section as a residual-repair extension, but it
must be visually separated from cold-start rows.

### Main Timing Table

Use [EVAS_SPECTRE_TIMING_PLAN.md](EVAS_SPECTRE_TIMING_PLAN.md) to report:

```text
EVAS wall time
Spectre wall time
speedup
inner-loop counterfactual cost
EVAS-inner-loop + Spectre-final-acceptance cost
```

The timing table should make clear that EVAS does not replace Spectre as the
final judge; it reduces the cost of repeated generation, repair, and data
construction attempts before final Spectre acceptance.

### Ablation Table

Use this only if space allows:

```text
B
C
D-B / F-B
E / G
I-on-F
```

### Engineering Evidence Table

These are not model scores:

```text
I-runner
I-final
R22/R23/R24/R25/R26 closure steps
```

## Rerun Requirements

Clean reruns must satisfy all of the following:

1. Use a fresh generated root and fresh result root.
2. Never read from `generated-experiment/condition-*` by default.
3. Fail fast if `generation_meta.json` has `dry_run: true`.
4. Fail fast if a formal generated sample contains `*_placeholder.va` or
   `tb_*_placeholder.scs`.
5. Record the exact condition definition in `generation_meta.json`.
6. Record whether the condition used public contracts, checker source, skill
   notes, EVAS feedback, or materialization.
