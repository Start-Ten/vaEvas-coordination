# Reference Papers

This folder stores papers used to position the vaEVAS paper.

Current goal: publish our Verilog-A practice, not a generic RTL-generation
survey. Prioritize papers about analog/mixed-signal practice, simulator
feedback, executable benchmark design, and behavioral-model verification. RTL
papers are still useful, but only as evaluation-method references.

## Tier 1: Closest To The vaEVAS Story

| Priority | Paper | Local file | Why it matters |
| --- | --- | --- | --- |
| 1 | AnalogCoder, AAAI 2024 | [AnalogCoder_AAAI2024.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/AnalogCoder_AAAI2024.pdf) | Closest analog-domain LLM peer: training-free generation with SPICE feedback. Use it as the main foil: it designs transistor-level analog circuits, while vaEVAS builds a Verilog-A behavioral benchmark/evaluator. |
| 2 | AMS-IO-Bench and AMS-IO-Agent, AAAI 2026 | [AMS-IO-Bench_Agent_2026.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/AMS-IO-Bench_Agent_2026.pdf) | Strong recent AMS practice paper: benchmark + structured agent + industrial deliverables + tape-out validation. Useful for arguing "real AMS workflow, not toy HDL." |
| 3 | AutoSizer / AMS-SizingBench, 2026 | [AutoSizer_AMS-SizingBench_2026.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/AutoSizer_AMS-SizingBench_2026.pdf) | Recent simulator-backed AMS benchmark and agent loop. Useful contrast: transistor sizing optimization vs Verilog-A behavioral model generation/evaluation. |
| 4 | Evaluating LLM-based Workflows for Switched-Mode Power Supply Design, 2025 | [SMPS_SPICE_Workflows_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/SMPS_SPICE_Workflows_2025.pdf) | Uses SPICE simulation feedback in a concrete circuit-design loop. Useful for positioning EVAS/Spectre feedback as the analogous behavioral-model loop. |
| 5 | AMSbench, 2025 | [AMSbench_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/AMSbench_2025.pdf) | Broad AMS multimodal benchmark. Useful to show that AMS evaluation is emerging, but it is QA/perception-heavy rather than executable Verilog-A generation. |
| 6 | AnalogSAGE, 2025 | [AnalogSAGE_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/AnalogSAGE_2025.pdf) | Self-evolving analog multi-agent framework with simulation-grounded feedback. Useful as an agentic AMS comparison. |
| 7 | EasySize, 2025 | [EasySize_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/EasySize_2025.pdf) | LLM-guided analog sizing with heuristic search. Lower priority, but useful for the "LLM + simulator loop" trend. |
| 8 | Self-Calibrating LLM Analog Sizing, 2026 | [Self-Calibrating-LLM-Analog-Sizing_2026.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/Self-Calibrating-LLM-Analog-Sizing_2026.pdf) | Interpretable design-equation loop with calibration. Useful only for discussion of analog automation beyond benchmark/evaluator scope. |
| 9 | MMCircuitEval, 2025 | [MMCircuitEval_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/MMCircuitEval_2025.pdf) | General multimodal circuit benchmark; cite as broad circuit-MLLM evaluation, not as direct executable benchmark. |

## Tier 2: HDL Benchmark And Verification Method References

| Priority | Paper | Local file | Why it matters |
| --- | --- | --- | --- |
| 1 | CVDP, 2025 | [CVDP_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/CVDP_2025.pdf) | Best recent RTL benchmark counterpart: agentic/non-agentic tasks and explicit design/verification framing. |
| 2 | RealBench, 2025 | [RealBench_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/RealBench_2025.pdf) | Real-world IP-level Verilog benchmark; useful for "benchmark should use realistic artifacts." |
| 3 | ProtocolLLM, 2025 | [ProtocolLLM_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/ProtocolLLM_2025.pdf) | Protocol-level waveform/timing correctness; useful analogy for Verilog-A behavioral checker design. |
| 4 | ChipBench, 2026 | [ChipBench_2026.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/ChipBench_2026.pdf) | Broad chip-design benchmark across generation, debugging, and reference-model tasks. |
| 5 | VeriCoder, 2025 | [VeriCoder_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/VeriCoder_2025.pdf) | Functional-validation-backed RTL data generation; directly highlights why syntax-only datasets are insufficient. |
| 6 | ACE-RTL, 2026 | [ACE-RTL_2026.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/ACE-RTL_2026.pdf) | Agentic RTL generation/debug comparison after CVDP. |
| 7 | SiliconMind-V1, 2026 | [SiliconMind-V1_2026.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/SiliconMind-V1_2026.pdf) | Recent RTL multi-agent/debug-reasoning baseline. |
| 8 | Synthesis-in-the-Loop RTL Evaluation, 2026 | [Synthesis-in-the-Loop_RTL_2026.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/Synthesis-in-the-Loop_RTL_2026.pdf) | Useful for "functional pass is not enough"; analogous to our claim-gated score/speed/report policy. |

## Tier 3: Legacy Or Lower-Priority Context

| Paper | Local file | Use |
| --- | --- | --- |
| RTLCoder, 2024/2025 | [RTLCoder_2024.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/RTLCoder_2024.pdf) | Model-training/data-generation reference. Its syntax-only filtering weakness motivates executable functional validation. |
| VerilogEval v2, 2025 | [VerilogEval_v2_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/VerilogEval_v2_2025.pdf) | Prompt-tuning/failure-classification update to VerilogEval; useful context, but lower priority than CVDP. |
| BetterV, 2024 | [BetterV_ICML2024.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/BetterV_ICML2024.pdf) | HDL generation method reference, not a direct benchmark peer. |
| OpenLLM-RTL, 2025 | [OpenLLM-RTL_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/OpenLLM-RTL_2025.pdf) | Dataset/framework context. |
| VerilogEval, 2023 | [VerilogEval_2023.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/VerilogEval_2023.pdf) | Historical executable Verilog benchmark predecessor. |
| VGen, 2022 | [VGen_2022.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/VGen_2022.pdf) | Historical minimal compile/test loop. |
| QiMeng-CodeV-R1, 2025 | [QiMeng-CodeV-R1_2025.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/QiMeng-CodeV-R1_2025.pdf) | Recent Verilog-specialized model/training reference; low relevance to Verilog-A practice. |
| COEVO, 2026 | [COEVO_2026.pdf](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/referencepaper/COEVO_2026.pdf) | RTL functional/PPA optimization; use only if discussing optimization beyond correctness. |

## Positioning Notes For vaEVAS

The strongest story is not "we trained another HDL model." It is:

1. Analog/AMS LLM papers increasingly use simulator feedback, but mostly target transistor sizing, netlist/schematic generation, I/O ring automation, or QA.
2. RTL benchmark papers have better executable evaluation discipline, but target digital Verilog/SystemVerilog rather than Verilog-A behavioral models.
3. vaEVAS sits in the gap: a public Verilog-A behavioral benchmark with gold assets, deterministic checkers, EVAS/Spectre dual certification, score denominators, and claim-gated reports.

Use the phrase "Verilog-A behavioral modeling practice" when describing our
target. Avoid letting the related work drift into generic RTL model training.

## Recommended Reading Order

1. AnalogCoder
2. AMS-IO-Bench / AMS-IO-Agent
3. AutoSizer / AMS-SizingBench
4. SMPS SPICE workflows
5. AMSbench
6. CVDP
7. RealBench and ProtocolLLM
8. VeriCoder
9. ChipBench
10. RTLCoder and BetterV only for legacy/model-training contrast
