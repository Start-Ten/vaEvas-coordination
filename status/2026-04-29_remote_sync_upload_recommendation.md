# Remote Sync Upload Recommendation

Date: 2026-04-29

## Repository Layout

`vaEvas` root is not itself a git repository. The active git repositories are:

- `EVAS`
- `behavioral-veriloga-eval`
- `coordination`
- `veriloga-skills`

Therefore remote sync should be done per sub-repository, not by uploading the entire `vaEvas` folder.

## Upload First

### EVAS

Upload the EVAS core changes because they affect EVAS/Spectre parity and strict-v3 scoring:

- `README.md`
- `evas-capabilities.manifest`
- `evas/compiler/ast_nodes.py`
- `evas/compiler/lexer.py`
- `evas/compiler/parser.py`
- `evas/netlist/runner.py`
- `evas/netlist/spectre_parser.py`
- `evas/simulator/backend.py`
- `evas/simulator/engine.py`
- `tests/test_compiler.py`
- `tests/test_engine.py`
- `tests/test_netlist.py`

Do not upload local caches or environments:

- `.pytest_cache/`
- `.ruff_cache/`
- `.venv/`
- `evas_sim.egg-info/`

### behavioral-veriloga-eval

Upload the reusable benchmark/system code and compact evidence:

- `benchmark-v2/`
- `docs/`
- `runners/`
- `tasks/**/prompt.md`
- `tasks/**/contracts.json`
- `prompt-defect-cases/`
- `specs/`
- `tables/RUN_REGISTRY.md`

Important runner additions include:

- `runners/audit_completion_package.py`
- `runners/build_closedset92_assets.py`
- `runners/completion_package_materialize_benchmark_v2.py`
- `runners/materialize_benchmark_v2_tasks.py`
- `runners/rag_v2_router.py`
- `runners/run_circuit_mechanism_rag_audit.py`
- `runners/spectre_validate_baseline.py`
- `runners/validate_benchmark_v2_gold.py`

Upload only compact generated evidence:

- `generated-completion-package-benchmark-v2-2026-04-29-r1/`

Upload selected result summaries, not the full `results/` tree:

- `results/completion-package-audit-2026-04-29/`
- `results/completion-package-benchmark-v2-evas-2026-04-29-r1/`
- `results/completion-package-benchmark-v2-spectre-2026-04-29-r1/`
- `results/benchmark-v2-gold-validation-2026-04-29-r2/`
- `results/benchmark-v2-gold-validation-spectre-2026-04-29-r1/`
- Current A/D/F/G/H/I/RAG summary JSON/MD files needed by the paper table.

Do not bulk upload:

- `results/` as a whole, currently about `12G`
- old `generated-*` historical sweeps
- `scratch/`
- `tmp/`
- `.pytest_cache/`
- `.env.table2`
- `**/generation_meta.json`
- `**/repair_prompt.md`, unless explicitly needed for a provenance audit
- `**/tran.csv`

### coordination

Upload the current paper/experiment coordination material:

- `docs/architecture/`
- `docs/benchmark/`
- `docs/paper/`
- `scripts/`
- `remote-results/`
- `status/00_CURRENT_MAINLINE.md`
- `status/2026-04-12_repo-visibility-note.md`
- `status/2026-04-29_*.md`
- selected `status/2026-04-28_*.md` used by the A/D/F/G strict-v3 narrative
- `status/archive/2026-04-legacy-collaboration/README.md`

Make sure `docs/benchmark/EVAS_SPECTRE_TIMING_PLAN.md` is included because timing evidence is now part of the main paper story.

Do not upload the archived historical files as current status unless a paper appendix explicitly cites them.

Do not upload local bridge environment files:

- `status/local-private/virtuoso_bridge_sui.env`

For public remote repositories, avoid uploading copied reference PDFs or full translated third-party papers unless license status is clear.

### veriloga-skills

Upload the skill/card knowledge changes:

- `veriloga/SKILL.md`
- `veriloga/references/categories/adc-sar.md`
- `veriloga/references/categories/dac.md`
- `veriloga/references/categories/digital-logic.md`
- `veriloga/references/categories/pll-clock.md`
- `veriloga/references/evas-capabilities.manifest`

Do not upload:

- `.pytest_cache/`
- `.DS_Store`

## Upload Later Or Archive Separately

These folders may contain useful history but should not block the main remote sync:

- old `behavioral-veriloga-eval/generated-*` experiment directories
- old `behavioral-veriloga-eval/results/*` full simulation folders
- root `results/`
- `refine-logs/`
- `worksche/`
- `interesting-findings/`
- `reference/`
- `testspace/`

If preserving history is important, package them into a separate compressed archive or object storage bucket rather than committing to the main code remote.

## Security Notes

A quick text scan found environment-variable names and provider names, but no obvious raw API key pattern in ordinary source/docs. Still, before public upload, re-run a secret scan and manually exclude:

- `*.env`
- `.env*`
- local bridge profiles
- SSH host/user/port profiles
- generated metadata that may contain prompts, model configs, or local paths

## Recommended Sync Strategy

1. Commit/push the four git repos separately: `EVAS`, `behavioral-veriloga-eval`, `coordination`, `veriloga-skills`.
2. In `behavioral-veriloga-eval`, commit source/docs/benchmark-v2 first.
3. Add only selected result summary folders after checking size.
4. Keep full raw `results/` and old generated sweeps local or archive them outside git.
