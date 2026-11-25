# Git 实操实验手册（Ubuntu）

> 配套已学课程 `git-and-github`（c1–c6）  
> 原则：每关先做、再对照「验收」；卡住把终端输出贴给 tutor  
> 建议目录：`~/git-labs/`（与学习笔记仓分开，避免误改）

---

## 0. 环境准备（5 分钟）

```bash
git --version
mkdir -p ~/git-labs && cd ~/git-labs
```

若尚未配置身份（只影响本机提交作者）：

```bash
git config --global user.name  "你的名字"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global --get user.name
git config --global --get user.email
```

**验收：** `git --version` 有输出；`user.name` / `user.email` 非空。

---

## Lab 1 · 三区循环（对应 c1–c2）

目标：亲手看见「工作区 → 暂存区 → 仓库」。

```bash
cd ~/git-labs
rm -rf lab1 && mkdir lab1 && cd lab1
git init
echo 'hello' > note.txt
git status
git add note.txt
git status
git commit -m "feat: add note"
git log --oneline
git ls-files -s
```

再改一次文件，只观察、先不提交：

```bash
echo 'world' >> note.txt
git status
git diff                 # 工作区 vs 暂存区
git add note.txt
git diff                 # 应空
git diff --staged        # 暂存区 vs HEAD
git commit -m "feat: append world"
```

**验收：**

- [ ] 两次 commit 出现在 `git log --oneline`
- [ ] 能说出：`git diff` 与 `git diff --staged` 各比哪两边

**自测题：** 执行 `git add note.txt` 之后、`commit` 之前，改动主要在哪个区？

---

## Lab 2 · 撤销四层（对应 c3）

在 Lab 1 仓库继续，或：

```bash
cd ~/git-labs/lab1
```

### 2.1 撤销 add（保留工作区）

```bash
echo 'oops' >> note.txt
git add note.txt
git restore --staged note.txt
git status                 # 应仍是 modified，未 staged
```

### 2.2 丢弃工作区未提交改动（慎用）

```bash
git restore note.txt       # 回到上次 commit 内容
git status                 # 应 clean
```

### 2.3 soft reset：拆掉最近一次 commit，改动留在暂存区

```bash
echo 'keep-me' >> note.txt
git add note.txt
git commit -m "wip: will soft-reset"
git log --oneline -3
git reset --soft HEAD~1
git status                 # 改动应还在 staged
git commit -m "feat: keep-me properly"
```

**验收：**

- [ ] 做过一次 `restore --staged` 且工作区改动还在
- [ ] `reset --soft` 后能重新 commit，历史里没有那个 `wip` 提交（若未 push）

**红线：** 已 push 到共享分支的 commit，不要用 `--hard` / `--amend` 改写后强推。

---

## Lab 3 · 分支、快进、冲突（对应 c4 · 弱项加强）

### 3.1 快进合并（Fast-forward）— 必做

```bash
cd ~/git-labs
rm -rf lab3 && mkdir lab3 && cd lab3
git init
echo 'base' > app.txt
git add app.txt && git commit -m "chore: base"

git switch -c feature
echo 'feature-line' >> app.txt
git add app.txt && git commit -m "feat: feature-line"

git switch main
git log --oneline --graph --all
git merge feature          # 观察提示是否含 Fast-forward
git log --oneline --graph --all
```

**要点：** `main` 没有自己的新提交时，合并只是把 `main` 指针挪到 `feature` → **fast-forward**。

### 3.2 非快进（三方合并）

> 注意：若在 `main-only` **之后**才 `switch -c other`，再只在 other 上提交，合回仍是 **FF**。  
> 非快进需要分叉后**两边都有**对方没有的提交，例如：

```bash
# 仍在 lab3（分支名可能是 master）
echo 'main-only' >> app.txt
git add app.txt && git commit -m "feat: main-only"

git switch -c other
echo 'other-only' >> other.txt
git add other.txt && git commit -m "feat: other-only"

# 关键分叉：master 与 other 各自再提交
git switch master    # 或 main
echo 'master-extra' >> app.txt
git add app.txt && git commit -m "feat: master-extra"

git switch other
echo 'other-extra' >> other.txt
git add other.txt && git commit -m "feat: other-extra"

git switch master
git merge other            # 应出现 merge commit（非 FF）
git log --oneline --graph --all
```

### 3.3 制造并解决冲突

```bash
git switch -c conflict-a
echo 'AAA' > shared.txt
git add shared.txt && git commit -m "feat: AAA"

git switch main
git switch -c conflict-b
echo 'BBB' > shared.txt
git add shared.txt && git commit -m "feat: BBB"

git switch main
git merge conflict-a       # 先合入 A
git merge conflict-b       # 应冲突
git status
cat shared.txt             # 看 <<<<<<< ======= >>>>>>>
```

手动改成最终内容（例如只留一行 `AB`），然后：

```bash
# 编辑 shared.txt 去掉冲突标记，保存为最终内容
git add shared.txt
git commit -m "merge: resolve shared.txt"
git log --oneline --graph --all
```

**验收：**

- [ ] 能指出哪一次是 FF、哪一次产生了 merge commit
- [ ] 冲突解决后 `git status` 干净

**自测题：** 「什么时候产生 fast-forward？」用自己的话写一句。

---

## Lab 4 · 本地「远程」（不依赖 GitHub，对应 c5）

用 **裸仓库** 模拟 `origin`，练习 `push` / `fetch` / `pull`。

```bash
cd ~/git-labs
rm -rf remote.git lab4
git init --bare remote.git

git clone remote.git lab4
cd lab4
echo 'v1' > readme.md
git add readme.md && git commit -m "docs: v1"
git push -u origin main

# 另开一个「同事」克隆
cd ~/git-labs
git clone remote.git lab4-colleague
cd lab4-colleague
echo 'from-colleague' >> readme.md
git add readme.md && git commit -m "docs: colleague"
git push

# 回到你这边：先故意落后再 pull
cd ~/git-labs/lab4
echo 'local-wip' >> readme.md
git add readme.md && git commit -m "docs: local-wip"
git fetch origin
git log --oneline --graph --all
git pull --no-rebase       # 若冲突则按 Lab 3 解决
git push
```

**验收：**

- [ ] `git remote -v` 能看到 `origin`
- [ ] 经历过一次「本地有提交 + 远程也有新提交」后的同步

---

## Lab 5 · GitHub（可选，对应 c5–c6）

若网页建仓仍失败，可先跳过；通了再做：

1. GitHub 建 **空 Private** 仓（不要勾 README / gitignore）
2. 把 Lab 1 或新建小项目推上去：

```bash
cd ~/git-labs/lab1   # 或你的项目
git remote add origin git@github.com:你的用户名/仓库名.git
# 或 https://github.com/你的用户名/仓库名.git
git push -u origin main
```

3. 网页上从 `main` 拉分支改文件 → Open Pull Request → Merge  
4. 本地：`git checkout main && git pull`

---

## 关卡清单（建议今天下午顺序）

| 顺序 | Lab | 约时 | 对应课 |
|------|-----|------|--------|
| 1 | Lab 1 三区 | 15–20 min | c1–c2 |
| 2 | Lab 2 撤销 | 15 min | c3 |
| 3 | Lab 3 分支/FF/冲突 | 25–30 min | c4（加强） |
| 4 | Lab 4 本地远程 | 20 min | c5 |
| 5 | Lab 5 GitHub | 视账号 | c5–c6 |

做完一关，在聊天里发：`Lab N 完成` + 可选贴 `git log --oneline --graph --all` 截一段，tutor 帮你验收并出下一关提示。
