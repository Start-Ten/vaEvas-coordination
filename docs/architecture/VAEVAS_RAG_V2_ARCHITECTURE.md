# VAEVAS RAG-v2 Architecture

Date: 2026-04-29

## Purpose

The current RAG layer is useful as a routing prototype, but it is still too close
to keyword search.  RAG-v2 should make retrieval function-level and
verification-aware:

```text
prompt + interface + EVAS failure
-> functional IR
-> query rewriting + HyDE mechanism hypothesis
-> hybrid retrieval
-> reranking
-> slot binding
-> materialized template/skeleton
-> EVAS
-> Spectre
-> verified memory update
```

The immediate use case is closed-set 92 completion.  The later use case is
benchmark-v2 perturbation transfer.

## Inputs

For each task/run, RAG-v2 should read:

- public prompt text
- task family and task_id
- expected artifacts
- generated module/testbench interface
- EVAS status, checker notes, and metric gaps
- Spectre status, if available
- current best artifact root
- inferred functional IR and prompt templates

## Knowledge Sources

Ranked by confidence:

1. verified artifact store: EVAS+Spectre PASS artifacts
2. closed-set concrete circuit templates
3. R26/gold distilled templates
4. mechanism skeletons
5. contract/repair cards
6. prompt-checker templates
7. broad Verilog-A skill notes
8. negative memory from failed retrievals

## Stage 1: Functional IR

Convert prompt/failure into a compact structure:

```json
{
  "mechanism_candidates": ["adc_dac_quantize_reconstruct"],
  "ports": {
    "analog_input": "input",
    "clock": "clk",
    "code_outputs": ["bit0", "bit1", "bit2", "bit3"],
    "analog_output": "recon"
  },
  "parameters": {
    "width": 4,
    "reference": "vdd_vss"
  },
  "positive_constraints": ["quantized reconstruction", "monotonic output"],
  "negative_constraints": ["not thermometer unless unit-cell/unary requested"],
  "failure_signature": ["coverage_zero", "vout_tracks_raw_input"]
}
```

This stage is allowed to use simple rules first.  It does not require model
training.

## Stage 2: Query Rewriting

Raw prompts are often not good search queries.  Rewrite them into mechanism
queries.

Example:

Raw:

```text
The node named input carries the measured analog level. Produce four decision
outputs and a reconstructed analog level.
```

Rewritten:

```text
ADC-DAC quantization and reconstruction; analog input; 4-bit code outputs;
monotonic reconstructed analog output; shared held code state.
```

The rewritten query should also carry negative constraints:

```text
Do not retrieve thermometer/unary DAC unless prompt asks unit cells or active-count coding.
```

## Stage 3: HyDE Mechanism Hypothesis

Generate a short hypothetical ideal mechanism description, then retrieve real
knowledge around it.

Example hypothesis:

```text
This task is solved by keeping one integer code as the source of truth.  The
code is updated from the sampled analog input and then used both for code-bit
outputs and reconstructed analog output.  The reconstruction should not track
the raw input continuously.
```

This helps when the prompt avoids standard keywords like ADC, DAC, DWA, PFD, or
PLL.

## Stage 4: Hybrid Retrieval

Use multiple retrieval signals:

- lexical/token retrieval: robust for exact terms and signal names
- semantic retrieval: robust for paraphrases and missing keywords
- rule filters: prevent known false positives
- graph retrieval: useful for system tasks with internal relations

Initial implementation can keep the current lexical retriever and add the other
signals incrementally.

## Stage 5: Reranking

Rerank raw candidates using features:

- mechanism compatibility
- slot coverage
- negative-constraint violation
- source confidence
- prior EVAS/Spectre success
- task-family compatibility
- failure-signature match

Suggested source confidence:

```text
verified artifact > concrete circuit template > R26 template > skeleton > repair card > prompt template > skill note
```

Reranker output should be inspectable:

```json
{
  "node_id": "template:adc_dac_quantize_reconstruct",
  "raw_score": 12.4,
  "rerank_score": 0.91,
  "reasons": ["mechanism_match", "width_bound", "output_slots_bound"],
  "risks": []
}
```

## Stage 6: Slot Binding

Bind abstract mechanism slots to current task names:

```json
{
  "skeleton": "adc_dac_quantize_reconstruct_skeleton",
  "slot_coverage": 0.92,
  "bindings": {
    "vin": "input",
    "clock": "clk",
    "code_outputs": ["bit0", "bit1", "bit2", "bit3"],
    "vout": "recon",
    "width": 4,
    "reference": ["vdd", "vss"]
  },
  "missing": [],
  "ambiguous": ["reset"]
}
```

If slot coverage is too low, do not spend expensive LLM repair calls.  Write a
failure packet and improve the extractor or template.

## Stage 7: Materialization

Use the bound slots to produce one of three outputs:

1. exact verified artifact replay
2. concrete circuit template with slots filled
3. skeleton-guided LLM repair prompt

The system should prefer deterministic materialization over free-form repair
when enough slots are bound.

## Stage 8: EVAS/Spectre Feedback Memory

Every attempt should update memory:

Positive memory:

```json
{
  "query": "...",
  "retrieved_nodes": ["skeleton:dwa_pointer_window_skeleton"],
  "bindings": {"code_bits": ["code0", "code1", "code2", "code3"]},
  "outcome": "EVAS_PASS_SPECTRE_PASS",
  "artifact_root": "...",
  "mechanism": "dwa_rotating_pointer_window"
}
```

Negative memory:

```json
{
  "query": "...",
  "retrieved_nodes": ["template:thermometer_decode"],
  "outcome": "FAIL_WRONG_MECHANISM",
  "reason": "prompt explicitly requested binary-weighted DAC, not thermometer"
}
```

## Metrics

Retrieval metrics:

- mechanism recall@1/@3/@5
- forbidden mechanism top-k rate
- slot coverage
- reranker lift over raw retrieval

Repair metrics:

- EVAS PASS
- Spectre PASS
- EVAS/Spectre agreement
- attempts per PASS
- cost per PASS

Knowledge-growth metrics:

- positive memory count
- negative memory count
- repeated-error reduction
- perturbation transfer success

## Implementation Priority

Night priority:

1. router output schema
2. query rewrite stub
3. HyDE mechanism hypothesis text
4. slot binding prototype
5. reranker score with transparent features
6. positive/negative memory JSON

Later:

1. embedding index
2. learned reranker
3. post-training data export
4. benchmark-v2 transfer experiments
