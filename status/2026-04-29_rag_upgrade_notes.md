# RAG-v2 Router Notes

Date: 2026-04-29

This is an inspectable router prototype for the current closed-set residual failures. It does not admit artifacts by itself.

- Scope: `closed-set residual failures`
- Total routed tasks: `0`
- Action counts: `{}`

## Routes

| Task | Action | Selected | Slot Coverage | Top Risks |
|---|---|---|---:|---|

## Interpretation

- `exact_replay_then_spectre` means a same-task R26/teacher artifact exists but needs real Spectre confirmation before strict admission.
- `slot_materializer` means the router found enough slot coverage for a deterministic or semi-deterministic materializer attempt.
- Low slot coverage should stop broad LLM repair and produce a failure packet.
