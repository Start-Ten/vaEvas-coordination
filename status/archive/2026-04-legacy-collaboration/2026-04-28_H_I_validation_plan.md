# H/I Validation Plan

Date: 2026-04-28

## Goal

Validate whether structured diagnosis improves the clean F loop without leaking benchmark-specific answers.

Current paper-grade anchor policy:

Use the real-Spectre-compatible strict-v3 A baseline as the official prompt-only
baseline. This is stricter than the earlier EVAS-runner clean snapshot and has
92/92 pass/fail agreement with remote Spectre validation.

| Condition | Meaning | Current result | Status |
|---|---|---:|---|
| A | prompt-only, real-Spectre-compatible strict-v3 baseline | 22/92 | official anchor |
| D | A + public Spectre/Verilog-A strict-v3 generation rules | 47/92 old strict-v3; 44/92 after later preflight-r2 recheck | rerun needed under final strict-v3 rules |
| F | D + EVAS-only repair loop, max 3 rounds | 60/92 core, 62/92 after EVAS/checker false-negative fixes | useful evidence; rerun recommended from final D |

Previous EVAS-ladder anchors, retained only for historical comparison:

| Condition | Meaning | Current result |
|---|---|---:|
| A | prompt-only clean baseline | 40/92 |
| D | A + public Spectre/Verilog-A strict v3 rules | 45/92 |
| F | D + EVAS-only repair loop, max 3 rounds | 60/92 repair gain, 62/92 after EVAS/checker false-negative fixes |

The previous `40/92` A row must not be used as the main paper baseline, because
it is less strict than real Spectre compatibility. It can be cited only as an
EVAS-runner historical snapshot.

The next experiments should answer two questions:

1. Does failure-signature/mechanism-guided repair improve over F?
2. Does task-contract/functional-IR-guided repair improve over H without overfitting to task names, gold files, or checker constants?

Related distillation audit:

```text
coordination/status/2026-04-28_r26_to_coldstart_distillation_audit.md
coordination/status/2026-04-28_r26_to_coldstart_distillation_audit.json
```

That audit decomposes the historical R26 92/92 closure into cold-start-transferable mechanisms vs direct artifact reuse that must be excluded.

## Required Experimental Hygiene

Before launching H/I as paper-grade experiments, freeze these switches explicitly in the runner or run config:

| Switch | F | H | I |
|---|---|---|---|
| public Spectre/Verilog-A strict v3 rules | on | on | on |
| EVAS repair loop, max 3 rounds | on | on | on |
| raw EVAS notes | on | on | on |
| failure-signature classification | off or minimal | on | on |
| mechanism repair templates | off | on | on |
| skill/circuit mechanism cards | off | off for clean H | on for I if mechanism-only and no task-name matching |
| contract diagnosis from task-local contracts.json | off | off | on only if generated from prompt/public checker semantics, not gold implementation |
| functional IR from prompt | off | off | on |
| Spectre in the repair loop | off | off | off |
| final Spectre/APS gate | final only | final only | final only |

Important: current code already contains some diagnosis/mechanism prompt paths. For a clean paper run, record the exact flags/environment variables that make F/H/I distinct.

## H Definition

H = F + failure-signature and mechanism-template repair.

Inputs allowed:

- original `tasks/**/prompt.md`;
- public Spectre/Verilog-A strict v3 rules;
- EVAS status, EVAS notes, and transient CSV statistics from failed attempts;
- generic mechanism templates such as edge-sampled logic, reset priority, monotonic converter transfer, PFD pulse exclusivity, PLL feedback cadence, timer/window behavior.

Inputs forbidden:

- task-name-specific routing;
- gold DUT implementation;
- gold-specific internal node names;
- exact checker threshold leakage unless the threshold is explicitly part of public prompt/spec;
- manual one-off patch recipes for known benchmark tasks.

Expected evidence:

- H should improve F on at least some F-failed behavior tasks.
- H should not regress F-pass tasks.
- For every H repair, save the triggered signature and mechanism-template ID.

## I Definition

