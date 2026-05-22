# vaEVAS Related-Work Reading Order

Date: 2026-05-21

Goal: read papers in the order that best supports a Verilog-A behavioral
modeling practice paper. Do not let the related work drift into generic RTL
model training.

## Group 1: Closest Peers For The vaEVAS Story

1. **AnalogCoder**
   - Why first: closest analog-domain LLM/SPICE-feedback peer.
   - Read for: analog task definition, SPICE feedback loop, contribution framing, and limitations.
   - vaEVAS contrast: transistor-level analog design vs Verilog-A behavioral benchmark/evaluator.

2. **AMS-IO-Bench / AMS-IO-Agent**
   - Why second: recent AMS benchmark + structured agent + industrial deliverable framing.
   - Read for: how an engineering workflow becomes a publishable benchmark/agent paper.
   - vaEVAS contrast: I/O design automation vs behavioral Verilog-A validation and certification.

3. **AutoSizer / AMS-SizingBench**
   - Why third: benchmark + LLM agent + simulator loop for AMS sizing.
   - Read for: benchmark construction, simulator feedback, metric design, and agent workflow.
   - vaEVAS contrast: transistor sizing optimization vs behavioral-model generation/evaluation.

## Group 2: Simulator Feedback And AMS Benchmark Context

4. **SMPS SPICE Workflows**
   - Read for: LLM workflow plus SPICE tool interface and simulation-feedback benchmark design.

5. **AMSbench**
   - Read for: broad AMS benchmark motivation and task taxonomy.
   - Caveat: more multimodal/QA than executable Verilog-A generation.

6. **AnalogSAGE**
   - Read for: simulation-grounded multi-agent design and memory/experience framing.
   - Caveat: agent method is context, not vaEVAS's main contribution.

## Group 3: HDL Benchmark Method References

7. **VerilogEval / VerilogEval v2**
   - Read for: classic HDL benchmark prompt mechanics, completion vs spec-to-RTL
     prompting, output extraction, ICL risks, and failure classification.
   - vaEVAS contrast: digital self-contained RTL modules vs behavioral Verilog-A
     DUT/TB/bugfix/E2E tasks with EVAS/Spectre validation.

8. **CVDP**
   - Read for: modern RTL benchmark taxonomy and agentic/non-agentic evaluation.
   - vaEVAS contrast: CVDP extends workflow categories; VerilogEval is still the
     cleaner prompt/evaluation protocol reference.

9. **RealBench**
   - Read for: realistic IP-level artifact selection and benchmark realism.

10. **ProtocolLLM**
   - Read for: protocol/waveform/timing correctness as an evaluation target.

11. **VeriCoder**
   - Read for: functional-validation-backed data generation and why syntax-only filtering is weak.

## Group 4: Legacy Or Lower-Priority Context

12. **RTLCoder**
    - Use as model-training/data-generation legacy context.

13. **BetterV / VGen / OpenLLM-RTL**
    - Use only for related-work coverage and historical framing.

## Reading Rule

For each paper, extract:

1. problem setting.
2. task/benchmark definition.
3. simulator or checker feedback loop.
4. evaluation metrics.
5. claimed contribution.
6. limitations.
7. one paragraph on how vaEVAS is different.
