# Case Showcase

更新日期: 2026-04-19

### digital_basics_smoke
- **Family**: end-to-end
- **Circuit type**: digital-logic
- **Why interesting**: 用最小 AND/OR/NOT/DFF 组合快速验证 EVAS 的基础事件调度没有回退。
- **Key check**: 逻辑关系与时钟驱动状态更新是否一致。
- **Gold path**: `tasks/end-to-end/voltage/digital_basics_smoke/gold/`

### dac_therm_16b_smoke
- **Family**: end-to-end
- **Circuit type**: data-converter
- **Why interesting**: 代表 thermometer 风格数据转换器的静态映射和码字单调性。
- **Key check**: 输出 swing 与 thermometer code 对应关系。
- **Gold path**: `tasks/end-to-end/voltage/dac_therm_16b_smoke/gold/`

### comparator_hysteresis_smoke
- **Family**: end-to-end
- **Circuit type**: comparator
- **Why interesting**: 覆盖状态记忆和方向相关翻转，是单阈值 comparator 之外更贴近真实建模的问题。
- **Key check**: 上升/下降扫描下的 trip window 是否分离且稳定。
- **Gold path**: `tasks/end-to-end/voltage/comparator_hysteresis_smoke/gold/`

### pfd_deadzone_smoke
- **Family**: end-to-end
- **Circuit type**: phase-detector
- **Why interesting**: near-deadzone 短脉冲最容易暴露事件抽样和 duty 估算错误。
- **Key check**: 加权 UP duty 和脉冲计数。
- **Gold path**: `tasks/end-to-end/voltage/pfd_deadzone_smoke/gold/`

### adpll_lock_smoke
- **Family**: end-to-end
- **Circuit type**: PLL / clock
- **Why interesting**: 代表基础锁定任务，说明 benchmark 不是只会看开环波形，而是能看闭环行为。
- **Key check**: task-aware lock time 与晚期反馈频率。
- **Gold path**: `tasks/end-to-end/voltage/adpll_lock_smoke/gold/`

### cppll_freq_step_reacquire_smoke
- **Family**: end-to-end
- **Circuit type**: PLL / closed-loop
- **Why interesting**: 这是目前最能主动暴露 EVAS / Spectre 尾部差异的 relock probe，也是对齐审计的代表用例。
- **Key check**: `pll_task_aware` relock 指标与晚期 `lock` 行为。
- **Gold path**: `tasks/end-to-end/voltage/cppll_freq_step_reacquire_smoke/gold/`

### swapped_pfd_outputs_bug
- **Family**: bugfix
- **Circuit type**: phase-detector
- **Why interesting**: 典型“编译能过但行为方向错了”的修复任务，能检查 agent 是否理解 PFD 语义。
- **Key check**: `up` / `dn` 脉冲方向恢复正确。
- **Gold path**: `tasks/bugfix/voltage/swapped_pfd_outputs_bug/gold/`

### gain_step_tb
- **Family**: tb-generation
- **Circuit type**: measurement
- **Why interesting**: 代表测量型 testbench，不要求 `sim_correct`，但要求 bench 可编译、可运行、能产出可消费波形。
- **Key check**: testbench compile 与 transient 生成。
- **Gold path**: `tasks/tb-generation/voltage/gain_step_tb/gold/`