I = H + prompt-derived functional IR / contract-guided repair.

Compared with H, I should know more about the task before or during repair:

- expected functional class, e.g. clocked digital, data converter, PLL, PFD, sample-hold;
- interface and observable signals;
- mechanism-level invariants, e.g. monotonicity, edge sampling, ratio/lock, no long up/dn overlap;
- allowed hierarchy and artifact requirements.

Inputs allowed:

- prompt-derived functional IR;
- public strict v3 rules;
- EVAS status/notes/CSV statistics;
- broad circuit mechanism cards from `veriloga-skills`, if selected by prompt semantics and not task id;
- contract checks generated from prompt/checker-visible semantics.

Inputs forbidden:

- task-name lookup as a primary selector;
- gold implementation, gold hidden states, or known passing artifact reuse;
- exact benchmark-specific numeric repairs not present in prompt;
- post-hoc materialization of locally fixed artifacts as if they were cold-start I.

Expected evidence:

- I should outperform H or at least solve a different class of failures.
- I should remain robust under prompt perturbation: changed values, changed port aliases, and same mechanism with different wording.

## R26 Distillation Policy For I

Historical 92/92 closure should not be copied into cold-start. It should be distilled as follows:

| Source | Cold-start policy |
|---|---|
| runner/checker/parser/Spectre mode fixes | Adopt as common infrastructure for all A/D/F/H/I. |
| R23/R24 PLL graph patches | Convert into prompt-selected PLL feedback/cadence/lock mechanism cards. |
| R25 remaining mechanism patches | Convert into generic mechanism cards for bus truth table, converter transfer, divider ratio switch, analog equation accuracy, event/timer grid. |
| R26 DWA/PFD closure | Convert into DWA pointer/wrap and PFD pulse exclusivity cards. |
| I-runner local overlay with ref/gold leakage flags | Exclude direct reuse; redistill only after removing ref filenames, task-specific harness details, and exact patch recipes. |

Every adopted mechanism must log provenance: prompt phrase, EVAS note, CSV metric, and selected card ID.

## Main Run Matrix

### Block 1: H-on-F-fail Fast Increment

Purpose: fast evidence that failure-signature/mechanism diagnosis adds value.

Run only the 30 tasks that fail under F after EVAS alignment.

Use:

- source generated tree: `generated-condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-2026-04-28/`
- source EVAS result: `results/condition-F-public-strictv3-evasloop-kimi-full92-strict-r2-combined-evas-after-evasfix-full92-2026-04-28/`
- repair rounds: 3
- Spectre in loop: no
- final gate: EVAS first, then Spectre/APS only for new passes

Success criterion:

- at least +3 net new EVAS passes over F-failed subset;
- no evidence of task-name/gold leakage in logged signature triggers.

Interpretation:

- If positive, run full H.
- If negative, do not spend API on full H until signature templates are audited.

### Block 2: H full92 Cold Start

Purpose: paper-grade H condition.

Run all 92 tasks from the final strict-v3 D initial generation policy, but with
H repair enabled. Do not mix an H run based on older EVAS-ladder artifacts with
the real-Spectre-compatible A baseline.

Success criterion:

- H full92 > F full92 under the same scorer;
- H pass set includes all or nearly all F passes;
- final Spectre/APS gate confirms newly gained EVAS passes.

Paper role:

- Ablation between F and I.
- Shows whether failure diagnosis alone is enough.

### Block 3: I-on-F-fail Fast Increment

Purpose: fast evidence that functional IR/contracts add value beyond F.

Run the same F-failed subset, but enable I features:

- prompt-derived functional IR;
- mechanism-card retrieval by prompt semantics;
- contract diagnosis only from prompt/public checker semantics;
- no gold implementation and no task-name primary matching.

Success criterion:

- I-on-F-fail >= H-on-F-fail;
- I repairs include cases H does not solve, especially PLL/data-converter/system tasks.

### Block 4: I full92 Cold Start

Purpose: final main method condition.

