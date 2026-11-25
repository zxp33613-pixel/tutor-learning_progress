# Linux 常用命令速查

> 面向日常开发 / 运维碎片查阅。默认假设 **Bash + Ubuntu/Debian**（`apt`）。  
> 约定：`<>` 必填、`[]` 可选；多数命令可加 `-h` / `--help` 看帮助。

---

## 1. 帮助与手册

| 命令 | 说明 |
|------|------|
| `cmd --help` / `cmd -h` | 简短用法 |
| `man cmd` | 手册页（`q` 退出，`/` 搜索） |
| `man 5 passwd` | 指定手册章节（1 命令，5 配置格式…） |
| `whatis cmd` | 一行简介 |
| `type cmd` | 看是别名、内建还是外部程序 |
| `which cmd` / `command -v cmd` | 可执行文件路径 |
| `apropos 关键词` | 按关键词搜手册 |

---

## 2. 目录与路径

| 命令 | 说明 |
|------|------|
| `pwd` | 当前目录绝对路径 |
| `cd /path` | 进入目录 |
| `cd` / `cd ~` | 回家目录 |
| `cd -` | 回到上一次目录 |
| `cd ..` / `cd ../..` | 上级 / 上上级 |
| `ls` | 列出（短名） |
| `ls -l` | 长列表（权限、所有者、大小、时间） |
| `ls -la` / `ls -alh` | 含隐藏文件；`-h` 人类可读大小 |
| `ls -lt` / `ls -ltr` | 按修改时间新→旧 / 旧→新 |
| `ls -R` | 递归列出 |
| `tree` | 树形目录（需安装 `tree`） |
| `realpath path` | 解析为绝对路径 |
| `basename path` / `dirname path` | 取文件名 / 取目录部分 |

**路径速记**

- `.` 当前，`..` 上级，`~` 家目录，`/` 根
- `~user` 某用户家目录
- 相对路径相对 `pwd`；绝对路径以 `/` 开头

---

## 3. 文件与目录操作

| 命令 | 说明 |
|------|------|
| `touch a.txt` | 创建空文件 / 更新时间戳 |
| `mkdir dir` | 建目录 |
| `mkdir -p a/b/c` | 递归建多级目录 |
| `cp src dst` | 复制文件 |
| `cp -r src_dir dst` | 复制目录 |
| `cp -a src dst` | 归档式复制（权限、时间等尽量保留） |
| `mv src dst` | 移动 / 重命名 |
| `rm file` | 删文件（慎用） |
| `rm -r dir` | 递归删目录 |
| `rm -rf path` | 强制递归删除（**极危险**，先确认路径） |
| `rmdir dir` | 删空目录 |
| `ln -s target link` | 软链接（快捷方式） |
| `ln target hardlink` | 硬链接（同 inode） |
| `install -D -m 644 src dst` | 复制并设权限，可顺带建父目录 |
| `truncate -s 0 file` | 清空文件内容（保留 inode） |
| `rename 's/old/new/' *.txt` | 批量改名（发行版工具名可能不同） |

**安全习惯**：删重要目录前先 `ls` / `echo rm -rf ...` 预览；尽量避免 root 下乱 `rm -rf`。

---

## 4. 查看文件内容

| 命令 | 说明 |
|------|------|
| `cat file` | 整文件输出 |
| `cat -n file` | 带行号 |
| `tac file` | 倒序输出行 |
| `less file` | 分页看（空格翻页，`/` 搜，`q` 退出） |
| `more file` | 简单分页 |
| `head -n 20 file` | 前 20 行 |
| `tail -n 20 file` | 后 20 行 |
| `tail -f file` | 跟踪追加（看日志） |
| `tail -F file` | 跟踪，文件被轮转后仍跟新文件 |
| `wc -l file` | 行数（`-w` 词，`-c` 字节） |
| `nl file` | 带行号输出 |
| `od -c file` / `xxd file` | 看原始字节 / hex |
| `file path` | 猜测文件类型 |
| `stat path` | 详细元数据（大小、inode、时间） |

---

## 5. 编辑（终端内）

