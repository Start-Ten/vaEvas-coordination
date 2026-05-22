# Group 1 Closest Peers

Date: 2026-05-21

This group should be read before the RTL benchmark/model-training papers because
it is closest to the vaEVAS paper story: analog/AMS tasks, simulator or EDA-tool
feedback, benchmark construction, and engineering deliverables.

## Reading Order Inside The Group

1. AnalogCoder
   - Role: closest analog-domain LLM/SPICE feedback paper.
   - Key question: how do they turn natural-language analog intent into an
     executable artifact and validate it?
   - vaEVAS angle: useful simulator-feedback precedent, but target is
     transistor-level PySpice circuit design rather than Verilog-A behavioral
     model evaluation.

2. AMS-IO-Bench / AMS-IO-Agent
   - Role: closest engineering-deliverable paper.
   - Key question: how do they make an AMS workflow publishable through a
     benchmark, structured intermediate representation, DRC/LVS checks, and
     tape-out validation?
   - vaEVAS angle: useful for framing practical AMS workflow value; task is I/O
     ring generation, not behavioral modeling.

3. AutoSizer / AMS-SizingBench
   - Role: closest benchmark-plus-simulator-loop paper for AMS optimization.
   - Key question: how do they package circuits, variables, constraints, and
     simulation workflows into a reusable benchmark?
   - vaEVAS angle: useful for benchmark construction and simulation-loop
     metrics; task is transistor sizing optimization, not model correctness.

## Group-Level Takeaway

The strongest related-work story is not "LLMs can generate circuits." It is:
recent AMS papers are moving from one-shot generation toward executable,
tool-verified workflows. vaEVAS fits this trend but moves the target to
Verilog-A behavioral models and makes evaluator certification itself a first
class contribution.
