# Docker 入门

> Taught: 2026-11-25

## TL;DR

- 容器共享宿主机内核，通常比 VM 更轻。
- 镜像 = 只读模板；容器 = 运行实例。
- 本机环境：`docker` 29.x，用户在 `docker` 组，`docker ps` 可用。

## Explanation

### c0 环境就绪

验收标准：`systemctl` 显示 docker **active**；存在 `/var/run/docker.sock`；用户属于 `docker` 组；`docker ps` 成功（空列表也算）。

本机结果（2026-11-25）：已通过。

### c1 镜像 vs 容器 vs VM

- 镜像：只读模板（分层）；容器：运行实例（镜像 + 可写层）。
- 相对 VM：共享宿主机内核，通常更轻、启动更快。
- 同一镜像可多次 `docker run`，得到多个互不影响的容器（各有自己的可写层）。

### c2 生命周期

常用链：`pull` → `run -d --name` → `ps` / `logs` → `exec` → `stop` → `rm`。  
公司网直连 Docker Hub 可能超时；可用 `docker.m.daocloud.io/library/...` 再 `tag` 成本地名。

## Key Examples

```bash
docker --version
docker ps
docker pull docker.m.daocloud.io/library/nginx:alpine
docker tag docker.m.daocloud.io/library/nginx:alpine nginx:alpine
docker run -d --name web1 nginx:alpine
docker exec -it web1 sh -c "hostname"
docker stop web1 && docker rm web1
```

## Gotchas

- 有 `docker` 命令 ≠ daemon 在跑；要以 `docker ps` 为准。
- 不在 `docker` 组时常见权限错误，需 `sudo` 或加组后重新登录。
- `docker ps` 默认只显示运行中；停了的要用 `docker ps -a`。
- 删容器 `rm` 不删镜像；勿误删工作上的旧容器（如本机已有 `matrix-studio`）。
- `-p`：宿主机端口:容器端口；宿主机端口被占用就换一个（如 `18080:80`）。
- `-v` 绑定挂载：把宿主机目录映进容器；`:ro` 只读。数据在宿主机上，删容器不丢挂载内容。
- `docker build -t name:tag .` 末尾的 `.` 不能少；Dockerfile 里每条指令单独一行。
- `FROM nginx:alpine` + `COPY` 可把静态页打进镜像；与 `-v` 挂载不同：内容固化在镜像里。

### c4 Dockerfile

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

```bash
docker build -t myweb:1 .
docker run -d --name web3 -p 18080:80 myweb:1
```

## Visualization

（暂无）

### c5 Compose

- 用 `compose.yaml` 声明服务；`docker compose up -d` / `ps` / `down`。
- 本机：Compose v2.40；示例 `~/docker-labs/compose-demo/` 使用本地镜像 `myweb:1`。

## Related Topics

Git 与 GitHub 入门；Docker 第 2 课 Compose 多容器