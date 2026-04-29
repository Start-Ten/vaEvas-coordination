# Remote Sync Final-Version Manifest

Date: 2026-04-29

## Principle

Yes, upload the final version only for the main remote branch.

The project now contains many exploration variants such as `r1/r2/v1/v2/smoke/materialized/failXX`. These are useful locally for provenance and debugging, but they should not all be pushed to the main remote. The remote should show:

- final runnable code,
- final benchmark/task definitions,
- final distilled knowledge assets,
- compact final result summaries,
- one or two provenance ledgers that explain where the final numbers came from.

Historical variants should be represented by summary documents, not by uploading every raw generated/result folder.

## behavioral-veriloga-eval Final Upload Set

### Always Upload

- `benchmark-v2/`
- `docs/`
- `runners/`
- `specs/`
- `prompt-defect-cases/`
- `tables/RUN_REGISTRY.md`
- `tasks/**/prompt.md`
- `tasks/**/contracts.json`

### Docs: Keep Final Version

Upload:

- `docs/COMPLETION_PACKAGE_MANIFEST.json`
- `docs/CLOSEDSET92_COMPLETION_LEDGER.json`
- `docs/VERIFIED_ARTIFACT_STORE.json`
- `docs/CLOSEDSET_CIRCUIT_TEMPLATES.json`
- `docs/CIRCUIT_MECHANISM_SKELETONS.json`
- `docs/SPECTRE_COMPATIBILITY_TEMPLATES.json`
- `docs/CONTRACT_REPAIR_CARDS.json`
- `docs/CONTRACT_REPAIR_CARDS_FULL_PROVENANCE.json`
- `docs/PROMPT_CHECKER_SPECS_ADOPTED.json`
- `docs/SYSTEM_CONTRACT_GRAPHS.json`
- `docs/FAILURE_ATTRIBUTION_POLICY.md`
- `docs/BEHAVIOR_CONTRACT_TEMPLATES.md`
- `docs/ADC_SYSTEM_DECOMPOSITION.md`

Do not upload as mainline assets:

- `docs/CONTRACT_REPAIR_CARDS_B_ADC_DAC_DRAFT.json`
- `docs/CONTRACT_REPAIR_CARDS_CODEX_SYSTEM_ONLY.json`
- `docs/CONTRACT_REPAIR_CARDS_HISTORY_ONLY.json`

Those are intermediate ablation/source variants. Their useful information is already represented in `CONTRACT_REPAIR_CARDS.json` and `CONTRACT_REPAIR_CARDS_FULL_PROVENANCE.json`.

### Generated Artifacts: Keep Only Final Roots

Upload these if the remote needs to reproduce accepted artifacts:

- `generated-condition-A-strictv3-kimi-full92-2026-04-28-rerun/`
- `generated-condition-D-strictv3-kimi-full92-2026-04-28-rerun/`
- `generated-condition-F-strictv3-evasloop-kimi-full92-materialized-2026-04-28-rerun/`
- `generated-condition-G-targeted-materialized-spectre-aligned-kimi-2026-04-28/`
- `generated-condition-I-Full-on-Hv2-finalG27-kimi-2026-04-29/`
- `generated-r26-teacher-spectrefix-remaining10-2026-04-29/`
- `generated-completion-package-benchmark-v2-2026-04-29-r1/`

Do not upload the older generated roots such as:

- `generated-A-prompt-cleanup-*`
- `generated-clean-A-*`
- `generated-D-public-*`
- `generated-condition-G-syntax-zero-*`
- `generated-condition-G-compileclean*`
- `generated-condition-H-v1-*`
- `generated-condition-H-v2-*`
- `generated-condition-I-GSeed-*`
- `generated-condition-I-History-*`
- `generated-condition-I-Codex-*`
- old `generated-adaptive-*`
- old `generated-overfit-guard-*`

Their conclusions should be kept through status summaries, not raw upload.

### Results: Keep Compact Final Roots Only

Upload these result folders:

