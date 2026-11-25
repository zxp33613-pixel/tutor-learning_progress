# Docker 系统课 · 课程大纲

> 归档日期：2026-11-25  
> **本阶段状态：暂标完成（够用即止）** — 第 3/4 课与第 2 课 c5 综合栈未深挖，以后需要再开。  
> 本机：Docker 29.x + Compose v2；拉 Hub 优先 DaoCloud 加速。

## 框架一览

```text
第1课 入门 ✅           环境 → 心智模型 → 生命周期 → 端口/卷 → Dockerfile → Compose入门
第2课 多容器 ✅（核心）  多服务网络 → depends_on → 命名卷 → env（Web+Redis 实操可以后补）
第3课 镜像进阶 ⏸        多阶段 / 缓存 / .dockerignore / 安全 —— 未开
第4课 开发工作流 ⏸      联调 / Git / 排查 —— 未开
选修 编排展望 ⏸         Swarm / K8s 地图 —— 未开
```

| 课 | slug | 状态 |
|----|------|------|
| 1 | `docker-basics` | ✅ 完成 |
| 2 | `docker-compose-multicontainer` | ✅ 核心块完成（c5 综合栈可选补） |
| 3 | `docker-image-advanced`（拟） | ⏸ 未开 |
| 4 | `docker-dev-workflow`（拟） | ⏸ 未开 |
| 选修 | `docker-orchestration-map`（拟） | ⏸ 未开 |

---

## 第 1 课 · Docker 入门 ✅

| # | 块 | 要点 |
|---|-----|------|
| c0 | 环境 | daemon active、`docker` 组、`docker ps` |
| c1 | 心智模型 | 镜像=模板；容器=实例；比 VM 轻（共享内核） |
| c2 | 生命周期 | pull → run → ps/logs → exec → stop → rm |
| c3 | 端口与卷 | `-p 宿主机:容器`；绑定挂载 `-v` |
| c4 | Dockerfile | `FROM` + `COPY`；`docker build -t name:tag .` |
| c5 | Compose 入门 | `up -d` / `ps` / `down` |

## 第 2 课 · Compose 与多容器 ✅（本阶段）

| # | 块 | 要点 | 本阶段 |
|---|-----|------|--------|
| c1 | 多服务网络 | 服务名=DNS；容器内 `127.0.0.1`≠兄弟服务 | ✅ 已练 |
| c2 | depends_on | 管启动顺序，不管业务就绪 | ✅ |
| c3 | 命名卷 vs 绑定挂载 | 数据用命名卷；开发源码用绑定挂载 | ✅ |
| c4 | env / restart | 配置外置；密钥勿进镜像 | ✅ |
| c5 | Web+Redis 栈 | 综合实操 | ⏸ 可以后补 |

## 第 3–4 课 & 选修 ⏸

保留原分块设计（多阶段构建、联调排查、K8s 地图等），**暂不展开**。详见 git 历史或旧版大纲段落；需要时再说「继续 Docker 第 3 课」。

---

## 实验目录（本机）

| 路径 | 用途 |
|------|------|
| `~/docker-labs/myimage/` | Dockerfile → `myweb:1` |
| `~/docker-labs/compose-demo/` | 单服务 Compose |
| `~/docker-labs/multi-demo/` | 多服务 DNS（web+box） |
| `~/docker-labs/web-redis/` | Web+Redis 草稿（未强制跑完） |

## 关联笔记

- 精简复习版：`Docker-学习笔记.md`（同目录）  
- 分课讲义：`docker-basics/session.md`、`docker-compose-multicontainer/session.md`

## 当前进度

- [x] 第 1 课  
- [x] 第 2 课核心（c1–c4）  
- [x] **本阶段 Docker 暂标完成**  
- [ ] 第 2 课 c5 / 第 3–4 课 / 选修 — 搁置  
