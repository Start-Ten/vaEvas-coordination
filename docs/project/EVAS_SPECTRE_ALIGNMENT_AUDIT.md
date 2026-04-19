# EVAS Spectre Alignment Audit

更新日期: 2026-04-19

## 1. 目标

这份文档专门记录一类很容易被混淆的问题:

1. benchmark 失败或修复
2. benchmark/testbench 工程清理
3. EVAS 与 Virtuoso/Spectre 的语义或可接受建模表面不一致

配套候选清单见：

1. [EVAS_TRANSITION_COMPATIBILITY_INVENTORY.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/project/EVAS_TRANSITION_COMPATIBILITY_INVENTORY.md)

项目原则应当是：

1. 如果差异来自 benchmark 资产自身写法、旧语法或检查脚本，就修 benchmark。
2. 如果差异来自 EVAS 对 Spectre 已接受行为的额外限制，就优先修 EVAS，让它更接近 Virtuoso/Spectre。

## 2. 当前结论

不是“以前所有 benchmark 都是 EVAS 和 Virtuoso 不一致”。

从现有结果表、例子库和历史 gold 改写来看，历史问题大致分成四类：

1. `EVAS` 过严的编译/语义限制
2. benchmark / gold testbench 的 Spectre 兼容性清理
3. parity 指标或 runner 层面的对齐问题
4. 任务本身的 testbench/激励设置问题

只有第一类应当直接归到 “修 EVAS 让它向 Virtuoso 靠齐”。

## 3. 已识别的 mismatch 分类

### 3.1 EVAS 过严的 `transition()` 目标限制

这类问题已经在仓库里留下了明确证据。

#### 已有本地证据

1. [cmp_ideal.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/comparator/comparator/cmp_ideal.va:44)
   使用 `transition(vdd * xoutp, ...)` 这类 rail scaling。
2. [dither_adder.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/measurement/gain_extraction/dither_adder.va:32)
   使用 `transition(V(VRES_P) + dither_diff * 0.5, 0)`。
3. [gain_amp.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/examples/measurement/gain_extraction/gain_amp.va:49)
   使用 `transition(vth + vout_diff * 0.5, 0)`。
4. [nrz_prbs.va](/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/tasks/spec-to-va/voltage/signal-source/nrz_prbs/gold/nrz_prbs.va:43)
   使用 `transition(vcm + 0.5 * amp * level, ...)`。

#### 历史上怎么处理

1. comparator 路径曾通过重写 gold，把连续 rail scaling 挪到 `transition()` 外面来绕过 EVAS。
2. gain extraction 的 gold `dither_adder` 也曾直接改成非 `transition()` 贡献，理由就是 “EVAS-compatible”。

这说明过去确实存在 “为了过 EVAS，只能改 benchmark/gold 写法” 的情况。

#### 本轮处理

1. 已先前支持 `transition(vdd * bit_state, ...)` 一类放缩形式。
2. 已去掉 EVAS 对 continuous-target `transition()` 的编译期拦截，因为本地 Spectre 运行记录已经证明这类写法在 Virtuoso/Spectre 下可编译可运行。
3. 已放开 conditional `transition()` 的编译限制；本地 Spectre 已证明原始 `adc_ideal_4b.va` 虽会报 `VACOMP-1116` warning，但能成功编译并完成 transient。

### 3.2 Spectre 旧语法 / bench hygiene 问题

这些不是 EVAS 核心语义 mismatch，而是 benchmark 资产需要清理。

典型例子：

1. 旧式 `save vin:3f clk:2e ...` 限定符导致 Spectre warning。
2. PWL 续行、token 数、换行格式不稳。

这类问题已经通过：

1. `tests/test_save_statements.py`
2. `tests/test_pwl_statements.py`

来防回归，应该继续保持在 benchmark/tooling 层解决。

### 3.3 parity 指标 / runner 对齐问题

这类不是 DUT 语义不一致，而是比较方式需要任务感知。

典型例子：

