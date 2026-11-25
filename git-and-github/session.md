# Git 与 GitHub 入门

> Taught: 2026-11-23

## TL;DR

- Git 存的是**快照**（内容寻址），不是差异；diff 是事后比出来的。
- 三个区域：工作区 → `git add` → 暂存区(index) → `git commit` → 仓库(objects + refs)。
- 分支只是一个指向 commit 的**指针**，HEAD 指向"当前在哪个分支"。

## Explanation

### 1. 三个区域

```
  工作区 (working tree)      暂存区 (index/staging)        仓库 (.git)
  ┌──────────────────┐  add  ┌──────────────────┐ commit ┌────────────────┐
  │ 你正在编辑的文件  │ ────► │ 下次提交的"取景框"│ ─────► │ 一串不可变的    │
  │                  │ ◄──── │                  │ ◄───── │ commit 快照     │
  └──────────────────┘restore└──────────────────┘ restore└────────────────┘
                                                     --staged
```

### 2. 快照，不是差异

每次 commit，Git 记下"这一刻所有被跟踪文件的完整内容"的指纹（内容寻址：相同内容只存一份）。
你看到的 diff，是两个快照比出来的结果，不是 Git 存储的东西。

### 3. 一个 commit 长什么样

```
   a1b2c3d  ← 40 位 SHA-1 的内容哈希
   ├ tree:    这棵树（目录 + 文件内容）
   ├ parent:  ← 指向上一个 commit     ← 这就是"历史"的全部秘密
   ├ author/committer + 时间
   └ message: "fix: 修正 c2 溢出判断"
```

所以历史只是一条（或几条）**有向无环图（DAG）**。分支轻得离谱——只是一个指向某个 commit 的指针文件：

```
  A ── B ── C ── D   ← main  （main 就是写着 "D" 的一行文本）
                 ↑
                HEAD      （HEAD 指向"当前在哪个分支"）
```

### 4. 暂存区到底存在哪（追问补充）

暂存区没有独立目录，它就是 **`.git/index` 这一个二进制文件**，本质是一张清单表，
每行记录：文件模式 + blob 哈希 + 路径。

`.git` 里三个关键角色：

- `objects/` 存**内容**（blob / tree / commit 对象，压缩存放，按哈希寻址）
- `index` 记**"下一次拍什么"**（候选清单）
- `refs/`（含 `HEAD`）记**"历史走到哪"**（分支/tag 指针）

## Key Examples

在任意仓库里直接读 index：

```bash
$ git ls-files -s          # 直接查看暂存区清单
100644 0a92a06... 0  .gitignore
100644 28aec65... 0  C-语言课程大纲.md
100644 39b6780... 0  INDEX.md
#       ↑mode   ↑内容哈希  ↑路径

$ git cat-file -t 39b6780...
blob                        # 哈希指向的对象确实存在
```

观察点：`git add` 的那一刻，内容**已经**写进 `.git/objects` 了；index 只是把这批 blob
登记为"下一次提交的候选"。因为它还不属于任何 commit，所以不在历史里，反悔很容易。

## Gotchas

- 只有 **commit 过的内容**才可能被找回。没 add 的修改，`reset` 救不回来。
- **分支不是文件夹副本**。切换分支不复制代码，只改指针 + 更新工作区。
- 删掉 `.git` 目录 = 历史全灭，代码退化成普通文件夹。
- `git add` 之后内容已在 objects 里，但"存在 objects" ≠ "进了历史"。

## Visualization

<!-- 暂无 -->

## Related Topics

Git 与 GitHub 入门 · c2 建仓与提交

---

<!-- tutor-notes -->

## Lesson notes

### 实操加练（2026-11-24）

- 手册：`hands-on-lab.md`（Ubuntu 跟做）
- 弱项加强：Lab 3 Fast-forward / 非 FF / 冲突 —— 已实操过关
- Lab1–Lab5 均完成（Lab4/5 因公司网用本地裸仓模拟 origin/PR）
- 回家可连 GitHub 时：空仓 + `remote set-url` + 网页 Open PR / Merge，步骤与 Lab5 相同


