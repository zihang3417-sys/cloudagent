# CloudAgent GitHub 发布方案

## 当前情况

原始仓库：

```text
https://github.com/zihang3417-sys/cloudagent
```

企业级副本：

```text
F:\agent0520\cloudagent_enterprise
```

企业级副本当前 remote 指向同一个 GitHub 仓库：

```text
origin https://github.com/zihang3417-sys/cloudagent.git
```

## 推荐方案

建议保留原来的 GitHub 仓库地址，把它升级成公开展示用的企业级版本，同时把原来的学习原型保留成分支。

推荐结构：

```text
main                 -> 企业级改造后的 CloudAgent
learning-prototype   -> 原始学习/玩具原型版本
enterprise-mvp-v1    -> 最终简历版 tag
```

这样做的好处：

- 简历上只放一个 GitHub 地址，干净、集中。
- 面试官打开默认 `main` 就能看到最强版本。
- 原来的学习项目不会丢，只是换到 `learning-prototype` 分支。
- 项目演进路线很自然：学习 Demo -> 企业级 AI Agent MVP。

## 备选方案

也可以新建一个仓库：

```text
cloudagent-enterprise
```

适合你完全不想动原仓库 `main` 的情况。

缺点是简历上可能要解释两个仓库，注意力会分散。除非你特别想保留原仓库主页，否则我更推荐使用同一个仓库。

## 推荐推送流程

执行前一定先确认两个目录的 Git 状态，不要把 `.env`、`.venv`、`node_modules`、`data`、SQLite 文件或 API Key 推上去。

### 1. 在原项目里保存学习版分支

```powershell
cd F:\agent0520\cloudagent
git status
git branch learning-prototype
git push origin learning-prototype
```

然后去 GitHub 网页确认 `learning-prototype` 分支确实存在。

### 2. 在企业副本里做最终验证

```powershell
cd F:\agent0520\cloudagent_enterprise
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe cloud_agent\evals\run_eval.py --mode static
.\.venv\Scripts\python.exe cloud_agent\evals\run_eval.py --mode route
docker compose -f infra\docker-compose.yml -f infra\docker-compose.enterprise.yml config --quiet
```

### 3. 推送企业版到 main

```powershell
cd F:\agent0520\cloudagent_enterprise
git status
git push origin main
```

如果 Git 提示远端历史不一致，先停下来检查，不要立刻 force push。只有确认 `learning-prototype` 已经备份成功后，才考虑是否强推。

### 4. 可选：打一个简历版本 tag

```powershell
git tag enterprise-mvp-v1
git push origin enterprise-mvp-v1
```

这样你以后可以明确告诉面试官：简历使用的是 `enterprise-mvp-v1` 版本。

## README 首页建议

README 开头建议直接写中文：

```text
CloudAgent Enterprise 是一个面向云平台客服/运维场景的企业级 AI 助手 MVP。项目基于 FastAPI + Vue3 + LangGraph 构建，融合 Multi-Agent 编排、MCP-style 业务工具、RAG/GraphRAG、记忆系统、语义缓存、可观测性、安全边界、CI/Eval 与部署就绪骨架，适合作为小公司内部 AI 助手试点或简历项目展示。
```

README 推荐顺序：

1. 项目能做什么。
2. 架构图。
3. 快速启动。
4. 推荐演示问题。
5. 企业级改造点。
6. 当前边界。
7. 简历/面试如何表述。

## 不要发布的内容

不要发布：

- `.env`
- `.env.container`
- `.venv/`
- `node_modules/`
- `data/`
- SQLite checkpoint 文件
- API Key
- 本地 IDE 配置

当前 `.gitignore` 和 `.dockerignore` 已经覆盖这些类别，但每次 push 前仍然要看：

```powershell
git status --short
```
