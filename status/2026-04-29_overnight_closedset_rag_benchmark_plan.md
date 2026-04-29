# Overnight Plan: Closed-Set Completion + Benchmark/RAG Expansion

Date: 2026-04-29

## Goal

Use the long overnight window to push the project along two tracks:

1. Closed-set 92 completion: use verified artifacts, R26/gold-derived mechanisms, materialized skeletons, EVAS feedback, and Spectre confirmation to drive the current 92 tasks toward near-100% pass.
2. Generalization foundation: create harder perturbation benchmark plans and upgrade the RAG/materializer path so later results can prove the system is not just replaying 92 task answers.

This plan deliberately separates closed-set engineering success from generalization evidence.

RAG is part of the closed-set critical path, not only a later side experiment.
For the current 92 tasks, RAG should route each failure to a verified artifact,
mechanism skeleton, repair card, or negative memory before any new LLM repair:

```text
prompt + interface + EVAS failure
-> functional/failure query
-> retrieve verified artifacts, R26/gold templates, skeletons, cards, negative memory
-> rerank by mechanism and slot compatibility
-> exact replay or slot-bound materializer
-> EVAS
-> Spectre
-> verified memory update
```

## Non-Negotiable Rules

- Do not report reused gold/R26 artifacts as cold-start success.
- Every adopted artifact must record provenance: gold, R26, G/H/I repair, manual, RAG, or materializer.
- EVAS PASS is a fast filter; Spectre PASS is the strict compatible result.
- If EVAS and Spectre disagree, first classify whether the issue is EVAS kernel, checker, runner, or genuine circuit behavior.
- Preserve current A/D/F/G results and result roots unless explicitly archiving them; do not delete active baselines.
- No single task may block the whole night. Every failed path must have a retry budget, a stop condition, and a written failure packet before moving on.
- New perturbation benchmarks must live in a separate namespace/directory from the original 92 tasks.  Do not mix generated benchmark-v2 tasks into `tasks/` until their manifest, gold, checker, and Spectre parity are reviewed.

## Retry Budgets and Stop Conditions

The overnight run should optimize total progress, not heroic work on one task.

### Per-Task Retry Budget

For each remaining failed task:

1. Exact verified-artifact replay:
   - Attempts: 1.
   - Stop if interface/hash/module mismatch is obvious.
   - If replay passes EVAS but fails Spectre, classify as EVAS/Spectre mismatch; do not keep replaying blindly.

2. Slot-bound materializer:
   - Attempts: up to 2 candidate variants.
   - Required before running: at least 70% slot coverage for ports/width/clock/reset/outputs.
   - Stop if both variants fail for the same compile/interface reason.

3. RAG-guided LLM repair:
   - Attempts: up to 3 repair rounds.
   - A round must change either failure class or at least one measurable metric gap to count as progress.
   - If two consecutive rounds produce the same failure signature, stop and write a failure packet.

4. Spectre confirmation:
   - Attempts: up to 2 for infrastructure/tool issues only.
   - If failure is genuine Verilog-A/Spectre incompatibility, send the task back to materializer/repair instead of retrying Spectre.

### Failure Packet

When a task exhausts its budget, write a compact packet:

- task_id
- best artifact root
- best EVAS status and note
- best Spectre status and note, if attempted
- retrieved RAG nodes
- slot-binding coverage
- failure class
- why we stopped
- next recommended action

These packets become training data for the next RAG/materializer iteration.

## Decision Gates

### Gate 1: After Closed-Set Ledger

Proceed to RAG/materializer only if:

- every active task has a known latest result root, or
- unknown roots are explicitly marked as `missing_result_root`.

If the ledger itself is inconsistent, spend at most 30 minutes fixing the ledger. If still inconsistent, freeze the inconsistency in the ledger and continue on the tasks with reliable roots.

### Gate 2: After RAG Routing Audit

Proceed to candidate generation if:

- top-3 retrieval contains a plausible mechanism/artifact for at least 70% of remaining failures, or
- the missed tasks are clearly marked as `no_knowledge_coverage`.

If retrieval is poor:

- do not spend many LLM calls;
- expand skeletons/cards for the missing mechanism families first;
- rerun retrieval audit once.

