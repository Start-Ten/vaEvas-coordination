# G Compile-Clean Optimization

Date: 2026-04-28

## Goal

Move Condition G closer to the intended invariant:

> compile / missing-file / interface / infra failures should be driven as close
> to zero as possible; remaining failures should mostly be behavior failures.

This is a targeted rerun over the seven compile/runtime-class failures observed
in the current G cold-start full92 result, not a new full92 score.

## Code Changes

- `behavioral-veriloga-eval/runners/simulate_evas.py`
  - Extracts actionable EVAS log diagnostics such as `ERROR: Failed to compile
    Verilog-A file ...` into `evas_notes` as `evas_log_diagnostic=...`.
- `behavioral-veriloga-eval/runners/score.py`
  - Keeps `evas_stdout_tail` for non-PASS cases.
- `behavioral-veriloga-eval/runners/run_adaptive_repair.py`
  - Treats interface-parameter guard issues as warnings during quick repair
    scoring, matching Spectre's warning-and-ignore behavior.
  - Adds syntax-blocker count to progress ranking.
  - Adds signature-triggered compile-clean templates for:
    `integer(...)`, embedded declarations, conditional `transition()`, dynamic
    analog vector indexing, TB single quotes, missing models/includes, invalid
    sources, and missing CSV.
  - Generalizes the conditional `transition()` repair into a multi-output
    target-buffer pattern, so the rule is not DWA-specific.
  - Materializes deterministic syntax-only TB cleanup for `key='expr'` into
    final G samples.
- `behavioral-veriloga-eval/runners/build_repair_prompt.py`
  - Treats runtime diagnostics such as `transition() contribution is inside...`
    as syntax markers.
