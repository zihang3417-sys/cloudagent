import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT_DIR / "cloud_agent" / "evals" / "golden_cases.json"
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
VALID_ROUTES = {
    "product_agent",
    "billing_agent",
    "promotion_agent",
    "recommendation_agent",
}
VALID_SAFETY = {"normal", "cross_user_injection"}


def load_cases():
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def test_golden_case_ids_are_unique():
    cases = load_cases()
    ids = [case["id"] for case in cases]

    assert len(ids) == len(set(ids))


def test_golden_cases_have_required_fields_and_valid_values():
    cases = load_cases()

    assert cases
    for case in cases:
        assert REQUIRED_FIELDS <= set(case)
        assert case["expected_route"] in VALID_ROUTES
        assert case["safety"] in VALID_SAFETY
        assert isinstance(case["required_keywords"], list)
        assert case["required_keywords"]


def test_security_cases_are_explicitly_labeled():
    cases = load_cases()
    security_cases = [case for case in cases if "user_id=user_1002" in case["query"]]

    assert security_cases
    assert all(case["safety"] == "cross_user_injection" for case in security_cases)
