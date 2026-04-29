# vaEvas Cleanup Audit

Date: 2026-04-29

## Current Disk Profile

Workspace size:

- `vaEvas`: about 70G
- `behavioral-veriloga-eval`: about 67G
- `behavioral-veriloga-eval/results`: about 66G
- `EVAS`: about 126M
- `coordination`: about 11M
- `veriloga-skills`: about 1.9M

File-type pressure inside `behavioral-veriloga-eval/results`:

- `.csv`: about 63.9G across 9878 files
- Spectre `.tran` raw payloads: about 2.1G across 642 files
- `.json`: about 70M
- `.md`: about 30M
- `.va`, `.scs`, logs, prompts: small

Conclusion: the space problem is almost entirely waveform/result payloads,
especially `tran.csv`, not source code, prompts, skills, or generated Verilog-A.

## Keep Hot

These are mainline or still needed for current A/D/F/G/H/I work:

- `behavioral-veriloga-eval/tasks`
- `behavioral-veriloga-eval/runners`
- `behavioral-veriloga-eval/specs`
- `behavioral-veriloga-eval/docs`
- `EVAS`
- `veriloga-skills`
- `coordination/status`
- current strict-v3 A/D/F/G result summaries and generated artifacts
- final G result:
  - `generated-condition-G-targeted-materialized-spectre-aligned-kimi-2026-04-28`
  - `results/condition-G-targeted-materialized-spectre-aligned-kimi-evas-2026-04-28`
  - `results/condition-G-targeted-materialized-spectre-aligned-kimi-spectre-combined-2026-04-28`

For H/I dataset construction, keep at least:

- `result.json`
- `model_results.json`
- `summary.json` / `summary.md`
- generated `.va` / `.scs`
- `generation_meta.json`
- `repair_prompt.md`
- task `prompt.md`
- mechanism cards / contracts / specs

## Useful But Should Be Slimmed

These historical runs are useful as experience data, but not as full waveform
archives:

- old H/H2/I/F/G exploratory result roots
- `current-experiment-regression-2026-04-27` because it records historical
  engineering evidence but includes polluted baselines
- old `latest-system-score-*` roots
- old overfit-guard experiments
- gold perturbation / mechanism sweep outputs

Before deletion, extract a lightweight dataset:

- task id
- condition/run id
- status and scores
- EVAS/Spectre notes
- metrics / checker gaps
- failure domain / owner
- source artifact path or small source hash
- prompt path
- repair prompt if present

Usually the full `tran.csv` is not needed for H/I because the checker has
already compressed it into notes and metrics. Keep only selected waveforms when
developing a new checker or investigating a specific mechanism.

## Safe Cleanup Candidates

High-confidence cleanup candidates after slim extraction:

- `tran.csv` files in obsolete historical runs
- Spectre raw directories such as `spectre/*.raw`
- repeated full waveform payloads in superseded A/B/C/D/F/G/H/I runs
- aborted or mixed-mouth roots, for example:
  - `condition-G-coldstart-full92-kimi-evas-2026-04-28_ABORTED_D41_R0`
  - `generated-condition-G-coldstart-full92-kimi-2026-04-28_ABORTED_D41_R0`
- placeholder-contaminated baseline roots, keeping only summaries that explain
  why they are invalid

## Not Safe To Blindly Delete

Do not blindly delete:

- current mainline A/D/F/G roots
- current final G roots
- source artifacts for tasks that will seed H/I cards
- `coordination/status/*.md` experiment ledgers
- prompt defect archives
- mechanism-card and contract JSON files
- final Spectre comparison summaries

## Recommended Cleanup Workflow

1. Export a slim JSONL ledger from all `result.json` files.
2. Export a smaller H/I seed dataset from the current final G 27 failures.
3. For historical roots, preserve only summaries, JSON metadata, generated
   code, prompts, and repair prompts.
4. Delete or archive `tran.csv` and Spectre raw payloads from superseded roots.
5. Keep current G final waveforms temporarily until H/I signature extraction is
   stable; then slim them too.

Expected disk recovery:

- Removing obsolete `tran.csv` payloads can recover tens of GB.
- Removing Spectre raw payloads can recover about 2G.
- Deleting generated code directories gives little benefit and should not be
  the first target.

## Cleanup Applied

Applied on 2026-04-29 with:

```bash
python3 coordination/scripts/slim_results_and_cleanup.py --apply --skip-ledger
```

Before deletion, the dry run exported:

- `coordination/datasets/experiment_ledger_slim_2026-04-29.jsonl`
  - 18,103 records
- `coordination/datasets/hi_seed_final_G_failures_2026-04-29.jsonl`
  - 27 records from final G failures

Removed payloads:

- 9,356 non-protected `tran.csv` files
- 640 non-protected Spectre `.raw` directories
- Total removed: about 61.7G

Protected A/D/F/G paths were checked after cleanup:

- missing protected paths: 0
- final G `model_results.json` remains readable and still reports 65/92.

Post-cleanup disk profile:

- `vaEvas`: about 8.2G
- `behavioral-veriloga-eval`: about 4.9G
- `behavioral-veriloga-eval/results`: about 4.5G
- remaining `tran.csv` files: 500, all under protected or still-retained roots
- remaining Spectre `.raw` directories: 278, all under protected or
  still-retained roots
