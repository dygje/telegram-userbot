"""
API Error Handling Decorator
Provides consistent error handling for API endpoints
"""

from functools import wraps
from fastapi import HTTPException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_api_errors(func):
    """
    Decorator to handle API errors consistently
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            # Re-raise HTTP exceptions as they are already properly formatted
            raise
        except Exception as e:
            # Log the error for debugging
            logger.error(f"Error in {func.__name__}: {str(e)}")
            # Raise as HTTP 400 with the error message
            raise HTTPException(status_code=400, detail=str(e))

    return wrapper
