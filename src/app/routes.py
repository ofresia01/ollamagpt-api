from fastapi import APIRouter, HTTPException, Request, Header
from fastapi.responses import JSONResponse, StreamingResponse
from slowapi.errors import RateLimitExceeded
import ollama
from typing import AsyncGenerator, Optional
from .config import logger, MODEL_NAME, limiter
from .models import PromptRequest
from .metrics import ollama_requests_total, ollama_errors_total, ollama_response_time
import time

router = APIRouter()

async def generate_stream(prompt: str) -> AsyncGenerator[str, None]:
    try:
        start_time = time.time()
        ollama_requests_total.inc()
        for chunk in ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}], stream=True):
            yield chunk["message"]["content"]
        ollama_response_time.set(time.time() - start_time)
    except Exception as e:
        ollama_errors_total.inc()
        logger.error(f"Error generating stream: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating stream")

@router.post("/chat")
@limiter.limit("5/minute")
async def chat_stream(request: Request, prompt_request: PromptRequest):
    try:
        logger.info(f"Received prompt: {prompt_request.prompt}")
        return StreamingResponse(generate_stream(prompt_request.prompt), media_type="text/plain")
    except HTTPException as e:
        logger.error(f"HTTPException: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing prompt")

@router.get("/")
def root():
    try:
        test_prompt = "Health check"
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": test_prompt}], stream=False)
        if response:
            logger.info("Ollama server is running")
            return {"message": "Ollama FastAPI server is running!"}
        else:
            logger.error("Ollama server is not responding")
            raise HTTPException(status_code=500, detail="Ollama server is not responding")
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")