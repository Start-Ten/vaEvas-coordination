---
name: vaevas-git-sync
description: Audit, commit, push, and optionally open PRs for vaEvas sub-repositories. Use when the user asks whether local vaEvas folders are synced with remotes, wants to commit/push EVAS, behavioral-veriloga-eval, coordination, or veriloga-skills changes, wants to merge to main, or wants a repeatable safe git publication workflow for vaEvas.
---

# vaEvas Git Sync

## Overview

Use this skill to publish vaEvas work without accidentally uploading local experiment noise, private bridge profiles, raw model outputs, or third-party reference materials.

Default repositories under `vaEvas/`:

1. `EVAS`
2. `behavioral-veriloga-eval`
3. `coordination`
4. `veriloga-skills`
5. `reference/verilog-eval`
6. `reference/verilog-eval-v2`

## Quick Audit

Run the bundled audit first:

```bash
python3 ~/.codex/skills/vaevas-git-sync/scripts/check_vaevas_git_sync.py /Users/bucketsran/Documents/TsingProject/vaEvas --fetch
```

Use the output to report:

1. current branch,
2. tracking remote,
3. ahead/behind counts,
4. modified/deleted/staged files,
5. untracked files,
6. ignored local-private files.

Interpret `ahead=0 behind=0` as “current branch is synced with its tracking remote”. Still mention untracked files separately.

## Publication Workflow

1. Fetch remotes with `git fetch --all --prune`.
2. Inspect `git status -sb` before staging anything.
3. Stage only the scope requested by the user.
4. Exclude local and noisy files.
5. Run validation.
6. Commit with a concise message.
7. Push to the intended branch.
8. If requested, open a draft PR to upstream.
9. Re-run the audit and report residual untracked files.

## Exclusion Rules

Never stage these unless the user explicitly asks and the file is safe:

1. `.env`, `*.env`, API keys, SSH profiles, bridge profiles.
2. `status/local-private/`.
3. `.DS_Store`, caches, virtualenvs.
4. raw LLM outputs: `raw_response.txt`, `generation_meta.json`, `repair_prompt.md`.
5. simulation bulk: `tran.csv`, logs, full raw `results/`, scratch/tmp/refine logs.
6. third-party or copied paper assets under `referencepaper/` unless license/publication use is clear.

For `behavioral-veriloga-eval`, prefer final mainline artifacts and compact summaries over old generated sweeps.

For `coordination`, prefer current release pointers, related-work notes, current status summaries, skills, and templates; do not publish local-private bridge env files or stale experiment ledgers.

## Validation Checklist

Before commit:

```bash
git diff --cached --check
git diff --cached --name-only '*.py' | xargs -r python3 -m py_compile
git diff --cached --name-only '*.json' | xargs -r python3 -c 'import json,sys; [json.load(open(p)) for p in sys.argv[1:]]'
```

For JSONL:

```bash
git diff --cached --name-only '*.jsonl' | xargs -r python3 -c $'import json,sys\nfor p in sys.argv[1:]:\n    [json.loads(line) for line in open(p) if line.strip()]'
```

Run a secret scan over staged files:

```bash
git diff --cached --name-only | xargs -r rg -n '(^|[^A-Za-z])sk-[A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{16}|OPENAI_API_KEY=|ANTHROPIC_API_KEY=|DASHSCOPE_API_KEY=|MOONSHOT_API_KEY=|MINIMAX_API_KEY=|api[_-]?key\s*[:=]\s*["'"'"'][A-Za-z0-9_-]{16,}' || true
```

Treat matches as suspicious until manually reviewed. Some words like `task-specific` can be false positives if the pattern is too broad.

## Reporting Format

Use this concise table:

| repo | branch | tracking | sync | local residue |
|---|---|---|---|---|

For `sync`, use:

1. `synced`: `ahead=0 behind=0` and no tracked changes.
2. `synced + untracked local files`: branch matches remote, but local scratch/untracked files remain.
3. `ahead N`: local commits not pushed.
4. `behind N`: remote has commits not pulled.
5. `diverged`: both ahead and behind.

End with commit hash, push target, PR link if any, and any files intentionally left local.
