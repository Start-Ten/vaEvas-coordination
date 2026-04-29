# 2026-04-29 H/I Sequence Results

## Scope

Execution order requested:

`A -> D -> F -> G -> H-v1 -> H-v2 -> I-GSeed -> I-History -> I-Codex -> I-Full`

This note records the H/I continuation on top of the current same-baseline G result.

## Current Same-Baseline Anchor

| Condition | Accepted result |
| --- | ---: |
| A | 23/92 |
| D | 43/92 |
| F | 59/92 |
| G | 65/92 |

G is treated as the anchor. H/I were run only on the 27 tasks that still failed after G.

## EVAS Core Fix During H/I

During I-Full Spectre validation, `adpll_timer_smoke` was EVAS PASS but Spectre FAIL. Root cause was an EVAS expression typing bug:

- Intended Spectre/Verilog-A behavior: `parameter integer navg / 2` should use integer division.
- Incorrect EVAS behavior after the earlier integer-division patch: `1.0 * dco_code / 1023.0` was also treated as integer division because the expression contained an integer variable.
- Fix: preserve raw numeric-literal form in the lexer/parser and only treat plain integer tokens such as `2` as integer literals. Real-looking literals such as `1.0`, `1023.0`, `10e-9`, and SI-suffixed values remain real.

Touched files:

- `EVAS/evas/compiler/ast_nodes.py`
- `EVAS/evas/compiler/lexer.py`
- `EVAS/evas/compiler/parser.py`
- `EVAS/evas/simulator/backend.py`
- `EVAS/tests/test_engine.py`

Regression:

`PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_compiler.py EVAS/tests/test_engine.py EVAS/tests/test_netlist.py -q`

Result: `316 passed`.

## H/I Results On Final-G27

| Stage | Mechanism | Raw EVAS on 27 | Strict accepted after Spectre/core-fix | New accepted tasks vs previous stage |
| --- | --- | ---: | ---: | --- |
| H-v1 | failure-signature translation, no contract cards | 2/27 before core fix | 1/27 | `adpll_timer` |
| H-v2 | functional-IR translation, task-id-specific hints disabled | 2/27 | 2/27 | `cppll_timer` |
| I-GSeed | generated behavior contracts from current G/H residuals | 2/27 | 2/27 | none |
| I-History | current contracts + history/local repair cards | 4/27 before core fix | 3/27 | `comparator_hysteresis_smoke` |
| I-Codex | history result + Codex/system-relation cards | 5/27 before core fix | 4/27 | `cdac_cal` |
| I-Full | full card catalog | 5/27 before core fix; 4/27 after core fix | 4/27 | none |

Final accepted pass set on final-G27:

- `adpll_timer`
- `cppll_timer`
- `comparator_hysteresis_smoke`
- `cdac_cal`

Spectre validation for the corrected final set:

`results/condition-I-Full-on-Hv2-finalG27-kimi-spectre-pass4-after-realliteralfix-2026-04-29`

Result: `4/4` Spectre PASS, all matched EVAS after the EVAS core fix.

## Corrected Cumulative Result

| Anchor | Added accepted H/I fixes | Corrected cumulative |
| --- | ---: | ---: |
| G = 65/92 | +4 | 69/92 |

The previously observed `adpll_timer_smoke` PASS is not counted, because it was caused by an EVAS integer/real division mismatch and fails in real Spectre.

## Remaining Failure Shape After I-Full

Corrected I-Full on the 27 G-fail tasks:

- PASS: 4
- `FAIL_SIM_CORRECTNESS`: 22
- `FAIL_TB_COMPILE`: 1

Remaining compile failure:

- `dwa_ptr_gen_smoke`: Spectre-incompatible `transition()` contribution inside conditional/event/loop/case structure.

This is the strongest evidence so far that G successfully removes most syntax/interface/infra failures, while H/I as currently implemented only add a few behavior-level repairs. The next useful optimization is to harden behavior repair templates, especially system-level timer/PLL, DWA pointer/update, PRBS/edge-generation, and ADC/SAR composition constraints.
