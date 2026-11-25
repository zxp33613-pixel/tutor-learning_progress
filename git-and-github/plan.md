# Plan — Git 与 GitHub 入门

## Goal

能独立完成日常开发所需的 Git 操作：建仓、提交、看历史、回退、分支、合并与冲突处理，
把代码推到 GitHub 并用 PR 参与协作；遇到常见报错能自己定位。

## Probe result

| strand | status |
|--------|--------|
| 摸底 | 跳过（学员选择从零开讲） |

## Dependency map

```mermaid
flowchart LR
  k1["会用终端与编辑器"] --> c1["Git 心智模型"]
  c1 --> c2["建仓与提交"]
  c2 --> c3["看历史与撤销"]
  c3 --> c4["分支与合并/冲突"]
  c2 --> c5["远程仓库"]
  c4 --> c5
  c5 --> c6["GitHub 协作：PR/Issue"]
  c6 --> goal["🎯 独立用 Git 干活"]
  classDef done fill:#12261e,stroke:#3fb950,color:#e6edf3
  classDef doing fill:#0d2240,stroke:#58a6ff,color:#e6edf3,stroke-width:2px
  classDef todo fill:#161b22,stroke:#30363d,color:#8b949e
  classDef known fill:#12261e,stroke:#3fb950,color:#e6edf3,stroke-dasharray:4 3
  classDef gap fill:#2a1215,stroke:#f85149,color:#e6edf3
  classDef goal fill:#1f1a0d,stroke:#d29922,color:#e6edf3
  class c1 done
  class c2 done
  class c3 done
  class c4 done
  class c5 done
  class c6 done
  class k1 known
  class goal goal
```

## Chunks

| # | chunk | 核心内容 | status |
|---|-------|----------|--------|
| c1 | Git 心智模型 | 为什么用版本控制；快照而非差异；工作区/暂存区/仓库；commit 图与分支指针 | ✅ |
| c2 | 建仓与提交 | `git config`、`init`、`status`、`add`、`commit`、`log`、`.gitignore`；提交粒度 | ✅ |
| c3 | 看历史与撤销 | `diff`、`log` 过滤、`restore`、`reset --soft/--mixed/--hard`、`amend`；危险边界 | ✅ |
| c4 | 分支与合并 | `branch`、`switch`、`merge`（快进 vs 三方合并）、冲突解决、`rebase` 何时用 | ✅ |
| c5 | 远程仓库 | `remote`、`clone`、`fetch` vs `pull`、`push`、上游跟踪、拒绝推送怎么处理 | ✅ |
| c6 | GitHub 协作 | 仓库权限模型、Fork vs 分支、PR 流程与 Review、Issue、Conventional Commits | ✅ |
