# GitHub 上传与公网部署说明

## 1. 目标

这份文档解决两件事：

- 把当前项目上传到 GitHub
- 把项目部署到公网，让所有人都可以访问

当前最推荐的部署方案是：

- 代码托管：GitHub
- 前端部署：Vercel
- 后端部署：Render
- MySQL 数据库：Railway MySQL 或你自己的云数据库

这样拆分的原因是：

- React 前端部署到 Vercel 最简单
- FastAPI 后端部署到 Render 稳定直观
- MySQL 需要单独托管，Railway 上手最省事

---

## 2. 部署前必须知道的事情

当前项目不是纯静态站点，而是三部分协同：

1. 前端网页
2. 后端接口
3. MySQL 数据库

所以真正上线时，不是只传一个前端就结束，而是要让：

- 前端能访问公网后端地址
- 后端能连接公网数据库

为此我已经帮你做好了以下准备：

- 前端改成通过环境变量读取 API 地址
- 后端支持通过环境变量配置 CORS 域名
- 增加了 `.env.example` 模板文件
- 增加了生产环境变量模板文件
- 增加了 `vercel.json`，避免 React Router 刷新 404
- 增加了 `render.yaml`，方便直接在 Render 中按仓库配置部署

---

## 3. 先上传到 GitHub

### 3.1 在 GitHub 创建仓库

先登录 GitHub，新建一个空仓库。

建议仓库名：

```text
408-grad-info-hub
```

创建时建议：

- Repository name：`408-grad-info-hub`
- Visibility：Public 或 Private 都可以
- 不要勾选自动添加 README、.gitignore、License

创建完成后，GitHub 会给你一个仓库地址，例如：

```text
https://github.com/你的用户名/408-grad-info-hub.git
```

或者：

```text
git@github.com:你的用户名/408-grad-info-hub.git
```

---

### 3.2 本地初始化 Git

进入项目根目录：

```bash
cd /Users/macbook/Desktop/408project/information
```

初始化仓库：

```bash
git init
```

查看状态：

```bash
git status
```

---

### 3.3 提交代码

先把所有文件加入版本控制：

```bash
git add .
```

提交：

```bash
git commit -m "feat: initial 408 grad info hub project"
```

如果 Git 提示你没有用户名或邮箱，请先设置：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

然后重新提交。

---

### 3.4 绑定 GitHub 仓库

把远程仓库地址替换成你自己的：

```bash
git remote add origin https://github.com/你的用户名/408-grad-info-hub.git
```

把默认分支改为 `main`：

```bash
git branch -M main
```

推送：

```bash
git push -u origin main
```

如果你使用 HTTPS 推送，GitHub 现在通常需要 Token，而不是密码。

---

## 4. GitHub Token 的使用

如果 `git push` 时要求认证：

1. 打开 GitHub
2. 进入 `Settings`
3. 进入 `Developer settings`
4. 进入 `Personal access tokens`
5. 创建新 token
6. 勾选至少仓库相关权限

推送时：

- Username：你的 GitHub 用户名
- Password：填 GitHub Token

---

## 5. 公网部署推荐方案

### 推荐方案

- 前端：Vercel
- 后端：Render
- 数据库：Railway MySQL

这是目前最适合你这个项目结构的组合。

---

## 6. 第一步：部署 MySQL

### 方案 A：Railway MySQL

在 Railway 新建一个 MySQL 服务。

创建后你会拿到一组连接信息，通常包括：

- host
- port
- user
- password
- database

然后拼成：

```env
DATABASE_URL=mysql+pymysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4
```

例如：

```env
DATABASE_URL=mysql+pymysql://root:abc123@containers-us-west-xxx.railway.app:6543/railway?charset=utf8mb4
```

---

## 7. 第二步：部署后端到 Render

### 7.1 新建 Web Service

在 Render 中：

1. 选择 New
2. 选择 Web Service
3. 连接你的 GitHub 仓库
4. 选择这个项目仓库

---

### 7.2 Render 的关键配置

因为后端代码在 `backend/` 子目录，所以建议配置如下：

- Root Directory：`backend`
- Runtime：Python

如果你想少手动填一些内容，也可以直接使用仓库根目录的：