- `EVAS/evas/netlist/spectre_parser.py`
  - Aligns EVAS with real Spectre by rejecting bare multi-line instance node
    lists unless the line uses explicit `\` continuation.
- `EVAS/evas/simulator/engine.py`
  - Aligns EVAS with real Spectre by requiring strictly increasing PWL
    timestamps instead of accepting duplicate-time ideal steps.
- `EVAS/tests/test_netlist.py`
  - Adds regressions for strict PWL time ordering and bare multi-line instance
    rejection.
- `behavioral-veriloga-eval/specs/spectre_veriloga_public_rules.md`
  - Adds public rules for strictly increasing PWL times and explicit Spectre
    line continuation on long instance node lists.
- `veriloga-skills/veriloga/SKILL.md`
  - Adds a generic multi-output `transition()` target-buffer corollary.
- `veriloga-skills/veriloga/references/categories/dac.md`
  - Clarifies that the DWA skeleton is one instance of the generic
    multi-output target-buffer pattern.

Validation:

- `PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_compiler.py EVAS/tests/test_engine.py EVAS/tests/test_netlist.py -q`
  passed: 314 tests.

## Targeted Rerun Inputs

Current scorer rescore of the seven D artifacts:

- Root:
  `behavioral-veriloga-eval/results/condition-D-table43R0-current-rescore-compileclean7-2026-04-28`
- Result: 0/7 PASS. All seven were compile/TB/runtime-class failures under the
  current scorer.

Optimized G generated root:

- `behavioral-veriloga-eval/generated-condition-G-compileclean7-currentR0-kimi-v2-2026-04-28`

Optimized G standard EVAS result:

- `behavioral-veriloga-eval/results/condition-G-compileclean7-currentR0-kimi-v2-evas-standard-after-pwlfix-full7-2026-04-28`

## Targeted Result

| Task | Current D Rescore | Optimized G Targeted Result | Interpretation |
|---|---|---|---|
| `cmp_delay_smoke` | compile/TB failure | PASS | Single-quoted Spectre param expression + duplicate PWL step timestamps were repaired into Spectre-compatible finite steps. |
| `d2b_4bit` | DUT compile failure | PASS | `integer(...)`-style issue was repaired by G. |
| `dwa_wraparound_smoke` | parser/runtime failure | PASS | Bare multi-line Spectre instance was repaired into Spectre-compatible instance syntax; behavior still passes. |
| `pipeline_stage` | DUT compile failure | PASS | Conditional transition / embedded declaration pattern was repaired. |
| `dwa_ptr_gen_no_overlap_smoke` | DUT compile failure | `FAIL_SIM_CORRECTNESS` | Compile layer is clean; remaining issue is behavior/coverage. |
| `nrz_prbs` | DUT compile failure | `FAIL_SIM_CORRECTNESS` | Compile layer is clean; remaining issue is behavior activity. |
| `dwa_ptr_gen_smoke` | DUT compile failure | `FAIL_TB_COMPILE` | Still blocked by transition contribution inside conditional/event/loop/case. |

Aggregate targeted result:

- PASS: 4/7
- Moved compile/runtime -> behavior: 2/7
- Still compile/TB/runtime: 1/7

## Spectre-Alignment Follow-Up And G Replacement

When the 4/7 targeted PASS artifacts were checked in real Spectre,
`cmp_delay_smoke` and `dwa_wraparound_smoke` initially failed for simulator
compatibility reasons that EVAS had been too permissive about:

- `cmp_delay_smoke`: duplicate PWL timestamps such as `4n ... 4n ...`.
- `dwa_wraparound_smoke`: bare multi-line `XDUT (...) module` instance without
  explicit `\` continuation.

Those rules were added to EVAS/strict-v3 as hard compatibility checks, the two
tasks were rerun through G, and both passed EVAS and Spectre:

- EVAS follow-up root:
  `behavioral-veriloga-eval/results/condition-G-spectre-align-followup-kimi-evas-2026-04-28`
- Spectre follow-up root:
  `behavioral-veriloga-eval/results/condition-G-spectre-align-followup-kimi-spectre-2026-04-28`
- Result: 2/2 EVAS PASS and 2/2 Spectre PASS.

The final materialized G full92 replacement is:

- Generated:
  `behavioral-veriloga-eval/generated-condition-G-targeted-materialized-spectre-aligned-kimi-2026-04-28`
- EVAS:
  `behavioral-veriloga-eval/results/condition-G-targeted-materialized-spectre-aligned-kimi-evas-2026-04-28`
- Spectre-combined:
  `behavioral-veriloga-eval/results/condition-G-targeted-materialized-spectre-aligned-kimi-spectre-combined-2026-04-28`

Final replacement result: 65/92 EVAS, 65/92 Spectre.

## Template-Hardening Finding

The targeted run shows a useful split:

- Signature-triggered soft templates are enough for common local legality
  issues: `integer(...)`, embedded declarations, single-quoted Spectre
  parameters, duplicate PWL timestamps, and multi-line instance parsing.
- They are not enough for the remaining multi-output conditional-transition
  case.

The blocker is not DWA-specific. The general failure pattern is:

> many electrical outputs are driven by `transition()` inside runtime
> `if` / `case` / `for` control flow.

For Spectre-compatible Verilog-A, the correct implementation is a
multi-output target-buffer structure:

1. Declare held target variables at module scope, such as `real out_t[0:N-1]`
   or explicit `real out0_t, out1_t, ...`.
2. Update only those targets inside `@(initial_step)`, `@(cross(...))`, reset
   branches, state-machine branches, and integer loops.
3. Emit all electrical contributions once at analog top level:
   `V(out[k]) <+ transition(out_t[k], 0, tr, tf);` using module-scope `genvar`,
   or explicit unrolled contribution lines.

Why this needs a harder template:

- It is a structural rewrite, not a local textual edit. The model must separate
  state computation from electrical contribution placement.
- The number of affected outputs can be large. A single missed output or one
  remaining runtime-loop contribution keeps the design in compile failure.
- Natural-language constraints say what is forbidden, but do not force the
  model to instantiate the full target-buffer skeleton.
- The pattern is broadly reusable across DWA, thermometer DACs, serializers,
  counters, bus drivers, multi-bit logic blocks, and any multi-output
  transition-driven model.

Therefore, the next G implementation should treat this as a reusable hard
template / rewrite primitive:

`multi_output_transition_blocker -> target_buffer_skeleton`

This should be triggered by either strict preflight notes such as
`conditional_transition=...` or runtime diagnostics such as
`transition() contribution is inside a conditional/event/loop/case statement`.

## Takeaway

The optimized G mechanism is effective for the intended direction:

- Before optimization/current rescore: 7/7 were compile/TB/runtime-class
  failures.
- After optimized G targeted rerun and Spectre-alignment follow-up: the
  materialized full92 G result improves to 65/92; the final full92 rescore still
  has two TB-compile-class failures (`dwa_ptr_gen_smoke` and
  `pfd_deadzone_smoke`).

The remaining case, `dwa_ptr_gen_smoke`, likely needs a more deterministic DWA
bus-output skeleton or a structured Verilog-A rewrite template. We generalized
the rule into a multi-output target-buffer pattern and reran only
`dwa_ptr_gen_smoke`:

- Generated root:
  `behavioral-veriloga-eval/generated-condition-G-multi-transition-followup-kimi-2026-04-28`
- Result root:
  `behavioral-veriloga-eval/results/condition-G-multi-transition-followup-kimi-evas-2026-04-28`
- Result: still `FAIL_TB_COMPILE` with
  `transition() contribution is inside a conditional/event/loop/case statement`.

This suggests that a natural-language template is insufficient for this
remaining case. The next step should be a more deterministic multi-output
transition skeleton/rewrite: compute output targets in events, then emit a
top-level unconditional contribution block using either module-scope `genvar`
or explicit unrolled lines.

Recommended next step after publishing the 65/92 G replacement:

1. Add a deterministic or strongly structured multi-output target-buffer
   template for `transition()`-inside-loop/case failures.
2. Rerun the remaining `dwa_ptr_gen_smoke`.
3. Audit and repair `pfd_deadzone_smoke`, the other final TB-compile-class
   failure.
4. Materialize only newly validated replacements and run Spectre on changed
   PASS/FAIL boundary tasks.
