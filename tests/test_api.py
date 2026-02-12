import json
import requests
import pytest

API_URL = "http://localhost:8000/chat"


def load_test_cases():
    with open("tests/test_cases.json", "r") as f:
        return json.load(f)


@pytest.mark.parametrize("case", load_test_cases())
def test_support_agent(case):
    response = requests.post(
        API_URL,
        json={"message": case["input"]},
        timeout=30,
    )

    assert response.status_code == 200

    data = response.json()

    print("\n")
    print("TEST:", case["name"])
    print("INPUT:", case["input"])
    print("ESCALATE:", data.get("escalate"))
    print("ANSWER:", data.get("answer")[:150], "...")

    assert data.get("escalate") == case["expected_escalate"]