| 命令 | 说明 |
|------|------|
| `nano file` | 简单编辑器（Ctrl+O 存，Ctrl+X 退出） |
| `vim file` | 强大编辑器（`i` 插入，`Esc`，`:wq` 存退，`:q!` 不存退） |
| `echo 'text' > file` | 覆盖写入 |
| `echo 'text' >> file` | 追加写入 |
| `printf '%s\n' 'a' 'b' > file` | 更可控的写入 |
| `tee file` | 标准输出同时写入文件（管道常用） |
| `tee -a file` | 追加 |

---

## 6. 权限、所有者、特殊位

### 6.1 看懂 `ls -l`

```text
-rwxr-xr--  1 user group  4096 Nov 25 12:00 demo.sh
│└─┬─┘└─┬─┘└─┬─┘
│  │    │    └─ 其他人
│  │    └─ 同组
│  └─ 所有者
└─ 类型：- 文件  d 目录  l 链接
```

权限三位：`r=4 w=2 x=1`，如 `755` = `rwxr-xr-x`。

### 6.2 常用命令

| 命令 | 说明 |
|------|------|
| `chmod 755 file` | 数字改权限 |
| `chmod u+x file` | 所有者加执行 |
| `chmod -R a+r dir` | 递归给所有人读（慎用） |
| `chown user file` | 改所有者 |
| `chown user:group file` | 改所有者与组 |
| `chown -R user:group dir` | 递归 |
| `chgrp group file` | 只改组 |
| `umask` | 查看默认掩码（新建文件权限受其影响） |
| `lsattr file` / `chattr +i file` | 扩展属性（如不可改，需 root） |

**目录的 `x`**：进入该目录需要执行位；只有 `r` 不够 `cd`。

---

## 7. 查找文件与内容

### 7.1 `find`（按路径/属性）

```bash
find /path -name '*.log'          # 文件名（区分大小写）
find /path -iname '*.Log'         # 忽略大小写
find /path -type f                # 只文件；d=目录 l=链接
find /path -mtime -7              # 7 天内改过
find /path -mtime +30             # 30 天前改过
find /path -size +100M            # 大于 100MB
find /path -user alice            # 所有者
find /path -perm 644              # 精确权限
find /path -name '*.tmp' -delete  # 找到并删除（先 dry-run 确认）
find /path -name '*.c' -exec ls -l {} \;
find /path -name '*.c' -print0 | xargs -0 grep -n 'main'
```

### 7.2 `grep` / `rg`（按内容）

```bash
grep 'pattern' file
grep -n 'pattern' file          # 行号
grep -i 'pattern' file          # 忽略大小写
grep -r 'pattern' dir           # 递归
grep -R --exclude-dir=.git 'pat' .
grep -l 'pattern' *.c           # 只列文件名
grep -v 'pattern' file          # 反向匹配
grep -E 'a|b' file              # 扩展正则
grep -F 'exact*' file           # 固定字符串（不按正则）
```

`ripgrep`（若已装）：`rg pattern` / `rg -n pattern dir`，通常比 `grep -r` 更快。

### 7.3 其他定位

| 命令 | 说明 |
|------|------|
| `locate name` | 用数据库快搜（需 `updatedb`，可能不是实时） |
| `whereis cmd` | 二进制/手册/源码大致位置 |
| `fc-list` | 字体列表（桌面环境） |

---

## 8. 管道、重定向与组合

| 写法 | 说明 |
|------|------|
| `cmd > file` | 标准输出覆盖写入 |
| `cmd >> file` | 追加 |
| `cmd 2> err.log` | 标准错误写入 |
| `cmd &> file` | stdout+stderr 都写入（bash） |
| `cmd > file 2>&1` | 同上（可移植写法） |
| `cmd < file` | 标准输入来自文件 |
| `cmd1 \| cmd2` | 管道：前输出变后输入 |
| `cmd1 && cmd2` | 前成功才执行后 |
| `cmd1 \|\| cmd2` | 前失败才执行后 |
| `cmd1 ; cmd2` | 顺序执行，不管成败 |
| `( cmd1 ; cmd2 )` | 子 shell |
| `{ cmd1 ; cmd2 ; }` | 当前 shell 分组 |
| `xargs` | 把标准输入变成参数：`find ... -print0 \| xargs -0 rm` |

**过滤示例**

```bash
ps aux | grep nginx | grep -v grep
dmesg | tail -n 50
history | grep docker
```

---

## 9. 文本处理

