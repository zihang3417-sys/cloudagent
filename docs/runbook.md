# CloudAgent 运行手册

本文档用于在实验室电脑、个人电脑或新环境中复现 CloudAgent 本地演示。

## 1. 拉取仓库

```powershell
git clone https://github.com/zihang3417-sys/cloudagent.git
cd cloudagent
```

如果仓库仍为 Private，需要先登录有权限的 GitHub 账号。

## 2. 安装基础软件

需要：

- Python 3.10 or 3.11
- Node.js 20.19+ or 22.12+
- Docker Desktop
- Ollama
- Git

验证：

```powershell
python --version
node --version
npm --version
docker --version
ollama --version
git --version
```

## 3. 准备 Ollama 模型

```powershell
ollama pull qwen2.5:7b
ollama list
```

确保列表里有：

```text
qwen2.5:7b
```

## 4. 配置 `.env`

复制示例文件：

```powershell
Copy-Item cloud_agent\agent\.env.full_demo.example cloud_agent\agent\.env
```

编辑：

```text
cloud_agent\agent\.env
```

至少需要填写：

```text
DASHSCOPE_API_KEY=your_dashscope_api_key
```

注意：`.env` 不会上传 GitHub。换电脑后需要重新配置或从安全位置复制。

## 5. 启动基础服务

```powershell
cd infra
docker compose up -d
cd ..
```

常用服务：

| Service | Port |
| --- | --- |
| MySQL | 3306 |
| Redis | 6379 |
| Milvus | 19530 |
| Neo4j Browser | 7474 |
| Neo4j Bolt | 7687 |
| Attu | 8000 |

## 6. 安装 Python 环境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r cloud_agent\agent\requirements.txt
```

PyCharm 中建议把解释器设置为项目内的虚拟环境：

```text
<your-project-path>\.venv\Scripts\python.exe
```

新电脑路径不同，按实际项目路径选择 `.venv\Scripts\python.exe`。

## 7. 初始化演示数据

MySQL：

```powershell
docker exec -i cloudagent-mysql mysql -uroot -pRootPass123! cloud_platform < cloud_agent\agent\database\init_mock_data.sql
```

Milvus RAG：

```powershell
.\.venv\Scripts\python.exe cloud_agent\agent\test\milvus_rag.py --ingest --data-dir cloud_agent\mock_data --query "什么是VPC？"
```

语义缓存：

```powershell
.\.venv\Scripts\python.exe cloud_agent\app\preload_cache.py
```

Neo4j GraphRAG：

```powershell
.\.venv\Scripts\python.exe cloud_agent\agent\test\import_kg_jsons.py --clear
```

## 8. 自检

```powershell
.\.venv\Scripts\python.exe check_full_demo.py
```

成功标志：

```text
Full demo environment is ready.
```

如果失败，优先检查：

- Docker 服务是否启动。
- `.env` 是否存在。
- DashScope Key 是否可用。
- Ollama 是否已拉取 `qwen2.5:7b`。
- MySQL mock 数据是否导入。
- Milvus/Neo4j 是否已初始化数据。

## 9. 启动项目

后端：

```powershell
.\.venv\Scripts\python.exe run_backend.py
```

默认后端地址：

```text
http://127.0.0.1:5000
```

前端：

```powershell
.\.venv\Scripts\python.exe run_frontend.py
```

打开 Vite 输出地址，常见为：

```text
http://localhost:5173/
```

## 10. 两台电脑同步建议

适合用 GitHub 同步：

- 源码
- README 和 docs
- mock 数据
- `.env.full_demo.example`
- 运行脚本

不要用 GitHub 同步：

- `.env`
- `.venv/`
- `node_modules/`
- Docker volume 数据
- 数据库文件
- API Key
- 本地 IDE 配置

换电脑后的最小恢复流程：

```powershell
git pull
Copy-Item cloud_agent\agent\.env.full_demo.example cloud_agent\agent\.env
# 填写 DASHSCOPE_API_KEY
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r cloud_agent\agent\requirements.txt
cd cloud_agent\front\cloud_agent
npm install
cd ..\..\..
cd infra
docker compose up -d
cd ..
.\.venv\Scripts\python.exe check_full_demo.py
```