### Gate 3: After First 10 Targeted Admissions

If at least 3/10 produce new EVAS PASS candidates:

- continue targeted closed-set admission.

If fewer than 3/10 produce EVAS PASS:

- stop broad repair;
- switch to diagnosis mode:
  - inspect whether slot binding is wrong,
  - whether RAG retrieved wrong mechanisms,
  - whether failures are mostly checker/runner/tooling,
  - whether materializer skeletons are too weak.

### Gate 4: After New EVAS PASS

Only run Spectre for:

- newly admitted EVAS PASS tasks;
- tasks where EVAS/Spectre parity is uncertain and the result affects the main table.

Do not run Spectre for every failed EVAS task unless debugging an EVAS bug.

### Gate 5: Before Paper Update

Update paper narrative only after the result type is clear:

- closed-set completion result,
- perturbation benchmark plan/result,
- RAG retrieval audit,
- EVAS/Spectre parity correction.

Do not mix closed-set replay numbers with cold-start claims.

## Night Workstreams

### Workstream A: Closed-Set 92 Completion

Owner: primary terminal

Purpose: make current 92 tasks as complete as possible, without pretending this is cold-start generalization.

Steps:

1. Build a closed-set task ledger.
   - For every task, collect current best status across A/D/F/G/H/I/R26/gold/manual artifacts.
   - Fields: task_id, family, mechanism family, best EVAS status, best Spectre status, current best generated root, provenance, failure class, latest notes.

2. Build a verified artifact store.
   - Include artifacts that already pass EVAS + Spectre.
   - Store prompt hash, module/interface signature, mechanism label, source root, output files, and validation paths.

3. Classify the remaining failures.
   - Classes:
     - syntax/interface/missing file
     - simulator/tool mismatch
     - checker issue
     - behavior mechanism missing
     - system relation missing
     - unknown
   - Expected outcome: know exactly which failures can be solved by replay/materializer and which need mechanism work.

4. Run the closed-set RAG router.
   - Query inputs:
     - public prompt
     - module/interface signature
     - EVAS checker notes and metric gaps
     - current generated artifact summary
     - failure class
   - Retrieval corpus:
     - verified artifact store
     - R26/gold distilled templates
     - mechanism skeletons
     - contract/repair cards
     - negative memory from failed retrievals
   - Ranking criteria:
     - mechanism compatibility
     - slot coverage
     - forbidden-mechanism exclusion
     - prior EVAS/Spectre success
     - provenance confidence

5. Implement/complete materializer admission logic.
   - Exact replay when task signature matches a verified artifact.
   - Slot-bound materializer when mechanism matches but names/parameters differ.
   - Use concrete circuit templates/executable skeletons when available, similar in spirit to the previous 92PASS/R26 closure artifacts, but record them as closed-set teacher-derived templates rather than cold-start generation.
   - LLM repair only after the above two fail.

6. Run targeted repair/admission on remaining failures.
   - First EVAS quick or standard depending on task runtime.
   - Then Spectre only for newly admitted EVAS PASS artifacts.

Deliverables by morning:

- `coordination/status/2026-04-29_closedset92_completion_ledger.md`
- `behavioral-veriloga-eval/docs/VERIFIED_ARTIFACT_STORE.json`
- `behavioral-veriloga-eval/docs/CLOSEDSET_CIRCUIT_TEMPLATES.json`
- `behavioral-veriloga-eval/results/closedset92_completion_*/summary.json`
- List of newly admitted PASS tasks.
- List of remaining failures with root cause and next action.

## Workstream B: Mechanism Knowledge Distillation

Owner: primary terminal when waiting, or secondary terminal

Purpose: turn R26/gold/previous 92-pass knowledge into reusable mechanism templates and executable skeletons.

Steps:

1. Expand `docs/CIRCUIT_MECHANISM_SKELETONS.json` beyond the current four skeletons.
   - Add at least:
     - divider / counter ratio
     - comparator threshold/hysteresis
     - binary/thermometer DAC distinction
     - SAR logic/update chain
     - sample-hold
     - PRBS/LFSR
     - calibration/search/settled flag

