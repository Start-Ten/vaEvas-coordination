# vaEvas Figure Plan

Status: figure planning draft, 2026-04-26.

This file lists the figures needed by the bilingual paper draft. The current recommendation is to keep diagrams editable until the paper story is frozen, then render them as SVG/PDF or generate polished visuals.

## Figure 1: EVAS-Guided Closed-Loop Repair

Purpose: show the core contribution: EVAS is the fast executable feedback engine inside the LLM repair loop.

Mermaid source:

```mermaid
flowchart LR
  P[Task prompt] --> G[LLM Verilog-A generation]
  G --> C[EVAS compile]
  C --> S[EVAS simulation]
  S --> K[Checker / assertion]
  K --> F[Structured failure signature]
  F --> R[Repair proposal]
  R --> C
  K --> B[Best EVAS-passing artifact]
  B --> V[Spectre/Virtuoso acceptance]
```

Suggested visual style:

1. EVAS loop in a bold colored inner cycle.
2. Spectre/Virtuoso as a final validation box outside the loop.
3. Show CSV/waveform/checker outputs between EVAS simulation and failure signature.

Image-generation prompt if needed:

```text
Create a clean academic systems diagram for a paper. The diagram shows an LLM generating Verilog-A from a task prompt, then an EVAS compile/simulation loop producing CSV traces, checker results, structured failure signatures, and repair prompts back to the LLM. Outside the loop, show Spectre/Virtuoso as final industrial acceptance validation. Use a professional IEEE-style visual design, white background, blue and orange accents, crisp vector shapes, no decorative icons, readable labels.
```

## Figure 1b: Why EVAS Is Fast

Purpose: explain the architectural source of EVAS speed without overclaiming that EVAS is a full Spectre replacement.

Recommended layout:

1. Left side: Spectre/Virtuoso path.
2. Left-side labels: device/current contributions, KCL/KVL equations, MNA matrix assembly, nonlinear continuous-time solve.
3. Right side: EVAS path.
4. Right-side labels: voltage-domain behavioral subset, event queue for `cross/above/timer`, direct voltage-state update for `V() <+`, CSV/checker output.
5. Bottom callout: "Fast because EVAS avoids full MNA/KCL solving; scope is pure voltage-domain behavioral Verilog-A."

Image-generation prompt if needed:

```text
Create a clean academic comparison diagram showing why EVAS is faster than Spectre/Virtuoso for behavioral Verilog-A repair. Left column: Spectre/Virtuoso SPICE-class flow with current contributions, KCL/KVL equations, MNA matrix solve, nonlinear continuous-time iteration. Right column: EVAS event-driven voltage-domain flow with V() voltage contributions, cross/timer/above event queue, transition output shaping, CSV checker output. Add a clear boundary note: EVAS is for pure voltage-domain behavioral models, not arbitrary current-domain SPICE simulation. Professional IEEE-style vector diagram, white background, readable labels.
```

## Figure 2: Condition Ladder A/D/F/H/I

Purpose: explain why the main story can be simplified to A/D/F/H, while showing I as the ongoing contract/assertion extension.

Mermaid source:

```mermaid
flowchart TB
  A[A: raw prompt] --> D[D: single EVAS feedback round]
  D --> F[F: multi-round EVAS repair]
  F --> H[H: signature-guided EVAS repair]
  H --> I[I: contract-aligned assertion-guided repair]
  I --> SP[Spectre/Virtuoso confirmation]
```

Suggested visual style:

1. Use a staircase or ladder.
2. Put pass counts next to completed steps: A 18/92, D 48/92, F 58/92, H 59/92.
3. Mark I as "ongoing / TBD" rather than an established result.
4. Mark B/C/E/G as small side ablation bubbles, not in the main path.

## Figure 3: Failure Taxonomy and Feedback Quality

Purpose: show that compile/TB failures are mostly solved by EVAS repair, while remaining failures are behavior-level and motivate signature-guided repair.

Recommended plot:

1. grouped bar chart for A/D/F/H;
2. categories: behavior failure, DUT compile failure, TB compile failure, other;
3. use values from the latest snapshot:
   - A: 48, 20, 5, 1
   - D: 41, 1, 0, 2
   - F: 31, 1, 0, 2
   - H: 30, 1, 0, 2

## Figure 4: EVAS vs Spectre Consistency and Speed

Purpose: key missing evidence table/figure.

Required data:

1. task subset;
2. EVAS pass/fail;
3. Spectre/Virtuoso pass/fail;
4. EVAS runtime;
5. Spectre/Virtuoso runtime.

Recommended visualization:

1. left: agreement heatmap or confusion matrix;
2. right: runtime speedup bar chart.

Status: TBD until Spectre/Virtuoso runs are collected.

## Table: Cross-Model Performance

Purpose: show whether the EVAS-guided system works beyond a single LLM.

Reserved columns:

1. model name;
2. raw-prompt EVAS score;
3. best EVAS repair score under F/H;
4. Spectre/Virtuoso acceptance score;
5. dominant failure modes;
6. reproducibility notes and run date.

Current placeholders:

| Model | Raw EVAS | Best F/H EVAS | Spectre/Virtuoso | Dominant failures | Notes |
|---|---:|---:|---:|---|---|
| Kimi | 18/92 | F: 58/92; H: 59/92 | TBD | Behavior failures after repair | Current primary snapshot |
| Qwen | 25/92 | TBD | TBD | TBD | Needs current-system refresh |
| GPT-5.5/API model | TBD | TBD | TBD | TBD | Requires reproducible API entry |
