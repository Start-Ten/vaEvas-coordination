# SSH 隧道与 Daemon 对齐操作手册（AI/新人直接执行）

## 1. 目标

这份手册用于让 AI 或新同学直接跑通 bridge 链路，不需要填写表单。

核心要求：

1. SSH tunneling 可用
2. daemon 进程可用
3. tunneling 端口与 daemon 监听端口一致

---

## 2. 前置条件

1. 本地 `ssh` 可用
2. 已配置 `~/.ssh/config` 主机别名
3. bridge 仓库依赖已安装：`<repo>/iccad/virtuoso-bridge-lite`

最小检查：

```bash
ssh <target-host> 'echo ok_target && hostname'
ssh -o BatchMode=yes <target-host> 'echo batch_ok'
```

---

## 3. 标准执行路径（推荐）

优先使用项目脚本自动处理 tunnel + daemon：

```bash
cd <repo>/iccad/virtuoso-bridge-lite
zsh ./start_thu_bridge.sh
zsh ./status_thu_bridge.sh
```

状态判定：

1. tunnel running
2. daemon OK
3. spectre 可用或有明确报错定位

---

## 4. 手动路径（脚本异常时）

## 4.1 启动隧道（终端 A）

```bash
ssh -N -L 5971:localhost:5971 <target-host>
```

说明：

1. `5971` 是本地端口，必须与 daemon 配置一致
2. 这个终端保持前台运行，不要关闭

## 4.2 启动 daemon（终端 B）

```bash
cd <repo>/iccad/virtuoso-bridge-lite
source .venv/bin/activate
virtuoso-bridge start
```

## 4.3 检查 tunnel/daemon 匹配

```bash
cd <repo>/iccad/virtuoso-bridge-lite
virtuoso-bridge status
```

如果状态异常，再查：

```bash
lsof -nP -iTCP:5971 | cat
tail -n 200 logs/commands.log | cat
```

---

## 5. 最小功能烟测

在 bridge 就绪后执行：

```python
from virtuoso_bridge import BridgeClient

c = BridgeClient()
print(c.execute_skill("1+2"))
```

若返回正常数值，说明 tunnel + daemon + SKILL 调用链路可用。

---

## 6. 常见故障快速修复

## 6.1 隧道建立失败

1. 先检查 host alias 是否正确
2. 检查跳板链路和密钥权限
3. 用 `ssh -v <target-host>` 看握手报错

## 6.2 daemon 启动失败

1. 检查 `.venv` 是否激活
2. 检查依赖是否完整安装
3. 用 `virtuoso-bridge restart` 重启并复查状态

## 6.3 spectre 不可用

1. 检查 `.env` 的 `VB_CADENCE_CSHRC`
2. 远端验证：

```bash
ssh <target-host> 'csh -c "source <cadence-cshrc>; which spectre"'
```

---

## 7. 与闭环验证衔接

当 tunnel + daemon 状态正常后，再进入 EVAS-first 闭环：

1. EVAS 预检
2. EVAS + Spectre 对照
3. gate 判定

参考：`docs/benchmark/EVAS_VIRTUOSO_CLOSED_LOOP_BENCHMARK.md`
