# 408 统考研究生招生信息库 (408 Grad Info Hub)

这是一个自动查询全国计算机类统考 408 研究生招生信息的网站项目。

## 🎯 项目目标
- 从“研招网”和“各大高校官网”实时/定期收集考研408相关专业的招生信息。
- 汇总展示：院校列表、专业详情、招生简章、历年复试及录取分数线、官方通知等权威信息。
- 提供 Apple 极简设计风格的 UI，为考生提供清爽、直观的浏览体验。

## 🛠️ 技术栈
### 前端 (Frontend)
- 框架：React + Vite (TypeScript)
- 样式：Tailwind CSS (Apple Design Style / 极简拟物与玻璃态)
- 状态管理/路由：React Router, Zustand/Redux (待定)

### 后端 (Backend API)
- 框架：Python + FastAPI
- 数据库连接：SQLAlchemy
- 接口风格：RESTful API

### 爬虫 (Scraper)
- 语言：Python
- 工具库：Scrapy / BeautifulSoup4 / Selenium / Requests
- 任务调度：Celery 或 简单的 Cron 定时任务（用于实时更新和定时全量爬取）

### 数据存储 (Database)
- 数据库：MySQL
- 主要表结构：
  - 院校表 (Institutions)
  - 专业表 (Majors)
  - 招生简章/通知 (Notices)
  - 历年数据 (Historical Data)

## 📁 目录结构
```text
/
├── frontend/       # React 前端应用
├── backend/        # FastAPI 后端接口
├── scraper/        # Python 爬虫模块
└── docs/           # 项目文档及数据库设计
```

## 📘 使用说明

完整使用手册请查看：

- [使用说明.md](file:///Users/macbook/Desktop/408project/information/docs/使用说明.md)
- [Git与GitHub使用说明.md](file:///Users/macbook/Desktop/408project/information/docs/Git与GitHub使用说明.md)

快速启动：

1. 启动 MySQL
2. 执行数据导入脚本
3. 启动 FastAPI 后端
4. 启动 React 前端

注意：

- `npm run dev` 和 `npm run build` 必须在 `frontend/` 目录执行
- `uvicorn main:app --reload --port 8000` 必须在 `backend/` 目录执行
- 数据刷新推荐执行 `scraper/seed_comprehensive_408.py`

## 🚀 后续开发计划
1. **[进行中]** 初始化项目结构。
2. **[待办]** 设计 MySQL 数据库表结构，包含各个业务实体的关联关系。
3. **[待办]** 开发 Python 爬虫，定向采集研招网及特定高校官网的408统考信息。
4. **[待办]** 开发 FastAPI 后端，提供数据 API。
5. **[待办]** 完善 React 前端界面及搜索、筛选、展示等交互功能。
6. **[待办]** 联调测试及部署上线。
