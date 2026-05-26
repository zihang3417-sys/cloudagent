import os
from dataclasses import dataclass
from pathlib import Path

import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


DEFAULT_CHECKPOINT_PATH = Path("data") / "langgraph_checkpoints.sqlite"


@dataclass
class CheckpointResources:
    path: Path
    connection: aiosqlite.Connection
    saver: AsyncSqliteSaver

    async def close(self) -> None:
        await self.connection.close()


def checkpoint_enabled_from_env() -> bool:
    value = os.getenv("LANGGRAPH_CHECKPOINT_ENABLED", "true").strip().lower()
    return value not in {"0", "false", "no", "off"}


def checkpoint_path_from_env() -> Path:
    return Path(os.getenv("LANGGRAPH_CHECKPOINT_PATH", str(DEFAULT_CHECKPOINT_PATH)))


async def build_sqlite_checkpoint_resources(path: str | Path) -> CheckpointResources:
    checkpoint_path = Path(path)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    connection = await aiosqlite.connect(checkpoint_path)
    saver = AsyncSqliteSaver(connection)
    await saver.setup()
    return CheckpointResources(
        path=checkpoint_path,
        connection=connection,
        saver=saver,
    )


async def build_checkpoint_resources() -> CheckpointResources | None:
    if not checkpoint_enabled_from_env():
        return None
    return await build_sqlite_checkpoint_resources(checkpoint_path_from_env())
