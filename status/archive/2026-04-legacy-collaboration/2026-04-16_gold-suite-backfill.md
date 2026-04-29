# Gold Suite Backfill + Dual Validation — 2026-04-16

## 背景

`behavioral-veriloga-eval` 里已有 13 个 end-to-end voltage task 补上了 `gold/` DUT 与 testbench。

今天先完成两步证据回填：

1. 本地 EVAS gold suite 批量可执行
2. 基于 Spectre 的联合验证批量落地

其中第 2 步不是沿用旧的 `sshConnect/virtuoso-bridge-lite` 路径，而是改用当前仓库里实际可用的：

1. `iccad/virtuoso-bridge-lite`

同时显式补上远端 Cadence 环境脚本：

1. `VB_CADENCE_CSHRC=/home/cshrc/.cshrc.cadence.IC618SP201`

## 本次动作

仓库：

1. `vaEvas/behavioral-veriloga-eval`
2. `vaEvas/coordination`

新增/使用：

1. `runners/run_gold_suite.py`
2. `runners/run_gold_dual_suite.py`
3. `results/gold-suite/summary.json`
4. `results/gold-dual-suite-final/summary.json`

执行命令：

1. `python3 runners/run_gold_suite.py`
2. `python3 runners/run_gold_dual_suite.py --bridge-repo /Users/bucketsran/Documents/TsingProject/iccad/virtuoso-bridge-lite --cadence-cshrc /home/cshrc/.cshrc.cadence.IC618SP201 --output-root results/gold-dual-suite-final`

## EVAS-only 结果

13 个带 `gold/` 目录的 task 全部 `PASS`，结果汇总在：

1. `behavioral-veriloga-eval/results/gold-suite/summary.json`

这一步只说明 EVAS 侧 gold 资产可执行，不足以单独提升到 `verified/passed`。

## 联合验证结果

最终以：

1. `behavioral-veriloga-eval/results/gold-dual-suite-final/summary.json`

为准。

统计：

1. `tasks_total = 13`
2. `pass_count = 9`
3. `fail_count = 4`

### 已 dual-pass 的 9 个 task

1. `dac_binary_clk_4b_smoke`
2. `dac_therm_16b_smoke`
3. `dwa_ptr_gen_smoke`
4. `flash_adc_3b_smoke`
5. `gray_counter_4b_smoke`
6. `mux_4to1_smoke`
7. `noise_gen_smoke`
8. `pfd_updn_smoke`
9. `sample_hold_smoke`

### 仍 blocked / failed 的 4 个 task

1. `adc_dac_ideal_4b_smoke`
   - EVAS pass，Spectre behavior 可过，但 `dout_*` parity 偏差大
   - `p95_nrmse = max_nrmse = 0.5587`
2. `sar_adc_dac_weighted_8b_smoke`
   - EVAS pass，Spectre behavior 未对齐
   - `unique_codes=25 avg_abs_err=0.0045`
3. `serializer_8b_smoke`
   - 两边都能满足“0xA5 serialize”行为检查，但 `sout` 波形 parity 仍偏大
   - `p95_nrmse = max_nrmse = 0.4825`
4. `xor_pd_smoke`
   - EVAS pass，Spectre 侧 `pd_out` 占空比约 `0.284`
   - 当前 testbench 注释写“2.5ns = 90-degree”，但对 20ns 周期实际更接近 45-degree，需要后续统一口径

## 兼容性修补

为跑通联合验证，本次顺手补了几处 Spectre 兼容性问题：

1. `serializer_8b` 的 `%x` strobe 之前已改为十进制输出
2. `gray_counter_4b` 的 `%x` strobe 也改为十进制输出
3. `simulate_evas.py` 中的 checker 补了：
   - ADC/SAR 无 `dout_code` 时按 `dout_*` 位线重构
   - `serializer_8b` 同时接受 `LOAD` 后首位立即可见与“从下一拍开始移位”两种合法时序
4. `run_gold_dual_suite.py` 统一负责：
   - EVAS 运行
   - Spectre 运行
   - `tran_spectre.csv` 导出
   - 同一行为检查
   - 波形 parity 摘要

## 已回填到 coordination 的内容

文件：

1. `docs/benchmark/BENCHMARK_RESULT_TABLE.md`
2. onboarding 里若干仍指向 `sshConnect/virtuoso-bridge-lite` 的路径说明

回填口径：

1. dual-pass 的 9 个 task 提升到 `tier=verified`、`verification_status=passed`
2. 未通过的 4 个 task 记为 `verification_status=failed`
3. 非 PLL task 的 `evas_fb_hz/spectre_fb_hz/ppm_cross_delta/lock_time_delta_s` 继续记 `N/A`
4. `parity_status` 改为：
   - `dual-validated`：联合验证通过
   - `needs-review`：行为过但 parity 偏差大
   - `behavior-mismatch`：Spectre 行为检查未过
5. `result_path` 统一指向 `behavioral-veriloga-eval/results/gold-dual-suite-final/<task>`

## 结论

这批 task 不再是“只有 EVAS 本地证据”的状态了。

截至 2026-04-16：

1. 13 个 gold task 中已有 9 个完成 EVAS + Spectre 联合验证
2. 4 个 task 暂时不应提升到 formal benchmark 口径
3. `xor_pd_smoke` 暴露了 EVAS 与 testbench 相位语义之间的真实分歧，值得后续单独排查
4. `adc_dac_ideal_4b_smoke`、`serializer_8b_smoke` 更像 parity 仍未闭合，而不是简单的“跑不起来”
