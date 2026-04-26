# Benchmark Expansion Plan: 46 → 200 Tasks

This document describes the phased strategy for expanding the vaEvas benchmark from the current 46 tasks to a target of 200 verified tasks across all four task families.

---

## Benchmark Structure

The vaEvas benchmark has **four task families**, each testing a different AI capability:

| family | what it tests | AI output | key checks |
|---|---|---|---|
| `end-to-end` | spec → DUT + TB + simulation | `.va` + `.scs` | compile + sim_correct + EVAS↔Spectre parity |
| `spec-to-va` | spec → DUT only | `.va` | compile + behavioral correctness |
| `bugfix` | fix a broken `.va` | corrected `.va` | compile + bug actually fixed |
| `tb-generation` | write a testbench for a given DUT | `.scs` | TB compile + waveform produced |

All four families count toward the 200-task target.

---

## Guiding Constraints

All benchmark tasks must satisfy:

1. **EVAS-compatible (voltage-domain only)**
   - Uses `V() <+`, `@(cross(...))`, `@(initial_step)`, `@(timer(...))`, `transition()`
   - Does NOT use `I() <+`, `ddt()`, `idt()`, `idtmod()`, `laplace_nd()`, `slew()`, `flicker_noise()`
2. **`end-to-end` tasks require EVAS + Spectre parity** (`parity_required: true`)
3. **Every task has at least 2 meaningful `sim_correct` checks** (no `manual_review_expected_output` placeholders)
4. **Every task needs a gold reference answer** before it can be used to evaluate AI models
5. **Tier progression**: `raw → verified` requires EVAS run + (for end-to-end) Spectre cross-check

---

## Current State (as of 2026-04-05)

| family | total tasks | verified | raw/pending | gold answer exists |
|---|---|---|---|---|
| `end-to-end` | 26 | 6 | 20 | 21 (examples) |
| `spec-to-va` | 12 | 0 | 12 | 0 (all `manual_review`) |
| `bugfix` | 4 | 0 | 4 | 0 |
| `tb-generation` | 4 | 0 | 4 | 0 |
| **total** | **46** | **6** | **40** | **21** |

**Critical gap**: spec-to-va, bugfix, tb-generation have no gold answers and no automated checks — the two students' first job is to close this gap.

---

## Phase 1: Close Infrastructure Gaps + First Verification Wave (target: ~80 tasks)

**Goal**: make all 46 existing tasks evaluatable (have gold + automated checks), then push to verified.

### Step 1a: Gold answers + automated checks (students' work)

| family | tasks needing gold | responsible |
|---|---|---|
| `spec-to-va` | all 12 | shenbufan (digital/pll) + liangyuxuan (adc/dac) |
| `bugfix` | all 4 | shenbufan |
| `tb-generation` | all 4 | liangyuxuan |

Concretely: replace every `manual_review_expected_output` in `checks.yaml` with a real behavioral check. Write the gold `.va` or `.scs` file.

### Step 1b: EVAS + Spectre parity (end-to-end tasks, students' work)

20 end-to-end tasks are `raw/pending`. Both students run EVAS + Spectre on their assigned tasks to push them to `verified`.

### Step 1c: Add ~34 new tasks (from existing examples)

Each of the 21 examples can produce 3–4 tasks by varying difficulty. Target: +34 end-to-end tasks.

| example | new variants |
|---|---|
| comparator | hysteresis, offset-search, strongarm, rail-to-rail |
| dac_binary_clk_4b | 6b, 8b, with mismatch |
| sar_adc_dac_weighted_8b | 10b, with noise, with offset |
| lfsr | 16b, 23b, with enable |
| gray_counter_4b | 8b, with load, async reset |
| flash_adc_3b | 4b, with offset |
| pfd_updn | with dead-zone, with reset delay |
| serializer_8b | deserializer_8b, 16b |
| (others) | 1–2 variants each |

**Phase 1 total: ~80 tasks**

---

## Phase 2: New Circuit Domains (target: ~130 tasks)

**Goal**: add 5 new circuit categories with full example + task coverage.

| new category | representative circuits | est. tasks |
|---|---|---|
| oscillator | ring_osc_3stage, vco_behavioral (timer-based), relaxation_osc | 12 |
| frequency-divider | div2, div4, dual_modulus_div | 8 |
| encoder-decoder | priority_encoder_4b, therm2bin_8b, manchester_encoder | 10 |
| pipeline-logic | 4-stage pipeline register, forwarding logic | 8 |
| power-switch | behavioral transmission gate, programmable gain switch | 8 |

For each new category: write example → define tasks across all 4 families (end-to-end + spec-to-va variants + bugfix with introduced bugs + tb-generation).

**Phase 2 net new tasks: ~46 → total ~130**

---

## Phase 3: System-Level + AI-Driven Curation (target: ~200 tasks)

### System-level end-to-end tasks (~20)

| system | components | difficulty |
|---|---|---|
| charge-pump PLL behavioral | PFD + CP + divider + VCO | hard |
| delta-sigma modulator 1st order | accumulator + 1b DAC + feedback | hard |
| pipelined ADC 2-stage | MDAC×2 + flash + digital correction | expert |
| serializer + CDR | serializer + clock recovery | hard |

### AI-generation-driven tasks (~30)

Once the evaluation pipeline is running, high-quality AI outputs that pass all checks can be curated into the benchmark:

```
model output → EVAS compile + sim_correct → Spectre parity → human review → benchmark PR
```

This directly supports the paper claim: "our framework enables AI-assisted benchmark construction."

**Phase 3 net new tasks: ~50 → total ~200**

---

## Target Distribution at 200

| family | target count |
|---|---|
| `end-to-end` | 80 |
| `spec-to-va` | 60 |
| `bugfix` | 30 |
| `tb-generation` | 30 |
| **total** | **200** |

| category | target count |
|---|---|
| digital-logic | 30 |
| data-converter | 35 |
| pll-closed-loop | 20 |
| phase-detector | 15 |
| oscillator | 15 |
| sample-hold | 10 |
| calibration | 10 |
| stimulus | 10 |
| measurement | 10 |
| encoder-decoder | 15 |
| comms | 15 |
| power-switch | 10 |
| **total** | **~195** |

---

## Bottleneck Analysis

| bottleneck | mitigation |
|---|---|
| spec-to-va has no automated checks | students write gold `.va` + convert checks |
| every new example needs EVAS + Spectre validation | batch by category; reuse testbench templates |
| bugfix gold answers require domain knowledge | start from known EVAS pitfalls (wrong genvar/integer, missing transition) |
| AI-driven tasks need human review gate | require all 3 executable checks to pass before merging |

---

## Assignment Summary

| phase | who |
|---|---|
| Phase 1 gold answers + parity | shenbufan + liangyuxuan (historical assignment archived in `../archive/2026-04-pre-paper-pivot/project/WORK_ASSIGNMENT.md`) |
| Phase 1 new example variants | automated (Claude Code) |
| Phase 2 new circuit categories | Claude Code + team review |
| Phase 2–3 parity validation | students |
| AI model evaluation runs | full team |
