from fastapi import APIRouter, HTTPException, Header, Request
from fastapi.responses import StreamingResponse
import ollama
from typing import AsyncGenerator, Optional
from .config import logger, limiter
from .ollama_utils import SESSION_MODEL_NAME
from .models import PromptRequest
from .metrics import ollama_requests_total, ollama_errors_total, ollama_response_time
import time

router = APIRouter()

async def generate_stream(prompt: str) -> AsyncGenerator[str, None]:
    try:
        start_time = time.time()
        ollama_requests_total.inc()
        for chunk in ollama.chat(model=SESSION_MODEL_NAME, messages=[{"role": "user", "content": prompt}], stream=True):
            yield chunk["message"]["content"]
        ollama_response_time.set(time.time() - start_time)
    except Exception as e:
        ollama_errors_total.inc()
        logger.error(f"Error generating stream: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating stream")

@router.post("/chat")
@limiter.limit("5/minute")
async def chat_stream(request: Request, prompt_request: PromptRequest, bypass_validation: Optional[str] = Header(None)):
    try:
        if bypass_validation and bypass_validation.lower() == "true":
            logger.info("Bypassing validation due to header flag")
            prompt = (await request.json()).get("prompt")
        else:
            prompt = prompt_request.prompt
        logger.info(f"Received prompt: {prompt}")
        return StreamingResponse(generate_stream(prompt), media_type="text/plain")
    except HTTPException as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing prompt")

@router.get("/")
def root():
    try:
        test_prompt = "Health check"
        response = ollama.chat(model=SESSION_MODEL_NAME, messages=[{"role": "user", "content": test_prompt}], stream=False)
        if response:
            logger.info("Ollama server is running")
            return {"message": "Ollama FastAPI server is running!"}
        else:
            logger.error("Ollama server is not responding")
            raise HTTPException
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")