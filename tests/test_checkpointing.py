from pathlib import Path
from types import SimpleNamespace

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from typing import TypedDict

from core.workflow.checkpointing import build_sqlite_checkpoint_resources
from core.workflow.graph_manager import AgentGraphManager


class CounterState(TypedDict):
    value: int


@pytest.mark.asyncio
async def test_build_sqlite_checkpoint_resources_supports_async_graph_ainvoke(tmp_path):
    db_path = tmp_path / "nested" / "checkpoints.sqlite"

    resources = await build_sqlite_checkpoint_resources(db_path)

    async def increment(state: CounterState) -> CounterState:
        return {"value": state["value"] + 1}

    try:
        builder = StateGraph(CounterState)
        builder.add_node("increment", increment)
        builder.add_edge(START, "increment")
        builder.add_edge("increment", END)
        graph = builder.compile(checkpointer=resources.saver)
        result = await graph.ainvoke(
            {"value": 1},
            config={"configurable": {"thread_id": "checkpoint-test"}},
        )

        assert result == {"value": 2}
        assert db_path.parent.exists()
        assert resources.saver is not None
        assert resources.path == db_path
    finally:
        await resources.close()


def test_agent_graph_manager_compiles_with_checkpointer():
    saver = InMemorySaver()
    manager = AgentGraphManager.__new__(AgentGraphManager)

    async def passthrough(state):
        return {}

    manager.orchestrator = SimpleNamespace(route=passthrough)
    manager.product_node = passthrough
    manager.billing_node = passthrough
    manager.promotion_node = passthrough
    manager.recommendation_node = passthrough
    manager.finops_node = passthrough
    manager.checkpoint_resources = SimpleNamespace(saver=saver)

    graph = manager.build_graph()

    assert graph.checkpointer is saver
