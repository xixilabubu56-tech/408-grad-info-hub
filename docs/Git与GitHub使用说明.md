# Git 与 GitHub 使用说明

## 1. 这份文档是做什么的

这份文档专门讲三件事：

- 怎么在本地使用 Git 管理项目
- 怎么把本地项目连接到 GitHub
- 怎么把代码提交并推送到 GitHub

这份说明适合你当前这个项目，也适合以后其他本地项目使用。

---

## 2. Git 和 GitHub 的区别

先理解两个概念：

- **Git**：本地版本管理工具，用来记录代码变化
- **GitHub**：远程代码托管平台，用来保存代码、同步代码、备份代码

你可以把它理解成：

- Git = 你电脑里的“版本记录器”
- GitHub = 互联网上的“远程仓库”

---

## 3. 先检查本机有没有 Git

在终端执行：

```bash
git --version
```

如果能看到类似：

```bash
git version 2.x.x
```

说明 Git 已经安装好了。

如果没有安装，可以在 macOS 上执行：

```bash
xcode-select --install
```

---

## 4. 第一次使用 Git 前的基础配置

第一次使用 Git，建议先配置用户名和邮箱：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

查看是否配置成功：

```bash
git config --global --list
```

你应该能看到类似：

```bash
user.name=你的GitHub用户名
user.email=你的GitHub邮箱
```

---

## 5. Git 最常用的工作流程

Git 日常最常见的流程其实就 4 步：

### 第一步：查看当前改了什么

```bash
git status
```

### 第二步：把改动加入暂存区

```bash
git add .
```

或者只添加某一个文件：

```bash
git add README.md
```

### 第三步：提交到本地仓库

```bash
git commit -m "写一句说明这次改了什么"
```

例如：

```bash
git commit -m "fix: 修复院校详情页展示问题"
```

### 第四步：推送到 GitHub

```bash
git push
```

---

## 6. 常用 Git 命令速查

### 6.1 查看状态

```bash
git status
```

### 6.2 查看提交历史

```bash
git log --oneline
```

### 6.3 查看当前分支

```bash
git branch
```

### 6.4 查看远程仓库地址

```bash
git remote -v
```

### 6.5 拉取远程最新代码

```bash
git pull
```

### 6.6 推送当前分支

```bash
git push
```

---

## 7. 怎么把一个本地项目变成 Git 仓库

如果你有一个新项目，还没有启用 Git，就进入项目目录执行：

```bash
cd /你的项目目录
git init
```

执行后，当前目录就会变成 Git 仓库。

然后查看状态：

```bash
git status
```

---

## 8. 怎么连接 GitHub 仓库

连接 GitHub 的完整流程如下。

### 8.1 先去 GitHub 创建一个仓库

在 GitHub 中新建一个仓库，例如：

```text
408-grad-info-hub
```

创建时建议：

- 可以选 Public 或 Private
- 不要勾选自动创建 README
- 不要勾选自动创建 `.gitignore`

创建好后，你会拿到一个仓库地址。

例如 SSH 地址：

```text
git@github.com:xixilabubu56-tech/408-grad-info-hub.git
```

或者 HTTPS 地址：

```text
https://github.com/xixilabubu56-tech/408-grad-info-hub.git
```

---

### 8.2 本地初始化并添加远程仓库

进入项目目录：

```bash
cd /Users/macbook/Desktop/408project/information
```

如果还没有 Git 仓库：

```bash
git init
```

把主分支改成 `main`：

```bash
git branch -M main
```

添加远程仓库：

```bash
git remote add origin git@github.com:xixilabubu56-tech/408-grad-info-hub.git
```

如果之前已经加过远程仓库，可以先删除旧的：

```bash
git remote remove origin
git remote add origin git@github.com:xixilabubu56-tech/408-grad-info-hub.git
```

查看是否绑定成功：

```bash
git remote -v
```

---

## 9. 怎么第一次推送到 GitHub

第一次推送通常这样做：

