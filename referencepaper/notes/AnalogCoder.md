# AnalogCoder Reading Note

Paper: AnalogCoder: Analog Circuit Design via Training-Free Code Generation
Date read: 2026-05-21
Local PDF: `coordination/referencepaper/AnalogCoder_AAAI2024.pdf`

## Paper Type

Analog-domain LLM agent plus benchmark. It is not an RTL model-training paper.
It is closer to vaEVAS because it uses executable circuit simulation feedback, but
its target artifact is transistor-level analog circuit design through PySpice code,
not Verilog-A behavioral modeling.

## Core Contribution

AnalogCoder converts natural-language analog circuit design tasks into Python
code using PySpice. The system adds three pieces around a base LLM:

1. domain-specific prompt engineering with an analog design example and
   chain-of-thought-style design planning.
2. a feedback-enhanced design flow that runs circuit checks and feeds failures
   back to the LLM for repair.
3. a circuit tool library that stores successful basic circuits as reusable
   subcircuits for harder composite tasks.

The paper also introduces a 24-task analog circuit design benchmark covering
basic circuits and composite circuits.

## Problem Setting

The authors argue that LLMs are weaker on analog design than digital design
because analog circuits require low-level physical components, dense
interconnections, continuous-valued behavior, and SPICE-like expertise. They
also point out that public SPICE code is scarce compared with Python, so they
ask the LLM to generate Python/PySpice rather than raw SPICE.

This is important for us because it is an explicit argument for using an
intermediate execution surface that LLMs can handle better. In vaEVAS, our
corresponding move is different: we keep the target artifact as Verilog-A, but
build deterministic checker assets and a fast evaluator around it.

## Method

The generated artifact is executable Python/PySpice code. The paper's checking
loop has four stages:

1. requirement check: required input/output nodes and basic topology constraints.
2. simulation and operating-point check: simulation errors, floating nodes, and
   MOSFET activity/operating conditions.
3. DC sweep check: whether output changes with input and whether a better bias
   point can be selected.
4. function check: circuit-type-specific AC/DC/transient behavior checks.

Failed stages return concrete error information to the LLM. The default limit is
three attempts for basic circuits and two attempts for composite circuits.

The circuit tool library stores successful basic circuits with simulated
specifications such as gain and phase. For composite designs, the LLM retrieves
subcircuits and calls them directly from generated PySpice code.

## Benchmark And Metrics

The benchmark has 24 tasks:

1. tasks 1-15 are basic analog circuits such as amplifiers, inverters, current
   mirrors, and op-amps.
2. tasks 16-24 are composite circuits such as oscillators, integrator,
   differentiator, adder, subtractor, Schmitt trigger, VCO, and PLL.

The main metric is Pass@k, with Pass@1 and Pass@5 reported. They also report
the number of distinct tasks solved at least once across repeated trials.

Functional correctness is circuit-type-specific. Examples include positive gain
and drain current for amplifiers, differential-mode gain greater than common-mode
gain for op-amps, oscillation peak/amplitude/period checks for oscillators, and
formula-based waveform checks for integrator/adder/subtractor tasks.

## Results

AnalogCoder is GPT-4o plus the circuit tool library, prompt engineering, and
feedback flow. It solves 20 of 24 benchmark tasks, compared with 15 solved by
GPT-4o without the tool library. The reported average Pass@1/Pass@5 for
AnalogCoder is 66.1/75.9.

The ablation section is useful for our framing:

1. generating Python/PySpice is stronger than generating SPICE directly.
2. in-context examples, chain-of-thought planning, and feedback flow each matter.
3. fine-tuning GPT-3.5 improves success rate on already-solvable tasks, but does
   not expand the number of distinct circuits solved under limited data.

This supports our earlier intuition: RTLCoder-style training is not the deepest
axis for our paper; simulator/checker-grounded workflow and benchmark validity
matter more.

## Limitations

The paper explicitly says current LLMs still cannot design highly complex analog
circuits. The benchmark uses simplified settings such as Level-1 MOSFET models,
and the main goal is functional circuit creation rather than industrial-grade
optimization or full process signoff.

For vaEVAS positioning, the bigger limitation is that the benchmark is not about
Verilog-A behavioral modeling. It does not define a behavioral model release
package with public prompts, gold Verilog-A assets, deterministic checkers,
score denominators, and independent simulator certification.

## Relevance To vaEVAS

AnalogCoder should be cited as the closest earlier analog-domain LLM agent:
it shows that simulation feedback can make LLM-generated analog artifacts more
reliable, and it provides an analog task benchmark.

Our contrast should be direct:

1. AnalogCoder targets transistor-level analog circuit construction through
   PySpice; vaEVAS targets Verilog-A behavioral model generation/evaluation.
2. AnalogCoder uses SPICE/PySpice simulation to repair generated circuits;
   vaEVAS uses EVAS as a fast behavioral evaluator and Spectre as the final
   certification reference.
3. AnalogCoder's contribution is an agent method plus a 24-task analog design
   benchmark; vaEVAS's contribution is a benchmark/evaluator practice package
   with release artifacts, deterministic checkers, EVAS/Spectre parity evidence,
   and claim gates.
4. AnalogCoder validates generated circuits by task-specific checks; vaEVAS
   separates L0 evaluator conformance from L1/L2 scored behavioral tasks and
   preserves the no EVAS PASS / Spectre FAIL invariant.

## Positioning Sentence

AnalogCoder demonstrates that simulator-grounded LLM loops are viable for analog
circuit construction; vaEVAS targets the complementary gap for Verilog-A
behavioral modeling by providing benchmark assets, deterministic functional
checkers, and EVAS/Spectre certification around executable behavioral models.
