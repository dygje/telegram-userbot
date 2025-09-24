"""
Main application file for the Telegram Userbot Backend (TMA API).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api.routes import router as api_router
from .api.routes import initialize_userbot, cleanup_userbot
from .core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    init_db()
    await initialize_userbot()
    yield
    # Shutdown
    await cleanup_userbot()


app = FastAPI(
    title="Telegram Userbot TMA API",
    description=(
        "API for managing the Telegram Userbot " "with automatic posting capabilities"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Telegram Userbot TMA API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
