import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[2]
AGENT_DIR = ROOT_DIR / "cloud_agent" / "agent"
if str(AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(AGENT_DIR))

CASES_PATH = Path(__file__).with_name("golden_cases.json")
VALID_ROUTES = {
    "product_agent",
    "billing_agent",
    "promotion_agent",
    "recommendation_agent",
}
VALID_SAFETY = {"normal", "cross_user_injection"}
REQUIRED_FIELDS = {
    "id",
    "query",
    "user_id",
    "session_id",
    "expected_route",
    "required_keywords",
    "safety",
    "requires_live",
}


def load_cases() -> list[dict[str, Any]]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def validate_cases(cases: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        missing = REQUIRED_FIELDS - set(case)
        if missing:
            errors.append(f"case[{index}] missing fields: {sorted(missing)}")
            continue
        case_id = case["id"]
        if case_id in seen_ids:
            errors.append(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)
        if case["expected_route"] not in VALID_ROUTES:
            errors.append(f"{case_id}: invalid expected_route={case['expected_route']}")
        if case["safety"] not in VALID_SAFETY:
            errors.append(f"{case_id}: invalid safety={case['safety']}")
        if not isinstance(case["required_keywords"], list) or not case["required_keywords"]:
            errors.append(f"{case_id}: required_keywords must be a non-empty list")
    return errors


def predict_static_route(query: str) -> str:
    from agents.orchestrator import OrchestratorAgent

    route = OrchestratorAgent._keyword_route(query)
    if route == "finops_agent_trigger":
        return "billing_agent"
    return route or "product_agent"


def run_static() -> int:
    cases = load_cases()
    errors = validate_cases(cases)
    if errors:
        print("STATIC EVAL FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"STATIC EVAL PASSED: {len(cases)} cases validated")
    return 0


def run_route() -> int:
    cases = load_cases()
    errors = validate_cases(cases)
    if errors:
        print("ROUTE EVAL FAILED: invalid cases")
        for error in errors:
            print(f"- {error}")
        return 1

    failures: list[str] = []
    skipped = 0
    checked = 0
    for case in cases:
        if case.get("requires_live"):
            skipped += 1
            continue
        checked += 1
        predicted = predict_static_route(case["query"])
        if predicted != case["expected_route"]:
            failures.append(
                f"{case['id']}: expected {case['expected_route']}, got {predicted}"
            )

    if failures:
        print("ROUTE EVAL FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"ROUTE EVAL PASSED: {checked} checked, {skipped} live cases skipped")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CloudAgent golden evals.")
    parser.add_argument("--mode", choices=["static", "route"], default="static")
    args = parser.parse_args()

    if args.mode == "route":
        return run_route()
    return run_static()


if __name__ == "__main__":
    raise SystemExit(main())