- `results/condition-A-strictv3-kimi-full92-evas-2026-04-28-rerun/`
- `results/condition-A-strictv3-kimi-full92-spectre-2026-04-28-rerun/`
- `results/condition-D-strictv3-kimi-full92-evas-2026-04-28-rerun/`
- `results/condition-D-strictv3-kimi-full92-spectre-2026-04-28-rerun/`
- `results/condition-F-strictv3-evasloop-kimi-full92-materialized-evas-2026-04-28-rerun/`
- `results/condition-F-strictv3-evasloop-kimi-full92-materialized-spectre-2026-04-28-rerun/`
- `results/condition-G-targeted-materialized-spectre-aligned-kimi-evas-2026-04-28/`
- `results/condition-G-targeted-materialized-spectre-aligned-kimi-spectre-combined-2026-04-28/`
- `results/condition-I-Full-on-Hv2-finalG27-kimi-spectre-pass4-after-realliteralfix-2026-04-29/`
- `results/r26-teacher-remaining23-spectre-2026-04-29/`
- `results/r26-teacher-spectrefix-remaining10-evas-2026-04-29-r2/`
- `results/r26-teacher-spectrefix-remaining10-spectre-2026-04-29-r2/`
- `results/completion-package-audit-2026-04-29/`
- `results/benchmark-v2-gold-validation-2026-04-29-r2/`
- `results/benchmark-v2-gold-validation-spectre-2026-04-29-r1/`
- `results/completion-package-benchmark-v2-evas-2026-04-29-r1/`
- `results/completion-package-benchmark-v2-spectre-2026-04-29-r1/`

Do not upload the full `results/` directory. It is about `12G` and contains many obsolete or superseded experiment variants.

## coordination Final Upload Set

### Upload As Mainline Status

- `status/00_CURRENT_MAINLINE.md`
- `status/2026-04-12_repo-visibility-note.md`
- `status/2026-04-28_ADFG_same_baseline_current.md`
- `status/2026-04-29_HI_sequence_results.md`
- `status/2026-04-29_overnight_execution_summary.md`
- `status/2026-04-29_overnight_closedset_rag_benchmark_plan.md`
- `status/2026-04-29_closedset92_completion_ledger.md`
- `status/2026-04-29_completion_package_audit.md`
- `status/2026-04-29_completion_package_practice_validation.md`
- `status/2026-04-29_benchmark_v2_gold_validation.md`
- `status/2026-04-29_circuit_mechanism_rag_audit.md`
- `status/2026-04-29_mechanism_skeleton_coverage.md`
- `status/2026-04-29_rag_upgrade_notes.md`
- `status/2026-04-29_gold_r26_template_generalization.md`
- `status/2026-04-29_cleanup_protect_manifest.json`
- `status/2026-04-29_remote_sync_upload_recommendation.md`
- `status/2026-04-29_remote_sync_final_version_manifest.md`

### Upload Paper/Benchmark Docs

- `docs/architecture/`
- `docs/benchmark/`
- `docs/paper/`
- `scripts/`
- `remote-results/`

### Do Not Upload Mainline

- `status/local-private/virtuoso_bridge_sui.env`
- `status/*fail*.txt`
- individual H/I debugging files when covered by `2026-04-29_HI_sequence_results.md`
- old qwen/kimi exploratory status files unless they are needed for an appendix
- translated reference paper assets unless license/publication usage is clear

## EVAS Final Upload Set

Upload current source and tests. There is no need to preserve multiple versions here; git history will handle that.

Upload:

- `evas/`
- `tests/`
- `README.md`
- `evas-capabilities.manifest`

Do not upload:

- `.pytest_cache/`
- `.ruff_cache/`
- `.venv/`
- `evas_sim.egg-info/`

## veriloga-skills Final Upload Set

Upload the current knowledge cards:

- `veriloga/SKILL.md`
- `veriloga/references/categories/adc-sar.md`
- `veriloga/references/categories/dac.md`
- `veriloga/references/categories/digital-logic.md`
- `veriloga/references/categories/pll-clock.md`
- `veriloga/references/evas-capabilities.manifest`

Do not upload:

- `.DS_Store`
- `.pytest_cache/`

## If A File Has Many Versions

Use this rule:

1. If it affects executable behavior now, upload only the current source file.
2. If it is an experiment result, upload only the final result root and a summary markdown.
3. If it is a knowledge asset, upload the merged final asset plus a provenance asset if needed.
4. If it is a failed/smoke/ablation variant, do not upload raw files unless the paper explicitly cites that ablation.
5. If it contains local paths, bridge config, model metadata, or prompts with API metadata, keep it local unless sanitized.

## Recommended Remote Shape

The clean remote should make this story easy to follow:

`A/D/F/G` strict baseline line -> `H/I` limited continuation -> `92/92` closed-set completion package -> `benchmark-v2` same-type transfer validation.

Anything that does not support this story should either stay local or be moved to a separate archival remote/object store.
