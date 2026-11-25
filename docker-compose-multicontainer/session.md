# Docker：Compose 与多容器

> Taught: 2026-11-25

## TL;DR

- 同项目多服务默认在同一网络；**服务名 = DNS 主机名**。
- 容器内的 `127.0.0.1` 是「自己」，不是兄弟容器。
- `depends_on` 管启动顺序，不管应用是否真正就绪。
- Redis 等持久数据用命名卷；密钥不要烤进镜像。

## Explanation

### c1 多服务与默认网络

Compose 为项目创建默认网络。`web` 访问 `http://box/` 成功，说明服务名解析生效。  
`box` 未映射宿主机端口时，宿主机浏览器不能直接打开它，但同网络内容器可以。

### c2 depends_on

控制启动先后；默认不保证依赖服务「业务就绪」。应用层重试或 healthcheck 仍需要。

### c3 命名卷 vs 绑定挂载

- 开发挂源码/配置 → 绑定挂载
- DB/Redis 持久数据 → 命名卷
- `compose down -v` 会删命名卷，生产慎用

### c4 环境变量与重启

配置用 `environment` / `.env`；密钥不要写进镜像层；`restart` 只管拉起进程。

## Key Examples

```bash
cd ~/docker-labs/multi-demo
docker compose up -d
docker compose exec web wget -qO- http://box/ | head -3
```

```bash
# c5 见 ~/docker-labs/web-redis/compose.yaml
docker pull docker.m.daocloud.io/library/redis:alpine
docker tag docker.m.daocloud.io/library/redis:alpine redis:alpine
cd ~/docker-labs/web-redis && docker compose up -d
```

## Gotchas

- 容器内不要用 `127.0.0.1` 去找另一个服务。
- 服务名以 `compose.yaml` 里的 key 为准。
- 公司网拉 Hub 用 DaoCloud 再 tag。

## Related Topics

Docker 入门；Docker 第 3 课镜像进阶
