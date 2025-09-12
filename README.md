# Telegram Userbot (MTProto)

A modular Telegram userbot with automatic posting capabilities built with Python and PyroFork. This system enables automated messaging to Telegram groups with intelligent blacklist management and a modern web interface for configuration.

## Features

- Automatic posting to Telegram groups via MTProto API
- User authentication with phone number and OTP (2FA supported)
- Group management through TMA (Telegram Management Application)
- Message template management for automated posting
- Automated blacklist management for error handling
- Configurable posting delays (between messages and between cycles)
- Modular architecture for easy extension
- Real-time status monitoring through web interface
- Role-based access control for security
- Dark mode support in web interface
- Docker-based deployment for easy setup

## Technical Stack

- **Backend**: Python 3.11+, PyroFork (MTProto client), FastAPI, SQLAlchemy
- **Frontend**: React + TypeScript + Next.js, Tailwind CSS
- **Database**: SQLite (local) or PostgreSQL (production)
- **Authentication**: JWT for TMA, MTProto session management
- **Deployment**: Docker & Docker Compose
- **Infrastructure**: Clean Architecture principles

## Prerequisites

- Docker & Docker Compose (recommended for production)
- Python 3.11+ and Node.js 18+ (for local development)
- Telegram API credentials (API ID and Hash)
- Phone number for initial Telegram authentication

## Project Structure

```
telegram-userbot/
├── .github/                 # GitHub configurations (workflows, templates)
├── backend/                 # Backend source code
│   ├── alembic/             # Database migrations
│   ├── app/                 # Main application code
│   │   ├── api/             # API routes and endpoints
│   │   ├── core/            # Core application logic
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas for validation
│   │   ├── services/        # Business logic services
│   │   ├── utils/           # Utility functions
│   │   ├── __init__.py      # Package initializer
│   │   └── main.py          # Application entry point
│   ├── tests/               # Unit and integration tests
│   ├── alembic.ini          # Alembic configuration
│   └── requirements.txt     # Python dependencies
├── docs/                    # Documentation files
│   ├── CHANGELOG.md         # Changelog
│   ├── CODE_OF_CONDUCT.md   # Code of conduct
│   ├── CONTRIBUTING.md      # Contribution guidelines
│   ├── DEVELOPMENT.md       # Development guidelines
│   ├── DOCUMENTATION.md     # Detailed documentation
│   ├── PRODUCTION.md        # Production deployment guide
│   └── SECURITY.md          # Security guidelines
├── frontend/                # Frontend source code
│   ├── pages/               # Page components (Next.js pages)
│   ├── styles/              # Global styles
│   ├── package.json         # Node.js dependencies and scripts
│   └── ...                  # Other frontend configuration files
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
   - TMA Web UI: http://localhost:3000
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

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Access the TMA Web UI at http://localhost:3000

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
- `NEXT_PUBLIC_API_URL`: API URL for frontend (default: http://localhost:8000)

## Qwen Code CLI Integration

This project is configured to work with Qwen Code CLI for AI-assisted development. The configuration includes:

- Context file: `QWEN.md`
- Session token limit: 32000
- File filtering respecting `.gitignore`

To use Qwen Code CLI with this project:

1. Install Qwen Code CLI:
   ```bash
   npm install -g @qwen-code/qwen-code@latest
   ```

2. Navigate to this project directory and run:
   ```bash
   qwen
   ```

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
   docker-compose -f docker-compose.yml up -d
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
4. Build and run frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   npm start
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

### Frontend Tests

```bash
cd frontend
npm run test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

MIT