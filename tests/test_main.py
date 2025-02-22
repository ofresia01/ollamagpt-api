from fastapi.testclient import TestClient
from src.app.main import app
import pytest
from unittest.mock import AsyncMock, patch

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_rate_limit():
    # Reset the rate limit state before each test
    app.state.limiter.reset()

@patch('src.app.routes.AsyncClient.chat', new_callable=AsyncMock)
@patch('src.app.ollama_utils.create_model')
async def test_post_chat(mock_create_model, mock_chat):
    async def mock_chat_generator(*args, **kwargs):
        yield {"message": {"content": "Hello, user!"}}
        yield {"message": {"content": "How can I help you?"}}
    mock_chat.return_value = mock_chat_generator()

    payload = {"prompt": "Hello, LLM!"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200

    # Read the streaming response content
    response_content = ""
    async for chunk in response.aiter_text():
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

@patch('src.app.routes.AsyncClient.chat', new_callable=AsyncMock)
@patch('src.app.ollama_utils.create_model')
def test_rate_limiting(mock_create_model, mock_chat):
    async def mock_chat_generator(*args, **kwargs):
        yield {"message": {"content": "Hello, user!"}}
    mock_chat.return_value = mock_chat_generator()

    payload = {"prompt": "Hello, LLM!"}
    for _ in range(5):
        response = client.post("/chat", json=payload)
        assert response.status_code == 200

    # The 6th request should be rate limited
    response = client.post("/chat", json=payload)
    assert response.status_code == 429  # Too Many Requests

@patch('src.app.routes.AsyncClient.chat', new_callable=AsyncMock)
@patch('src.app.ollama_utils.create_model')
def test_health_check(mock_create_model, mock_chat):
    mock_chat.return_value = [{"message": {"content": "Health check response"}}]
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ollama FastAPI server is running!"}

@patch('src.app.routes.AsyncClient.chat', new_callable=AsyncMock)
@patch('src.app.ollama_utils.create_model')
def test_post_chat_bypass_validation(mock_create_model, mock_chat):
    async def mock_chat_generator(*args, **kwargs):
        yield {"message": {"content": "Hello, user! Your message is processing normally."}}
    mock_chat.return_value = mock_chat_generator()
    payload = {"prompt": "This should bypass validation."}
    response = client.post("/chat", json=payload, headers={"bypass_validation": "true"})
    assert response.status_code == 200