| 命令 | 说明 |
|------|------|
| `cut -d: -f1 /etc/passwd` | 按分隔符取字段 |
| `sort file` / `sort -n` / `sort -r` | 排序；数值；倒序 |
| `sort -u` / `uniq` | 去重（`uniq` 前通常先 `sort`） |
| `uniq -c` | 去重并计数 |
| `tr 'a-z' 'A-Z'` | 字符替换/删除 |
| `tr -d '\r' < win.txt > unix.txt` | 去 CR（Windows 换行） |
| `paste f1 f2` | 并排合并 |
| `join` | 按字段连接两个已排序文件 |
| `diff a b` / `diff -u a b` | 差异；统一格式补丁风 |
| `comm f1 f2` | 比较两个已排序文件 |
| `sed -n '10,20p' file` | 打印 10–20 行 |
| `sed 's/old/new/g' file` | 替换（加 `-i` 原地改，先备份） |
| `awk '{print $1}' file` | 按空白取第 1 列 |
| `awk -F: '{print $1,$3}' /etc/passwd` | 指定分隔符 |
| `column -t` | 对齐成表 |
| `fmt` / `fold` | 整理行宽 |

**一行统计高频**

```bash
sort file | uniq -c | sort -nr | head
```

---

## 10. 压缩与归档

| 命令 | 说明 |
|------|------|
| `tar -cvf a.tar dir` | 打包 |
| `tar -xvf a.tar` | 解包 |
| `tar -czvf a.tar.gz dir` | gzip 压缩打包 |
| `tar -xzvf a.tar.gz` | 解压 `.tar.gz` / `.tgz` |
| `tar -cJvf a.tar.xz dir` | xz 压缩 |
| `tar -xJvf a.tar.xz` | 解 xz |
| `gzip file` / `gunzip file.gz` | 压/解单个文件 |
| `bzip2` / `bunzip2` | bz2 |
| `xz` / `unxz` | xz |
| `zip -r a.zip dir` | zip 包 |
| `unzip a.zip` | 解压 zip |
| `unzip -l a.zip` | 只列内容 |

查看压缩包内文件而不解压：`tar -tzvf a.tar.gz`。

---

## 11. 磁盘与文件系统

| 命令 | 说明 |
|------|------|
| `df -h` | 各挂载点空间 |
| `df -i` | inode 使用情况 |
| `du -h path` | 目录占用 |
| `du -sh path` | 合计一行 |
| `du -h --max-depth=1` | 只看下一层 |
| `lsblk` | 块设备树 |
| `mount` / `umount /mnt` | 查看挂载 / 卸载 |
| `mount /dev/sdX1 /mnt` | 挂载 |
| `free -h` | 内存与 swap |
| `swapon --show` | swap 设备 |
| `ncdu` | 交互看磁盘占用（需安装） |

---

## 12. 进程与资源

| 命令 | 说明 |
|------|------|
| `ps aux` | 所有进程（BSD 风格） |
| `ps -ef` | 所有进程（System V） |
| `ps -u $USER` | 当前用户进程 |
| `pgrep -a name` | 按名找 PID |
| `pkill name` | 按名发信号（默认 TERM） |
| `kill PID` | 结束进程（SIGTERM） |
| `kill -9 PID` | 强制杀（SIGKILL，最后手段） |
| `killall name` | 按进程名杀 |
| `jobs` | 当前 shell 后台任务 |
| `Ctrl+Z` | 挂起前台任务 |
| `bg` / `fg` | 后台继续 / 调回前台 |
| `nohup cmd &` | 挂后台且忽略挂断 |
| `disown` | 从任务表移除，关终端不易杀 |
| `top` / `htop` | 实时监控（`htop` 更友好，需装） |
| `uptime` | 运行时长与负载 |
| `vmstat 1` | 虚拟内存/CPU 抽样 |
| `iostat` | 磁盘 IO（`sysstat` 包） |
| `lsof -i :8080` | 谁占用 8080 端口 |
| `lsof /path` | 谁打开了该文件 |
| `fuser -v /path` | 占用文件/端口的进程 |
| `nice` / `renice` | 调整优先级 |

---

## 13. 用户、组与提权

