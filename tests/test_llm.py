from fastapi.testclient import TestClient

from enterprise_network_ai.main import app


client = TestClient(app)


def test_troubleshoot_endpoint(monkeypatch):

    def fake_ask_llm(question: str, network_context: str) -> str:
        return "R1 has high CPU utilization."

    monkeypatch.setattr(
        "enterprise_network_ai.main.ask_llm",
        fake_ask_llm,
    )

    response = client.post(
        "/troubleshoot",
        json={
            "device_id": "R1",
            "question": "Why is the CPU high?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["device_id"] == "R1"
    assert data["question"] == "Why is the CPU high?"
    assert data["answer"] == "R1 has high CPU utilization."


def test_troubleshoot_unknown_device():

    response = client.post(
        "/troubleshoot",
        json={
            "device_id": "R999",
            "question": "Why is the CPU high?",
        },
    )

    assert response.status_code == 404