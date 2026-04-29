# I-clean Functional IR Run

## Brief

Goal: turn condition I from task-name/benchmark-name matching into a cleaner functional mechanism condition.

The intended I-clean path is:

1. infer behavior from the public prompt into a compact functional IR;
2. generate behavior contracts from public prompt observables, prompt-derived roles, and EVAS failure surfaces;
3. select mechanism cards from contract/failure vectors plus functional IR claims, not from task ids or gold files;
4. run based-on-F repair first, then full92 repair, then Spectre validation for adopted/pass artifacts.

## KPI

- No direct task-id matching in I-clean card selection.
- No gold save names used for live prompt spec inference unless explicitly opted in.
- F-fail subset produces a measurable result.
- full92 I-clean produces a complete EVAS summary.
- Spectre validation is run on I-clean accepted/pass artifacts or the changed pass delta.

## Non-goals

- Do not reuse local PASS overlay artifacts as cold-start evidence.
- Do not rewrite official scoring semantics.
- Do not make task-specific patches for one benchmark unless they are recorded as non-cold-start engineering closure.

## Execution Log

- 2026-04-28 06:24 CST: started audit and implementation.
- Implemented live prompt inference without gold save names by default.
- Added functional IR/template provenance into generated contracts and contract reports.
- Added functional-only repair-card matching via `VAEVAS_FUNCTIONAL_IR_ONLY=1`; task keyword matching is ignored in that mode.
- Generated F-fail I-clean contracts at `behavioral-veriloga-eval/results/generated-behavior-contracts-I-clean-functional-ir-on-Ffail-2026-04-28/`.
- Smoke check: `adc_dac_ideal_4b_smoke` selected cards from failed contracts plus `functional_claim_any`/`prompt_template_any`, not task keywords.
- F-fail based-on-F repair:
  - output: `behavioral-veriloga-eval/results/condition-I-clean-functional-ir-on-Ffail-kimi-evas-2026-04-28/`
  - PASS: `7/30`
  - pass tasks: `comparator_hysteresis_smoke`, `bbpd_data_edge_alignment_smoke`, `dac_therm_16b_smoke`, `mux_4to1_smoke`, `pfd_deadzone_smoke`, `cdac_cal`, `segmented_dac`
- Full92 materialization:
  - generated tree: `behavioral-veriloga-eval/generated-condition-I-clean-functional-ir-full92-materialized-kimi-2026-04-28/`
  - materialization report: `coordination/status/2026-04-28_I_clean_full92_materialization.md`
  - replacement count: `7`
- Full92 EVAS score:
  - result: `behavioral-veriloga-eval/results/condition-I-clean-functional-ir-full92-materialized-kimi-evas-2026-04-28/model_results.json`
  - PASS: `69/92`
  - Pass@1: `0.750`
  - F baseline after EVAS fixes was `62/92`; I-clean adds `+7`.
- Spectre delta7 validation:
  - attempted output: `behavioral-veriloga-eval/results/condition-I-clean-functional-ir-full92-materialized-kimi-spectre-delta7-rerun-2026-04-28/`
  - validation did not reach Spectre simulation. The remote bridge failed during upload with `Connection closed by UNKNOWN port 65535`.
  - `virtuoso-bridge start --env .env` also failed because the remote bridge precheck reported `No Python interpreter found on thu-wei`.
  - Current Spectre status is therefore `INFRA_BLOCKED`, not an artifact-level fail.

## Interim Conclusion

I-clean is now cleaner than the previous I variant:

- live prompt inference no longer uses gold save names by default;
- repair-card matching can run in functional-only mode with task-keyword matching disabled;
- recovered PASS cases came from functional claim/template and contract-vector matches;
- full92 EVAS improves from `62/92` to `69/92`.

The remaining missing evidence is remote Spectre confirmation for the 7 newly admitted artifacts once the Virtuoso bridge is available again.
