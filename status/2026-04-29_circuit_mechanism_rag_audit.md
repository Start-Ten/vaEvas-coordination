# Circuit-Mechanism RAG 检索实验

日期：2026-04-29

## 目的

这轮实验验证一个很小但关键的问题：如果后续把机制卡片升级为 RAG + 电路匹配，检索层能不能根据公开 prompt、功能 IR、EVAS/contract failure vector 找到正确机制。

这不是 LLM repair pass-rate，也不调用 API。它只是判断 RAG 检索是否值得进入下一步修复实验。

## 新增脚本

- `behavioral-veriloga-eval/runners/run_circuit_mechanism_rag_audit.py`

知识库来源：

- `behavioral-veriloga-eval/docs/CONTRACT_REPAIR_CARDS.json`
- `behavioral-veriloga-eval/docs/PROMPT_CHECKER_SPECS_ADOPTED.json`
- `behavioral-veriloga-eval/results/gold-r26-template-generalization-2026-04-29/gold_r26_mechanism_templates.json`
- `veriloga-skills/veriloga/references/categories/*.md`

输出：

- `behavioral-veriloga-eval/results/circuit-mechanism-rag-audit-2026-04-29/summary.json`
- `behavioral-veriloga-eval/results/circuit-mechanism-rag-audit-2026-04-29/summary.md`

## 实验集

总计 23 个 no-API 检索 case：

- 19 个来自 mechanism generalization benchmark：数值扰动、命名扰动、结构扰动、拼写/别名、functional paraphrase、negative control。
- 4 个新增 R26 near-neighbor case：PLL、DWA、PFD、ADC/DAC。

## 结果

当前 guarded RAG 结果（加入 R26 near-neighbor、功能 IR 和 DWA guard 后重跑）：

| 指标 | 结果 |
|---|---:|
| positive cases | 20 |
| negative/no-expected cases | 3 |
| top-1 mechanism hit | 18/20 = 0.9000 |
| top-3 mechanism hit | 20/20 = 1.0000 |
| top-5 mechanism hit | 20/20 = 1.0000 |
| forbidden top-3 retrieval | 5/23 = 0.2174 |

R26 near-neighbor 子集：

| 子集 | top-3 hit |
|---|---:|
| PLL/DWA/PFD/ADC-DAC near-neighbor | 4/4 |

## 解释

这个结果说明 Circuit-Mechanism RAG 方向是可行的，但不能直接使用普通文本相似度。

首版 lexical RAG 的 top-3 只有 11/23，并且 forbidden top-3 有 6/23。加入 functional IR、模板节点、R26 机制节点和否定语义 guard 后，top-3 可以覆盖全部 positive cases；但为了让 DWA 这种“binary code + pointer/thermometer mask”机制不被误杀，当前 guard 放宽后 forbidden top-3 回升到 5/23。这说明 RAG 层需要分成两步：第一步高召回找到相关机制，第二步在压缩成 repair hint 前做更严格的 final guard。

这说明：

1. 机制检索不能只靠关键词或普通文本相似度。
2. 必须显式处理否定语义，例如 `not thermometer`、`no parameter override`、binary counter vs Gray counter。
3. R26 机制模板可以作为 RAG 知识源：新增的 4 个 near-neighbor case 都能在 top-3 找到相关机制。
4. 机制卡片仍然有价值，但更适合作为 RAG 检索结果的可控摘要，而不是最终知识库。

## 剩余问题

当前没有 positive top-3 miss，但仍有 5 个 forbidden top-3：

- `therm_dac_width12_vstep025`：召回了 generic `dac_code_to_output_span`。
- `binary_dac_no_thermometer_control`
- `binary_dac_monotocin_dinp_alias`
- `pfd_no_bbpd_control`
- `binary_dac_functional_order_no_keyword`

这些不是直接的 pass-rate 失败，但说明压缩成 repair hint 前还需要一个 final guard：如果 prompt 明确不是 thermometer/unary，不应把 thermometer template 放入最终提示；如果 prompt 是 PFD 而不是 BBPD，不应把 BBPD lead/lag 卡放入最终提示。当前 repair prompt 侧已经额外加入了这种压缩前过滤。

## 端到端 EVAS/Spectre Repair Pilot

在检索实验之后，已经做了一个小规模端到端验证，不再只看 retrieval 分数。

代码改动：

- `behavioral-veriloga-eval/runners/build_repair_prompt.py`
  - 新增 `VAEVAS_ENABLE_CIRCUIT_RAG=1` 开关；
  - 在 repair prompt 中追加 `Circuit-Mechanism RAG Hints`；
  - 使用多路召回：优先保留一个 R26 template、一个 repair-card、一个 prompt-template，而不是只取全局相似度前三。