2. For each skeleton, add:
   - mechanism label
   - positive trigger semantics
   - negative trigger semantics
   - slot schema
   - implementation skeleton
   - Verilog-A anti-patterns
   - provenance

3. Build a skeleton coverage report over 92 tasks.
   - Which tasks map to a skeleton?
   - Which skeletons are missing?
   - Which mappings are dangerous/ambiguous?

Deliverables:

- Updated `behavioral-veriloga-eval/docs/CIRCUIT_MECHANISM_SKELETONS.json`
- `coordination/status/2026-04-29_mechanism_skeleton_coverage.md`

## Workstream C: Hard Perturbation Benchmark Design

Owner: secondary terminal or background planning

Purpose: create the next benchmark split that can later prove mechanism-level generalization.

Storage rule:

- Draft new benchmark tasks under `behavioral-veriloga-eval/benchmark-v2/`.
- Do not place them directly under `behavioral-veriloga-eval/tasks/` during drafting.
- Keep a parallel structure so migration is easy:
  - `benchmark-v2/tasks/.../prompt.md`
  - `benchmark-v2/tasks/.../gold/dut.va`
  - `benchmark-v2/tasks/.../gold/tb_*.scs`
  - `benchmark-v2/tasks/.../checker.py` or checker metadata
  - `benchmark-v2/manifests/v2-small.json`
  - `benchmark-v2/README.md`
- Only after gold/EVAS/Spectre parity is reviewed should a task be promoted into the official `tasks/` tree.

Perturbation levels:

1. Surface rename:
   - `din` -> `dinp`, `ref_clk` -> `refclk`, reordered ports.

2. Semantic alias:
   - `din` -> `input`, `stimulus`, `sense_node`, `measured_level`, `external_drive`.

3. Keyword removal:
   - Remove names like DWA, PLL, PFD, monotonic, thermometer.
   - Replace with functional descriptions.

4. Negative/distractor cases:
   - binary DAC explicitly not thermometer.
   - binary counter explicitly not Gray code.
   - arbitrary code ordering explicitly not monotonic.

5. Parameter and checker perturbation:
   - bit width, ratio, VDD, pulse width, ramp time, tolerance, window size.

6. System composition:
   - ADC-DAC + calibration.
   - PLL + ratio hop.
   - PFD + reset race + lock detector.
   - DWA + segmented DAC glitch.

Immediate overnight scope:

- Draft `v2-small`: 5-8 mechanisms x 5 variants = 25-40 tasks.
- Do not try to fully author all gold/checkers overnight unless closed-set work finishes early.
- Produce machine-readable manifest first.

Deliverables:

- `coordination/docs/benchmark/VAEVAS_BENCHMARK_V2_PERTURBATION_PLAN.md`
- `behavioral-veriloga-eval/benchmark-v2/README.md`
- `behavioral-veriloga-eval/benchmark-v2/manifests/v2-small.json`

## Workstream D: RAG Architecture Upgrade Plan / Partial Implementation

Owner: primary terminal after closed-set ledger, or secondary terminal

Purpose: move RAG from keyword hints to functional mechanism retrieval and make it usable by Workstream A.

This workstream should explicitly borrow mature RAG patterns instead of only
doing ad-hoc keyword search:

- Query rewriting: rewrite raw prompts/failures into mechanism-level retrieval queries.
- HyDE-style retrieval: generate a hypothetical ideal mechanism description, then retrieve real templates/cards/skeletons around it.
- Hybrid retrieval: combine lexical/BM25-style token matching, semantic/embedding retrieval, and rule-based negative filters.
- Reranking: rerank top candidates by mechanism compatibility, forbidden-mechanism conflicts, slot coverage, and prior verified success.
- Graph/structure retrieval: use circuit relation graphs for system tasks such as PLL/PFD/ADC-DAC instead of flat text chunks only.
- Self-RAG/CRAG-style feedback: use EVAS/Spectre outcomes to decide whether retrieval was useful, then write positive/negative memory.

Target architecture:

```text
prompt + EVAS failure
-> Functional IR
-> query rewriting / mechanism hypothesis
-> hybrid retrieval
-> reranker
-> slot binding
-> materialized skeleton
-> EVAS
-> Spectre
-> verified memory update
```

