# CloudAgent Enterprise 客户介绍与快速启动

## 给客户的一句话介绍

CloudAgent Enterprise 是一个面向云平台客服/运维场景的内部 AI 助手 MVP。它可以帮助用户用自然语言查询订单、云服务器实例、产品知识、成本优化建议和推广物料。

它不是一个简单聊天机器人，而是一个完整的 AI 应用原型，包含：

- Web 聊天界面。
- FastAPI 流式后端。
- LangGraph 多 Agent 编排。
- Billing、Product、Recommendation、Promotion、FinOps 等专家 Agent。
- 订单、实例、监控、商品、推广物料等业务工具。
- Milvus 文档 RAG。
- Neo4j GraphRAG。
- Redis/Milvus 记忆与缓存。
- 日志、指标、健康检查、CI、限流、超时、安全拦截等工程化骨架。

## 客户能用它做什么

用户可以问：

```text
帮我查一下最近的订单。
帮我看看我名下运行中的云服务器实例。
什么是 VPC？
服务器利用率低，怎么节省成本？
我是 Java 接口服务 + MySQL，2 核 4G 够吗？
ecs.g8a.xlarge 支持多少块弹性网卡？
```

系统会根据问题类型路由到对应专家 Agent，必要时调用业务工具、RAG 或 GraphRAG，然后把答案流式返回到浏览器。

## 最简单的理解方式

```text
用户问题
-> Web 聊天界面
-> FastAPI /api/chat
-> demo 鉴权边界
-> 请求限流
-> 输入安全检查
-> 语义缓存
-> 记忆上下文
-> LangGraph 总调度
-> 专家 Agent
-> 业务工具 / RAG / GraphRAG
-> 流式答案
-> 指标和结构化日志
```

## 当前启动方式

### 方式 A：本地学习/演示版

适合你自己学习、PyCharm 调试和本地完整演示。

```powershell
cd F:\agent0520\cloudagent_enterprise
Copy-Item cloud_agent\agent\.env.full_demo.example cloud_agent\agent\.env
# 在 cloud_agent\agent\.env 中填写 DASHSCOPE_API_KEY

cd infra
docker compose up -d
cd ..

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r cloud_agent\agent\requirements.txt

cd cloud_agent\front\cloud_agent
npm install
cd ..\..\..
```

初始化演示数据：

```powershell
docker exec -i cloudagent-mysql mysql -uroot -pRootPass123! cloud_platform < cloud_agent\agent\database\init_mock_data.sql
.\.venv\Scripts\python.exe cloud_agent\agent\test\milvus_rag.py --ingest --data-dir cloud_agent\mock_data --query "什么是VPC？"
.\.venv\Scripts\python.exe cloud_agent\app\preload_cache.py
.\.venv\Scripts\python.exe cloud_agent\agent\test\import_kg_jsons.py --clear
```

自检：

```powershell
.\.venv\Scripts\python.exe check_full_demo.py
```

启动后端：

```powershell
.\.venv\Scripts\python.exe run_backend.py
```

启动前端：

```powershell
.\.venv\Scripts\python.exe run_frontend.py
```

### 方式 B：企业后端容器版

适合验证后端部署骨架。

```powershell
cd F:\agent0520\cloudagent_enterprise
Copy-Item cloud_agent\agent\.env.container.example cloud_agent\agent\.env.container
# 在 cloud_agent\agent\.env.container 中填写 DASHSCOPE_API_KEY

docker compose -f infra\docker-compose.yml -f infra\docker-compose.enterprise.yml up -d --build
```

健康检查：

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/health
Invoke-RestMethod http://127.0.0.1:5000/api/ready
```

## 推荐的一键启动体验

当前项目已经有：

```text
check_full_demo.py
run_backend.py
run_frontend.py
```

为了让 GitHub 访客和客户更容易试用，下一步建议补 3 个 PowerShell 包装脚本：

```text
scripts/setup_demo.ps1        -> 安装依赖、复制 env 示例文件
scripts/init_demo_data.ps1    -> 导入 MySQL、Milvus、语义缓存、Neo4j 演示数据
scripts/start_demo.ps1        -> 启动 Docker 基础服务、后端和前端
```

这样 README 可以写成：

```powershell
.\scripts\setup_demo.ps1
.\scripts\init_demo_data.ps1
.\scripts\start_demo.ps1
```

Python 脚本继续保留，方便 PyCharm 调试；PowerShell 脚本负责给客户和 GitHub 访客一个更顺手的一键路径。

## 诚实边界

适合说：

- 小公司内部试点。
- 简历展示项目。
- 小团队 AI 助手原型。
- 本地可复现实验/演示环境。

暂时不要说：

- 公网 SaaS 生产系统。
- 真实 OAuth/JWT 多租户系统。
- 分布式可观测平台。
- 分布式限流部署。
- 生产级密钥管理方案。
