# Onboarding Status — 2026-04-08

## 结论

当前 blocker 不是 Cadence 环境，而是仓库路径未知。

## 已确认

1. `VNC -> thu-jin` 可用
2. `ssh -X -> thu-wu` 可用
3. `source /home/cshrc/.cshrc.cadence.IC618SP201` 后，`spectre` 和 `virtuoso` 可解析

## 缺失信息

1. `vaEvas`
2. `behavioral-veriloga-eval`
3. `sshConnect/virtuoso-bridge-lite`

## 下一步

1. 先确认服务器上的实际路径
2. 如果无共享目录，则按 [REPOSITORIES.md](/Users/bucketsran/Documents/TsingProject/vaEvas/coordination/docs/project/REPOSITORIES.md) 中的上游地址 clone
3. 路径确认后再继续 bridge 和 example 验证
