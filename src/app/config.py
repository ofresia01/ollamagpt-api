import os
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