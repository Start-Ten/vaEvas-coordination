---
name: Architecture Issue: Hardcoded Checkers
description: Checker 函数硬编码导致扩展性和一致性问题
type: project
---

# Architecture Issue: Hardcoded Checkers in simulate_evas.py

**发现时间**: 2026-04-21
**发现方式**: loop 实验中 `digital_basics_smoke` 失败，`structure_diagnosis` 诊断出 mismatch

## 问题现象

`digital_basics_smoke` 任务失败，原因：

| 检查项 | 期望 | 实际 |
|--------|------|------|
| prompt.md | 生成 4 模块 (AND/OR/NOT/DFF) | ✓ 模型正确理解 |
| TB 生成 | 4 个测试电路 | ✓ 正确生成 |
| CSV 列名 | `a`, `y` (checker 硬编码) | `not_a`, `not_y` (模型生成) |
| Checker | `check_not_gate()` 只查 NOT | ✗ 找不到列，返回 "missing a/y" |

**仿真本身成功** (returncode=0)，但 checker 硬编码的信号命名约定和模型生成的命名不匹配。

## 根因分析

当前架构：

```
tasks/<task_id>/
├── prompt.md        → 给 LLM 的任务描述
├── meta.json        → 任务元数据 (声明 artifacts)
├── checks.yaml      → 声明式检查描述 (如 "gates_truth_table")
└── gold/            → 参考实现

runners/simulate_evas.py:
├── CHECKS = {...}   → 70+ 个硬编码 Python 函数
└── def check_xxx()  → 每个函数硬编码信号名、阈值、逻辑
```

**问题**：

1. **扩展性差**: 3000 行代码，70+ checker 函数，新增任务必须手写 Python
2. **约定隐式**: checker 硬编码 `a`, `y` 等信号名，但 prompt 里没写
3. **三方不一致**: prompt / checks.yaml / checker 容易 drift
4. **不可自动生成**: 新任务无法自动获得 checker

## Why: 为什么变成这样？

历史演进：
- 初期是少量 seed tasks，手写 checker 可接受
- 任务逐渐增加，checker 也跟着增加
- checks.yaml 作为"声明式描述"被引入，但实际验证仍靠硬编码函数
- 没有统一的设计约束，导致 drift

## 2026-04-21 修复进展

### 已完成

1. **新增 4 个单模块任务**:
   - `not_gate_smoke` ✓ PASS
   - `and_gate_smoke` ✓ PASS
   - `or_gate_smoke` ✓ PASS
   - `dff_rst_smoke` ✓ PASS

2. **重写 `digital_basics_smoke` 多模块版本**:
   - 更新 gold TB 测试全部 4 模块
   - 新增 `check_digital_basics_multi` checker
   - 支持 `not_a`, `not_y` 等带前缀信号名

3. **新增 checker 函数**:
   - `check_and_gate`: AND truth table
   - `check_or_gate`: OR truth table
   - `check_dff_rst`: DFF clocked + reset + QB complement
   - `check_digital_basics_multi`: 多模块组合检查

### 闭环验证结果 (2026-04-21)

使用 kimi-k2.5 模型，4 rounds:

| Task | Result | Notes |
|------|--------|-------|
| `digital_basics_smoke` | FAIL | TB 编译失败 (colon-instance syntax) → checker 信号名不匹配 |
| `xor_pd_smoke` | FAIL | conditional transition (违反 skill bundle 规则 12) |
| `cmp_delay_smoke` | FAIL | 编译成功，但 checker 找不到预期信号列 |
| `sample_hold_smoke` | **PASS @ round 3** | ✓ 闭环有效！经过 3 轮反馈后通过 |

**关键发现**：
- `sample_hold_smoke` 成功证明了闭环有效性
- 失败任务主要因为：
  1. 模型违反 skill bundle 规则 (conditional transition)
  2. TB/DUT 信号命名约定不一致
  3. Repair prompt 反馈不够明确

### 待解决

1. **digital_basics_smoke**: gold TB 信号命名需要更明确写入 prompt
2. **xor_pd_smoke**: repair prompt 需要更明确指出 conditional transition 问题
3. **cmp_delay_smoke**: 需要分析 checker 期望的信号名

## 架构问题：这个流程是否合理？

**对比其他 benchmark**：

| Benchmark | Checker 来源 | 扩展方式 |
|-----------|-------------|----------|
| HumanEval | 单元测试 (Python assert) | LLM 可生成 |
| MBPP | 单元测试 | LLM 可生成 |
| VerilogEval | 仿真波形比对 | 需要 reference |
| **vaEvas** | 硬编码 Python 函数 | 必须人工 |

**核心问题**：vaEvas 的 checker 不是"可执行测试"，而是"硬编码验证逻辑"。

## 可能的改进方向

### 方案 A: 声明式 Checker Engine
```yaml
# checks.yaml 增强
checks:
  - type: signal_match
    expected_columns: [a, y]
    tolerance: 0.1
  - type: truth_table
    inputs: [a]
    output: y
    table: [[0, 1], [1, 0]]
```
由通用引擎解析执行，不用手写 Python。

### 方案 B: LLM 生成 Checker
- 根据 task spec + skill 自动生成 checker 函数
- checker 本身也是代码，可以验证
- 类似 HumanEval 的单元测试生成

### 方案 C: Waveform Comparison
- Gold waveform 作为 reference
- 生成的波形与 gold 比对 (NRMSE, correlation)
- 不需要硬编码检查逻辑

### 方案 D: 结构化 Task Spec
- prompt + meta + checks 三合一
- 信号命名约定显式声明
- checker 从 spec 自动派生

## How to apply

1. 短期：修复现有不一致的 tasks (prompt 与 checker 对齐) ✓ 部分完成
2. 中期：引入声明式 checker engine
3. 长期：让 LLM 根据 skill 自动生成 checker 或使用 waveform comparison

---

**相关文件**:
- `runners/simulate_evas.py:2646` (CHECKS dict)
- `tasks/end-to-end/voltage/digital_basics_smoke/`
- `runners/build_repair_prompt.py` (已加入 structure_diagnosis)
- `docs/TABLE2_VERILOGA_SKILL_BUNDLE.md` (规则 11, 12 禁止 conditional transition)