| 命令 | 说明 |
|------|------|
| `whoami` | 当前用户名 |
| `id` | uid/gid/组 |
| `who` / `w` | 登录用户 |
| `last` | 登录历史 |
| `su - user` | 切换用户（带登录环境） |
| `sudo cmd` | 以管理员执行 |
| `sudo -i` | root 交互 shell |
| `passwd` | 改自己密码 |
| `sudo passwd user` | 改他人密码 |
| `sudo adduser name` | 添加用户（Debian 友好） |
| `sudo useradd -m name` | 添加用户（更底层） |
| `sudo usermod -aG group user` | 把用户加入附加组 |
| `groups` | 当前用户所属组 |
| `sudo groupadd g` | 建组 |

配置文件：`/etc/passwd`、`/etc/group`、`/etc/shadow`（shadow 仅 root 可读）。

---

## 14. 软件包（Ubuntu / Debian）

| 命令 | 说明 |
|------|------|
| `sudo apt update` | 刷新软件源索引 |
| `sudo apt upgrade` | 升级已装包 |
| `apt search 关键词` | 搜包 |
| `apt show 包名` | 包详情 |
| `sudo apt install 包名` | 安装 |
| `sudo apt remove 包名` | 卸载（留配置） |
| `sudo apt purge 包名` | 卸载并删配置 |
| `sudo apt autoremove` | 删无用依赖 |
| `dpkg -l` | 已装包列表 |
| `dpkg -L 包名` | 包安装了哪些文件 |
| `dpkg -S /path/to/file` | 文件属于哪个包 |
| `apt-cache policy 包名` | 版本与来源 |

其他发行版：`dnf`/`yum`（Fedora/RHEL）、`pacman`（Arch）、`zypper`（openSUSE）。

---

## 15. 网络

| 命令 | 说明 |
|------|------|
| `ip a` / `ip addr` | 网卡与 IP（替代旧 `ifconfig`） |
| `ip r` / `ip route` | 路由表 |
| `ip link set eth0 up` | 启网卡（需权限） |
| `ping -c 4 host` | 连通性 |
| `traceroute host` / `tracepath host` | 路径追踪 |
| `dig domain` / `nslookup domain` | DNS 查询 |
| `host domain` | 简单 DNS |
| `curl URL` | 发 HTTP 请求 |
| `curl -I URL` | 只看响应头 |
| `curl -O URL` | 下载并保留远程文件名 |
| `wget URL` | 下载 |
| `ss -tulnp` | 监听端口（替代旧 `netstat`） |
| `ss -tp` | TCP 连接与进程 |
| `nc -zv host port` | 测端口是否开（netcat） |
| `scp file user@host:/path` | 远程复制 |
| `scp -r dir user@host:/path` | 复制目录 |
| `rsync -avP src/ dst/` | 增量同步（本地或远程） |
| `ssh user@host` | 登录远程 |
| `ssh -L 8080:localhost:80 user@host` | 本地端口转发 |
| `ftp` / `sftp` | 文件传输（优先 sftp/scp） |

**防火墙（Ubuntu 常见）**

```bash
sudo ufw status
sudo ufw allow 22/tcp
sudo ufw enable
```

---

## 16. 系统信息与日志

| 命令 | 说明 |
|------|------|
| `uname -a` | 内核与架构 |
| `hostnamectl` | 主机名与系统信息 |
| `cat /etc/os-release` | 发行版信息 |
| `lscpu` | CPU |
| `lsusb` / `lspci` | USB / PCI 设备 |
| `dmesg -T` | 内核环缓冲 |
| `journalctl -xe` | systemd 日志（近期错误） |
| `journalctl -u nginx -f` | 跟踪某服务日志 |
| `journalctl --since "1 hour ago"` | 时间过滤 |
| `sudo tail -f /var/log/syslog` | 经典 syslog（视发行版） |
| `date` | 当前时间 |
| `timedatectl` | 时区与 NTP 状态 |
| `cal` | 日历 |
| `env` / `printenv` | 环境变量 |
| `echo $PATH` | 可执行搜索路径 |
| `export VAR=value` | 当前 shell 设环境变量 |
| `history` | 命令历史 |
| `history \| grep foo` | 搜历史 |
| `!!` | 上一条命令 |
| `!$` | 上一条最后一个参数 |
| `Ctrl+R` | 交互式搜历史 |

---

## 17. 服务（systemd）

