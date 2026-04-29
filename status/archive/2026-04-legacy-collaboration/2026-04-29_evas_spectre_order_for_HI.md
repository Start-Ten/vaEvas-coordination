# EVAS / Spectre Order For A-D-F-G-H-I

Date: 2026-04-29

## Current Anchor

Use the same real-Spectre-compatible strict-v3 lineage as the current ADFG table:

| Condition | EVAS PASS | Spectre PASS | Role |
|---|---:|---:|---|
| A | 23/92 | 23/92 | prompt-only baseline |
| D | 43/92 | 43/92 | A + public Spectre/Verilog-A rules |
| F | 59/92 | 59/92 | D + EVAS-only repair loop |
| G | 65/92 | 65/92 | F + syntax-zero / compile-clean gate |

H and I should start from this G lineage unless explicitly marked as a historical or diagnostic run.

## Main Rule

EVAS is the repair-loop simulator and feedback source. Spectre is the final
compatibility gate and the calibration source for EVAS itself.

Do not use Spectre logs inside the repair loop for F/G/H/I. If a candidate
passes EVAS, then run Spectre only as a final gate. If EVAS and Spectre
disagree, fix EVAS/scoring/checker infrastructure first, then rerun the affected
delta tasks under all relevant conditions.

## Experiment Order

### 1. Infrastructure Freeze

Before running H/I, freeze:

- public strict-v3 Verilog-A/Spectre rules;
- EVAS core parser/engine behavior;
- checker versions;
- Spectre mode policy;
- materialization logic;
- result-counting script.

Any later EVAS/Spectre mismatch fix is an infrastructure update, not a method
gain. It must be applied consistently to A/D/F/G/H/I by delta rerun or full rerun.

### 2. A and D

Run order:

1. Generate full92 artifacts.
2. Score all tasks with EVAS.
3. Run Spectre final gate.
4. Compare EVAS/Spectre pass-fail.
5. If mismatch exists, repair EVAS/checker/scorer, then rerun the mismatched
   tasks and update A/D counts.

A and D do not use repair feedback. They establish whether the prompt and public
rules produce Spectre-compatible artifacts.

### 3. F

Run order:

1. Start from D policy.
2. Run EVAS-only repair loop, max 3 rounds.
3. Use only EVAS status, EVAS notes, compile logs, and checker metrics as LLM
   feedback.
4. Materialize the best artifact per task.
5. Score full92 with EVAS.
6. Run Spectre final gate for the final materialized artifacts.
7. If EVAS/Spectre mismatch exists, repair EVAS/checker/scorer and rerun affected
   deltas.

F measures whether raw EVAS feedback can improve over public-rule prompting.

### 4. G

Run order:

1. Start from F artifacts and failure classes.
2. Apply compile/interface/missing-file/syntax-zero gate repair.
3. Keep the feedback source as EVAS only.
4. Materialize newly fixed artifacts only after EVAS PASS.
5. Run Spectre final gate for changed tasks, then synthesize the full92 count.
6. If a changed task exposes EVAS/Spectre mismatch, fix EVAS/checker/scorer and
   rescore the affected A/D/F/G deltas.

G measures whether compile/pipeline failures can be driven toward zero before
behavior-level diagnosis begins.

### 5. H-v1

Run order:

1. Start from final G failures only for the fast targeted run.
2. Add H-v1 failure-signature translation.
3. Do not add Codex expert mechanism cards or historical memory.
4. Run EVAS repair loop, max 3 rounds.
5. For each attempt, log raw EVAS feedback, H signature, confidence, and repair
   focus.
6. Materialize EVAS PASS candidates.
7. Run Spectre final gate on newly materialized passes.

H-v1 tests whether a basic diagnostic translation layer helps beyond G.

### 6. H-v2

Run order:

1. Audit H-v1 translations against the final G 27 failures.
2. Use Codex only to improve the translator rules, not to provide circuit
   solutions for individual tasks.
3. Freeze the H-v2 signature rule set.
4. Rerun the same G-failed target set with EVAS-only repair.
5. Spectre-gate only new EVAS passes.

H-v2 tests whether better error translation helps. Codex involvement here is
allowed only as rule-authoring before the run, not as per-case repair memory.

### 7. I-GSeed / I-History / I-Codex / I-Full

Run order for each I variant:

1. Start from the same final G failures for targeted development.
2. Use H-v2 signatures as the diagnostic front end.
3. Inject only the allowed knowledge source for that variant:
   - I-GSeed: current G failure-derived mechanism cards.
   - I-History: historical fail/pass distilled experience.
   - I-Codex: Codex-curated general circuit mechanism knowledge.
   - I-Full: all allowed sources combined.
4. Run EVAS repair loop, max 3 rounds.
5. Log provenance for every injected hint and every accepted repair.
6. Materialize EVAS PASS candidates.
7. Run Spectre final gate on new passes.
8. After targeted evidence is positive, run full92 cold-start I-Full.

I measures whether external experience and circuit mechanism knowledge add value
beyond H's translation layer.

## Mismatch Handling

When EVAS and Spectre disagree, do not continue counting method gains until the
cause is classified.

| Mismatch | Meaning | Required action |
|---|---|---|
| EVAS PASS, Spectre FAIL | EVAS false positive or Spectre-mode issue | Patch EVAS core, preflight, checker, or Spectre runner; rerun affected deltas |
| EVAS FAIL, Spectre PASS | EVAS false negative, checker sampling issue, or simulator semantic gap | Patch EVAS/checker if Spectre behavior is valid; rerun affected deltas |
| Both FAIL but for different reasons | diagnostic inconsistency | classify as infrastructure risk; patch only if pass/fail can change |
| Both PASS | accepted | no action |

Every infrastructure patch must be recorded with:

- root cause;
- touched files;
- affected tasks;
- before/after EVAS result;
- before/after Spectre result;
- whether the full92 count changed.

## Reporting Order

For every condition, report two numbers:

```text
EVAS PASS / 92
Spectre PASS / 92
```

For development-stage targeted runs, also report:

```text
targeted new EVAS PASS
targeted new Spectre-confirmed PASS
regressions among previously PASS tasks
remaining compile/interface/missing-file failures
remaining behavior failures
```

## Paper Interpretation

The method story should not claim that Spectre teaches the loop. The clean story is:

1. EVAS provides fast approximate feedback for iterative repair.
2. Spectre validates final compatibility.
3. EVAS/Spectre mismatches are treated as simulator/scorer infrastructure bugs.
4. H improves feedback interpretability.
5. I improves behavior repair by adding auditable mechanism knowledge and
   provenance.