Overnight implementation priority:

1. Closed-set RAG router prototype.
   - Given a task_id and current failure record, output:
     - top artifact candidates
     - top concrete circuit-template candidates
     - top skeleton candidates
     - top repair cards
     - forbidden/risky candidates
     - slot coverage score

2. Query rewriting and HyDE mechanism hypothesis.
   - Input: raw prompt + EVAS notes + failure class.
   - Output:
     - rewritten mechanism query
     - hypothetical ideal mechanism description
     - explicit negative constraints
   - Example:
     - Raw: "The node named input carries the measured analog level..."
     - Rewritten: "ADC-DAC quantization; analog input; code outputs; reconstructed monotonic analog output."
     - Negative: "not thermometer unless prompt asks unit-cell/unary code."

3. Functional IR export.
   - Save per-task inferred mechanism claims and slots.

4. Slot binding prototype.
   - Bind port names, width, clock/reset, outputs, references from prompt and interface.

5. Hybrid retrieval and reranking.
   - Lexical retrieval: current token/IDF path.
   - Semantic retrieval: optional embedding index if local package/API is available; otherwise leave as pluggable.
   - Rule filters: binary-vs-thermometer, Gray-vs-binary, PLL-vs-divider, PFD-vs-generic pulse.
   - Reranking features:
     - mechanism match
     - slot coverage
     - negative constraint violation
     - EVAS/Spectre provenance confidence
     - source type: verified artifact > concrete template > skeleton > card > broad skill.

6. Retrieval audit metrics.
   - mechanism recall@k
   - forbidden mechanism top-k rate
   - slot binding coverage
   - artifact-replay admission rate
   - reranker lift over raw retrieval
   - positive/negative memory hit rate

7. Verified memory update.
   - EVAS+Spectre PASS retrievals become positive memory.
   - Repeated wrong retrievals become negative memory.
   - Memory entries must include task_id, mechanism, query, retrieved nodes, outcome, and reason.

Defer if time is short:

- trained reranker.
- post-training data export.

Deliverables:

- `coordination/status/2026-04-29_rag_upgrade_notes.md`
- Optional prototype scripts under `behavioral-veriloga-eval/runners/`

## Workstream E: Paper Narrative Update

Owner: only after A/B/C have concrete artifacts

Purpose: keep the paper story aligned with the new plan.

Update narrative:

1. EVAS enables fast closed-loop validation.
2. 92-task seed set is used for teacher-distilled closed-set completion.
3. R26/gold/history are distilled into verified mechanism knowledge.
4. Perturbed benchmark is used for generalization, not the original 92 closed-set.
5. RAG/materializer is evaluated by both closed-set completion and perturbation transfer.

Deliverables:

- Update `coordination/docs/paper/VAEVAS_PAPER_DRAFT_ZH.md`
- Update `coordination/docs/paper/VAEVAS_OPENLLM_STYLE_DRAFT.md`

## Suggested Time Order

### T0-T30 min: Snapshot and Ledger Setup

- Record git status and active result roots.
- Generate closed-set task ledger skeleton.
- Do not start expensive model calls until the ledger identifies remaining failures.

Decision gate:

- If current best roots are inconsistent, stop and write the inconsistency.
- If roots are clear, proceed to materializer/admission.

### T30-T120 min: Closed-Set Failure Classification

- Collect best result per task.
- Classify remaining failures.
- Identify exact replay candidates and materializer candidates.

Decision gate:

- If many failures are still compile/interface, prioritize G-style hard constraints/materializer wrappers.
- If many failures are behavior/system, prioritize skeleton/materializer.

### T2-T5 h: Targeted Closed-Set Admission

- Run RAG-routed exact replay/materializer candidates.
- EVAS score targeted changed tasks.
- Spectre validate only new EVAS PASS tasks.

Decision gate:

- Adopt only EVAS+Spectre PASS.
- Record EVAS-only PASS separately.

### T5-T7 h: Knowledge and RAG Upgrade

- Expand skeletons for uncovered mechanisms.
- Run retrieval audit on 92 + current synthetic cases.
- Implement slot-binding prototype if time permits.

Decision gate:

