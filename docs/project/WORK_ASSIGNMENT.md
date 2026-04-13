# Work Assignment

这份文件是当前阶段最直接的任务分配单。

目的：

1. 让每个人知道自己先做什么
2. 避免重复劳动
3. 保证 benchmark 四个任务族都有覆盖、结果表、PR 三件事一起推进

如果你只想知道"我现在该做哪个 case"，优先看这份文件。

## 开始前先确认一件事

这份分工单记录的是“当前阶段应该做的任务”，不是“保证已经全部进入你本地 `upstream/main` 的任务”。

如果你在这里看到了某个 case，但自己本地的 `behavioral-veriloga-eval` 看不到对应目录：

1. 先不要默认自己拉错仓库
2. 先看 [REPOSITORIES.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/project/REPOSITORIES.md)
3. 再看 [2026-04-12_repo-visibility-note.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/status/2026-04-12_repo-visibility-note.md)
4. 先确认当前 remote / branch，再继续执行任务

---

## 执行回填最小要求（三件套）

每位同学每次声称“任务已推进”，都必须同步三项证据：

1. `branch + commit`：明确写出分支名与至少一个可检索 commit
2. `result_path`：给出可复核的结果路径（本地相对路径或仓库相对路径）
3. `table_row_update`：在 `coordination/docs/benchmark/BENCHMARK_RESULT_TABLE.md` 中更新对应行

判定规则：

1. 三件套未齐，不计入“已完成”或“可验收”
2. 仅有代码提交但未回填结果表，计入“进行中”
3. 仅有结果截图但无 commit / path，计入“证据不足”

---

## 0. benchmark 四个任务族说明

vaEvas benchmark 分四个任务族（task families），测试 AI 模型的不同能力：

| 任务族 | 考的是什么 | AI 输入 | AI 输出 | 主要验收标准 |
|---|---|---|---|---|
| `end-to-end` | 全链路：从规格写出 DUT + TB + 跑通仿真 | 自然语言规格 | `.va` + `.scs` | compile + sim_correct + EVAS↔Spectre parity |
| `spec-to-va` | 从规格写出 DUT | 自然语言规格 | `.va` | compile + 行为是否符合规格 |
| `bugfix` | 修复有 bug 的 `.va` | 含 bug 的 `.va` | 修正后的 `.va` | compile + bug 是否实际修复 |
| `tb-generation` | 给已知 DUT 写 testbench | DUT `.va` + 意图描述 | `.scs` | TB compile + 能产生波形 |

**两位同学的任务覆盖全部四族**，不只是 end-to-end。

---

## 1. 当前分工原则

1. 每个任务族都需要：① 参考答案（gold）② 自动化 `sim_correct` check ③ EVAS 验收
2. end-to-end 任务额外需要：EVAS + Spectre/Virtuoso 双验证（parity）
3. 每个人的任务都必须以 `结果表 + benchmark seed + PR` 结束

---

## 2. shenbufan — digital-logic / phase-detector / pll 方向

### A. End-to-end parity（优先级最高）

对以下任务运行 EVAS + Spectre，完成 parity 验证，填 BENCHMARK_RESULT_TABLE：

| 任务 | 路径 |
|---|---|
| `lfsr_smoke` | `tasks/end-to-end/voltage/lfsr_smoke` |
| `clk_burst_gen_smoke` | `tasks/end-to-end/voltage/clk_burst_gen_smoke` |
| `digital_basics_smoke` | `tasks/end-to-end/voltage/digital_basics_smoke` |
| `gray_counter_4b_smoke` | `tasks/end-to-end/voltage/gray_counter_4b_smoke` |
| `mux_4to1_smoke` | `tasks/end-to-end/voltage/mux_4to1_smoke` |
| `xor_pd_smoke` | `tasks/end-to-end/voltage/xor_pd_smoke` |
| `pfd_updn_smoke` | `tasks/end-to-end/voltage/pfd_updn_smoke` |

### B. Spec-to-va gold answers（次优先）

以下任务目前只有 `prompt.md`，`sim_correct` 是占位符 `manual_review_expected_output`。需要：
1. 写出参考 `.va`（gold solution）
2. 将 `checks.yaml` 中的 `manual_review_expected_output` 替换为可执行的行为检查

| 任务 | 路径 |
|---|---|
| `clk_divider` | `tasks/spec-to-va/voltage/digital-logic/clk_divider` |
| `prbs7` | `tasks/spec-to-va/voltage/digital-logic/prbs7` |
| `therm2bin` | `tasks/spec-to-va/voltage/digital-logic/therm2bin` |
| `bbpd` | `tasks/spec-to-va/voltage/pll-clock/bbpd` |
| `multimod_divider` | `tasks/spec-to-va/voltage/pll-clock/multimod_divider` |

### C. Bugfix 验收

确认以下 bugfix 任务有正确的 gold fix，并在 EVAS 上验证修复后代码能通过行为检查：

| 任务 | 已知 bug 类型 |
|---|---|
| `bad_bus_output_loop` | 向量总线赋值用了 `V(DOUT) <+` 而非 `V(DOUT[i]) <+` |
| `missing_transition_outputs` | 输出端口缺少 `transition()` 包装 |

### 最低目标

1. end-to-end：至少 3 个 parity 验证完成
2. spec-to-va：至少 2 个 gold answer + 自动化 check 写完
3. bugfix：2 个 gold fix 确认
4. 填 BENCHMARK_RESULT_TABLE（end-to-end 部分）和 SPEC_TO_VA_RESULT_TABLE
5. 提 1 个 PR（可合并多族内容）

---

