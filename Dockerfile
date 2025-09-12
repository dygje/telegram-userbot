# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install TgCrypto for better performance
RUN apt-get update && apt-get install -y gcc && pip install TgCrypto && apt-get clean

# Copy application code
COPY backend/ .

# Create default .env file if it doesn't exist
RUN if [ ! -f .env ]; then \
        echo "# Telegram API Credentials (use real values for production)" > .env && \
        echo "TELEGRAM_API_ID=123456" >> .env && \
        echo "TELEGRAM_API_HASH=dummy_api_hash_for_development" >> .env && \
        echo "PHONE_NUMBER=+1234567890" >> .env && \
        echo "SESSION_STRING=dummy_session_string_for_development" >> .env && \
        echo "" >> .env && \
        echo "# Application Settings" >> .env && \
        echo "SECRET_KEY=dummy_secret_key_for_development_abcdefghijklmnopqrstuvwxyz" >> .env && \
        echo "DATABASE_URL=postgresql+asyncpg://user:password@db:5432/telegram_bot" >> .env && \
        echo "" >> .env && \
        echo "# TMA Web UI Settings" >> .env && \
        echo "NEXT_PUBLIC_API_URL=http://localhost:8000" >> .env; \
    fi

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]