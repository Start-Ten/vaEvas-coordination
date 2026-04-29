---
name: vaevas-workflow
description: >
  Run vaEvas project work through an interview-led execution loop before coding. Use when working
  in `vaEvas`, `EVAS`, `behavioral-veriloga-eval`, or `veriloga-skills` and the task involves
  implementation, bugfixing, benchmark authoring, workflow setup, or structured project planning.
  This skill turns vague requests into a brief, KPI, controlled plan, execution log, and review so
  the human can manage scope and outcomes instead of micromanaging code changes.
---

# vaEvas Workflow

## Overview

Use this skill to keep `vaEvas` work inside a repeatable management loop:

1. clarify project intent
2. interview before planning
3. define KPI before coding
4. execute with validation
5. leave auditable logs and a review

Start by reading [references/project-goals.md](./references/project-goals.md). Read [references/execution-loop.md](./references/execution-loop.md) next for the operating procedure.

## Operating Rules

Follow these rules on every non-trivial `vaEvas` task:

1. Infer as much context as possible from local docs before questioning the user.
2. Interview before writing a plan.
3. Write a brief and KPI before implementation.
4. Keep the user in the manager role: ask for decisions only when risk or scope is unclear.
5. Validate every meaningful code change.
6. Record reproducible logs, not just narrative summaries.
7. End with KPI status, residual risk, and the next reusable improvement.

## Project Priorities

Optimize decisions against these project priorities:

1. Keep the benchmark EVAS-only unless the user explicitly expands the scope.
2. Prefer executable evidence over text-only evaluation.
3. Protect deterministic `Pass@1`, compile success, and simulation correctness as primary metrics.
4. Turn repeated workflows into reusable templates, skills, or scripts.

## Workflow

### 1. Orient

Identify the layer:

1. `EVAS`
2. `behavioral-veriloga-eval`
3. `veriloga-skills`

Read the nearest local instruction files first.

### 2. Interview

Before planning, collect the missing information needed to fill:

1. success condition
2. non-goals
3. compatibility constraints
4. acceptance metrics
5. required reusable artifacts

Use the shortest possible interview that resolves material uncertainty.

### 3. Prepare Execution Artifacts

Create these artifacts before substantial coding:

1. Brief from [assets/brief-template.md](./assets/brief-template.md)
2. KPI from [assets/kpi-template.md](./assets/kpi-template.md)
3. Plan from [assets/plan-template.md](./assets/plan-template.md)

Skip only when the user explicitly wants lightweight exploration and no implementation.

### 4. Execute

Implement in focused increments. After each meaningful increment:

1. run the smallest relevant validation
2. classify failures explicitly
3. decide whether to repair, stop, or escalate

### 5. Log and Review

Capture execution facts with [assets/log-template.md](./assets/log-template.md) and summarize using [assets/review-template.md](./assets/review-template.md).

## Default KPI Mapping

Use this default mapping unless the user defines a better one.

### `EVAS`

1. example or test pass rate
2. behavior correctness
3. runtime or wall-clock impact when relevant

### `behavioral-veriloga-eval`

1. `dut_compile`
2. `tb_compile`
3. `sim_correct`
4. deterministic `Pass@1`
5. failure attribution completeness

### `veriloga-skills`

1. first-pass DUT compile success
2. verification closure on representative cases
3. reusability of guidance or templates

## Stop Conditions

Pause or escalate when:

1. the same failure class repeats twice without new evidence
2. a fix would change scoring semantics or benchmark scope
3. local docs conflict and the correct rule cannot be inferred safely
4. validation cannot be run and the missing evidence affects correctness

## Output Standard

The final response should always state:

1. what changed
2. what was verified
3. whether KPI was met
4. what remains risky
5. what should be templated or skill-ified next