Run all 92 from clean prompt + final public strict-v3 rules + I repair. The
reported I row should be regenerated from the same strict-v3 generation/scoring
rules as A/D/F/H.

Success criterion:

- I full92 is the best cold-start result among A/D/F/H/I;
- final Spectre/APS gate confirms the new pass set;
- logs show trigger evidence from prompt/CSV/checker notes, not task IDs or gold.

Paper role:

- Main method result.

## Overfitting Guards

### Guard 1: No-Task-Name Audit

For every H/I repair prompt, save:

- task id;
- triggered signature;
- triggered mechanism card or contract;
- evidence source: prompt phrase, EVAS note, CSV metric;
- whether task id was used.

Pass criterion:

- task id is never the primary match key.

### Guard 2: Prompt Perturbation Mini-Set

Create 8-12 perturbed tasks from F/H/I-sensitive categories:

- clocked digital edge logic;
- DAC/ADC monotonic transfer;
- PFD/PLL feedback;
- sample-hold/timing-window;
- DWA pointer/wraparound.

Perturb:

- port aliases, e.g. `din` -> `dinp`, `ref_clk` -> `refclk`;
- numeric values, e.g. frequency, bit width, threshold if prompt-visible;
- wording, e.g. `monotonic` misspelled or paraphrased as "never decreases".

Pass criterion:

- H/I still choose the same mechanism family from semantics, not exact keywords.

### Guard 3: Cross-Model Sanity

Run at least A/D/F/I on one other model, preferably Qwen or MiniMax.

Pass criterion:

- I improves over F or reduces the same dominant failure class on at least one non-Kimi model.

## Recommended Overnight Execution Order

1. Run H-on-F-fail.
2. Run I-on-F-fail.
3. If either gives meaningful new passes, launch H full92 and I full92 in parallel.
4. For new EVAS passes, run targeted Spectre/APS gate only on changed pass set.
5. Generate audit tables:
   - pass-set diff vs F;
   - trigger provenance;
   - failure taxonomy change;
   - Spectre agreement.

## Result Paths To Use

Suggested output roots:

```text
behavioral-veriloga-eval/generated-condition-H-signature-kimi-full92-2026-04-28/
behavioral-veriloga-eval/results/condition-H-signature-kimi-full92-evas-2026-04-28/
behavioral-veriloga-eval/results/condition-H-signature-kimi-newpasses-spectre-2026-04-28/

behavioral-veriloga-eval/generated-condition-I-functional-ir-kimi-full92-2026-04-28/
behavioral-veriloga-eval/results/condition-I-functional-ir-kimi-full92-evas-2026-04-28/
behavioral-veriloga-eval/results/condition-I-functional-ir-kimi-newpasses-spectre-2026-04-28/
```

## Reporting Table

| Condition | Start | Added guidance | Repair rounds | EVAS pass | Spectre/APS pass | Evidence type |
|---|---|---|---:|---:|---:|---|
| A | prompt | none | 0 | 22/92 | 22/92, agreement 92/92 | official strict-v3 baseline |
| D | prompt | public strict v3 | 0 | 47/92 old; 44/92 after later preflight-r2 recheck | 42/92 old full92 Spectre; rerun needed | rule injection |
| F | D | raw EVAS loop | <=3 | 60/92 core, 62/92 after EVAS fixes | 62 known by targeted Spectre/APS evidence | closed-loop baseline, rerun recommended |
| H | final D/F policy | failure signature + mechanism templates | <=3 | TBD | TBD | diagnosis ablation |
| I | final D/F policy | functional IR + contracts + mechanism cards | <=3 | TBD | TBD | main method |

## Stop/Go Rules

- If H-on-F-fail adds fewer than 2 passes and trigger logs look noisy, skip H full92 and use H only as a negative ablation.
- If I-on-F-fail adds fewer than 2 passes, do prompt-IR/contract audit before launching I full92.
- If any H/I gain comes from task-name matching or gold leakage, exclude that run from the paper-grade table.
- If EVAS and Spectre disagree on a new pass, classify it as validation infrastructure first, circuit behavior second.