## 3. liangyuxuan — data-converter / calibration / comms / sample-hold 方向

### A. End-to-end parity（优先级最高）

| 任务 | 路径 |
|---|---|
| `dac_binary_clk_4b_smoke` | `tasks/end-to-end/voltage/dac_binary_clk_4b_smoke` |
| `adc_dac_ideal_4b_smoke` | `tasks/end-to-end/voltage/adc_dac_ideal_4b_smoke` |
| `dwa_ptr_gen_smoke` | `tasks/end-to-end/voltage/dwa_ptr_gen_smoke` |
| `noise_gen_smoke` | `tasks/end-to-end/voltage/noise_gen_smoke` |
| `dac_therm_16b_smoke` | `tasks/end-to-end/voltage/dac_therm_16b_smoke` |
| `sar_adc_dac_weighted_8b_smoke` | `tasks/end-to-end/voltage/sar_adc_dac_weighted_8b_smoke` |
| `sample_hold_smoke` | `tasks/end-to-end/voltage/sample_hold_smoke` |
| `flash_adc_3b_smoke` | `tasks/end-to-end/voltage/flash_adc_3b_smoke` |
| `serializer_8b_smoke` | `tasks/end-to-end/voltage/serializer_8b_smoke` |

### B. Spec-to-va gold answers（次优先）

| 任务 | 路径 |
|---|---|
| `sar_logic` | `tasks/spec-to-va/voltage/adc-sar/sar_logic` |
| `sar_12bit` | `tasks/spec-to-va/voltage/adc-sar/sar_12bit` |
| `d2b_4bit` | `tasks/spec-to-va/voltage/adc-sar/d2b_4bit` |
| `pipeline_stage` | `tasks/spec-to-va/voltage/adc-sar/pipeline_stage` |
| `segmented_dac` | `tasks/spec-to-va/voltage/dac/segmented_dac` |
| `cdac_cal` | `tasks/spec-to-va/voltage/dac/cdac_cal` |

### C. TB-generation 验收

确认以下任务生成的 `.scs` 能在 EVAS 上编译并产生波形，写 gold `.scs` 参考答案：

| 任务 | 路径 |
|---|---|
| `clk_div_min_tb` | `tasks/tb-generation/voltage/clk_div_min_tb` |
| `comparator_offset_tb` | `tasks/tb-generation/voltage/comparator_offset_tb` |
| `dac_ramp_tb` | `tasks/tb-generation/voltage/dac_ramp_tb` |
| `inl_dnl_probe` | `tasks/tb-generation/voltage/testbench/inl_dnl_probe` |

### 最低目标

1. end-to-end：至少 4 个 parity 验证完成
2. spec-to-va：至少 3 个 gold answer + 自动化 check 写完
3. tb-generation：4 个任务都有 gold `.scs` 并在 EVAS 上验收
4. 填 BENCHMARK_RESULT_TABLE（end-to-end 部分）和 SPEC_TO_VA_RESULT_TABLE
5. 提 1 个 PR

---

## 4. 当前负责人（你）

定位：`维护高价值 parity case、审核 benchmark 方法、推进论文主线。`

1. 审核两位同学的 gold answers 和 parity 结果
2. 维护 CPPLL / ADPLL 闭环案例
3. 维护论文草稿与 related work
4. 决定哪些 case 升格正式 benchmark
5. 继续扩展 examples（新电路类别）

---

## 5. 每个人必须交什么

### end-to-end 任务
1. EVAS 运行命令 + 结果路径
2. `dut_compile / tb_compile / tran_generated / sim_correct` 结果
3. Spectre 结果路径（用于 parity）
4. `evas_fb_hz / spectre_fb_hz / ppm_cross_delta`（如适用）
5. 在 BENCHMARK_RESULT_TABLE 中填对应行

### spec-to-va 任务
1. Gold `.va` 文件（参考答案）
2. 更新后的 `checks.yaml`（替换 `manual_review_expected_output`）
3. EVAS compile 通过确认
4. 在 SPEC_TO_VA_RESULT_TABLE 中填对应行

### bugfix 任务
1. Gold `dut_fixed.va` 文件
2. EVAS compile 通过确认
3. `sim_correct` 行为验收通过

### tb-generation 任务
1. Gold `tb_*.scs` 文件
2. EVAS TB compile 通过确认
3. `tran.csv` 产生确认

---

## 6. 不要重复做什么

以下已有完整 verified 结果，不需要重新做：

- `clk_div_smoke`
- `comparator_smoke`
- `ramp_gen_smoke`
- `d2b_4bit_smoke`
- `adpll_lock_smoke`
- `cppll_timer`
- `adpll_timer`
- `adpll_idtmod`

---

## 7. 执行顺序建议（新人）

1. 看 `onboarding/00_START_HERE.md`
2. 看 `onboarding/NEW_MEMBER_START.md`
3. 看 `docs/benchmark/EXAMPLE_TO_BENCHMARK_WORKFLOW.md`
4. **先跑自己负责的 end-to-end 任务的 EVAS**（L0 = compile，L1 = sim_correct）
5. 再跑 Spectre，对比 parity
6. 然后做 spec-to-va gold answers
7. 最后处理 bugfix / tb-generation 验收
8. 全程填两张表（BENCHMARK_RESULT_TABLE + SPEC_TO_VA_RESULT_TABLE）
9. 提 PR

---

## 8. 一句话版

`每个人的工作覆盖全部四个任务族：end-to-end parity 验证、spec-to-va gold answer 编写、bugfix/tb-generation 验收。benchmark 的价值不只来自"能跑通"，还来自"有参考答案可以自动评分"。`
