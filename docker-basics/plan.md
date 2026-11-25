# Plan — Docker 入门

## Goal

理解镜像与容器，能在本机拉取镜像、运行/查看/清理容器，使用卷与端口映射，编写简单 `Dockerfile` 并构建；知道 Compose 解决什么问题（本机若未装插件则先讲概念与安装）。

## Probe result

| strand | status |
|--------|--------|
| 摸底 | ✅ 5/5（容器轻量、镜像/容器、数据默认丢失、`-p` 方向、Dockerfile） |
| 环境（daemon / 权限） | ✅ `docker ps` 已通；Compose 插件仍待装（c5） |
| 镜像与容器 | ✅ 概念已知，课内加深 |
| 数据与网络 | ✅ 方向已知，待实操 |
| 镜像构建 | ✅ 用途已知，待实操 |

## Dependency map

```mermaid
flowchart LR
  k1["会用终端；Git 已学"] --> c0["环境：daemon与权限"]
  c0 --> c1["镜像 vs 容器心智模型"]
  c1 --> c2["run/ps/logs/exec/清理"]
  c2 --> c3["端口、卷、常用参数"]
  c3 --> c4["Dockerfile 与 build"]
  c4 --> c5["Compose 概念与入门"]
  c5 --> goal["🎯 能独立跑通小服务"]
  classDef done fill:#12261e,stroke:#3fb950,color:#e6edf3
  classDef doing fill:#0d2240,stroke:#58a6ff,color:#e6edf3,stroke-width:2px
  classDef todo fill:#161b22,stroke:#30363d,color:#8b949e
  classDef known fill:#12261e,stroke:#3fb950,color:#e6edf3,stroke-dasharray:4 3
  classDef gap fill:#2a1215,stroke:#f85149,color:#e6edf3
  classDef goal fill:#1f1a0d,stroke:#d29922,color:#e6edf3
  class c0,c1,c2,c3,c4,c5 done
  class k1 known
  class goal goal
```

## Chunks

| # | chunk | exam tasks | depth | status |
|---|-------|------------|-------|--------|
| c0 | 环境就绪：daemon、权限、`docker ps` | 0.1 | 实操门禁 | ✅ |
| c1 | 镜像 vs 容器 vs 虚拟机 | 1.1 | 概念图（可略讲） | ✅ |
| c2 | 生命周期：`pull`/`run`/`ps`/`logs`/`exec`/`stop`/`rm` | 1.2 | 命令实操 | ✅ |
| c3 | `-p` 端口、`-v` 卷、常用 flag | 1.3 | 表格+实验 | ✅ |
| c4 | `Dockerfile` + `build` + 标签 | 1.4 | 写文件实操 | ✅ |
| c5 | Compose：多容器编排入门（含安装提示） | 1.5 | 概念+最小示例 | ✅ |
