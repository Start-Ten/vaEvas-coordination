# Closed-Loop Flow Example: Comparator

This document is a presentation example of the layered closed-loop workflow.

Purpose:

1. show how the workflow looks on a concrete case
2. separate lightweight executable validation from heavier parity validation
3. make the team flow easier to read than a single flat checklist

This example uses the existing comparator assets in `behavioral-veriloga-eval`.

Reference paths:

1. example path:
   `vaEvas/behavioral-veriloga-eval/examples/comparator/comparator`
2. existing task path:
   `vaEvas/behavioral-veriloga-eval/tasks/end-to-end/voltage/comparator_smoke`

---

## 1. Why Comparator Is A Good Example

Comparator is a good workflow demo because it is simpler than PLL closed-loop cases but still has real behavioral meaning.

It is useful for showing the workflow layers:

1. it has a clear functional target
2. it is easy to run in EVAS
3. it already has example and task assets
4. it usually does not require Spectre parity in the first round

So it is a good case for demonstrating:

1. `L0` minimal executable loop
2. `L1` behavior validation loop
3. `L3` benchmark landing loop

It is not the best case for demonstrating full `L2` parity debugging, because comparator smoke is not the most parity-sensitive closed-loop workload.

---

## 2. The Four-Layer Flow

We present the workflow as four layers.

### L0: Minimal Executable Loop

Goal:

`Can the candidate run at all?`

Required outputs:

1. DUT compiles
2. testbench compiles
3. transient output is generated

### L1: Behavior Validation Loop

Goal:

`Does the runtime behavior match the intended comparator function?`

Required outputs:

1. non-degenerate output behavior
2. task-specific comparator check passes
3. result can be classified as pass/fail with evidence

### L2: Parity Loop

Goal:

`If this case becomes parity-sensitive later, does EVAS match Spectre closely enough?`

For comparator smoke, this layer is optional in the first round.

### L3: Benchmark Landing Loop

Goal:

`Can this case be packaged, tracked, and submitted as a benchmark asset?`

Required outputs:

1. benchmark task assets are complete
2. result is recorded in the team table
3. PR is submitted

---

## 3. L0 Example: Minimal Executable Loop

### Input

Use a comparator example such as:

1. `cmp_ideal.va`
2. `tb_cmp_ideal.scs`

### What We Check

At this layer, do not overcomplicate the goal.

We only ask:

1. does EVAS accept the model
2. does EVAS accept the testbench
3. is `tran.csv` generated

### Pass Condition

The case passes `L0` if all are true:

1. DUT compile = pass
2. TB compile = pass
3. transient generation = pass

### Typical Output Row

This is the kind of row that should appear in the result table:

| owner | case_name | dut_compile | tb_compile | tran_generated | sim_correct | parity_status |
| --- | --- | --- | --- | --- | --- | --- |
| `[owner]` | `comparator_smoke` | `pass` | `pass` | `pass` | `[TODO at L1]` | `N/A` |

### Why This Layer Matters

This is the closest layer to the VGen-style minimal loop:

`prompt/example -> code -> compile -> simulate`

It filters out tasks that are not yet worth deeper analysis.

---

## 4. L1 Example: Behavior Validation Loop

### Input

Continue from the same successful `L0` run.

### What We Check

Now the question is no longer only "did it run", but:

`did it behave like a comparator?`

Example comparator-specific checks can include:

1. output toggles instead of staying flat
2. output polarity follows input differential sign at decision points
3. clocked comparator output changes near expected clock events

### Comparator-Specific Evidence

For a smoke-style comparator task, acceptable evidence may be:

1. output waveform is non-trivial
2. validation script reports pass
3. output transitions are consistent with intended decision behavior

### Pass Condition

The case passes `L1` if:

1. `L0` already passed
2. comparator validation script or task check passes
3. no degenerate waveform issue is found

### Result Interpretation

At this point, the case is not merely runnable.

It is now:

1. executable
2. behavior-checked
3. ready to be considered for benchmark packaging

### Typical Output Row

| owner | case_name | dut_compile | tb_compile | tran_generated | sim_correct | benchmark_seed |
| --- | --- | --- | --- | --- | --- | --- |
| `[owner]` | `comparator_smoke` | `pass` | `pass` | `pass` | `pass` | `[candidate]` |

---

## 5. L2 Example: Parity Loop

### Is L2 Required For Comparator?

Usually not in the first round.

This is an important design point of the layered workflow:

1. not every case needs to go to Spectre immediately
2. parity is a selective heavier layer
3. parity should be reserved for cases where simulator semantics matter more

For comparator smoke:

1. `L0` and `L1` are usually enough for first-pass benchmark work
2. `L2` becomes useful only if:
   a. EVAS behavior looks suspicious
   b. comparator timing semantics become the research focus
   c. the case is promoted into a parity-sensitive benchmark family

### If We Do Run L2

Then the same logic applies:

1. run EVAS and Spectre on identical stimulus
2. compare waveform behavior
3. record mismatch metrics
4. if mismatch exists, first inspect EVAS semantics

### Comparator-Specific L2 Metrics

Possible metrics:

1. output transition timing difference
2. decision polarity agreement
3. sampled output mismatch rate

### Key Message

`L2 is not mandatory for every case.`

That is one of the main advantages of writing the flow in layers.

---

## 6. L3 Example: Benchmark Landing Loop

### Goal

Turn the validated comparator case into a tracked benchmark asset.

### Required Assets

For comparator smoke, the benchmark landing layer should include:

1. `prompt.md`
2. `meta.json`
3. `checks.yaml`
4. runner-side check logic if needed

### Team Tracking

This layer also requires:

1. add or update the row in [BENCHMARK_RESULT_TABLE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md)
2. attach result path
3. attach PR link

### Pass Condition

The case passes `L3` if:

1. benchmark assets exist
2. benchmark check passes on reference output
3. result row is filled
4. PR is submitted

---

## 7. Example Summary

For comparator, a realistic first-pass workflow looks like this:

1. `L0`
   run comparator example in EVAS and confirm compile + simulate success
2. `L1`
   confirm comparator behavior is valid through a task-specific check
3. `L3`
   package or verify benchmark task assets, fill table row, submit PR

`L2` is optional unless the case becomes parity-sensitive.

This is exactly why the layered workflow is useful:

1. simple cases do not get blocked by unnecessary heavy validation
2. heavy parity flow is still available when needed
3. all cases still end in a common benchmark and PR process

---

## 8. What This Example Shows About The Workflow

This comparator example demonstrates that the layered flow is not trying to replace the old logic.

Instead, it clarifies it:

1. `L0` corresponds to minimal executable closure
2. `L1` corresponds to behavior validation
3. `L2` corresponds to EVAS-Spectre parity
4. `L3` corresponds to benchmark landing and integration

That makes the overall project easier to explain to:

1. new team members
2. benchmark contributors
3. future paper readers

---

## 9. Suggested Next Step

If this presentation style is acceptable, the next good follow-up is:

1. add one PLL example in the same format
2. show how the same layered flow scales from comparator to CPPLL

That pair would make the workflow much easier to communicate:

1. comparator for lightweight path
2. CPPLL for full parity path