- If skeleton coverage is below 80% of 92 tasks, keep expanding mechanism skeletons before spending many LLM calls.

### T7-T8 h: Perturbation Benchmark Draft

- Draft v2-small perturbation manifest under `behavioral-veriloga-eval/benchmark-v2/`.
- Mark which tasks require new gold/checkers.
- Prioritize 10 tasks for the first actual execution run.

### Final 30 min: Morning Report

- Summarize:
  - A/D/F/G baseline unchanged.
  - closed-set progress.
  - newly verified artifacts.
  - remaining root causes.
  - perturbation benchmark draft.
  - RAG upgrade status.

## Parallelization Plan

### Terminal A: Critical Path

1. closed-set ledger
2. RAG router and slot-binding audit
3. materializer/admission
4. targeted EVAS
5. targeted Spectre
6. failure packets and morning summary

### Terminal B: Knowledge/Benchmark Sidecar

1. expand mechanism skeletons
2. create skeleton coverage table
3. draft perturbation manifest
4. write benchmark v2 plan

### Terminal C: Validation Sidecar, if available

1. Spectre validate only newly admitted EVAS PASS tasks
2. investigate EVAS/Spectre mismatch
3. update mismatch log

## Optional Sub-Agent / Reviewer Roles

If extra Codex terminals or sub-agents are available, use them as reviewers and sidecar workers rather than duplicating the critical path.

### Audit Agent: Provenance and Leakage Review

Scope:

- Read the closed-set ledger, verified artifact store, and morning summary.
- Check whether each PASS is labeled as cold-start, closed-set replay, RAG/materializer, or manual.
- Flag any result that could be accidentally presented as a stronger claim than it supports.

Output:

- `coordination/status/2026-04-29_audit_agent_provenance_review.md`

### Validation Agent: EVAS/Spectre Consistency

Scope:

- Inspect only tasks with EVAS/Spectre disagreement.
- Decide whether the issue belongs to EVAS kernel, checker, runner, bridge, or genuine generated code.
- Recommend the minimal fix and whether the result table needs updating.

Output:

- `coordination/status/2026-04-29_validation_agent_evas_spectre_review.md`

### RAG Agent: Retrieval Quality Review

Scope:

- Review RAG top-k results for remaining failures.
- Check false positives, especially binary-vs-thermometer, PLL-vs-divider, PFD-vs-generic pulse, Gray-vs-binary counter.
- Suggest missing skeletons or negative rules.

Output:

- `coordination/status/2026-04-29_rag_agent_retrieval_review.md`

### Benchmark Agent: Perturbation Design Review

Scope:

- Review the v2-small perturbation manifest.
- Ensure variants are harder than simple renaming.
- Ensure train/dev/test split can demonstrate generalization and not answer replay.

Output:

- `coordination/status/2026-04-29_benchmark_agent_v2_review.md`

### Agent Coordination Rules

- Agents should not edit active result roots unless explicitly assigned.
- Agents should write review files and concrete recommendations.
- If an agent makes code changes, it must own a disjoint file set and list changed files.
- Main terminal decides what to adopt.
- Reviewer findings should include file paths and line references where possible.

## What Counts as Success Tonight

Minimum useful outcome:

- A reliable closed-set ledger exists.
- Remaining 92 failures are classified.
- At least a few exact replay/materializer candidates are admitted with EVAS+Spectre.
- Perturbation benchmark v2-small is specified.

Good outcome:

- 92 closed-set PASS rises materially.
- Skeleton coverage covers most remaining failures.
- RAG retrieval has functional/forbidden metrics.

Excellent outcome:

- 92 closed-set is near complete.
- New perturbation benchmark has first executable tasks.
- RAG slot-binding prototype can generate materialized skeleton prompts.

## Morning Checklist

- [ ] Closed-set ledger exists.
- [ ] Verified artifact store exists or is drafted.
- [ ] Newly admitted tasks have EVAS + Spectre paths.
- [ ] Remaining failures are categorized.
- [ ] Skeleton coverage report exists.
- [ ] Benchmark v2-small draft exists.
- [ ] RAG upgrade notes exist.
- [ ] Paper narrative changes are either applied or listed as TODO.