- [render.yaml](file:///Users/macbook/Desktop/408project/information/render.yaml)

Build Command：

```bash
pip install -r requirements.txt
```

Start Command：

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

### 7.3 Render 环境变量

在 Render 的 Environment Variables 中填写：

```env
DATABASE_URL=mysql+pymysql://你的数据库用户名:你的数据库密码@你的数据库主机:端口/数据库名?charset=utf8mb4
CORS_ORIGINS=https://你的前端域名.vercel.app
```

如果你暂时还没有前端正式域名，可以先填：

```env
CORS_ORIGINS=*
```

上线后再改成正式前端域名更安全。

你也可以直接参考：

- [backend/.env.production.example](file:///Users/macbook/Desktop/408project/information/backend/.env.production.example)

---

### 7.4 初始化线上数据库

后端部署成功后，数据库表还需要初始化。

你有两种方式：

#### 方式 1：在本地用线上数据库地址初始化

把本地 [backend/.env](file:///Users/macbook/Desktop/408project/information/backend/.env) 临时改成线上数据库地址，然后执行：

```bash
cd /Users/macbook/Desktop/408project/information/backend
source venv/bin/activate
python init_db.py
```

再执行：

```bash
cd /Users/macbook/Desktop/408project/information/scraper
source venv/bin/activate
python seed_comprehensive_408.py
```

这样就会把数据写进线上 MySQL。

#### 方式 2：在云平台 shell 中执行

如果平台支持 shell，也可以在服务器环境内执行初始化脚本。

---

## 8. 第三步：部署前端到 Vercel

### 8.1 导入 GitHub 仓库

在 Vercel 中：

1. 选择 Add New Project
2. 导入 GitHub 仓库
3. 选择当前项目

---

### 8.2 Vercel 项目配置

因为前端代码在 `frontend/` 子目录，所以配置：

- Framework Preset：Vite
- Root Directory：`frontend`

Build Command：

```bash
npm run build
```

Output Directory：

```bash
dist
```

---

### 8.3 Vercel 环境变量

在 Vercel 中配置：

```env
VITE_API_BASE_URL=https://你的后端域名.onrender.com
```

例如：

```env
VITE_API_BASE_URL=https://grad-info-408-api.onrender.com
```

我已经帮你把前端改成读取这个环境变量，所以这是上线必填项。

可直接参考：

- [frontend/.env.production.example](file:///Users/macbook/Desktop/408project/information/frontend/.env.production.example)

---

### 8.4 React Router 刷新问题

我已经帮你加入了：

- [vercel.json](file:///Users/macbook/Desktop/408project/information/frontend/vercel.json)

作用是：

- 解决刷新详情页、列表页时出现 404 的问题

---

## 9. 上线后的最终访问链路

上线成功后，访问路径会变成：

- 用户访问前端：`https://你的前端域名.vercel.app`
- 前端请求后端：`https://你的后端域名.onrender.com/api/...`
- 后端读取数据库：Railway MySQL

---

## 10. 你实际要做的最短步骤

如果你想最快上线，按这个顺序来：

### 第一步：传 GitHub

```bash
cd /Users/macbook/Desktop/408project/information
git init
git add .
git commit -m "feat: initial project"
git branch -M main
git remote add origin https://github.com/你的用户名/408-grad-info-hub.git
git push -u origin main
```

### 第二步：开 Railway MySQL

- 创建 MySQL
- 拿到数据库连接串

### 第三步：部署 Render 后端

- Root Directory 选 `backend`
- 配置 `DATABASE_URL`
- 启动命令填：

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 第四步：导入线上数据

本地把 `.env` 改成线上数据库地址，然后执行：

```bash
cd /Users/macbook/Desktop/408project/information/backend
source venv/bin/activate
python init_db.py
```

```bash
cd /Users/macbook/Desktop/408project/information/scraper
source venv/bin/activate
python seed_comprehensive_408.py
```

### 第五步：部署 Vercel 前端

- Root Directory 选 `frontend`
- 配置：

```env
VITE_API_BASE_URL=https://你的Render后端域名
```

---

## 11. 部署前检查清单

部署前建议逐条确认：

- GitHub 仓库已创建
- 代码已成功 push 到 GitHub
- MySQL 已准备好公网连接
- 后端环境变量已配置 `DATABASE_URL`
- 前端环境变量已配置 `VITE_API_BASE_URL`
- Render 已能正常打开 `/api/summary`
- Vercel 已能正常打开首页和详情页

---

## 12. 常见问题

### 12.1 前端能打开，但没有数据

大概率是：

- `VITE_API_BASE_URL` 没配
- 后端没部署成功
- 后端 CORS 没配置对
- 数据库没有初始化

---

### 12.2 后端能打开，但接口报数据库错误

大概率是：

- `DATABASE_URL` 错了
- 线上数据库没开放公网连接
- 数据表还没初始化
- 数据还没导入

---

### 12.3 详情页刷新 404

Vercel 部署时必须保留：

- [vercel.json](file:///Users/macbook/Desktop/408project/information/frontend/vercel.json)

---

## 13. 最后建议

我建议你按下面顺序推进：

1. 先把项目上传 GitHub
2. 先部署数据库
3. 再部署后端
4. 后端能返回接口后，再部署前端
5. 最后再做域名绑定

这个顺序最稳，不容易卡住。
