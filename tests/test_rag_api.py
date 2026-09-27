from fastapi.testclient import TestClient

from enterprise_network_ai.main import app


client = TestClient(app)


def test_knowledge_ask(monkeypatch):

    def fake_ask(
        question: str,
        top_k: int,
    ):

        return {
            "answer": (
                "Check the BGP neighbor state "
                "and reset history."
            ),
            "sources": [
                {
                    "document_name": (
                        "bgp_troubleshooting.md"
                    ),
                    "title": (
                        "BGP Neighbor Troubleshooting"
                    ),
                    "similarity": 0.92,
                }
            ],
        }

    monkeypatch.setattr(
        "enterprise_network_ai.main.ask_knowledge_question",
        fake_ask,
    )

    response = client.post(
        "/knowledge/ask",
        json={
            "question": (
                "How do I troubleshoot BGP flapping?"
            ),
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        "BGP"
        in data["answer"]
    )

    assert len(
        data["sources"]
    ) == 1

    assert (
        data["sources"][0]["document_name"]
        == "bgp_troubleshooting.md"
    )


def test_knowledge_ask_validation():

    response = client.post(
        "/knowledge/ask",
        json={
            "question": "x"
        },
    )

    assert response.status_code == 422