---

# c2 · 建仓与提交

## TL;DR

- 一次性配置：`git config --global user.name/user.email/init.defaultBranch`，三层作用域就近覆盖。
- 核心循环：`init → status → add → commit → log`，**每个动作前先 `git status`**。
- 一个 commit = 一个逻辑变更；`git add -p` 是把同一文件拆成多次提交的利器。

## Explanation

### 一次性配置

```bash
git config --global user.name  "你的名字"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global core.editor vim
git config --global --list
```

配置三层作用域，就近覆盖：`--system` < `--global` < `--local`（当前仓库默认）。

### 核心循环

```bash
mkdir demo && cd demo
git init                      # 只创建 .git/，不动工作区文件
echo 'hello' > a.txt
git status                    # 先看，再动手
git add a.txt
git commit -m "feat: 添加首个文件 a.txt"
git log --oneline --graph --decorate -n 5
```

### `git status` 是三个区的翻译器

```
Untracked files:          ← 仓库没见过，暂存区也没有
Changes not staged:       ← 工作区改了，暂存区还是旧的
Changes to be committed:  ← 暂存区有了，下次 commit 就拍这个
```

### add 的三种粒度

- `git add a.txt` 精确到文件，最常用
- `git add -A` 全部，容易把临时脚本卷进来
- `git add -p a.txt` 交互式分块，同一文件分两次提交

### `.gitignore`

普通文本文件，放仓库根目录，声明不被跟踪的路径；本身应当被 commit。

## Key Examples

`git add -p` 的真实交互（一个文件里改了两处，拆成两个 commit）：

```
$ git add -p a.txt
@@ -1,5 +1,5 @@
-line 2
+line 2 CHANGED
(1/2) Stage this hunk [y,n,q,a,d,j,J,g,/,e,?]?   ← y
@@ -7,6 +7,6 @@
-line 10
+line 10 CHANGED
(2/2) Stage this hunk [y,n,q,a,d,K,g,/,e,?]?     ← n

$ git commit -m "feat: 修改第 2 行"
$ git add a.txt && git commit -m "feat: 修改第 10 行"

$ git log --oneline
f4d9556 feat: 修改第 10 行
5cd6679 feat: 修改第 2 行
562bdac init: 12 行
```

按键：`y` 收、`n` 跳过、`s` 再拆小、`q` 退出、`e` 手工编辑。
`-p` 只决定"哪些改动进暂存区"，真正切分历史的是每一次 `commit`。

`commit -m` 的内容属于这次的 commit（提交说明），不属于分支；分支只是一个指向 commit 的指针。

## Gotchas

- `.gitignore` 只对**未被跟踪**的文件生效；已 commit 过的文件需 `git rm --cached <file>` 先摘掉跟踪。
- 空目录不会被 Git 跟踪。
- 提交信息首行 ≤ 50 字符，先写"做了什么"，正文再说"为什么"。
- 判断提交粒度：这个 commit 能否被单独 revert 而不牵连其他改动。

## Visualization

<!-- 暂无 -->

## Related Topics

Git 与 GitHub 入门 · c3 看历史与撤销

---

# c3 · 看历史与撤销

## TL;DR

- `git log` 看历史（沿父链回溯），`git branch` 才是看分支。
- `git diff` 三张脸：工作区 vs 暂存区 / 暂存区 vs HEAD / 工作区 vs HEAD。
- 撤销先分层：未 add → `restore`；已 add → `restore --staged`；已 commit 未 push → `reset` 三档；已 push → `revert`。

## Explanation

### 1. `git log` 与 `git branch` 的区别

`git log --oneline` 每个 commit 一行：`短哈希 + 提交信息首行`，沿 parent 链往回走，显示"发生过什么"。

```bash
git branch -vv                          # 看分支（* 标记当前）
git log --oneline --graph --all -n 4    # 看历史（--all 才含所有分支）
```

