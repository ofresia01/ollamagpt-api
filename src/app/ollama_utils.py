import os
import ollama
from tqdm import tqdm
from .config import logger

# Model name configuration
BASE_MODEL_NAME = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")
SESSION_MODEL_NAME = "ollama-fastapi-rs-model"

# Load the system prompt from a file
def load_system_prompt(file_path: str) -> str:
    """
    Load the system prompt from a specified file path.
    This function reads the file and returns its content as a string.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error loading system prompt from {file_path}: {str(e)}")
        raise

def create_model():
    """
    Create the model using the ollama library.
    This function checks if the base model is already present. If not, it downloads the model.
    """
    try:
        if model_present(BASE_MODEL_NAME):
            system_prompt = load_system_prompt("prompts/default_system_prompt.txt")
            ollama.create(model=SESSION_MODEL_NAME, from_=BASE_MODEL_NAME, system=system_prompt)
            logger.info(f"Model {SESSION_MODEL_NAME} created successfully.")
        else:
            logger.warning(f"Model {BASE_MODEL_NAME} is not present. Downloading base model...")
            download_model(BASE_MODEL_NAME)
            system_prompt = load_system_prompt("prompts/default_system_prompt.txt")
            ollama.create(model=SESSION_MODEL_NAME, from_=BASE_MODEL_NAME, system=system_prompt)
            logger.info(f"Model {SESSION_MODEL_NAME} created successfully after downloading {BASE_MODEL_NAME}.")
    except Exception as e:
        logger.error(f"Error creating model {SESSION_MODEL_NAME}: {str(e)}")
        raise

def delete_model():
    """
    Delete the model created by the ollama library.
    This function is called during the shutdown of the FastAPI application.
    """
    try:
        ollama.delete(model=f"{SESSION_MODEL_NAME}")
        logger.info(f"Model deleted successfully.")
    except Exception as e:
        logger.error(f"Error deleting model {SESSION_MODEL_NAME}: {str(e)}")
        raise

def model_present(base_model_name: str) -> bool:
    """
    Check if the specified model is present in the list of available models.
    Returns True if the model is present, False otherwise.
    """
    try:
        listResponse: ollama.ListResponse = ollama.list()
        logger.info(f"Available models: {listResponse.models}")
        for model in listResponse.models:
            if model.model == base_model_name:
                logger.info(f"Model {base_model_name} is present.")
                return True
    except Exception as e:
        logger.error(f"Error checking list of available models: {str(e)}")
        return False

def download_model(base_model_name: str) -> None:
    """
    Download the specified model using the ollama library.
    This function streams the download progress and logs it using tqdm.
    """
    try:
        logger.info(f"Downloading model {base_model_name}...")
        current_digest, bars = "", {}
        for progress in ollama.pull(model=base_model_name, stream=True):
            digest = progress.get("digest", "")
            if digest != current_digest and current_digest in bars:
                bars[current_digest].close()

            if not digest:
                logger.info(f"Downloading {base_model_name}, status: {progress.get('status')}")

            if digest not in bars and (total := progress.get('total')):
                bars[digest] = tqdm(total=total, desc=f"Pulling digest {digest[7:19]}", unit='B', unit_scale=True)

            if completed := progress.get('completed'):
                bars[digest].update(completed - bars[digest].n)
            current_digest = digest
        logger.info(f"Model {base_model_name} downloaded successfully.")
    except Exception as e:
        logger.error(f"Error downloading model {base_model_name}: {str(e)}")
        raise