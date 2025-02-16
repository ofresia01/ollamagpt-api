from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator
from .config import create_model, delete_model, limiter
from .routes import router

app = FastAPI()

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_model() # Create the model on startup
    yield
    delete_model() # Delete the model on shutdown

# Instrument FastAPI application
Instrumentator().instrument(app).expose(app)