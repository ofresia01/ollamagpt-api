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