# Issue, PR, and WeChat Workflow

This workflow keeps technical evidence out of chat-only history.

## Rules

1. Open an issue for unclear benchmark content, checker weakness, EVAS/Spectre mismatch, stale report evidence, or missing reproduction data.
2. Open a PR for code, report, benchmark, skill, or coordination changes.
3. After opening a PR, send a short WeChat notification with the repo, PR link, validation, and review risk.
4. Do not submit API keys, bridge profiles, raw simulator scratch, or large generated result directories.

## Routing

| Topic | Issue/PR target |
| --- | --- |
| EVAS implementation or Spectre parity | `BucketSran/EVAS` |
| vaBench release package, reports, checkers, runners, baselines | `BucketSran/behavioral-veriloga-eval` |
| Verilog-A skills/rules/knowledge | `BucketSran/veriloga-skills` |
| related work or coordination docs | `BucketSran/vaEvas-coordination` |

## PR Evidence Checklist

Each PR should include:

1. changed files.
2. claim boundary affected.
3. validation command or source report.
4. EVAS/Spectre status if relevant.
5. remaining risk or blocked claim.

## WeChat Template

```text
我刚提了一个 vaEvas PR：

仓库：<repo>
PR：<link>
主题：<one-line summary>
验证：<command/report>
需要重点看：<risk or decision>
```
