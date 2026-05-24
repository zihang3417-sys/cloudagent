import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


AGENT_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = AGENT_DIR.parent
DEFAULT_DATA_DIR = PROJECT_DIR / "mock_data"

load_dotenv(AGENT_DIR / ".env")


def _safe_label(label: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in label.strip())
    if not cleaned:
        return "Entity"
    if cleaned[0].isdigit():
        cleaned = f"Entity_{cleaned}"
    return cleaned


def _safe_rel_type(rel_type: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in rel_type.strip().upper())
    return cleaned or "RELATED_TO"


def _props_from_list(properties: list[dict]) -> dict:
    props: dict[str, str] = {}
    for item in properties or []:
        key = str(item.get("key", "")).strip()
        if not key:
            continue
        safe_key = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in key)
        if safe_key and safe_key[0].isdigit():
            safe_key = f"p_{safe_key}"
        props[safe_key or "property"] = str(item.get("value", ""))
    return props


def import_json_file(driver, json_path: Path) -> tuple[int, int]:
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])

    with driver.session() as session:
        for node in nodes:
            node_id = str(node.get("id", "")).strip()
            if not node_id:
                continue
            label = _safe_label(str(node.get("label", "Entity")))
            props = _props_from_list(node.get("properties", []))
            props["id"] = node_id
            props["name"] = props.get("name", node_id)
            props["source_file"] = json_path.name
            session.run(
                f"MERGE (n:{label} {{id: $id}}) SET n += $props",
                id=node_id,
                props=props,
            )

        for edge in edges:
            source = str(edge.get("source", "")).strip()
            target = str(edge.get("target", "")).strip()
            if not source or not target:
                continue
            rel_type = _safe_rel_type(str(edge.get("type", "RELATED_TO")))
            session.run(
                f"""
                MATCH (source {{id: $source}})
                MATCH (target {{id: $target}})
                MERGE (source)-[r:{rel_type}]->(target)
                SET r.source_file = $source_file
                """,
                source=source,
                target=target,
                source_file=json_path.name,
            )

    return len(nodes), len(edges)


def main() -> None:
    parser = argparse.ArgumentParser(description="Import prepared KG JSON files into Neo4j.")
    parser.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR), help="Directory containing *.json KG files.")
    parser.add_argument("--clear", action="store_true", help="Clear existing Neo4j graph before importing.")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    json_files = sorted(data_dir.glob("*.json"))
    if not json_files:
        raise SystemExit(f"No JSON files found in {data_dir}")

    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    print(f"Connecting Neo4j: {uri}")
    driver = GraphDatabase.driver(uri, auth=(user, password))

    if args.clear:
        print("Clearing existing Neo4j graph...")
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    total_nodes = 0
    total_edges = 0
    for json_path in json_files:
        nodes_count, edges_count = import_json_file(driver, json_path)
        total_nodes += nodes_count
        total_edges += edges_count
        print(f"Imported {json_path.name}: nodes={nodes_count}, edges={edges_count}")

    driver.close()
    print(f"Done. Total imported declarations: nodes={total_nodes}, edges={total_edges}")


if __name__ == "__main__":
    main()
