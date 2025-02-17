from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.app.main import app
from src.app.routes import generate_stream

client = TestClient(app)

@pytest.mark.asyncio
@patch("src.app.routes.ollama.chat")
async def test_generate_stream(mock_chat):
    mock_chat.return_value = [
        {"message": {"content": "Hello, user!"}},
        {"message": {"content": "How can I help you?"}}
    ]
    prompt = "Hello, LLM!"
    stream = generate_stream(prompt)
    result = [chunk async for chunk in stream]
    assert result == ["Hello, user!", "How can I help you?"]

@pytest.mark.asyncio
@patch("src.app.routes.ollama.chat", side_effect=Exception("Stream error"))
async def test_generate_stream_exception(mock_chat):
    prompt = "Hello, LLM!"
    with pytest.raises(HTTPException) as exc_info:
        stream = generate_stream(prompt)
        result = [chunk async for chunk in stream]
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Error generating stream"

@patch("src.app.routes.ollama.chat")
def test_chat_stream(mock_chat):
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

@pytest.mark.asyncio
@patch("src.app.routes.ollama.chat")
async def test_chat_stream_bypass_validation(mock_chat):
    mock_chat.return_value = [
        {"message": {"content": "Hello, user!"}},
        {"message": {"content": "How can I help you?"}}
    ]
    payload = {"prompt": "Hello, LLM!"}
    headers = {"bypass-validation": "true"}
    response = client.post("/chat", json=payload, headers=headers)
    assert response.status_code == 200

    # Read the streaming response content
    response_content = ""
    for chunk in response.iter_text():
        response_content += chunk

    assert response_content  # Ensure the response content is not empty
    assert isinstance(response_content, str)
    assert "Hello, user!" in response_content
    assert "How can I help you?" in response_content

def test_chat_stream_validation():
    # Test with an invalid prompt (too short)
    payload = {"prompt": ""}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

    # Test with an invalid prompt (contains bad words)
    payload = {"prompt": "This contains badword1"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

@patch("src.app.routes.ollama.chat")
def test_root(mock_chat):
    mock_chat.return_value = [{"message": {"content": "Health check response"}}]
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ollama FastAPI server is running!"}

@patch("src.app.routes.ollama.chat", return_value=None)
def test_root_no_response(mock_chat):
    response = client.get("/")
    assert response.status_code == 500
    assert response.json() == {"detail": "Health check failed"}

@patch("src.app.routes.ollama.chat", side_effect=Exception("Health check failed"))
def test_root_exception(mock_chat):
    response = client.get("/")
    assert response.status_code == 500
    assert response.json() == {"detail": "Health check failed"}