`git branch` 显示"现在有哪些指针"，`git log` 显示历史线。

### 2. `git diff` 三张脸

```
              git diff                        git diff --staged
工作区 ─────────────────► 暂存区 ─────────────────────► 最新 commit
        ◄─────────────────        ◄─────────────────────
          git restore              git restore --staged
```

```bash
git diff                 # 工作区 vs 暂存区（还没 add 的）
git diff --staged        # 暂存区 vs 最新 commit（下次提交会包含什么）
git diff HEAD            # 工作区 vs 最新 commit（两者之和）
```

习惯：commit 前先 `git diff --staged` 扫一眼。

### 3. `git log` 常用过滤

```bash
git log -p -2                          # 最近 2 个提交带 diff
git log --author="li" --since="2 weeks ago"
git log --oneline -- src/main.c        # 某文件的提交历史
git log -S"TODO" --oneline             # 哪次提交增删了这段字符串
git show f4d9556                       # 单个 commit 改了什么
```

### 4. 撤销：三个命令家族

| 命令 | 碰历史吗 | 用途 | 能公开吗 |
|---|---|---|---|
| `git restore` | 不碰 | 撤工作区 / 撤暂存区的未提交改动 | 随便用 |
| `git reset` | 改写指针 | 撤已提交但没 push 的 commit | 只限本地 |
| `git revert` | 追加一条新 commit | 撤已 push 的改动 | 安全，可公开 |

```bash
git restore a.txt                   # 工作区 ← 暂存区（丢弃未 add 的修改）⚠️
git restore --staged a.txt          # 暂存区 ← HEAD（取消 add，工作区不动）
git restore --source=HEAD~1 a.txt   # 把文件恢复成上个版本
```

### 5. reset 三档：只差"两个区要不要跟着回退"

`reset` 的第一步永远是"把 HEAD 往回挪一格"，三档差别在后续两步：

```
                      HEAD   暂存区(index)   工作区
--soft     挪指针      ✔回退   不动            不动    → 改动全在暂存区
--mixed    挪指针      ✔回退   重置到目标       不动    → 改动退回工作区
--hard     挪指针      ✔回退   重置到目标       重置    → 未提交的东西一起消失
```

## Key Examples

三个副本、同一初始状态（HEAD 在 c2，工作区还有未提交的 v3），只改 reset 档位：

```
=== reset --soft HEAD~1 ===
HEAD: c1   a.txt=v3-未提交   b.txt 还在
git status --short:  MM a.txt     A  b.txt   ← 暂存区有内容，全在里面

=== reset --mixed HEAD~1 ===
HEAD: c1   a.txt=v3-未提交   b.txt 还在
git status --short:   M a.txt     ?? b.txt   ← 暂存区空了，全退回工作区

=== reset --hard HEAD~1 ===
HEAD: c1   a.txt=v1          b.txt 没了
git status --short:  (干净)                  ← 全部抹掉
```

- `--soft`：撕下来放回桌上，内容与暂存状态全保留。适合合并 commit、改提交信息（`reset --soft HEAD~3` 把三次揉成一次）。
- `--mixed`（默认）：撕下来但打散，提交没了、改动还在但未 add。适合重新组织提交。
- `--hard`：撕下来还碎掉，未提交的改动永久消失。

```bash
git add forgotten.c
git commit --amend --no-edit    # 把漏掉的文件并进上一个提交
git commit --amend              # 顺便改提交信息
```

`--amend` 只改最近一次、且还没 push 的提交。

## Gotchas

- 撤销前先想清楚"要撤的东西在哪一层"，用决策树而不是凭记忆。
- `--hard` 前 `git status` 确认一次；执行后 `git reflog` 仍可捞回指针（默认 90 天），但**从未 add 过的文件内容不在 Git 里，reflog 也救不了**。
- 已 push 的历史不要 `reset`，会打断别人的分支；用 `git revert` 追加反向提交。
- `git diff` 不带参数看不到已 add 的内容，别误以为"改动没了"。