- `behavioral-veriloga-eval/runners/score.py`
  - 修复多行 `save ... \` 被 contract pruning 后遗留续行的问题。旧逻辑只替换第一行 `save`，真实 Spectre 会把 orphan continuation 误解析为实例，导致 EVAS PASS / Spectre FAIL。

## Skeleton-RAG 接入

为回答“R26/92PASS 是否只沉淀成文字经验，而没有可执行骨架”的问题，新增了一个显式 skeleton 知识层：

- `behavioral-veriloga-eval/docs/CIRCUIT_MECHANISM_SKELETONS.json`

当前包含 4 类从 R26/closure 经验抽象出的可执行机制骨架：

| skeleton | 来源机制 | 内容 |
|---|---|---|
| `dwa_pointer_window_skeleton` | `dwa_rotating_pointer_window` | pointer/code/window/cell-enable 的状态变量、数组 target、clock event、modulo window、unconditional transition 写法 |
| `adc_dac_quantize_reconstruct_skeleton` | `adc_dac_quantize_reconstruct` | 单一 held code 同时驱动 code bits 和 vout reconstruction |
| `pfd_edge_pulse_window_skeleton` | `pfd_mutual_exclusion_pulse_windows` | REF/DIV edge 到 UP/DN pulse、clear timer、non-overlap target |
| `pll_feedback_cadence_skeleton` | `pll_feedback_cadence_lock` | DCO timer、feedback divider、control update、lock-after-stable-ratio 的系统关系 |

接入方式：

- `run_circuit_mechanism_rag_audit.py` 现在把 skeleton 作为 `mechanism_skeleton` 类型的 RAG node；
- `build_repair_prompt.py` 的 RAG 注入改为多路召回：
  1. `mechanism_skeleton`
  2. `r26_template`
  3. `repair_card`
  4. `prompt_template`
- repair prompt 中会显示 skeleton 的 slot schema、implementation skeleton、Verilog-A shape 和 anti-pattern。

静态召回检查：

| task | top RAG skeleton |
|---|---|
| `dwa_ptr_gen_no_overlap_smoke` | `skeleton:dwa_pointer_window_skeleton` |
| `adc_dac_ideal_4b_smoke` | `skeleton:adc_dac_quantize_reconstruct_skeleton` |
| `cppll_tracking_smoke` | `skeleton:pll_feedback_cadence_skeleton` |
| `pfd_reset_race_smoke` | `skeleton:pfd_edge_pulse_window_skeleton` |

Pilot 任务：

- 从最终 G 剩余失败中选 8 个行为类任务：
  `adc_dac_ideal_4b_smoke`、`sar_adc_dac_weighted_8b_smoke`、`cppll_tracking_smoke`、`cppll_freq_step_reacquire_smoke`、`dwa_ptr_gen_no_overlap_smoke`、`pfd_reset_race_smoke`、`multimod_divider_ratio_switch_smoke`、`nrz_prbs`。

结果：

| 条件 | EVAS quick repair | 标准 EVAS | Spectre strict |
|---|---:|---:|---:|
| RAG-diverse on 8 G-fail tasks | 1/8 PASS | targeted `dwa_ptr_gen_no_overlap_smoke`: 1/1 PASS | targeted `dwa_ptr_gen_no_overlap_smoke`: 1/1 PASS |
| Skeleton-RAG on same 8 G-fail tasks | 1/8 PASS | targeted `dwa_ptr_gen_no_overlap_smoke`: 1/1 PASS | targeted `dwa_ptr_gen_no_overlap_smoke`: 1/1 PASS |
| no-RAG DWA control, same 2 rounds | 0/1 PASS | 未送 Spectre | 未送 Spectre |

关键新增 PASS：

- `dwa_ptr_gen_no_overlap_smoke`
  - G baseline: `FAIL_SIM_CORRECTNESS`
  - RAG round 1: still fail, but moved from no active cells to `max_active_cells=8, overlap_count=7`
  - RAG round 2: EVAS PASS, `overlap_count=0`
  - Standard EVAS after save-continuation fix: PASS
  - Spectre strict after save-continuation fix: PASS

相关结果目录：

- `behavioral-veriloga-eval/results/condition-I-rag-diverse-on-Gfailed-pilot-kimi-evas-2026-04-29`
- `behavioral-veriloga-eval/results/condition-I-rag-diverse-on-Gfailed-pilot-kimi-evas-standard-dwa-savefix-2026-04-29`
- `behavioral-veriloga-eval/results/condition-I-rag-diverse-on-Gfailed-pilot-kimi-spectre-dwa-savefix-2026-04-29`
- `behavioral-veriloga-eval/results/condition-no-rag-on-Gfailed-dwa-control-kimi-evas-2026-04-29`

结论：RAG 不是“检索到了就能修”。在 8 个真实失败任务里，当前版本只稳定救回 1 个；但这个新增 PASS 通过了标准 EVAS 和真实 Spectre，并且 no-RAG 对照没有救回同一 DWA 任务。因此 RAG 方向有实证价值，但还只是 pilot evidence，不能当作 full92 主结果。

Skeleton-RAG 的新增意义不是立刻多救更多任务，而是把 92PASS/R26 的经验从“文字机制摘要”推进到了“可审计、可检索、可注入的 Verilog-A 写法骨架”。当前骨架仍偏通用，复杂 PLL/SAR/PFD 任务没有因此直接 PASS，说明下一步需要把 skeleton 从 generic shape 继续细化到 slot-bound skeleton generator：根据 prompt 自动绑定端口名、参数名、位宽、reset polarity、保存节点和 checker metric gap。

## 下一步

建议下一步做扩展 repair 实验：

1. 从 G residual failures 中扩展到全部 27 个失败任务。
2. 对照三组：
   - current rule-card
   - RAG-only / RAG-diverse
   - RAG+card-summary / skeleton-template
3. 每组最多 2-3 轮 EVAS repair。
4. 新增 PASS 进行 Spectre 验证。

只有当 RAG+card 在同一批失败任务上比 current rule-card 多救任务，并且 Spectre 也确认，才把 Circuit-Mechanism RAG 写成正式方法结果。