1. PLL 的 `vctrl_mon` 在某些 Spectre `idtmod` 路径里保持 0 V，因此只能作为 informational monitor。
2. `cppll_tracking_smoke` 里 free-running `dco_clk` 的相位不能直接作为逐点 parity 核心指标。

这类问题应该修 runner 和 parity metric，而不是硬改 EVAS 波形去迎合错误指标。

### 3.4 testbench / 激励设置问题

这类问题也不是 EVAS 核心不一致。

典型例子：

1. SAR 输入频率/仿真时长设置不当，导致码字覆盖不足。
2. XOR phase detector 的延迟参数不是真 90 度相移。

这类应继续在 benchmark case 和 reference testbench 上修。

## 4. 当前仍然分开的事项

### 已有充分证据，应该继续向 EVAS 收敛

1. 历史上因 EVAS 过严而改写的 gold/example 资产回看
2. 把“Spectre 可运行但带 warning”的 `transition()` 例子固化为 EVAS 回归集

### 已验证应保持限制

1. `idtmod()` 位于 `if/case` 条件语句内的限制
2. `cross()` 位于 `if/case` 条件语句内的限制
3. `above()` 位于 `if/case` 条件语句内的限制

2026-04-18 的本地 probe 已补齐这条证据链：

1. EVAS 当前会在编译期拒绝该写法。
2. 若仅本地放开 compile guard，EVAS 运行时会表现为 hidden-state `catch_up_accumulate`。
3. Spectre 在同一最小用例上直接报 fatal error `VACOMP-2154`，明确不支持 “`idtmod` embedded in a conditionally-executed statement or in an expression”，见 [spectre.out](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/experiments/conditional_idtmod/output/spectre/spectre.out:77) 与 [probe_report.json](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/experiments/conditional_idtmod/output/probe_report.json)。

因此，这一项现在不应再被描述为“缺少 Spectre 结论”，而应被描述为：

1. EVAS 当前限制与 Spectre 一致；
2. 不应为了“向 Virtuoso 靠齐”而放开；
3. 真正可做的是把这条证据固化进文档和后续回归审计。

同日的 conditional operator suite 还补齐了另外两条本地 Spectre 证据：

1. Spectre 对 conditional `cross()` 直接报 fatal `VACOMP-2146`，见 [suite_report.json](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/experiments/conditional_operator_suite/output/suite_report.json) 与 [spectre.out](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/experiments/conditional_operator_suite/output/conditional_cross_late_enable/spectre/spectre.out:73)。
2. Spectre 对 conditional `above()` 直接报 fatal `VACOMP-2148`，见 [suite_report.json](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/experiments/conditional_operator_suite/output/suite_report.json) 与 [spectre.out](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/experiments/conditional_operator_suite/output/conditional_above_late_enable/spectre/spectre.out:73)。
3. EVAS 已同步补上编译期限制，使这两类 conditional event operator 现在也与 Spectre 的接受面保持一致。

### 仍需单独验证后再动

1. 其他 analog operator 的 conditional hidden-state 语义

`conditional timer()` 这条线在 2026-04-18 又补齐了一轮更细的结论：

1. 对 conditional absolute `timer(next_t)`，Spectre 在两个最小 probe 上都表现为 “no catch-up”：
   - 首次使能已经晚于目标时间，不补触发；
   - 先前已 arm、但在 disable 窗口内错过目标时间，重新使能后也不补触发。
2. 对 conditional periodic `timer(start, period)`，Spectre 在新增 probe 上表现为：
   - 不补触发已经错过的周期点；
   - 保留原始相位；
   - 在重新进入 active window 后，从第一个未来周期点继续触发。