## 撤销决策树

```
要撤的东西在哪？
├─ 只在工作区，还没 add      → git restore <file>
├─ 已经 add，还没 commit     → git restore --staged <file>
├─ 已经 commit，没 push
│   ├─ 想保留改动重新提交     → git reset --soft HEAD~1
│   ├─ 想重新挑要 add 的     → git reset --mixed HEAD~1   (默认)
│   └─ 彻底不要了            → git reset --hard HEAD~1   ⚠️
└─ 已经 push 出去了          → git revert <commit>   （别 reset！）
```

## Visualization

<!-- 暂无 -->

## Related Topics

Git 与 GitHub 入门 · c4 分支与合并

---

# c4 · 分支与合并

## TL;DR

- 分支只是一个指向 commit 的指针；`git switch` 只是"改指针 + 更新工作区"，不复制代码。
- merge 有两种：目标分支没动过 → **快进**（不产生 commit）；双方都前进过 → **三方合并**（产生合并提交）。
- 冲突不是出错，是 Git 不敢替你决定；解决三步：改文件 → `git add` → `git commit`。
- rebase 把提交"重贴"成直线，**不能用于已 push 的共享分支**。

## Explanation

### 1. 分支操作

```bash
git branch                    # 列出，* 是当前
git switch -c feature-a       # 新建并切过去
git switch main               # 切回
git branch -d feature-a       # 删除（已合并才允许；未合并用 -D 强删）
git branch -vv                # 带上游跟踪信息
```

切换不复制代码，只改指针并把工作区更新成该快照。切分支前要 `commit` 或 `stash`，否则未提交的改动会被带过去。

### 2. 快进 vs 三方合并

快进：目标分支自己没动过，指针直接前移，**不产生新 commit**。

```
$ git merge feature-a
更新 8bdce73..f653d32
Fast-forward

* f653d32 (HEAD -> main, feature-a) c1: A 的改动
* 8bdce73 c0 base
```

三方合并：两边各自前进过，用共同祖先 + 两边内容算出新快照，生成合并提交（两个父提交）。

```
$ git merge --no-edit feature-b
Merge made by the 'ort' strategy.

*   b5309d4 (HEAD -> main) Merge branch 'feature-b'
|\
| * 380f27c (feature-b) c2: B 加 g.txt
* | 4a1f7ad c3: main 加 h.txt
|/
* f653d32 c1: A 的改动
```

`git merge --no-ff` 强制留下合并记录，便于看清功能边界。

### 3. 冲突

```
$ git merge feature-c
自动合并 cfg.py
冲突（添加/添加）：合并冲突于 cfg.py
退出码: 1

<<<<<<< HEAD
version = "main"
=======
version = "feature"
>>>>>>> feature-c

$ git status --short
AA cfg.py
```

标准三步：

1. 编辑文件，删掉 `<<<<<<<` / `=======` / `>>>>>>>` 三行，留最终内容
2. `git add cfg.py`
3. `git commit`

反悔：`git merge --abort`。

### 4. rebase

```
merge:  保留真实分叉 → A─B─C─D─M（M 两个父）
rebase: 提交重贴到目标末尾 → A─B─C─D─E'─F'（一条直线）
```

```bash
git switch feature && git rebase main
```

黄金法则：不要 rebase 已 push 的共享提交——会生成新哈希，别人的历史对不上。个人分支整理用 rebase，公共分支只用 merge。

### 5. 日常形态

```
main ──●───────────────●──●────────
        \             /  /
         ●──●──●─────●  /
                  \    /
                   ●───●
```

一个功能一条分支，做完 PR 合回 main。

## Gotchas

- 切分支前有未提交改动：先 `commit` 或 `git stash`。
- `git branch -d` 拒绝删除未合并分支是保护，别急着 `-D`。
- 冲突标记行必须全部删干净，残留 `<<<<<<<` 会进代码。
- 冲突时 `git status` 的 `AA`/`UU` 表示"待解决"，`git add` 后变 `M`。
- rebase 过程中冲突每个提交都要解一次，`git rebase --abort` 可回退。

