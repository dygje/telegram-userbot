"""
Rate Limiting Module
Provides rate limiting functionality for API endpoints
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
# The settings import is intentionally kept for future use
from .config import settings  # noqa: F401

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)

# Define default rate limits
DEFAULT_LIMIT = "100/minute"  # 100 requests per minute per IP
