from fastapi.testclient import TestClient
from src.app.main import app
from src.app.models import PromptRequest
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_rate_limit():
    # Reset the rate limit state before each test
    app.state.limiter.reset()

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ollama FastAPI server is running!"}

def test_post_chat():
    payload = {"prompt": "Hello, LLM!"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200

    # Read the streaming response content
    response_content = ""
    for chunk in response.iter_text():
        response_content += chunk

    assert response_content  # Ensure the response content is not empty
    assert isinstance(response_content, str)

def test_post_chat_validation():
    # Test with an invalid prompt (too short)
    payload = {"prompt": ""}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

    # Test with an invalid prompt (contains bad words)
    payload = {"prompt": "This contains badword1"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_rate_limiting():
    payload = {"prompt": "Hello, LLM!"}
    for _ in range(5):
        response = client.post("/chat", json=payload)
        assert response.status_code == 200

    # The 6th request should be rate limited
    response = client.post("/chat", json=payload)
    assert response.status_code == 429  # Too Many Requests

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ollama FastAPI server is running!"}