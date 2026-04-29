# Issue, PR, and WeChat Workflow

这份流程给外部协作者使用。目标是让问题、代码改动和沟通都能追踪，而不是散落在聊天记录里。

## 1. 总原则

1. **发现问题先提 issue**：包括 benchmark 定义不清、checker 可疑、EVAS/Spectre 不一致、外部资料许可证不清楚、任务无法复现。
2. **有改动提 PR 给 bucketsran 的 fork**：不要直接把实验性改动推到 upstream 主仓。
3. **提完 PR 后微信通知 bucketsran**：微信只做提醒，技术内容必须写在 issue/PR 里。
4. **不要用聊天记录替代证据**：每个结论都要能指向文件、命令、日志摘要或结果表。

## 2. 仓库路由

| 内容 | issue/PR 目标 |
|---|---|
| EVAS 内核、parser、preflight、Spectre parity | `BucketSran/EVAS` |
| benchmark、runner、checker、A/D/F/G/H/I/RAG 实验 | `BucketSran/behavioral-veriloga-eval` |
| Verilog-A 规则、电路机制知识、生成/审查卡片 | `BucketSran/veriloga-skills` |
| 分工、论文叙事、时间表、协作规范 | `BucketSran/vaEvas-coordination` |

如果不确定放哪里，先在 `BucketSran/vaEvas-coordination` 开 issue，并标明“needs routing”。

## 3. 什么情况提 issue

提 issue 的典型情况：

1. 新 benchmark 的 gold 在 EVAS 或 Spectre 下不能通过。
2. EVAS PASS 但 Spectre FAIL，或反过来。
3. checker 报错看起来和 prompt 要求不一致。
4. runner 把编译/缺文件/interface 问题误判成行为失败。
5. prompt 存在污染、重复、接口不清或 artifact 要求不完整。
6. 外部 Verilog-A 资料可以转成 benchmark，但许可证或引用方式不清楚。
7. RAG/机制模板检索到了错误类型，导致修复方向明显偏离。

issue 不要求已经修好，但必须包含最小复现信息。

## 4. 什么情况提 PR

提 PR 的典型情况：

1. 新增 benchmark-v2 task。
2. 修复 checker/runner/EVAS/Spectre parity。
3. 新增或修订 Verilog-A skill/机制知识。
4. 更新实验结果表、论文叙事或协作文档。
5. 修复 issue 中已经定位清楚的问题。

PR 必须包含：

1. 修改内容概述。
2. 关联 issue。
3. 验证命令和结果。
4. EVAS/Spectre 状态，如果相关。
5. 剩余风险。

## 5. 推荐分支和标题

分支名：

```text
bench-v2/<short-topic>
evas/<short-topic>
skills/<short-topic>
coord/<short-topic>
```

issue 标题：

```text
[benchmark-v2] <task or mechanism>: <problem>
[EVAS parity] <feature>: <mismatch>
[checker] <task>: <wrong/missing behavior>
[docs] <area>: <change>
```

PR 标题：

```text
[benchmark-v2] add <mechanism> perturbation tasks
[EVAS parity] align <feature> with Spectre
[skills] add <mechanism> Verilog-A guidance
[coordination] update <workflow or assignment>
```

## 6. PR 后微信通知

提完 PR 后，给 bucketsran 发微信。微信只需要短，不要把全部技术细节塞进聊天。

模板：

```text
我刚提了一个 vaEvas PR，请看：

仓库：<repo>
PR：<link>
主题：<one-line summary>
验证：<EVAS/Spectre/pytest/other>
需要你重点看：<risk or decision>
```

如果只是 issue：

```text
我刚提了一个 vaEvas issue：

仓库：<repo>
Issue：<link>
问题：<one-line problem>
我已经附上：<repro/result/log summary>
```

## 7. 本地提交前检查

推荐安装并使用本仓库的 `vaevas-git-sync` skill：

```bash
cd /path/to/vaEvas/coordination
python3 skills/install_recommended_skills.py --skill vaevas-git-sync
```

提交前至少检查：

```bash
git status --short --branch
git diff --check
```

涉及 Python/JSON 时：

```bash
git diff --name-only '*.py' | xargs -r python3 -m py_compile
git diff --name-only '*.json' | xargs -r python3 -c 'import json,sys; [json.load(open(p)) for p in sys.argv[1:]]'
```

不要提交：

1. API key、`.env`、bridge profile。
2. `status/local-private/`。
3. 大型 raw CSV、仿真 scratch、完整 generated/results。
4. 没有许可证说明的外部代码或论文资源。
5. 纯聊天式总结但没有可复现证据的文件。
