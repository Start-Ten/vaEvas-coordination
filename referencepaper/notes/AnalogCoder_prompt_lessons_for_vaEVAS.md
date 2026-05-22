# AnalogCoder Prompt Lessons For vaEVAS

Date: 2026-05-21

This note isolates the prompt-design lesson from AnalogCoder and maps it to
vaEVAS. The goal is not to copy its PySpice task setting, but to improve how
vaEVAS prompts guide Verilog-A behavioral artifact generation without leaking
gold implementations.

## 1. What AnalogCoder Actually Does In Prompts

AnalogCoder's prompt design is stronger than a simple natural-language task
description. It has several deliberate layers:

1. Role anchoring:
   - "You are an analog integrated circuits expert."
   - This tells the model what domain assumptions to activate.

2. Worked example:
   - It provides a complete two-stage amplifier example.
   - The example includes both a design plan and runnable PySpice code.
   - The test tasks are distinct from the example, so the example teaches format
     and idioms more than task answers.

3. Explicit two-step output shape for basic circuits:
   - First give a detailed design plan: devices, interconnect nodes, properties.
   - Then write complete runnable code.

4. Hard implementation tips:
   - Correct MOSFET argument order.
   - Bulk tied to source.
   - Use threshold voltage when setting bias.
   - Ensure input/output node names appear.
   - Avoid placeholders.

5. Interface placeholders:
   - `[TASK]`, `[INPUT]`, `[OUTPUT]`.
   - This makes task contracts explicit and hard to ignore.

6. Separate prompt for composite circuits:
   - First retrieve subcircuits.
   - Then inject subcircuit information, notes, and exact call snippets into the
     design prompt.

7. Ablation-backed prompt choices:
   - Raw SPICE generation is weaker than Python/PySpice.
   - Removing the worked example hurts.
   - Removing design-plan-before-code hurts.
   - Removing feedback flow hurts.

The key lesson is that prompt design is part of the executable system, not
decorative wording.

## 2. What vaEVAS Prompts Already Do Well

From the release prompts, vaEVAS already has several good pieces:

1. Module/interface contracts:
   - exact module names.
   - exact port order.
   - electrical-domain constraints.

2. Behavioral contracts:
   - voltage-domain behavior.
   - reset, event, threshold, clamp, and transition requirements.

3. Public evaluation observables:
   - exact waveform columns.
   - transient windows.
   - non-gold public checker-facing constraints.

4. Output contracts:
   - exact artifact names.
   - no prose outside source contents.
   - preserve names, ports, waveform columns, and simulation contract.

These are important. They make vaBench more benchmark-like than AnalogCoder's
free-form task descriptions.

## 3. Current Weakness In vaEVAS Prompt Design

The current weakness is that our prompts are mostly "acceptance contracts" but
not enough "construction scaffolds."

Concretely:

1. Many DUT prompts state what must be true, but do not guide the model through
   how to construct a stable Verilog-A behavioral model.

2. The common Verilog-A pitfalls are not consistently visible in the release
   prompts:
   - no `reg`, `wire`, `logic`.
   - no `always`.
   - use `analog begin`.
   - use `@(initial_step)`.
   - use `@(cross(...))` for edge detection.
   - use `transition(...)` targets for outputs.
   - use voltage contributions unless explicitly allowed otherwise.

3. Testbench prompts are sometimes too generic:
   - they say to drive public scenarios and save observables.
   - but they often do not give enough stimulus-shape guidance, timing margins,
     or minimal Spectre idioms.

4. L2/e2e prompts can under-specify decomposition:
   - AnalogCoder has a separate composite prompt with retrieved subcircuit call
     information.
   - vaEVAS L2 prompts often state the integrated behavior, but do not give a
     public decomposition checklist such as state variables, event sources,
     observable handoff points, and checker windows.

5. Bugfix prompts describe the bug, but do not always structure feedback into:
   - interface failure.
   - syntax failure.
   - waveform missing.
   - semantic mismatch.
   - suggested repair direction.

## 4. What We Should Borrow

Borrow these ideas:

1. **Design-plan-before-code, but keep it internal.**
   - AnalogCoder asks the model to output a plan and code.
   - vaEVAS output contracts often require source-only answers.
   - So our prompt should say: "Before writing the code, internally derive the
     state variables, event triggers, update equations, reset behavior, output
     contribution targets, and observables. Do not output the plan."

2. **A small allowed idiom library.**
   - AnalogCoder's worked example teaches valid PySpice idioms.
   - vaEVAS should teach safe Verilog-A idioms:
     - electrical port declaration.
     - state initialized with `@(initial_step)`.
     - event update with `@(cross(...))`.
     - periodic update with `@(timer(...))`.
     - output driven with `transition(target, delay, trise)`.
     - scalar save-friendly node naming in Spectre testbenches.

