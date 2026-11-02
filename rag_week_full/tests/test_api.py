from fastapi.testclient import TestClient
from raglab.api import app
client=TestClient(app)

def test_health():
    assert client.get('/health').json()=={'status':'ok'}

def test_bad_question():
    assert client.post('/ask',json={'question':'x'}).status_code==422

def test_invalid_top_k():
    assert client.post('/ask',json={'question':'FedEx industry?','top_k':0}).status_code==422
