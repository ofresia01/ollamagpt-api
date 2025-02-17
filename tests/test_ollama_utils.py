from pytest import raises
from unittest.mock import patch, mock_open, MagicMock
from src.app.ollama_utils import load_system_prompt, create_model, delete_model, model_present, download_model

@patch("builtins.open", new_callable=mock_open, read_data="System prompt content")
def test_load_system_prompt(mock_file):
    file_path = "prompts/default_system_prompt.txt"
    content = load_system_prompt(file_path)
    assert content == "System prompt content"
    mock_file.assert_called_once_with(file_path, 'r')

@patch("builtins.open", side_effect=Exception("File not found"))
def test_load_system_prompt_exception(mock_file):
    file_path = "prompts/non_existent_file.txt"
    with raises(Exception, match="File not found"):
        load_system_prompt(file_path)
    mock_file.assert_called_once_with(file_path, 'r')

@patch("src.app.ollama_utils.ollama.create")
@patch("src.app.ollama_utils.model_present", return_value=True)
@patch("src.app.ollama_utils.load_system_prompt", return_value="System prompt content")
def test_create_model(mock_load_system_prompt, mock_model_present, mock_ollama_create):
    create_model()
    mock_model_present.assert_called_once_with("deepseek-r1:1.5b")
    mock_load_system_prompt.assert_called_once_with("prompts/default_system_prompt.txt")
    mock_ollama_create.assert_called_once_with(model="ollama-fastapi-rs-model", from_="deepseek-r1:1.5b", system="System prompt content")

@patch("src.app.ollama_utils.ollama.create")
@patch("src.app.ollama_utils.download_model")
@patch("src.app.ollama_utils.model_present", return_value=False)
@patch("src.app.ollama_utils.load_system_prompt", return_value="System prompt content")
def test_create_model_else_branch(mock_load_system_prompt, mock_model_present, mock_download_model, mock_ollama_create):
    create_model()
    mock_model_present.assert_called_once_with("deepseek-r1:1.5b")
    mock_download_model.assert_called_once_with("deepseek-r1:1.5b")
    mock_load_system_prompt.assert_called_once_with("prompts/default_system_prompt.txt")
    mock_ollama_create.assert_called_once_with(model="ollama-fastapi-rs-model", from_="deepseek-r1:1.5b", system="System prompt content")

@patch("src.app.ollama_utils.ollama.create", side_effect=Exception("Creation error"))
@patch("src.app.ollama_utils.model_present", return_value=True)
@patch("src.app.ollama_utils.load_system_prompt", return_value="System prompt content")
def test_create_model_exception(mock_load_system_prompt, mock_model_present, mock_ollama_create):
    with raises(Exception, match="Creation error"):
        create_model()
    mock_model_present.assert_called_once_with("deepseek-r1:1.5b")
    mock_load_system_prompt.assert_called_once_with("prompts/default_system_prompt.txt")
    mock_ollama_create.assert_called_once_with(model="ollama-fastapi-rs-model", from_="deepseek-r1:1.5b", system="System prompt content")

@patch("src.app.ollama_utils.ollama.delete")
def test_delete_model(mock_ollama_delete):
    delete_model()
    mock_ollama_delete.assert_called_once_with(model="ollama-fastapi-rs-model")

@patch("src.app.ollama_utils.ollama.delete", side_effect=Exception("Deletion error"))
def test_delete_model_exception(mock_ollama_delete):
    with raises(Exception, match="Deletion error"):
        delete_model()
    mock_ollama_delete.assert_called_once_with(model="ollama-fastapi-rs-model")

@patch("src.app.ollama_utils.ollama.list")
def test_model_present(mock_ollama_list):
    mock_list_response = MagicMock()
    mock_list_response.models = [MagicMock(model="deepseek-r1:1.5b")]
    mock_ollama_list.return_value = mock_list_response

    assert model_present("deepseek-r1:1.5b") is True
    mock_ollama_list.assert_called_once()

@patch("src.app.ollama_utils.ollama.list", side_effect=Exception("List error"))
def test_model_present_exception(mock_ollama_list):
    result = model_present("deepseek-r1:1.5b")
    assert result is False
    mock_ollama_list.assert_called_once()

@patch("src.app.ollama_utils.tqdm")
@patch("src.app.ollama_utils.ollama.pull", return_value=[
    {"digest": "digest_1234567890", "total": 100, "completed": 50},
    {"digest": "", "status": "in progress"},
    {"digest": "digest_0987654321", "total": 200, "completed": 100}
])
def test_download_model(mock_ollama_pull, mock_tqdm):
    download_model("deepseek-r1:1.5b")
    mock_ollama_pull.assert_called_once_with(model="deepseek-r1:1.5b", stream=True)
    assert mock_tqdm.call_count == 2
    mock_tqdm.assert_any_call(total=100, desc="Pulling digest 1234567890", unit='B', unit_scale=True)
    mock_tqdm.assert_any_call(total=200, desc="Pulling digest 0987654321", unit='B', unit_scale=True)

@patch("src.app.ollama_utils.ollama.pull", side_effect=Exception("Download error"))
def test_download_model_exception(mock_ollama_pull):
    with raises(Exception, match="Download error"):
        download_model("deepseek-r1:1.5b")
    mock_ollama_pull.assert_called_once_with(model="deepseek-r1:1.5b", stream=True)