3. **Task-specific tips block.**
   - For comparator: threshold, hysteresis memory, rail-referenced output.
   - For sample/hold: sample only on valid edge, hold state variable, droop by
     timer update or analytic decay, avoid combinational glitches.
   - For clock divider/counter: integer state, modulo wrap, stable voltage
     outputs after edge.
   - For measurement writers: exact file/metric timing and final-window write.

4. **Separate basic vs composite prompt templates.**
   - L1 prompt: one module/function with a local behavioral checklist.
   - L2 prompt: integrated system with public sub-behavior boundaries and
     handoff observables.

5. **Feedback prompt schema.**
   - When using EVAS/Spectre feedback, return categorized failures to the LLM:
     compile/interface, transient/runtime, missing columns, waveform shape,
     semantic checker condition.

## 5. What We Should Not Borrow

Do not copy these parts directly:

1. Do not turn Verilog-A tasks into Python/PySpice tasks. Our paper target is
   behavioral Verilog-A practice.

2. Do not expose gold implementation code as examples inside each benchmark
   prompt.

3. Do not require the submitted answer to include a natural-language plan if
   the scorer expects exact source artifacts.

4. Do not make prompt engineering the paper's central contribution. It should
   support the benchmark/evaluator/certification story.

## 6. Proposed vaEVAS Prompt Scaffold

This is the candidate template for future prompt materialization or baseline
experiments.

````markdown
# Task: {task_id}

You are generating pure voltage-domain behavioral Verilog-A for an EVAS/Spectre
validated benchmark task.

## Target Artifact

- Form: {dut|tb|bugfix|e2e}
- Required file(s): {artifact_names}
- Domain: pure voltage-domain behavioral Verilog-A.

## Interface Contract

- Module declaration: `{module_name}({ports})`
- Ports, all `electrical`, exactly in this order:
  - ...
- Parameters:
  - ...

## Behavioral Contract

- ...

## Construction Checklist

Before writing the final source, internally derive:

1. state variables and their initial values.
2. event triggers, such as `cross(...)`, `timer(...)`, or final-step behavior.
3. reset and priority order.
4. bounded voltage ranges and clamp behavior.
5. output contribution targets and transition times.
6. exact public observables that the testbench must save.

Do not output this checklist; return only the requested source artifact(s).

## Verilog-A Idiom Rules

- Use `electrical` ports and internal electrical nodes.
- Use `integer` or `real` state variables, not `reg`, `wire`, or `logic`.
- Put behavior inside `analog begin ... end`.
- Use `@(initial_step)` for initialization.
- Use `@(cross(V(signal) - threshold, direction))` for edge events.
- Use `@(timer(...))` only when the task requires periodic updates.
- Drive voltages with `V(out) <+ transition(target, 0, trf)`.
- Use voltage contributions only unless the task explicitly allows current
  contributions.
- Do not use digital Verilog `always`, `initial`, bit literals, or procedural
  assignments to ports.

## Public Evaluation Contract (Non-Gold)

- Required saved waveform columns:
  - ...
- Required transient setting:

```spectre
tran tran stop={stop} maxstep={maxstep}
```

## Output Contract

Return exactly {artifact_contract}. Do not include explanatory prose outside
the source file contents.
````

## 7. Proposed Repair Feedback Scaffold

AnalogCoder's repair loop works because error messages are concrete. For vaEVAS
feedback runs, the repair prompt should use this shape:

```markdown
The previous candidate failed validation.

## Failure Class

{compile | interface | transient_runtime | missing_observable | semantic_checker}

## Evidence

- Tool/backend: {EVAS|Spectre}
- Error or checker message:
  - ...
- Observed waveform/metric:
  - ...
- Expected public behavior:
  - ...

## Repair Direction

- Preserve the exact module name, port order, and artifact filenames.
- Change only the minimal logic needed to address the failure.
- Re-check initialization, event trigger, reset priority, output transition, and
  saved observable names before returning the full corrected source.

## Output Contract

Return the full corrected artifact(s), not a patch or explanation.
```

## 8. Suggested Next Experiment

Do a small prompt ablation before changing the release package:

1. Current prompt.
2. Current prompt + internal construction checklist.
3. Current prompt + checklist + Verilog-A idiom rules.
4. Current prompt + checklist + idiom rules + categorized EVAS feedback.

Use a fixed, small slice across:

1. one L1 event task.
2. one L1 analog-behavior task.
3. one L1 digital-control-in-voltage-domain task.
4. one L2 composition task.

Measure:

1. compile pass.
2. required observable presence.
3. EVAS pass.
4. Spectre pass where available.
5. no EVAS PASS / Spectre FAIL regression.

## 9. Paper Framing

The paper should not claim "we designed better prompts" as the main novelty.
Instead:

AnalogCoder motivates that prompt scaffolding and feedback structure matter for
analog LLM workflows. vaEVAS uses this insight to make Verilog-A benchmark tasks
clearer and more reproducible, while the central contribution remains the
benchmark/evaluator/certification package.