| 命令 | 说明 |
|------|------|
| `systemctl status nginx` | 状态 |
| `sudo systemctl start\|stop\|restart nginx` | 启停重启 |
| `sudo systemctl reload nginx` | 平滑重载配置 |
| `sudo systemctl enable\|disable nginx` | 开机自启开/关 |
| `systemctl is-active nginx` | 是否在跑 |
| `systemctl list-units --type=service` | 服务列表 |
| `systemctl list-timers` | 定时器 |
| `sudo systemctl daemon-reload` | 改完 unit 文件后重载 |

---

## 18. Shell 脚本与任务定时

### 18.1 脚本骨架

```bash
#!/usr/bin/env bash
set -euo pipefail   # 遇错退出；未定义变量报错；管道失败传递

echo "hello"
```

```bash
chmod +x script.sh
./script.sh
```

### 18.2 定时任务 `cron`

```bash
crontab -e          # 编辑当前用户 crontab
crontab -l          # 列出
```

格式：`分 时 日 月 周  命令`

```cron
0 9 * * 1-5  /home/me/bin/backup.sh
*/10 * * * * /usr/bin/php /path/job.php
```

系统级还可看 `/etc/cron.*` 与 `systemd timer`。

---

## 19. 开发向常用组合

```bash
# 目录占用 Top
du -h --max-depth=1 2>/dev/null | sort -hr | head

# 找大文件
find /var -type f -size +100M -exec ls -lh {} \; 2>/dev/null

# 端口占用
ss -tulnp | grep ':8080'

# 批量替换（先预览）
grep -RIn 'old' src/
# sed -i 's/old/new/g' ...   # 确认后再原地改

# 对比两个目录
diff -ruN dir_a dir_b

# 快速 HTTP 静态服务（Python）
python3 -m http.server 8000

# 看证书过期（若有 openssl）
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

---

## 20. 快捷键（Bash 终端）

| 按键 | 作用 |
|------|------|
| `Ctrl+C` | 中断当前前台进程 |
| `Ctrl+D` | EOF / 退出 shell（输入空时） |
| `Ctrl+L` | 清屏（同 `clear`） |
| `Ctrl+R` | 反向搜历史 |
| `Ctrl+A` / `Ctrl+E` | 行首 / 行尾 |
| `Ctrl+U` / `Ctrl+K` | 删到行首 / 删到行尾 |
| `Ctrl+W` | 删前一个词 |
| `Alt+.` | 插入上条命令最后参数 |
| `Tab` | 补全 |
| `Ctrl+Z` | 挂起任务 |

---

## 21. 易混对照

| 场景 | 更推荐 | 备注 |
|------|--------|------|
| 网卡信息 | `ip a` | 旧：`ifconfig` |
| 端口监听 | `ss -tulnp` | 旧：`netstat -tulnp` |
| 跟踪日志 | `tail -F` / `journalctl -f` | |
| 搜文件名 | `find` / `fd` | `locate` 可能不是最新 |
| 搜内容 | `rg` / `grep -R` | |
| 同步目录 | `rsync -avP` | 比反复 `scp -r` 更稳 |
| 看进程树 | `pstree` / `ps auxf` | |

---

## 22. 安全与习惯清单

1. 删除、`chmod -R`、`chown -R` 前先 `ls` / `echo` 确认路径。  
2. 生产机器少用 `kill -9`，先 `TERM` 再排查。  
3. 脚本里路径带空格用引号：`"$file"`。  
4. 管道与 `xargs` 处理含空格文件名时用 `-print0` / `-0`。  
5. 改系统配置先备份：`sudo cp file file.bak.$(date +%F)`。  
6. `sudo` 只给必要命令；不要习惯性 `sudo su` 后乱操作。  
7. 公网机器尽快配密钥登录并考虑关密码登录；防火墙只放行需要端口。

---

## 附录 A. 权限数字速查

| 数字 | 权限 |
|------|------|
| 7 | `rwx` |
| 6 | `rw-` |
| 5 | `r-x` |
| 4 | `r--` |
| 0 | `---` |

常见：文件 `644`，可执行 `755`，私密密钥 `600`，目录常 `755` 或 `750`。

## 附录 B. 本机延伸阅读

- Git：`git-and-github/`  
- Docker：`Docker-学习笔记.md`  
- C / 408：视频为主；`c-for-408` 待视频后再开  

---

*整理日期：2026-11-25 · 可按个人常用命令在文末自行追加「我的别名 / 收藏」。*
