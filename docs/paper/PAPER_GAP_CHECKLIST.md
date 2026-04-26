# Paper Gap Checklist

This document turns the current `vaEvas` paper draft into an execution checklist.

Scope:

1. what the draft already has
2. what is still missing
3. what must be done before the draft becomes paper-grade
4. who should help move which part forward

Primary drafts:

1. [VAEVAS_OPENLLM_STYLE_DRAFT.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/paper/VAEVAS_OPENLLM_STYLE_DRAFT.md)
2. [VAEVAS_PAPER_DRAFT_ZH.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/paper/VAEVAS_PAPER_DRAFT_ZH.md)
3. [VAEVAS_FIGURE_PLAN.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/paper/VAEVAS_FIGURE_PLAN.md)

Supporting table:

1. [BENCHMARK_RESULT_TABLE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md)

---

## 1. What We Already Have

These pieces are already strong enough to count as real paper material.

### 1.1 Problem framing

Status: `done`

We already have:

1. a clear motivation for Verilog-A evaluation
2. a clear contrast with RTL-centric benchmark work
3. an execution-first framing instead of text-only scoring

### 1.2 System structure

Status: `done`

We already have:

1. the four-repository structure
2. the EVAS-first loop
3. the example-to-benchmark workflow

### 1.3 Technical core

Status: `partially done`

We already have:

1. EVAS semantic fixes motivated by parity debugging
2. `while` support and timer-parity repair
3. `CPPLL` and `ADPLL` closed-loop evidence
4. at least one formalized benchmark task: `adpll_lock_smoke`

Still needed:

1. cleaner technical summary table
2. explicit claim boundaries for each contribution

---

## 2. Must-Have Missing Pieces

These are the most important missing pieces. Without them, the draft is still closer to a whitepaper than a paper.

### 2.1 Quantitative result table

Status: `in progress`

Current support:

1. [BENCHMARK_RESULT_TABLE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md)

Need to produce:

1. total number of cases considered
2. number of runnable cases
3. number of benchmark seeds
4. number of formal benchmark tasks
5. number of parity-qualified cases

Paper output needed:

1. one compact main table
2. one appendix-style extended table if needed

### 2.2 Baseline comparison

Status: `missing`

Need to explicitly compare:

1. compile-only evaluation
2. execution-first evaluation
3. parity-aware closed-loop evaluation

Questions the paper should answer:

1. what errors would compile-only evaluation miss
2. what benchmark value is added by runtime checks
3. what benchmark value is added by EVAS-Spectre parity

### 2.3 Related work

Status: `missing`

Must cover:

1. Verilog and RTL benchmark papers
2. Verilog-A modeling and tooling papers
3. simulator-aware evaluation or validation workflows

Minimum references to integrate:

1. `VerilogEval`
2. `VGen`
3. `OpenLLM-RTL`
4. `RTL-Coder`
5. prior Verilog-A tooling/modeling papers in `referencepaper` or later collected set

### 2.4 Figures

Status: `missing`

Need at least:

1. system overview figure
2. example-to-benchmark pipeline figure
3. EVAS-first parity loop figure

Recommended extras:

1. task taxonomy figure
2. result summary chart

---

## 3. Nice-to-Have Missing Pieces

These are not strictly required for an early draft, but they would strengthen the paper.

### 3.1 Failure taxonomy

Status: `missing`

Candidate categories:

1. parser/frontend failure
2. runtime failure
3. degenerate waveform
4. check failure
5. parity mismatch
6. benchmark packaging incomplete

### 3.2 Artifact schema

Status: `partial`

Need a more formal description of:

1. `prompt.md`
2. `meta.json`
3. `checks.yaml`
4. result artifact layout
5. benchmark maturity stages

### 3.3 LLM evaluation runs

Status: `missing`

Possible later step:

1. run a few LLMs on a small task subset
2. report compile rate, sim pass rate, and parity-qualified rate

This is not required for the current paper skeleton, but would make it much closer to an `OpenLLM-RTL`-style empirical paper.

---

## 4. Suggested Claim Boundary

Current strongest claim:

`EVAS is behaviorally aligned with Spectre/Virtuoso while being fast enough to serve as the inner loop of LLM Verilog-A generate-simulate-repair optimization.`

Current weaker claim:

`vaEvas is already a large mature benchmark suite for Verilog-A.`

Recommended paper angle:

1. EVAS-guided closed-loop repair paper
2. executable Verilog-A generation evaluation paper
3. benchmark/methodology paper

Not recommended yet:

1. claiming broad benchmark completeness
2. claiming large-scale model ranking leadership

---

## 5. Team Task Split

This section turns paper gaps into concrete team work.

### 5.1 Core owner

Suggested responsibility:

1. lock the paper angle
2. maintain the main draft
3. decide which results become main-paper tables
4. review whether new benchmark seeds are paper-relevant

### 5.2 shenbufan

Primary cases:

1. `lfsr`
2. `clk_burst_gen`
3. `digital_basics`

Required outputs:

1. run cases
2. fill corresponding rows in [BENCHMARK_RESULT_TABLE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md)
3. promote at least one case to benchmark seed if feasible
4. submit a PR

Paper contribution:

1. increase runnable task count
2. help populate main benchmark coverage table
3. provide at least one digital/stimulus task example

### 5.3 liangyuxuan

Primary cases:

1. `dac_binary_clk_4b`
2. `adc_dac_ideal_4b`
3. `dwa_ptr_gen`

Required outputs:

1. run cases
2. fill corresponding rows in [BENCHMARK_RESULT_TABLE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md)
3. promote at least one case to benchmark seed if feasible
4. submit a PR

Paper contribution:

1. increase task diversity beyond digital logic
2. improve converter/calibration coverage
3. provide evidence that the framework is not only about PLLs

### 5.4 Team-wide backlog

Shared responsibilities:

1. backfill PR links into the result table
2. convert closed-loop evidence into paper-ready tables
3. draft related work
4. build the first three figures

---

## 6. Immediate Next Actions

If we want the draft to improve quickly, do these next:

1. fill the currently blank rows in [BENCHMARK_RESULT_TABLE.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md)
2. extract one compact result table into the main draft
3. write a proper related-work subsection
4. create one system figure and one workflow figure
5. decide whether the target paper is `framework + benchmark construction` or `early benchmark`

---

## 7. Exit Criteria For A Paper-Ready Draft

The draft can be considered paper-ready only when all of the following are true:

1. the result table is no longer mostly `[TODO]`
2. at least one baseline comparison subsection exists
3. related work is complete enough to stand alone
4. at least three figures exist
5. the claim boundary is explicit and consistent across abstract, introduction, and conclusion
