# vaEvas Project Goals

## North Star

Increase the reliability of agent-generated, EVAS-compatible, pure voltage-domain Verilog-A work by closing the loop between code generation, executable verification, and structured benchmark scoring.

## System Roles

### `veriloga-skills/`

Purpose:

1. Encode authoring rules for Verilog-A behavioral models.
2. Improve first-pass code generation quality.
3. Route verification to the right backend: EVAS for voltage-domain, OpenVAF for current-domain.

Success signals:

1. Higher first-pass compile rate for generated DUTs.
2. Lower repair effort on common voltage-domain modules.
3. Reusable skill guidance instead of one-off prompting.

### `EVAS/`

Purpose:

1. Provide a lightweight event-driven simulator for voltage-mode Verilog-A behavioral models.
2. Make verification executable and reproducible with `.scs` testbenches, waveform output, and validation scripts.
3. Serve as the main execution backend for the voltage-domain benchmark.

Success signals:

1. Example suite remains stable.
2. Tests and validations pass.
3. Behavior stays aligned with expected outputs for supported constructs.

### `behavioral-veriloga-eval/`

Purpose:

1. Build a structured benchmark layer above skill-local eval lists.
2. Evaluate EVAS-compatible voltage-domain tasks using executable evidence.
3. Measure deterministic `Pass@1` rather than text-only rubric compliance.

Primary task families:

1. `spec-to-va`
2. `bugfix`
3. `tb-generation`
4. `end-to-end`

Primary scoring axes:

1. `dut_compile`
2. `tb_compile`
3. `sim_correct`

Success signals:

1. Task cases are runnable and reproducible.
2. Failure attribution is explicit.
3. Aggregate reporting reflects real execution, not precheck-only heuristics.

## Management Implications

When working in `vaEvas`, optimize for these outcomes:

1. Preserve EVAS-only benchmark scope unless the project explicitly expands.
2. Prefer executable validation over prose judgments.
3. Favor stable examples, reproducible commands, and explicit result artifacts.
4. Turn repeated execution patterns into reusable skills, templates, or scripts.
