# Closed-Set 92 Completion Ledger

Date: 2026-04-29

## Claim Boundary

- A/D/F/G remain the strict same-baseline result line.
- G is the current strict anchor at `65/92`.
- H/I add `4` Spectre-confirmed closed-set continuations.
- R26 teacher replay adds `13` real-Spectre-confirmed closed-set continuations.
- R26 teacher template/syntax repair adds `10` real-Spectre-confirmed closed-set continuations.
- The current closed-set accepted result is therefore `92/92`, but the R26 replay portion is not cold-start evidence.
- R26/92PASS artifacts are teacher/replay material. They are useful for closed-set completion and template distillation, but must not be reported as fresh LLM generation.

## Summary

- Total tasks: `92`
- Current closed-set accepted PASS: `92/92`
- R26 teacher EVAS PASS: `92/92`
- Current status counts: `{'PASS': 92}`
- Result role counts: `{'same_baseline_G_anchor': 65, 'closed_set_teacher_replay_spectre_confirmed': 13, 'closed_set_teacher_template_spectre_fixed': 10, 'closed_set_continuation': 4}`

## Output Files

- Ledger JSON: `behavioral-veriloga-eval/docs/CLOSEDSET92_COMPLETION_LEDGER.json`
- Artifact store: `behavioral-veriloga-eval/docs/VERIFIED_ARTIFACT_STORE.json`
- Closed-set templates: `behavioral-veriloga-eval/docs/CLOSEDSET_CIRCUIT_TEMPLATES.json`

## Remaining Failures By Mechanism

| Mechanism | Count |
|---|---:|

## Remaining Failure Tasks

| Task | Family | Mechanism | Status | Notes | R26 Teacher | Next Action |
|---|---|---|---|---|---|---|

## Provenance Notes

- `VERIFIED_ARTIFACT_STORE.json` contains both strict accepted artifacts and R26 teacher artifacts; check `claim_allowed` and `forbidden_claims` before using an entry in a paper table.
- R26 entries are marked `teacher_dataset_not_cold_start` and `spectre_pass=null` unless independently validated.
- R26 replay entries marked `closed_set_completion_not_cold_start` have real Spectre confirmation, but their provenance is still teacher replay.
- R26 spectrefix entries are also not cold-start; they combine teacher artifacts with explicit Spectre-compatibility templates.
- G entries marked `PASS_BY_COMPOSED_SUMMARY` inherit the combined Spectre summary rather than per-task result JSON.