## Visualization

<!-- 暂无 -->

## Related Topics

Git 与 GitHub 入门 · c5 远程仓库

---

# c5 · 远程仓库

## TL;DR

- `remote` 只是一个 URL 别名；`origin/main` 是本地缓存的"远程状态"，只在 fetch 时更新。
- `push` 本→远（送出新提交），`pull` 远→本（= fetch + merge/rebase）。
- push 被拒 = 远程有你没有的提交；正确解法是 fetch → pull --rebase → push，**不是 --force**。

## Explanation

### 1. "远程"是什么

```bash
git remote add origin git@github.com:you/repo.git
git remote -v
```

`origin` 只是默认别名。远程跟踪分支（`origin/main`）是本地缓存，只有 `fetch` 时才更新，不会自己变。

```
本地:  main ──────●   ← 你的工作分支
                    ↑ 手动合并
缓存:  origin/main ──●  ← fetch 时更新成远程的样子
远程:  GitHub 上的 main
```

### 2. fetch / pull / push 方向表

```
            push  （本 → 远，只送"新提交"，远程分支前移）
本地 main ───────────────────────────────► 远程 main
本地 main ◄─────────────────────────────── 远程 main
            pull  （远 → 本，= fetch + merge/rebase）
```

| 命令 | 更新 `origin/main` | 动你的 `main` | 产生合并提交 |
|---|---|---|---|
| `git fetch` | ✅ | ❌ | ❌ |
| `git pull`（默认） | ✅ | ✅ merge | 可能会 |
| `git pull --rebase` | ✅ | ✅ rebase | ❌ |
| `git clone` | 全套（首次） | ✅ | — |
| `git push` | 反向 | — | 不产生 |

**fetch 是侦察，pull 是侦察并合并。**

### 3. 推送与被拒

```bash
git push -u origin main     # 首次：-u 记住上游，之后直接 git push
git push                    # 日常
```

```
$ git push
 ! [rejected]        main -> main (fetch first)
提示：更新被拒绝，因为远程仓库包含您本地尚不存在的提交。
```

正确四步：

```bash
git fetch origin
git log --oneline main..origin/main   # 看差了什么
git pull --rebase                     # 把自己的提交接到最新上面
git push
```

绝不要用 `git push --force` 解决——会抹掉别人的提交。

### 4. 把远程拉到本地的三种情况

**① 本地没有这个仓库** → `git clone git@github.com:you/repo.git`

**② 已有仓库，别人推了新提交** → `git pull --rebase`

```bash
git fetch origin
git log --oneline main..origin/main
git diff main origin/main
git merge origin/main
```

**③ 只想要远程某个分支**

```bash
git fetch origin
git switch -c feature-x origin/feature-x
```

### 5. 典型的一天

```bash
git switch -c feature-login
# ... 写代码 ...
git add -p && git commit -m "feat: 登录接口"
git pull --rebase                # 推之前先收一手
git push -u origin feature-login
```

## Key Examples

远程被别人先推了 c2 之后的真实过程：

```
$ git fetch origin
$ git log --oneline -1 origin/main
a09af6c c2 from other          ← origin/main 更新了
                               ← 你的 main 没动

$ git pull --rebase
成功变基并更新 refs/heads/main。

$ git log --oneline --graph -4
* 500055a (HEAD -> main, origin/main) c3 local
* a09af6c c2 from other
* 6ae60a7 c1
```

## FAQ（学员当场提问）

**Q1: pull 和 push 的区别？**
方向相反：push 本地→远程（送出新提交），pull 远程→本地（fetch + 合并）。push 不改本地代码；pull 会更新工作区，可能冲突。push 危险动作只有 `--force`，pull 最坏是冲突。

**Q2: 推送到远程仓库之后，怎么拉取到本地？**
三种：本地没有 → `git clone`；已有 → `git pull --rebase`（或 `fetch` 先看再 merge）；只要某个分支 → `fetch` 后 `git switch -c <本地名> origin/<分支名>`。

