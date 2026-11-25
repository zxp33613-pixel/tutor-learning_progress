# Plan — Docker：Compose 与多容器

## Goal

能用 Compose 描述多服务应用：共享网络、声明依赖、区分命名卷与绑定挂载、用环境变量配置服务；跑通「Web + Redis（或同类依赖）」最小栈，并会看日志排查。

## Probe result

| strand | status |
|--------|--------|
| 摸底 | 跳过（学员选择从零） |
| 第1课 Compose 单服务 | ✅ 已会 up/ps/down |
| 多服务网络 | ❌ 待建 |
| 卷与配置 | ❌ 待建 |

## Dependency map

```mermaid
flowchart LR
  k1["第1课：run/卷/Dockerfile/单服务Compose"] --> c1["多服务与默认网络"]
  c1 --> c2["depends_on与启动顺序"]
  c2 --> c3["命名卷 vs 绑定挂载"]
  c3 --> c4["环境变量与.env"]
  c4 --> c5["Web+Redis最小栈实操"]
  c5 --> goal["🎯 能编排多容器小应用"]
  classDef done fill:#12261e,stroke:#3fb950,color:#e6edf3
  classDef doing fill:#0d2240,stroke:#58a6ff,color:#e6edf3,stroke-width:2px
  classDef todo fill:#161b22,stroke:#30363d,color:#8b949e
  classDef known fill:#12261e,stroke:#3fb950,color:#e6edf3,stroke-dasharray:4 3
  classDef gap fill:#2a1215,stroke:#f85149,color:#e6edf3
  classDef goal fill:#1f1a0d,stroke:#d29922,color:#e6edf3
  class c1,c2,c3,c4 done
  class c5 todo
  class k1 known
  class goal goal
```

## Chunks

| # | chunk | exam tasks | depth | status |
|---|-------|------------|-------|--------|
| c1 | 多服务 YAML：services、默认网络、服务名 DNS | 2.1 | 概念+改文件 | ✅ |
| c2 | `depends_on`：顺序直觉与「就绪」局限 | 2.2 | 易混点 | ✅ |
| c3 | 命名卷 vs 绑定挂载：何时用哪个 | 2.3 | 对比+实操 | ✅ |
| c4 | `environment` / `.env` / 重启策略 | 2.4 | 配置 | ✅ |
| c5 | Web + Redis 最小栈（镜像走国内加速） | 2.5 | 综合实操 | ⏸ 本阶段跳过 |
