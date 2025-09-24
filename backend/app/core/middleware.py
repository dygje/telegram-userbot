"""
Middleware Configuration Module
Configures various middleware for the FastAPI application
"""

from slowapi.middleware import SlowAPIMiddleware
from fastapi import FastAPI
from .rate_limiter import limiter


def add_middleware(app: FastAPI):
    """
    Add all required middleware to the FastAPI application
    
    Args:
        app: The FastAPI application instance
    """
    # Add the SlowAPI middleware for rate limiting
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
