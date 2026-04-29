# Benchmark-v2 Promotion Candidates

日期：2026-04-29

本文档用于人工审核：哪些 benchmark-v2 任务适合提升为主 benchmark 的新增任务。

当前原则是：先不修改原始 92 个任务，只列候选。审核通过后，再执行显式 promotion，把对应任务复制到正式 `behavioral-veriloga-eval/tasks/` 树中。

## 选择标准

候选任务需要同时满足：

1. gold 已通过 EVAS 和真实 Spectre 验证；
2. 不是原 92 的简单改名或简单参数扰动；
3. prompt 没有泄漏 gold 实现；
4. checker 能检查明确行为，而不是只检查文件存在；
5. 对论文叙事有帮助，能说明 benchmark 覆盖了更广的 Verilog-A 行为机制。

## 主推候选：4 个

这 4 个是当前最适合加入主 benchmark 的第一批候选。每个任务代表一种原始 92 中没有被干净覆盖的新功能机制。

主 benchmark 应保持精简，所以每个功能机制只选一个代表版本。端口改名、同机制多变体、参数扰动都保留在 benchmark-v2 中做泛化评估。

| priority | task id | family | 来源 | 推荐理由 | 审核建议 |
|---:|---|---|---|---|---|
| 1 | `v2_ext_threshold_detector_000` | threshold detector | external architecture | 新增阈值检测器，结构清晰，是比较器/传感器接口类任务的基础版本。 | 建议加入 |
| 2 | `v2_ext_window_detector_000` | window detector | external architecture | 新增窗口检测器，要求 inside/below/above 多输出互斥一致。 | 建议加入 |
| 3 | `v2_ext_limiter_model_000` | analog limiter | external architecture | 新增模拟限幅器，能区分 bounded transfer 和 raw follower。 | 建议加入 |
| 4 | `v2_ext_pulse_stretcher_000` | event pulse stretcher | external architecture | 新增事件触发脉冲展宽，覆盖边沿检测、保持窗口、自动回落。 | 建议加入 |

## 备选候选：10 个

这些任务也有价值，但不建议放进第一批精简主 benchmark。

| task id | family | 推荐理由 | 暂缓原因 |
|---|---|---|---|
| `v2_ext_threshold_detector_007` | threshold detector | 与 000 同机制但换成 `sensor_reading/trip_flag`，可测试端口语义泛化。 | 更适合留在 benchmark-v2 做泛化压力测试。 |
| `v2_ext_window_detector_007` | window detector | 与 000 同机制但输入名换成 `measured_voltage`。 | 更适合留在 benchmark-v2 做泛化压力测试。 |
| `v2_ext_limiter_model_007` | analog limiter | 与 000 同机制但端口换成 `unbounded_signal/clamped_level`。 | 更适合留在 benchmark-v2 做泛化压力测试。 |
| `v2_ext_pulse_stretcher_007` | event pulse stretcher | 与 000 同机制但端口换成 `trigger_level/pulse_out`。 | 更适合留在 benchmark-v2 做泛化压力测试。 |
| `v2_adc_dac_calibrated_chain_settled` | ADC-DAC plus calibration | 把量化重构和校准 settled flag 放到一个任务里，能测试系统级约束。 | 原 92 已有 ADC/DAC/SAR 任务，可作为二阶段系统组合扩展。 |
| `v2_dwa_segmented_dac_glitch` | DWA plus segmented DAC | 把 DWA 指针轮转和模拟输出毛刺约束绑定起来。 | 原 92 已有 DWA 和 DAC 任务，可作为二阶段系统组合扩展。 |
| `v2_pfd_lock_detector_composed` | PFD plus lock detector | 在 UP/DN pulse 外加入 lock-window 的时间聚合约束。 | 原 92 已有 PFD/PLL 任务，可作为二阶段系统组合扩展。 |
| `v2_sample_hold_calibration_settled` | sample-hold plus calibration | 采样保持后接 offset search 和 settled 判定。 | 原 92 已有 sample-hold 和 calibration 任务，可作为二阶段系统组合扩展。 |
| `v2_binary_dac_segmented_glitch_guard` | binary DAC with segment guard | 覆盖 binary coarse bits 与 unit-cell segment 的混合 DAC。 | 原 92 已有 DAC/glitch 相关任务，第一批可先少放。 |
| `v2_divider_pfd_feedback_stub` | divider plus event feedback | 覆盖分频器和事件比较器之间的系统关系。 | 与 PLL/PFD 任务相关，建议等 PFD 组合任务审核后再放。 |

## 不建议直接加入主 benchmark 的内容

以下类型更适合留在 benchmark-v2 做泛化评估，而不是提升进主 92：

1. 大量 `v2-seed-perturbation-r2` 参数扰动任务；
2. 大量 `v2-hard-negative-r1` 负约束陷阱任务；
3. 同一 external architecture 的第 3 个以后变体；
4. 只改变端口名、位宽或阈值参数，但机制没有变化的任务。

原因是主 benchmark 应该保持机制覆盖面，benchmark-v2 才负责规模化扰动和泛化压力测试。

## 审核后操作

如果以上 4 个通过审核，下一步建议：

1. 新建 promotion manifest，记录从 `benchmark-v2/tasks/<task_id>` 到正式任务树的映射；
2. 执行复制，不手改 gold/checker；
3. 对 promotion 后的新正式任务重跑 EVAS gold；
4. 抽样或全量跑 Spectre gold；
5. 在论文中把它们标记为 expanded official benchmark，而不是原始 92。
