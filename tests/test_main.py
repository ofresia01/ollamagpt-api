from fastapi.testclient import TestClient
from src.app.main import app
import pytest
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_rate_limit():
    # Reset the rate limit state before each test
    app.state.limiter.reset()

@pytest.fixture
def patched_ollama_functions():
    with patch('src.app.routes.ollama.chat') as mock_chat, patch('src.app.config.ollama.create'):
        def _mock_chat(response: str):
            mock_chat.return_value = [
                {"message": {"content": response}}
            ]
            return mock_chat
        yield _mock_chat

def test_get_root(patched_ollama_functions):
    mock_chat = patched_ollama_functions("Health check response")
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ollama FastAPI server is running!"}

def test_post_chat(patched_ollama_functions):
        mock_chat = patched_ollama_functions("Hello, user!")

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

def test_post_chat_validation():
    # Test with an invalid prompt (too short)
    payload = {"prompt": ""}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

    # Test with an invalid prompt (contains bad words)
    payload = {"prompt": "This contains badword1"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_rate_limiting(patched_ollama_functions):
        mock_chat = patched_ollama_functions("Hello, user!")

        payload = {"prompt": "Hello, LLM!"}
        for _ in range(5):
            response = client.post("/chat", json=payload)
            assert response.status_code == 200

        # The 6th request should be rate limited
        response = client.post("/chat", json=payload)
        assert response.status_code == 429  # Too Many Requests

def test_health_check(patched_ollama_functions):
    mock_chat = patched_ollama_functions("Health check response")
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ollama FastAPI server is running!"}

def test_post_chat_bypass_validation(patched_ollama_functions):
    mock_chat = patched_ollama_functions("Bypassing validation response")
    payload = {"prompt": "This should bypass validation."}
    response = client.post("/chat", json=payload, headers={"bypass_validation": "true"})
    assert response.status_code == 200