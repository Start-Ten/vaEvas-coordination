# LEGO-Style Skill RAG Progress

Date: 2026-04-29

## What Changed

We added a LEGO-style skill layer to `behavioral-veriloga-eval`.

This layer turns the current 92PASS/R26/gold-derived mechanism experience into
typed construction blocks rather than raw text snippets.

Each skill contains:

1. mechanism family;
2. functional concepts used for retrieval;
3. public slot schema and slot binding;
4. mechanism-level implementation skeleton;
5. compact Verilog-A code shape;
6. checker expectations;
7. Spectre compatibility constraints;
8. anti-patterns.

## New Files

In `behavioral-veriloga-eval`:

1. `runners/lego_skill_library.py`
2. `runners/run_lego_skill_audit.py`
3. `docs/LEGO_SKILL_BASED_RAG.md`
4. `docs/LEGO_MECHANISM_SKILLS.json`
5. `tests/test_lego_skill_library.py`

## Current Evidence

Prompt-only retrieval audit on benchmark-v2 small:

```text
Manifest: benchmark-v2/manifests/v2-small.json
Use task id / manifest family for routing: False
Use meta checker spec for slot binding: False
Top-1 primary skill: 28/30
Top-3 full skill-set recall: 30/30
Result root: results/lego-skill-audit-v2-small-2026-04-29-r6
```

This stricter audit requires composition tasks to retrieve every expected LEGO
block in Top-3. The two Top-1 misses are composition prompts where the
secondary block ranks first, but the full required set is still available to
the repair prompt. This is retrieval evidence only. It does not claim model
repair pass rate.

## Repair-Loop Integration

The EVAS repair prompt can inject LEGO skills with:

```bash
VAEVAS_ENABLE_LEGO_SKILLS=1
VAEVAS_LEGO_SKILL_TOP_K=3
```

The injected block includes:

1. selected mechanism skill;
2. functional routing evidence;
3. bound public slots;
4. checker expectations;
5. implementation skeleton;
6. Spectre constraints.

## Next Experiment

Run a controlled comparison on the current G-fail or benchmark-v2 generation
split:

1. G baseline: EVAS feedback + syntax-zero gate.
2. G + LEGO: same loop, plus `VAEVAS_ENABLE_LEGO_SKILLS=1`.
3. Final acceptance: EVAS pass candidates go through real Spectre validation.

Success criteria:

1. compile/interface/runtime failures do not regress;
2. behavior-fail cases improve in EVAS;
3. EVAS/Spectre mismatch does not increase;
4. generated repairs cite type-level skill IDs, not task IDs.
