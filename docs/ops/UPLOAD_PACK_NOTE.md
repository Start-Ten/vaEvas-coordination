# 单仓上传说明（只上传 coordination）

## 1. 结论

如果你只上传 `coordination`，请优先使用本仓库内的以下文档，它们已覆盖新人接入和 EVAS↔Virtuoso 闭环执行：

1. `onboarding/VIRTUOSO_EVAS_TEAM_GUIDE.md`
2. `onboarding/ONBOARDING_CHECKLIST_TEAM.md`
3. `docs/benchmark/EVAS_VIRTUOSO_CLOSED_LOOP_BENCHMARK.md`
4. `onboarding/NEW_MEMBER_START.md`

重要边界：

1. 本仓库可以单独完成“流程理解、任务分派、标准口径”。
2. 真实仿真执行仍依赖代码仓库与 bridge 环境，不能只靠本仓库直接跑通。

---

## 2. 本次已附着到 coordination 的关键文件

1. 闭环 benchmark 规范副本：
   - `docs/benchmark/EVAS_VIRTUOSO_CLOSED_LOOP_BENCHMARK.md`
2. 可独立使用的新成员清单：
   - `onboarding/ONBOARDING_CHECKLIST_TEAM.md`

这两份可替代原先对 `vaEvas/worksche` 的强依赖。

---

## 3. 仍属于外部仓库的信息

以下内容在只上传 coordination 时不会包含，请在团队执行前按需补充：

1. 真实代码与脚本（EVAS / testspace / skills）
2. `iccad/virtuoso-bridge-lite` 的运行文件和 `.env`
3. 历史仿真输出（output 目录中的报告与波形）

---

## 4. 建议给新同学的最小指令

可直接发送：

```text
先读 coordination 内的 VIRTUOSO_EVAS_TEAM_GUIDE、ONBOARDING_CHECKLIST_TEAM、EVAS_VIRTUOSO_CLOSED_LOOP_BENCHMARK；按 EVAS-first 闭环执行并提交 consistency_report + gate_decision + next_action。
```
