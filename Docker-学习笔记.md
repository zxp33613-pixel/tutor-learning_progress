# Docker 学习笔记（本阶段归档）

> 2026-11-25｜对应第 1 课全文 + 第 2 课核心｜暂标完成，够用复习用

---

## 1. 核心概念

| 概念 | 一句话 |
|------|--------|
| 镜像 image | 只读模板（分层文件系统） |
| 容器 container | 按镜像启动的运行实例（镜像 + 可写层） |
| 相对 VM | 共享宿主机内核 → 通常更轻、启动更快 |
| 同一镜像多次 run | 得到多个独立容器，各有可写层 |

---

## 2. 常用命令速查

```bash
# 环境
docker --version
docker ps          # 运行中
docker ps -a       # 含已停止

# 生命周期
docker pull <镜像>
docker run -d --name web1 nginx:alpine
docker logs web1
docker exec -it web1 sh
docker stop web1
docker rm web1
docker rm -f web1  # 强制删

# 端口：宿主机:容器
docker run -d --name web2 -p 18080:80 nginx:alpine

# 绑定挂载
docker run -d --name web2 -p 18080:80 \
  -v ~/docker-labs/web:/usr/share/nginx/html:ro \
  nginx:alpine

# 构建
cd ~/docker-labs/myimage
docker build -t myweb:1 .    # 末尾的 . 不能少
docker run -d --name web3 -p 18080:80 myweb:1

# Compose
docker compose version
docker compose up -d
docker compose ps
docker compose exec web sh -c "..."
docker compose logs --tail 20
docker compose down
# docker compose down -v   # 会删命名卷，慎用
```

---

## 3. 公司网拉镜像（重要）

直连 Docker Hub 常超时。可用：

```bash
docker pull docker.m.daocloud.io/library/nginx:alpine
docker tag  docker.m.daocloud.io/library/nginx:alpine nginx:alpine
```

其它官方库镜像同理：`docker.m.daocloud.io/library/<名>:<标签>`。

也可配置 `/etc/docker/daemon.json` 的 `registry-mirrors`（需 sudo + 重启 docker）。

---

## 4. Dockerfile 最小例

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

注意：每条指令单独一行；不要把 `EOF` 写进文件内容。

---

## 5. Compose 要点（第 1–2 课）

### 单服务

```yaml
services:
  web:
    image: myweb:1
    ports:
      - "18080:80"
```

### 多服务 + 网络

- 同项目默认一个网络  
- **服务名 = DNS 主机名**（如 `http://box/`、`redis:6379`）  
- 容器内的 `127.0.0.1` 只指向**自己**，不是兄弟容器  

### depends_on

- 控制**启动先后**  
- **不保证**依赖已经「业务就绪」（仍需重试/healthcheck）  

### 卷

| 类型 | 用途 |
|------|------|
| 绑定挂载 `./src:/app` | 开发挂源码、配置 |
| 命名卷 `redis-data:/data` | DB/Redis 等持久数据 |

### 配置与安全

- `environment` / `.env` 注入配置  
- **不要**把密码写进 Dockerfile 再推公共仓库  
- `restart: unless-stopped`：进程挂了/开机后尽量拉起  

### 多服务草稿示例

见 `~/docker-labs/web-redis/compose.yaml`（web + redis + 命名卷 + depends_on）。

---

## 6. 踩过的坑

1. `docker build -t myweb:1` 少了路径 `.` → 报 requires 1 argument  
2. Dockerfile 第一行粘成 `FROM ... COPY ... EOF` → parse error  
3. 宿主机 `8080` 被占用 → 改用 `18080:80`  
4. Hub 超时 → DaoCloud 再 tag  
5. `docker ps` 看不到已停止容器 → 用 `ps -a`  

---

## 7. 本机实验路径

| 目录 | 内容 |
|------|------|
| `~/docker-labs/web/` | 挂载用的 `index.html` |
| `~/docker-labs/myimage/` | Dockerfile + `myweb:1` |
| `~/docker-labs/compose-demo/` | 单服务 compose |
| `~/docker-labs/multi-demo/` | web + box 服务名互访 |
| `~/docker-labs/web-redis/` | Web+Redis 草稿 |

---

## 8. 以后若再学

大纲里第 3 课（多阶段/缓存）、第 4 课（联调排查）、第 2 课 c5（跑通 Redis 栈）均可补；对 tutor 说「继续 Docker」即可。