**Q3: push 和 commit 的区别？一个本地一个远程么？**
方向对，但关键差别在"产生什么"：

| | commit | push |
|---|---|---|
| 写到哪 | 本地 `.git` | 远程 |
| 需要网络 | 不需要 | 需要 |
| 产生新提交 | 产生 | **不产生**，只是复制已有提交 |
| 反悔成本 | 低（reset/amend） | 高（要 revert，别人可能已拉走） |
| 可见性 | 只有你 | 公开 |

```
工作区 → add → 暂存区 → commit → 本地仓库 → push → 远程
                        ↑ 私事              ↑ 这一步才是"发布"
```

commit 只是本地快照，**硬盘坏了就没了**；push 才是备份。

**Q4: A 电脑 commit 但没 push，B 电脑 pull 能看到吗？**
不能。提交只在 A 的本地仓库，从未到过远程，pull 拿不到。需要先在 A `push`。

**Q5: 离线 commit 了 3 次，联网后 push 一次，远程多出几个 commit？**
**3 个**。push 传的是"远程没有的提交集合"（`origin/main..HEAD` 里的全部），不是一次同步动作生成一个。
推论：push 前用 `git log origin/main..HEAD` 和 `git diff origin/main` 自检——这一步最容易漏掉误提交的密钥。

## Gotchas

- `origin/main` 不会自动更新，想知道远程最新状态必须 fetch。
- push 被拒不等于要 force；force 会覆盖别人的提交。
- `pull` 默认可能产生 merge commit；团队通常约定 `pull --rebase`（可全局配置 `git config --global pull.rebase true`）。
- `git remote set-url origin <新url>` 用于 GitHub 改名或 HTTPS→SSH。
- `git fetch --prune` 清理远程已删除的分支引用。

## Visualization

<!-- 暂无 -->

## Related Topics

Git 与 GitHub 入门 · c6 GitHub 协作

---

# c6 · GitHub 协作

## TL;DR

- 有权写 → 开分支走 PR；无权写 → **Fork** 到自己账号再 PR。
- PR 流程：更新 main → 开分支 → 小步提交 → push 分支 → 网页创建 PR → Review 后合并。
- commit 用 Conventional Commits：`<type>(<scope>): <subject>`。

## Explanation

### 1. 谁有权推

| 关系 | 能否直接 push 主仓库 | 典型做法 |
|---|---|---|
| Owner / Collaborator | ✅ | 仍建议开分支走 PR |
| 组织成员（写权限） | ✅ | 同上 |
| 外部贡献者 | ❌ | Fork 到自己账号 → 改 → PR 回原仓库 |

Fork vs 分支：分支在**同一个仓库**内；Fork 是**你账号下的一份完整副本**。开源走 Fork，公司内部走分支。

### 2. PR 完整流程

```bash
git switch main && git pull --rebase
git switch -c feature/login
git add -p && git commit -m "feat(login): 增加短信验证码登录"
git push -u origin feature/login      # 推分支，不是推 main
# → 终端打印创建 PR 的链接
```

PR 页面四块：Conversation（讨论/CI）、Commits、Checks、Files changed（逐行评论）。

Reviewer 提意见后：**在同一分支继续 commit + push**，PR 自动更新，无需重开。

| 合并方式 | 结果 | 适用 |
|---|---|---|
| Merge commit | 保留分叉 + 合并提交 | 团队默认 |
| Squash and merge | 多条压成一条 | 提交很碎 |
| Rebase and merge | 线性历史 | 要求直线 |

### 3. Issue

任务/bug 追踪单元。PR 描述写 `Closes #123`，合并时自动关闭。
规范链条：Issue → 分支 → PR → Review → 合并，让"为什么改"有据可查。

### 4. Conventional Commits

