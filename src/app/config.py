import os
import ollama
from slowapi import Limiter
from slowapi.util import get_remote_address

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiter configuration
limiter = Limiter(key_func=get_remote_address)

# Model name configuration
MODEL_NAME = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")

# Load the system prompt from a file
def load_system_prompt(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error loading system prompt from {file_path}: {str(e)}")
        raise

# Create the model on the executor
def create_model():
    try:
        system_prompt = load_system_prompt("prompts/default_system_prompt.txt")
        ollama.create(model="ollama-fastapi-rs-model", from_=MODEL_NAME, system=system_prompt)
        logger.info(f"Model {MODEL_NAME} created successfully.")
    except Exception as e:
        logger.error(f"Error creating model {MODEL_NAME}: {str(e)}")
        raise

create_model()