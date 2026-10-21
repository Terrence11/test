
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Industry Classifier API is running"


def test_fedex_classification():
    response = client.post(
        "/classify",
        json={"business_name": "FedEx"}
    )
    assert response.status_code == 200
    assert response.json()["industry"] == "TRANSPORTATION & LOGISTICS"


def test_microsoft_classification():
    response = client.post(
        "/classify",
        json={"business_name": "Microsoft"}
    )
    assert response.json()["industry"] == "TECHNOLOGY"


def test_invalid_request():
    response = client.post("/classify", json={})
    assert response.status_code == 422
