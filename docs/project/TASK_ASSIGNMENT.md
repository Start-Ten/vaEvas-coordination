# vaEvas 任务分工表

更新日期: 2026-04-17

---

## 当前状态概览

### end-to-end 任务 (双验证)

| 状态 | 数量 | 说明 |
|------|------|------|
| 已验证通过 | 22 | EVAS + Spectre 双验证成功 (含本次修复2个) |
| Spectre兼容问题 | 1 | adpll_lock_smoke (vctrl_mon idtmod问题,已记录) |

### spec-to-va 任务

| 状态 | 数量 | 说明 |
|------|------|------|
| 已通过 | 5 | shenbufan提交，待合并到main |
| 待创建gold | 8 | liangyuxuan负责 |
| 待创建gold | 2 | team公共任务 |

### bugfix 任务

| 状态 | 数量 | 说明 |
|------|------|------|
| 待运行验证 | 2 | shenbufan提交，gold文件在fix/pr2-review分支 |
| 待创建gold | 2 | team公共任务 |

### tb-generation 任务

| 状态 | 数量 | 说明 |
|------|------|------|
| 待创建gold | 4 | liangyuxuan负责 |

---

## 详细分工

### liangyuxuan 负责的任务 (共14个)

#### spec-to-va (10个)

| 任务名 | 类别 | 状态 | 优先级 | 备注 |
|--------|------|------|--------|------|
| sar_logic | adc-sar | pending | 高 | SAR逻辑控制器 |
| sar_12bit | adc-sar | pending | 高 | 12位SAR ADC |
| d2b_4bit | adc-sar | pending | 高 | 4位DAC转二进制 |
| pipeline_stage | adc-sar | pending | 中 | Pipeline ADC级 |
| segmented_dac | dac | pending | 中 | 分段DAC |
| cdac_cal | dac | pending | 中 | CDAC校准 |

**需要完成的工作:**
1. 创建 `gold/dut.va` 参考答案
2. 编写自动化检查函数 (simulate_evas.py)
3. 运行EVAS验证
4. 回填BENCHMARK_RESULT_TABLE.md

#### tb-generation (4个)

| 任务名 | 状态 | 优先级 | 备注 |
|--------|------|--------|------|
| clk_div_min_tb | pending | 中 | 时钟分频器最小测试 |
| comparator_offset_tb | pending | 中 | 比较器偏移测试 |
| dac_ramp_tb | pending | 低 | DAC斜坡测试 |
| inl_dnl_probe | pending | 低 | INL/DNL探针 |

**需要完成的工作:**
1. 创建 `gold/tb_*.scs` 参考testbench
2. 运行EVAS验证
3. 回填BENCHMARK_RESULT_TABLE.md

---

### shenbufan 负责的任务 (共7个)

#### 已完成的spec-to-va (5个) - 待合并

| 任务名 | 类别 | 当前状态 | 备注 |
|--------|------|----------|------|
| clk_divider | digital-logic | passed | origin/pr-2分支 |
| prbs7 | digital-logic | passed | origin/pr-2分支 |
| therm2bin | digital-logic | passed | origin/pr-2分支 |
| bbpd | pll-clock | passed | origin/pr-2分支 |
| multimod_divider | pll-clock | passed | origin/pr-2分支 |

**需要完成的工作:**
1. 将pr-2分支合并到main
2. 更新BENCHMARK_RESULT_TABLE.md的pr_link字段

#### bugfix (2个) - 待验证

| 任务名 | bug类型 | gold文件位置 | 备注 |
|--------|---------|--------------|------|
| bad_bus_output_loop | 向量赋值错误 | fix/pr2-review分支 | 已有gold，需运行验证 |
| missing_transition_outputs | 缺少transition() | fix/pr2-review分支 | 已有gold，需运行验证 |

**需要完成的工作:**
1. 切换到fix/pr2-review分支
2. 运行EVAS验证
3. 回填BENCHMARK_RESULT_TABLE.md

---

### team 公共任务 (共4个)

#### spec-to-va (2个)

| 任务名 | 类别 | 状态 | 备注 |
|--------|------|------|------|
| sc_integrator | amplifier-filter | pending | 开关电容积分器 |
| bg_cal | calibration | pending | 后台校准 |

#### bugfix (2个)

| 任务名 | bug类型 | 状态 | 备注 |
|--------|---------|------|------|
| mixed_domain_cdac_bug | I()<+与电压域混用 | pending | 需创建gold dut_fixed.va |
| spectre_port_discipline | inout端口共享问题 | pending | 需创建gold dut_fixed.va |

---

## 本次会话完成的工作

### 修复的2个阻塞任务 (2026-04-17 深夜)

| 任务 | 问题 | 修复方案 | 结果 |
|------|------|----------|------|
| `sar_adc_dac_weighted_8b_smoke` | Spectre unique_codes=32 < 阈值48 | fin 1MHz→100kHz, stop 5us→10us | PASS, max_nrmse=0.006 |
| `serializer_8b_smoke` | behavior check采样时机+LOAD/CLK竞争 | LOAD width 15n→12.5n, check wait 1ns | PASS, max_nrmse=0.02 |

### 根因分析

**sar_adc**: 高频正弦(1MHz)+低采样率(50MHz)导致每周期样本少，跳过大量code区域

**serializer**:
1. transition()需要~100ps完成，检查函数采样过早
2. LOAD fall与CLK rise在t=20ns同时发生(竞争条件)

### 提交记录

- `91eeecb` fix: serializer_8b_smoke dual-validation parity closure
- `5dabc0d` fix: sar_adc_dac_weighted_8b Spectre coverage + serializer check delay

### 新验证的任务

- lfsr_smoke ✅
- clk_burst_gen_smoke ✅
- digital_basics_smoke ✅
- gain_extraction_smoke ✅

### 代码改动

- `sar_adc_weighted_8b.va`: for循环→显式逐位操作
- `simulate_evas.py`: 行为检查改进
- `run_gold_dual_suite.py`: infer_digital容差调整

---

## 优先级建议

### 高优先级 (本周)

1. shenbufan: 合并pr-2分支，运行bugfix验证
2. liangyuxuan: 创建sar_logic, sar_12bit, d2b_4bit的gold文件

### 中优先级 (下周)

1. liangyuxuan: 完成其余spec-to-va任务
2. team: 创建sc_integrator, bg_cal的gold文件

### 低优先级

1. tb-generation任务
2. bugfix公共任务
3. 分支清理和合并

---

## 远程服务器目录结构

```
/home/jinzhihong/aiProject/evas/
├── behavioral-veriloga-eval/   # 项目代码克隆
└── results/                    # 仿真结果存储
```

virtuoso-bridge临时文件位于: `/tmp/virtuoso_bridge_jinzhihong/`