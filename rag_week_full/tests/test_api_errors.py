import pytest
from fastapi.testclient import TestClient

from raglab import api


client = TestClient(api.app)


@pytest.mark.parametrize(
    ("error", "status_code", "detail"),
    [
        (ValueError("unsupported option"), 400, "unsupported option"),
        (
            RuntimeError("index unavailable"),
            503,
            "RAG index or model response unavailable",
        ),
    ],
)
def test_ask_maps_processing_errors_to_http_responses(
    monkeypatch, error, status_code, detail
):
    def raise_error(*args):
        raise error

    monkeypatch.setattr(api, "answer_question", raise_error)

    response = client.post("/ask", json={"question": "What does FedEx do?"})

    assert response.status_code == status_code
    assert response.json() == {"detail": detail}
