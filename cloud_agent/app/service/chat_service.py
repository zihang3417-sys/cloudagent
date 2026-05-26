import asyncio
import json
import sys
import os
from time import perf_counter

# 初始化 Agent 和 Graph
AGENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent")
if AGENT_DIR not in sys.path:
    sys.path.insert(0, AGENT_DIR)

from core.workflow.graph_manager import AgentGraphManager
from core.memory.memory_manager import MemoryManager
from infra.cache import semantic_cache
from infra.error_response import classify_error
from infra.metrics import request_metrics
from infra.request_context import RequestContext
from infra.structured_logging import log_event

# Global variables for graph and memory
graph = None
memory = None

async def init_agent_system():
    global graph, memory
    if graph is None:
        print("🚀 初始化 Multi-Agent 图编排...")
        graph_manager = AgentGraphManager()
        graph = graph_manager.build_graph()
        
        print("🧠 初始化 Memory 系统...")
        from config import get_settings
        settings = get_settings()
        memory = MemoryManager(
            redis_url=settings.redis_url,
            redis_ttl=settings.redis_ttl,
            milvus_host=settings.milvus_host,
            milvus_port=settings.milvus_port,
            milvus_api_key=settings.milvus_api_key,
            embedding_api_key=settings.dashscope_api_key,
        )
        await memory.initialize()
        await semantic_cache.initialize()
        print("✅ Agent 系统初始化完成！")

async def _extract_memory_context(user_id: str, session_id: str, query: str) -> str:
    context_parts = []
    if memory and memory.short_term.available:
        history = await memory.short_term.get_messages(user_id, session_id)
        if history:
            recent_history = history[-10:] if len(history) > 10 else history
            context_parts.append("【近期对话历史】:")
            for msg in recent_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                context_parts.append(f"{role}: {msg['content']}")
    
    if memory and memory.long_term.available:
        prefs = await memory.long_term.retrieve_relevant(user_id, query)
        if prefs:
            context_parts.append("\n【用户长期偏好/背景】:")
            for p in prefs:
                context_parts.append(f"- {p}")
                
    return "\n".join(context_parts)

async def stream_chat(query: str, user_id: str, session_id: str):
    context = RequestContext.create(user_id=user_id, session_id=session_id)
    started_at = perf_counter()
    log_event("chat.request.started", context=context)

    try:
        cache_hit = await semantic_cache.get_cache(query, context.user_id)
        if cache_hit:
            request_metrics.record_cache_hit()
            response_text = cache_hit["answer"]
            log_event(
                "chat.cache.hit",
                context=context,
                cache_level=cache_hit.get("level"),
                distance=round(float(cache_hit.get("distance", 0.0)), 4),
                matched_question=cache_hit.get("matched_question"),
            )
        else:
            request_metrics.record_cache_miss()
            log_event("chat.cache.miss", context=context)
            log_event("chat.workflow.started", context=context)
            workflow_started_at = perf_counter()
            mem_context = await _extract_memory_context(
                context.user_id,
                context.session_id,
                query,
            )
            state = {
                "messages": [("user", query)],
                "user_id": context.user_id,
                "session_id": context.session_id,
                "memory_context": mem_context,
                "next_agent": "",
                "metadata": {"trace_id": context.trace_id},
            }
            config = {
                "configurable": {
                    "user_id": context.user_id,
                    "trace_id": context.trace_id,
                }
            }
            result = (
                await asyncio.to_thread(asyncio.run, graph.ainvoke(state, config=config))
                if not asyncio.iscoroutinefunction(graph.ainvoke)
                else await graph.ainvoke(state, config=config)
            )
            response_text = result["messages"][-1].content
            log_event(
                "chat.workflow.completed",
                context=context,
                latency_ms=round((perf_counter() - workflow_started_at) * 1000),
            )

        if memory and memory.short_term.available:
            turn = [
                {"role": "user", "content": query},
                {"role": "assistant", "content": response_text},
            ]
            await memory.save_conversation(context.user_id, context.session_id, turn)

        chunk_size = 5
        for i in range(0, len(response_text), chunk_size):
            chunk = response_text[i:i + chunk_size]
            yield f"data: {json.dumps({'content': chunk})}\n\n"
            await asyncio.sleep(0.02)

        latency_ms = round((perf_counter() - started_at) * 1000)
        request_metrics.record_request(latency_ms=latency_ms, success=True)
        log_event(
            "chat.request.completed",
            context=context,
            latency_ms=latency_ms,
        )
        yield f"data: {json.dumps({'done': True})}\n\n"
    except Exception as exc:
        latency_ms = round((perf_counter() - started_at) * 1000)
        request_metrics.record_request(latency_ms=latency_ms, success=False)
        error_payload = classify_error(exc)
        log_event(
            "chat.request.failed",
            context=context,
            error_code=error_payload["code"],
            error=type(exc).__name__,
            latency_ms=latency_ms,
        )
        yield f"data: {json.dumps({'error': error_payload}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"
