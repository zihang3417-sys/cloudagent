import sys
import os

os.environ.setdefault("NO_PROXY", "127.0.0.1,localhost")
os.environ.setdefault("no_proxy", "127.0.0.1,localhost")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 将 agent 目录加入 sys.path
AGENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent")
sys.path.insert(0, AGENT_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from router import chat
from service.chat_service import init_agent_system

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化
    await init_agent_system()
    yield
    # 关闭时清理
    pass

app = FastAPI(title="Multi-Agent Cloud Service API", lifespan=lifespan)

# 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_main:app", host="0.0.0.0", port=5000, reload=True)