```
<type>(<scope>): <subject>

feat(login): 增加短信验证码登录
fix(api): 修正分页越界
docs: 补充部署说明
refactor(core): 拆分 parser
test: 补 c5 远程分支用例
chore: 升级依赖
```

好处：一眼看出改动性质、能自动生成 CHANGELOG、可按类型过滤历史。

### 5. 完整协作模型

```
upstream (原仓库) ──fork──► 你的 fork (origin)
      ▲                        │
      │ PR                     │ push
      └────────────────────────┘
        git remote add upstream <原仓库url>
        git fetch upstream && git rebase upstream/main
```

## Gotchas

- 分支从旧 main 开的，PR 会混进无关改动：先 `git fetch` 再 `git rebase origin/main`。
- Fork 工作流有两个 remote（origin = 你的 fork，upstream = 原仓库），推之前 `git remote -v` 确认。
- 别人正在 review 的分支不要强推；只有自己独占的分支可 `--force-with-lease`。
- 直接 push 到 main 会绕过 review，很多仓库已用分支保护禁掉。

## Visualization

<!-- 暂无 -->

## Related Topics

Git 与 GitHub 入门 · 全部完成

---

# 补充 · Pull Request 深讲

## 名字的由来

不是"请求推送"，而是"**请把我这条分支 pull 到你的仓库里去**"。

```
你的 fork / 分支                    原仓库 main
  feature/login ──●──●──●            ●──●
                 │
                 └─ "麻烦你把我的提交 pull 过去"  → Pull Request
```

PR **不是 Git 的命令**，是 GitHub 平台的功能（GitLab 叫 Merge Request，意思相同）。

## 本质：两个分支的差异 + 一个讨论帖

```
base:    main            ← 合到哪（目标）
compare: feature/login   ← 从哪来（你的分支）
```

对比是动态的：继续往 `feature/login` 推提交，PR 自动把新提交算进去，**不需要新建 PR**。

## 完整生命周期

```
1. 开分支干活     git switch -c feature/login
2. 小步提交       git commit -m "feat(login): ..."
3. 推分支         git push -u origin feature/login
4. 创建 PR        填标题 + 描述
5. 自动检查       CI（Checks 全绿才能合）
6. Review         评论 → 改 → 再 push（PR 自动更新）
7. 合并           Merge / Squash / Rebase
8. 收尾           删远程分支、本地删分支
```

状态：Open → Merged 或 Closed（关了没合）。

## 改代码后 PR 怎么更新

```bash
git add -p
git commit -m "fix(login): 处理验证码过期"
git push          # 只有这一句，PR 自动刷新
```

分支落后 main 时：

```bash
git fetch origin
git rebase origin/main
git push --force-with-lease    # 只能对自己独占的 PR 分支
```

网页上点 "Update branch" 也可以，但会生成一个 merge commit。

## Review 的三种动作

| 动作 | 含义 | 你要做的 |
|---|---|---|
| Comment | 评论/提问 | 回复或改代码 |
| Approve | 同意合并 | 等有权限的人点 Merge |
| Request changes | 必须改完才能合 | 改 → push → 等重新 approve |

## 实用细节

```bash
# 别人的 PR 想在本地跑
git fetch origin pull/123/head:pr-123
git switch pr-123

# 描述里写 Closes #45 → 合并时自动关闭 Issue 45

# 没写完先开 Draft PR，防止误 merge

# Fork 工作流
git remote add upstream git@github.com:原作者/repo.git
git fetch upstream && git rebase upstream/main
```

## 最容易混的三个点

- **PR ≠ 分支**：分支是 Git 的，PR 是平台的；分支删了 PR 仍归档存在。
- **PR 合并 ≠ 本地 main 更新**：合并后要 `git switch main && git pull`。
- **冲突不一定在网页解决**：复杂冲突本地 `git rebase origin/main` 解完再推。

## 学员提问

**Q: 开 PR 后改一行再 push，需要新建 PR 吗？**
不需要。PR 跟踪的是分支，分支新增提交 PR 自动更新；只有换分支才需要新 PR。
