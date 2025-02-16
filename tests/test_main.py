from fastapi.testclient import TestClient
from src.app.main import app
import pytest
import responses
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_rate_limit():
    # Reset the rate limit state before each test
    app.state.limiter.reset()

@pytest.fixture
def mock_ollama_api():
    with responses.RequestsMock() as rsps:
        yield rsps

def test_get_root():
    with patch('src.app.routes.ollama.chat') as mock_chat:
        mock_chat.return_value = [{"message": {"content": "Health check response"}}]
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Ollama FastAPI server is running!"}

@patch('src.app.routes.ollama.chat')
def test_post_chat(mock_chat, mock_ollama_api):
    mock_chat.return_value = [
        {"message": {"content": "Hello, user!"}},
        {"message": {"content": "How can I help you?"}}
    ]

    payload = {"prompt": "Hello, LLM!"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200

    # Read the streaming response content
    response_content = ""
    for chunk in response.iter_text():
        response_content += chunk

    assert response_content  # Ensure the response content is not empty
    assert isinstance(response_content, str)
    assert "Hello, user!" in response_content
    assert "How can I help you?" in response_content

def test_post_chat_validation():
    # Test with an invalid prompt (too short)
    payload = {"prompt": ""}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

    # Test with an invalid prompt (contains bad words)
    payload = {"prompt": "This contains badword1"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

@patch('src.app.routes.ollama.chat')
def test_rate_limiting(mock_chat, mock_ollama_api):
    mock_chat.return_value = [
        {"message": {"content": "Hello, user!"}}
    ]

    payload = {"prompt": "Hello, LLM!"}
    for _ in range(5):
        response = client.post("/chat", json=payload)
        assert response.status_code == 200

    # The 6th request should be rate limited
    response = client.post("/chat", json=payload)
    assert response.status_code == 429  # Too Many Requests

def test_health_check():
    with patch('src.app.routes.ollama.chat') as mock_chat:
        mock_chat.return_value = [{"message": {"content": "Health check response"}}]
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Ollama FastAPI server is running!"}

def test_post_chat_bypass_validation():
    payload = {"prompt": "This should bypass validation."}
    response = client.post("/chat", json=payload, headers={"bypass_validation": "true"})
    assert response.status_code == 200