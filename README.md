# Telegram Userbot (MTProto)

A modular Telegram userbot with automatic posting capabilities built with Python and PyroFork. This system enables automated messaging to Telegram groups with intelligent blacklist management and a modern Telegram Mini App interface for configuration.

## Features

- Automatic posting to Telegram groups via MTProto API
- User authentication with phone number and OTP (2FA supported)
- Group management through TMA (Telegram Management Application)
- Message template management for automated posting
- Automated blacklist management for error handling
- Configurable posting delays (between messages and between cycles)
- Modular architecture for easy extension
- Real-time status monitoring through Telegram Mini App
- Role-based access control for security
- Dark mode support in Telegram Mini App
- Docker-based deployment for easy setup

## Technical Stack

- **Backend**: Python 3.11+, PyroFork (MTProto client), FastAPI, SQLAlchemy
- **Frontend**: React + TypeScript + Vite, Telegram Web App SDK
- **Database**: SQLite (local) or PostgreSQL (production)
- **Authentication**: JWT for TMA, MTProto session management
- **Deployment**: Docker & Docker Compose
- **Infrastructure**: Clean Architecture principles

## Prerequisites

- Docker & Docker Compose (recommended for production)
- Python 3.11+ (for local development)
- Telegram API credentials (API ID and Hash)
- Phone number for initial Telegram authentication

## Project Structure

```
telegram-userbot/
├── .github/                 # GitHub configurations (workflows, templates)
├── backend/                # Backend source code
│   ├── alembic/             # Database migrations
│   ├── app/                 # Main application code
│   │   ├── api/            # API routes and endpoints
│   │   ├── core/           # Core application logic
│   │   ├── models/         # Database models
│   │   ├── schemas/         # Pydantic schemas for validation
│   │   ├── services/        # Business logic services
│   │   ├── utils/          # Utility functions
│   │   ├── __init__.py      # Package initializer
│   │   └── main.py          # Application entry point
│   ├── tests/               # Unit and integration tests
│   ├── alembic.ini          # Alembic configuration
│   └── requirements.txt     # Python dependencies
├── docs/                   # Documentation files
│   ├── CHANGELOG.md         # Changelog
│   ├── CODE_OF_CONDUCT.md   # Code of conduct
│   ├── CONTRIBUTING.md      # Contribution guidelines
│   ├── DEVELOPMENT.md       # Development guidelines
│   ├── DOCUMENTATION.md     # Detailed documentation
│   ├── PRODUCTION.md        # Production deployment guide
│   └── SECURITY.md          # Security guidelines
├── telegram-mini-app/       # Telegram Mini App source code
│   ├── src/                 # Source code
│   │   ├── App.jsx          # Main application component
│   │   ├── App.css          # Styles
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node.js dependencies and scripts
│   └── vite.config.js       # Vite configuration
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker configuration for backend
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore patterns
├── LICENSE                  # License file
├── QWEN.md                  # Qwen Code CLI context
├── README.md                # Project documentation (this file)
└── ...                      # Other project files
```

## Quick Start with Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd telegram-userbot
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your Telegram API credentials and other settings
   ```

3. Start all services:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Telegram Mini App: http://localhost:3001
   - API Documentation: http://localhost:8000/docs

## Local Development Setup

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (see `.env.example`)

5. Run the backend:
   ```bash
   python app/main.py
   # Or with uvicorn:
   uvicorn app.main:app --reload
   ```

### Telegram Mini App

1. Navigate to the Telegram Mini App directory:
   ```bash
   cd telegram-mini-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Access the Telegram Mini App at http://localhost:3001

## Environment Variables

Create a `.env` file based on `.env.example` with your Telegram API credentials and other settings.

### Required Variables

- `TELEGRAM_API_ID`: Your Telegram API ID
- `TELEGRAM_API_HASH`: Your Telegram API Hash
- `SECRET_KEY`: Secret key for JWT authentication
- `DATABASE_URL`: Database connection string

### Optional Variables

- `PHONE_NUMBER`: Your phone number (for initial setup)
- `SESSION_STRING`: Persistent session string (after initial setup)
- `VITE_API_URL`: API URL for frontend (default: http://localhost:8000)

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

### Production Deployment with Docker

1. Update the `docker-compose.yml` file with your production settings
2. Set proper environment variables in `.env`
3. Run:
   ```bash
   docker-compose up -d
   ```

### Manual Deployment

1. Set up a PostgreSQL database
2. Configure environment variables
3. Install backend dependencies and run:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Build and run Telegram Mini App:
   ```bash
   cd telegram-mini-app
   npm install
   npm run build
   npm run preview
   ```

## Database Migrations

This project uses Alembic for database migrations. To create and run migrations:

1. Create a migration:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Migration message"
   ```

2. Apply migrations:
   ```bash
   alembic upgrade head
   ```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

MIT