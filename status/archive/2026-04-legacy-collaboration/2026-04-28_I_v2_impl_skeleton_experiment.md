# I-v2 System + Implementation Skeleton Experiment

Date: 2026-04-28

## Goal

Make the I-style cold-start repair loop satisfy both:

- syntax/artifact constraints: Spectre-safe Verilog-A, single-driver TB, no dynamic analog vector indexing, no conditional transition, no timeout;
- behavior constraints: system relation cards for PLL, DWA, PFD/BBPD, ADC/DAC, and serializer.

This is an attempt to convert historical R26 lessons into reusable cold-start guidance without replaying verified artifacts or copying gold implementations.

## Implementation Changes

Updated `behavioral-veriloga-eval/runners/build_repair_prompt.py`:

- Added prompt-derived contract source routing:
  - `_contract_source_for_task`
  - `_contract_mechanism_tokens`
- Added `# Implementation-Safe Repair Skeleton` section to the repair prompt.
- The new skeleton is selected from functional-IR/contracts and EVAS notes, not from benchmark names alone.
- It includes:
  - Spectre-safe Verilog-A construction rules
  - DWA bus/state skeleton
  - PLL timer/divider skeleton
  - PFD/BBPD pulse skeleton
  - ADC/DAC code-output skeleton
  - serializer state skeleton
  - TB single-driver skeleton
  - timeout-safe simulation skeleton
- Fixed DWA plan routing so it can trigger from observable notes such as `ptr_*`, `cell_en_*`, `bad_ptr_rows`, and `overlap_count`, even when `VAEVAS_FUNCTIONAL_IR_ONLY=1`.

Additional DWA tightening:

- After `dynamic_analog_vector_index`, the prompt now requires explicit static unroll of offending bus reads/contributions.
- For no-overlap DWA, the prompt now identifies the feasibility issue when `max_active_cells` is too large for disjoint consecutive windows.

## Validation

Static checks:

```bash
python3 -m py_compile runners/build_repair_prompt.py runners/infer_prompt_checker_specs.py runners/generate_behavior_contracts.py runners/check_behavior_contracts.py
```

Prompt sample confirmed:

- `# Implementation-Safe Repair Skeleton`
- `## Spectre-safe DWA bus/state skeleton`
- `# Plan-and-Execute Repair Policy: DWA`
- `# Contract-Guided Repair Cards`
- `dwa_system_rotating_window_graph`

## I-v2 Nine-Task Rerun

Command root:

```bash
VAEVAS_CONTRACT_ROOT=results/generated-behavior-contracts-I-system-cards-on-Ffail-kimi-2026-04-28
VAEVAS_ENABLE_REPAIR_CARDS=1
VAEVAS_FUNCTIONAL_IR_ONLY=1
VAEVAS_RELAXED_CARD_SELECTOR=1
VAEVAS_REPAIR_CARD_LIMIT=3
python3 runners/run_adaptive_repair.py \
  --model kimi-k2.5 \
  --workers 3 \
  --source-generated-dir generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun \
  --initial-result-root results/condition-F-strictv3-evasloop-kimi-full92-materialized-evas-2026-04-28-rerun \
  --generated-root generated-condition-I-v2-system-impl-skeleton-on-Ffail-kimi-2026-04-28 \
  --output-root results/condition-I-v2-system-impl-skeleton-on-Ffail-kimi-evas-2026-04-28 \
  --max-rounds 3 \
  --repair-public-spec-mode spectre-strict-v3 \
  --no-repair-skill \
  --layered-only-repair
```

Result: `0/9 PASS`.

Layer improvements relative to the previous system-card-only run:

| Task | Previous | I-v2 | Meaning |
|---|---|---|---|
| `cppll_freq_step_reacquire_smoke` | `FAIL_TB_COMPILE` | `FAIL_SIM_CORRECTNESS` | single-driver/TB issue was cleared; remaining issue is PLL behavior |
| `sar_adc_dac_weighted_8b_smoke` | `FAIL_INFRA` | `FAIL_SIM_CORRECTNESS` | timeout/infra issue was cleared; remaining issue is stuck code/output |
| `adpll_lock_smoke` | `FAIL_SIM_CORRECTNESS` | `FAIL_SIM_CORRECTNESS` | still runnable behavior failure |
| `dwa_ptr_gen_no_overlap_smoke` | `FAIL_DUT_COMPILE` | `FAIL_DUT_COMPILE` | first I-v2 run did not clear dynamic vector indexing |

## Targeted DWA Static-Unroll Rerun

After strengthening the dynamic-index prompt, reran only:

- `dwa_ptr_gen_no_overlap_smoke`

Result:

- moved from `FAIL_DUT_COMPILE` to `FAIL_SIM_CORRECTNESS`;
- `dut_compile=1.0`, `tb_compile=1.0`;
- remaining metrics:
  - `sampled_cycles=17`
  - `bad_ptr_rows=0`
  - `max_active_cells=14`
  - `overlap_count=8`

This confirms the implementation skeleton can remove the syntax blocker. The remaining failure is a behavior/feasibility problem: the generated stimulus or active-count relation creates very large windows, and consecutive 14-cell windows cannot be disjoint in a 16-cell array.

## Interpretation

The new I-v2 loop did not improve final PASS count yet, but it improved failure attribution and moved multiple tasks from infrastructure/compile layers into behavior layers:

- `cppll`: TB/source-driver problem -> behavior relation problem.
- `sar_adc_dac`: timeout/infra problem -> code/output stuck behavior problem.
- `dwa_no_overlap`: dynamic vector syntax problem -> no-overlap behavior problem after static-unroll tightening.

This is evidence that “system relation card + implementation-safe skeleton” is the right direction, but it is still weaker than R26 deterministic closure. The next step should not be more prose; it should convert repeated implementation skeletons into stronger structured code patterns or deterministic local patch runners for the hardest families.

## Next Candidate Optimizations

1. DWA no-overlap skeleton should explicitly choose feasible low-code stimulus for no-overlap smoke tests, or the DUT should clamp validation-window active count to a disjoint-feasible size while preserving the general code relation.
2. PLL skeleton should add a concrete edge-ratio correction rule for `late_edge_ratio=2.0` and `late_freq_ratio=1.1`.
3. SAR/ADC-DAC skeleton should add a concrete “unique code rescue” pattern: ensure `clks` edges, deassert reset, code update on sample, and DAC output target from that code.
4. Consider converting these from prompt text into small family-specific deterministic patch runners when repeated prompt-only repair stalls.