```bash
cd /Users/macbook/Desktop/408project/information
git add .
git commit -m "feat: initial project"
git branch -M main
git push -u origin main
```

解释一下：

- `git add .`：把当前所有改动加入暂存区
- `git commit -m "...”`：生成一次本地提交
- `git branch -M main`：把主分支命名为 `main`
- `git push -u origin main`：第一次把本地 `main` 推送到 GitHub，并建立跟踪关系

---

## 10. 以后怎么继续推送更新

第一次推送成功之后，以后每次更新只需要：

```bash
cd /Users/macbook/Desktop/408project/information
git add .
git commit -m "写这次更新说明"
git push
```

例如：

```bash
git add .
git commit -m "feat: 新增 Git 使用说明文档"
git push
```

---

## 11. 你当前这个项目的实际 Git 状态

当前这个项目已经：

- 初始化为 Git 仓库
- 已连接 GitHub 远程仓库
- 当前分支是 `main`

当前远程仓库地址是：

```text
git@github.com:xixilabubu56-tech/408-grad-info-hub.git
```

你可以自己检查：

```bash
cd /Users/macbook/Desktop/408project/information
git remote -v
git branch --show-current
```

---

## 12. 连接 GitHub 常见的两种方式

### 方式一：SSH

优点：

- 推送时更方便
- 不需要每次输账号密码

仓库地址长这样：

```text
git@github.com:用户名/仓库名.git
```

如果你用 SSH，建议先检查本机有没有 SSH key：

```bash
ls ~/.ssh
```

如果没有，可以生成：

```bash
ssh-keygen -t ed25519 -C "你的GitHub邮箱"
```

然后复制公钥内容：

```bash
cat ~/.ssh/id_ed25519.pub
```

把它粘贴到 GitHub：

- Settings
- SSH and GPG keys
- New SSH key

测试是否连接成功：

```bash
ssh -T git@github.com
```

---

### 方式二：HTTPS

优点：

- 更直观
- 不用配 SSH key

仓库地址长这样：

```text
https://github.com/用户名/仓库名.git
```

缺点：

- 推送时一般需要 GitHub Token

---

## 13. 如果 GitHub 推送失败怎么办

### 13.1 `Permission denied (publickey)`

原因：

- SSH key 没配置好

解决：

1. 生成 SSH key
2. 把公钥加到 GitHub
3. 再执行：

```bash
ssh -T git@github.com
```

---

### 13.2 `remote origin already exists`

原因：

- 已经添加过远程仓库

解决：

```bash
git remote remove origin
git remote add origin 你的仓库地址
```

---

### 13.3 `nothing to commit`

原因：

- 你没有新的改动

这不是报错，说明当前没有新的文件变化可提交。

可以先看：

```bash
git status
```

---

### 13.4 `failed to push some refs`

原因通常是：

- 远程仓库比本地新

先拉取再推送：

```bash
git pull --rebase origin main
git push origin main
```

---

## 14. 适合你现在直接使用的 Git 操作模板

### 查看仓库状态

```bash
cd /Users/macbook/Desktop/408project/information
git status
```

### 提交并推送改动

```bash
cd /Users/macbook/Desktop/408project/information
git add .
git commit -m "写你的更新说明"
git push
```

### 查看远程仓库绑定情况

```bash
cd /Users/macbook/Desktop/408project/information
git remote -v
```

### 查看最近提交

```bash
cd /Users/macbook/Desktop/408project/information
git log --oneline -5
```

---

## 15. 一句话版

如果你只想记住最核心的 Git/GitHub 用法，就记住这几条：

### 新项目第一次上传

```bash
git init
git add .
git commit -m "feat: initial project"
git branch -M main
git remote add origin git@github.com:你的用户名/你的仓库.git
git push -u origin main
```

### 平时更新代码

```bash
git add .
git commit -m "写更新说明"
git push
```

### 查看现在是什么状态

```bash
git status
git remote -v
git branch --show-current
```
