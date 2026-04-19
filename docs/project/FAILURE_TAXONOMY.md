# Verilog-A Generation Failure Taxonomy

更新日期: 2026-04-19

## F1 — 端口 discipline 不兼容

**症状**

1. Spectre 编译报 discipline / port declaration 相关错误

**触发 case**

1. `spectre_port_discipline`
2. 早期 PLL benchmark seed 中的端口共享写法

**修复策略**

1. 纯电压域模块所有端口使用 `electrical`
2. ANSI inline 端口声明中一行只写一个带 `electrical` 的端口

## F2 — `transition()` 目标值写成不稳定表达式

**症状**

1. DUT 可读性差，易触发 simulator surface 差异
2. benchmark gold 容易出现风格分叉

**触发 case**

1. comparator / gain extraction 历史 gold 改写
2. `cmp_delay_smoke` 早期 gold 风格

**修复策略**

1. 先写离散目标变量，再把该变量传给 `transition()`
2. benchmark gold 与 skill 示例统一采用这种保守写法

## F3 — PRBS / LFSR 初始种子为全零

**症状**

1. PRBS 输出全零
2. 没有状态推进，序列覆盖失效

**触发 case**

1. `prbs7`
2. `nrz_prbs`

**修复策略**

1. 在 `@(initial_step)` 中把 seed 设成非零值，例如 `7'h01`

## F4 — testbench `save` 语句沿用旧式限定符

**症状**

1. Spectre warning 报旧式 `:2e` / `:3f` / `:6f` / `:d`

**触发 case**

1. 早期 gold testbench

**修复策略**

1. 统一移除旧式限定符，仅保留 `save <signal>`
2. 用 `tests/test_save_statements.py` 防回归

## F5 — PLL 使用 generic parity 导致误判

**症状**

1. 主行为已经闭环，但 generic waveform parity 仍报 failed

**触发 case**

1. `adpll_lock_smoke`
2. `cppll_tracking_smoke`
3. `cppll_freq_step_reacquire_smoke`

**修复策略**

1. PLL / clock 类任务使用 `pll_task_aware` parity
2. 检查 `relock_time`、`lock` 状态、UP / DN 方向、`vctrl` 趋势，而不是逐点波形误差

## F6 — 短脉冲 duty 被自适应步长放大

**症状**

1. near-deadzone PFD 的短脉冲被误判为大占空比

**触发 case**

1. `pfd_deadzone_smoke`

**修复策略**

1. 行为检查按时间加权，而不是按采样点比例估 duty

## F7 — gold DUT 自身不满足当前 benchmark authoring 规则

**症状**

1. benchmark 接线完成后仍卡在 DUT compile

**触发 case**

1. `cmp_delay_smoke` 早期版本

**修复策略**

1. gold DUT 也遵守同一套电压域 / transition / include / save 风格规则
2. 新任务接入时走 authoring checklist