3. EVAS 已在同一 probe 上对齐到相同行为，见 [suite_report.json](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/experiments/conditional_operator_suite/output/suite_report.json)。
4. 进一步的独立 probe `timer() -> transition() -> cross()` 也已完成一轮同日修正：EVAS 现在会在同一时刻 contributions 更新后补做一次 cross/above 后检查，并仅重放非 event 的赋值/贡献逻辑，因此粗步长单测里的 crossing time 已从 12ns 拉回到与 Spectre 一致的 11ns，见 [2026-04-18_timer-transition-cross-audit.md](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/logs/2026-04-18_timer-transition-cross-audit.md)。
5. 同日新增的 PLL 风格 phase-update suite 又补齐了两条更贴近真实 DCO/PLL authoring 的结论，见 [suite_report.json](/Users/bucketsran/Documents/TsingProject/vaEvas/worksche/experiments/pll_timer_phase_update_suite/output/suite_report.json)：
   - 对已经 arm 的 absolute `timer(next_t)`，若后续事件把 `next_t` 改成另一个未来绝对时间，不论是 pull-in 到更早的未来点，还是 push-out 到更晚的未来点，Spectre 都会按新的目标时间触发；EVAS 现已对齐。
   - 对显式 `t_next = t_next + half_t` 的 DCO 写法，运行中只修改 `half_t` 不会 retroactively 挪动已经 arm 的下一次边沿；新的半周期从下一次 reschedule 开始生效；EVAS 现已对齐。
6. 因此，conditional `timer()` 的 absolute / periodic 两条主线、`timer() -> transition() -> cross()` 这条独立边界路径，以及 PLL 风格 absolute-timer / explicit-`t_next` 相位更新语义，目前都不再是 open mismatch；当前剩下的是其他 hidden-state operator 的 Spectre 证据与语义审计。

## 5. 推荐后续动作

1. 用现有 examples/tasks 做一轮 `transition()` compatibility inventory，列出哪些 gold 只是为了绕开旧 EVAS 限制而改写。
2. 对有 Spectre 运行证据的原始写法，持续补 EVAS regression tests，避免以后再次回退到“只好改 gold”。
3. 优先回看 `gain_extraction`、`adc_dac_ideal_4b`、comparator 这几条历史 workaround 最多的路径。
4. 在 benchmark/README/skills 中明确：
   “优先让 EVAS 向 Spectre 靠齐；只有在 benchmark 资产本身不规范时才改 benchmark。”
5. 对 `conditional idtmod()`，后续只需保留“Spectre 对齐的禁止项”说明，不再把它当作待放开的 EVAS 兼容 backlog。
6. 后续 timer 相关工作不再是基础对齐，而是继续扩展 probe 覆盖面，例如更复杂的 PLL lock/relock、divider-ratio hop、pulse-overlap、以及更多 hidden-state operator 审计。

## 6. 新增记录：`cppll_freq_step_reacquire_smoke` 尾部差异

这条记录单独归到 alignment audit，而不是 benchmark blocker。

### 6.1 当前结论

1. benchmark 口径下，这条 case 已通过正式双跑，结果位于 `behavioral-veriloga-eval/results/gold-dual-suite-cppll-initial-step-fix-v2/`。
2. 任务感知 parity 已闭环：
   - `relock_time_delta_s = 8.04e-11`
   - `pre_lock_time_delta_s = 6.72e-11`
   - `late_fb_freq_rel_delta = 5.07e-4`
   - `late_vctrl_mean_delta_v = 1.81mV`
3. 但波形级尾差异仍存在，主要集中在晚期 `lock` 脉冲。

### 6.2 仍需审计的点

1. EVAS 晚期第 5 个 `lock` 上升沿约早于 Spectre `19.5ns`
2. EVAS 晚期第 6 个 `lock` 上升沿约早于 Spectre `39ns`
3. 当前判断这更像 `lock_streak + lock_tol` 的边界样本敏感性，而不是主 relock 行为没有闭环

### 6.3 后续建议

1. 对 PLL 类任务单独区分“benchmark parity 已闭环”和“waveform-perfect tail alignment 未闭环”
2. 优先审计 `t_fb_last`、`phase_err`、`lock_streak` 是否完全基于内部离散状态更新
3. 不要为这条尾差异去改 benchmark gold DUT；若后续继续修，优先修 EVAS 内核或 runner 解释层
