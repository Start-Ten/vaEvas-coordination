# vaEvas Execution Loop

Use this workflow when handling `vaEvas` tasks. Keep the human in the manager role and keep execution inside the agent loop.

## 1. Intake

Identify:

1. Which layer the task belongs to: `EVAS`, `behavioral-veriloga-eval`, or `veriloga-skills`
2. Task type: feature, bugfix, benchmark, workflow, or docs
3. Existing constraints from local docs before asking the user to clarify anything

Read the nearest relevant docs first:

1. `EVAS/CLAUDE.md`
2. `behavioral-veriloga-eval/AGENTS.md`
3. `worksche/AI_WORKFLOW_OPTIMIZATION.md`
4. `references/project-goals.md` from this skill

## 2. Interview Before Plan

Before writing a plan, interview the user to fill the minimum missing context. Keep the interview short and concrete.

Collect:

1. Success condition
2. Non-goals
3. Compatibility constraints
4. Metrics or numbers that define acceptance
5. Whether this task should leave behind a reusable asset

If local docs already answer some of these, state the inferred answer and ask only for the unresolved parts.

## 3. Produce the Brief

Create a one-page task brief using `assets/brief-template.md`.

The brief must include:

1. Task
2. Scope
3. Non-goals
4. Constraints
5. Acceptance
6. KPIs
7. Required logs

If the brief is weak, stop and refine it before planning.

## 4. Set KPI Before Coding

Use `assets/kpi-template.md`.

Always define:

1. Primary KPI
2. Secondary KPI
3. Guardrails
4. Required evidence

Default KPI mapping by layer:

1. `EVAS`
   Use example pass rate, test pass rate, runtime, and behavior correctness.
2. `behavioral-veriloga-eval`
   Use task executability, deterministic `Pass@1`, and failure attribution completeness.
3. `veriloga-skills`
   Use first-pass compile success, verification closure, and reusability of the guidance.

## 5. Write a Controlled Plan

Use `assets/plan-template.md`.

Every plan must include:

1. Goal
2. Assumptions
3. Steps
4. Risks
5. Stop conditions

Do not jump into coding for non-trivial tasks until this exists.

## 6. Execute With Closed Loop

Sequence:

1. Implement
2. Run the smallest relevant validation
3. Classify any failure
4. Repair one focused issue at a time
5. Re-run validation

Do not drift into repeated blind edits. If the same failure type repeats twice, escalate in the final summary or pause for user input when the risk is material.

## 7. Log the Work

Use `assets/log-template.md`.

Always record:

1. Commands
2. Output paths
3. Changed files
4. Result summary
5. Failure labels
6. Next-step recommendation

Prefer reproducible facts over narrative.

## 8. Finish With Review

Use `assets/review-template.md`.

The final review should tell the user:

1. Whether KPI was achieved
2. What was verified
3. What remains risky or unverified
4. What should be templated or skill-ified next time
