# EVAS Transition Compatibility Inventory

更新日期: 2026-04-18

这份清单只关心一件事：

1. 哪些 Verilog-A 写法已经有本地 Spectre 运行证据
2. 哪些写法过去因为 EVAS 过严而被迫改写
3. 现在这些写法在 EVAS 里的状态如何

## 已闭环候选

| case | 原始写法 | 本地 Spectre 证据 | EVAS 当前状态 | 备注 |
| --- | --- | --- | --- | --- |
| [cmp_ideal.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/comparator/comparator/cmp_ideal.va:44) | `transition(vdd * xoutp, ...)` | benchmark/dual-validation 历史证据已存在 | 已接受 | 属于 rail scaling around piecewise state |
| [dither_adder.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/measurement/gain_extraction/dither_adder.va:32) | `transition(V(VRES_P) + dither_diff * 0.5, 0)` | [gain_extraction spectre.out](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/gain_extraction_smoke/gain_extraction_smoke/spectre/spectre.out:73) 显示编译并完成运行 | 已接受 | 之前 gold 曾改成 direct contribution workaround |
| [gain_amp.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/measurement/gain_extraction/gain_amp.va:49) | `transition(vth + vout_diff * 0.5, 0)` | [gain_extraction spectre.out](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/gain_extraction_smoke/gain_extraction_smoke/spectre/spectre.out:74) | 已接受 | continuous affine target |
| [nrz_prbs.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/tasks/spec-to-va/voltage/signal-source/nrz_prbs/gold/nrz_prbs.va:43) | `transition(vcm + 0.5 * amp * level, ...)` | dual-validation 历史证据已存在 | 已接受 | common-mode plus scaled piecewise level |
| [flash_adc_3b.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/data-converter/flash_adc_3b/flash_adc_3b.va:47) | `transition((code >> 2) & 1 ? V(VDD) : V(VSS), ...)` | example/task history already runnable | 已接受 | ternary branch access in target |
| [adc_ideal_4b.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/data-converter/adc_dac_ideal_4b/adc_ideal_4b.va:43) | conditional `transition(V(vdd)) / transition(V(vss))` inside `if` | 本轮本地 Spectre 运行已确认 “带 `VACOMP-1116` warning 但可成功 transient”，见 [worksche log](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/logs/2026-04-18_evas-spectre-alignment-audit.md:1) | 已接受 | 这一类推动了本轮 conditional `transition()` 放开 |

## 历史 workaround，建议回看

| workaround file | 现状 | 建议 |
| --- | --- | --- |
| [gain_extraction gold dither_adder](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/tasks/end-to-end/voltage/gain_extraction_smoke/gold/dither_adder.va:1) | 已清理 | 现已改成 “benchmark gold style / lower-warning choice”，不再描述为当前 EVAS 必需 workaround |
| [adc_ideal_4b_ref](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/tasks/end-to-end/voltage/adc_dac_ideal_4b_smoke/gold/adc_ideal_4b_ref.va:5) | 已清理 | 现已改成 “Spectre-clean / low-warning gold style”，不再写成 EVAS 必需 |
| [gain_extraction gold lfsr](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/tasks/end-to-end/voltage/gain_extraction_smoke/gold/lfsr.va:1) | 已清理 | 现已明确这是 benchmark gold 的显式输出存储风格，而不是当前 EVAS transition 检查的硬要求 |

## 相关非-transition 尾项

| item | 当前状态 | 说明 |
| --- | --- | --- |
| `gain_extraction` example/gold `lfsr.va` 的旧数组声明 | 已清理 | 现在 direct EVAS parse/compile 与 full-netlist 执行一致，不再保留为开放尾项 |

## 仍未闭环项

| item | 当前状态 | 说明 |
| --- | --- | --- |
| conditional `idtmod()` | 保持限制 | 2026-04-18 本地 probe 已确认 Spectre 对该写法直接报 fatal `VACOMP-2154`；EVAS 当前编译期拒绝与 Spectre 一致，而本地仅放开 guard 时会出现 `catch_up_accumulate` 运行语义，因此不应作为“待放开兼容项”。 |
| conditional `cross()` | 保持限制 | 2026-04-18 conditional operator suite 已确认 Spectre 对该写法直接报 fatal `VACOMP-2146`；EVAS 当前也已补上同类编译期限制。 |
| conditional `above()` | 保持限制 | 2026-04-18 conditional operator suite 已确认 Spectre 对该写法直接报 fatal `VACOMP-2148`；EVAS 当前也已补上同类编译期限制。 |
| conditional absolute `timer(next_t)` | 已对齐 | 2026-04-18 conditional operator suite 已确认：无论是首次晚使能，还是 disable 窗口内错过目标时间，Spectre 都不会补触发过期 absolute timer；EVAS 现已对齐到相同行为。 |
| conditional periodic `timer(start, period)` | 已对齐 | 2026-04-18 conditional operator suite 已确认：Spectre 会跳过 active window 之外错过的周期点，但保持原始相位，在重新进入 active window 后从第一个未来周期点继续；EVAS 现已对齐到相同行为。 |
| `timer() -> transition() -> cross()` same-time visibility | 已对齐 | 2026-04-18 独立 probe 已确认：当 timer 在本步更新离散状态、transition 在同一步产生斜坡、cross 监听该输出时，Spectre 会在 11ns 中点观察到 crossing；EVAS 现通过 post-update cross/above replay 对齐这一行为。 |
| PLL-style absolute `timer(next_t)` armed-edge retarget | 已对齐 | 2026-04-18 `pll_timer_phase_update_suite` 已确认：已 arm 的 absolute timer 在后续事件把 `next_t` 改成另一个未来时间后，Spectre 会按新的未来目标触发；EVAS 现已覆盖 pull-in 与 push-out 两种情况。 |
| 显式 `t_next = t_next + half_t` 的 DCO phase update | 已对齐 | 2026-04-18 `pll_timer_phase_update_suite` 已确认：运行中只改 `half_t` 不会 retroactively 改动已经 arm 的下一次边沿；新的周期从下一次 reschedule 起生效；EVAS 现已对齐。 |

## 当前回归保护

以下路径已经被纳入 EVAS 单测编译回归：

1. [cmp_ideal.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/comparator/comparator/cmp_ideal.va:44)
2. [dither_adder.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/measurement/gain_extraction/dither_adder.va:32)
3. [gain_amp.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/measurement/gain_extraction/gain_amp.va:49)
4. [flash_adc_3b.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/data-converter/flash_adc_3b/flash_adc_3b.va:47)
5. [adc_ideal_4b.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/data-converter/adc_dac_ideal_4b/adc_ideal_4b.va:43)
6. [nrz_prbs.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/tasks/spec-to-va/voltage/signal-source/nrz_prbs/gold/nrz_prbs.va:43)
7. [test_engine.py](/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/tests/test_engine.py:982)
8. [test_engine.py](/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/tests/test_engine.py:999)
9. [test_engine.py](/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/tests/test_engine.py:1016)

建议后续只要新增 “Spectre 可运行但 EVAS 曾经更严” 的样例，就同步加到这份回归集中。
