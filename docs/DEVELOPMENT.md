# Telegram Userbot Development Guide

## Project Overview

This document provides detailed information for developers who want to contribute to or extend the Telegram Userbot project.

## Architecture

The project follows a Clean Architecture pattern with the following layers:

1. **Presentation Layer**: FastAPI for REST API and React for Telegram Mini App
2. **Application Layer**: Business logic and use cases
3. **Domain Layer**: Core entities and interfaces
4. **Infrastructure Layer**: Database, external services, and frameworks

## Backend Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core application logic
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas for validation
│   ├── services/     # Business logic services
│   ├── utils/        # Utility functions
│   └── main.py       # Application entry point
├── tests/            # Unit and integration tests
├── requirements.txt  # Python dependencies
└── alembic/          # Database migrations
```

## Frontend Structure (Telegram Mini App)

```
telegram-mini-app/
├── src/              # Source code
│   ├── App.jsx       # Main application component
│   ├── App.css       # Styles
│   └── main.jsx      # Entry point
├── package.json      # Node.js dependencies and scripts
└── vite.config.js    # Vite configuration
```

## Development Workflow

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Write tests
5. Update documentation
6. Run tests and linters
7. Commit and push
8. Create a pull request

## Backend Development

### Setting up Development Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (see `.env.example`)

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all functions and variables
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

### Testing

Run tests with:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app
```

### Linting

Run linting with:
```bash
flake8 .
```

### Type Checking

Run type checking with:
```bash
mypy --package app
```

### Formatting

Format code with:
```bash
black .
```

## Frontend Development (Telegram Mini App)

### Setting up Development Environment

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run development server:
   ```bash
   npm run dev
   ```

### Code Style

- Follow ESLint and Prettier configurations
- Use TypeScript for all components
- Write JSDoc for complex functions
- Keep components small and focused
- Use meaningful variable and function names

### Testing

Run tests with:
```bash
npm test
```

### Building

Build for production with:
```bash
npm run build
```

## Database Migrations

### Creating Migrations

1. Make changes to models in `app/models/database.py`
2. Generate migration:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

### Applying Migrations

Apply migrations:
```bash
alembic upgrade head
```

Revert migrations:
```bash
alembic downgrade -1
```

## API Documentation

The API is documented using Swagger/OpenAPI. Access the documentation at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Docker Development

### Building Images

Build backend:
```bash
docker build -t telegram-userbot-backend .
```

Build Telegram Mini App:
```bash
cd telegram-mini-app && docker build -t telegram-userbot-mini-app .
```

### Running with Docker

Run all services:
```bash
docker-compose up
```

Run specific service:
```bash
docker-compose up backend
```

## Continuous Integration

The project uses GitHub Actions for CI. Workflows are defined in `.github/workflows/`.

### CI Pipeline

1. Code checkout
2. Setup Python/Node.js environment
3. Install dependencies
4. Run tests
5. Run linters
6. Run type checking

## Deployment

### Production Deployment

1. Update environment variables in production
2. Build Docker images
3. Push to container registry
4. Deploy to production environment

### Environment Variables

Ensure all required environment variables are set in production:
- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`
- `SECRET_KEY`
- `DATABASE_URL`

## Security Considerations

- Never commit sensitive data to the repository
- Use environment variables for secrets
- Validate all user inputs
- Use HTTPS in production
- Keep dependencies up to date
- Regularly audit dependencies for vulnerabilities

## Performance Considerations

- Use database indexes for frequently queried fields
- Implement caching for expensive operations
- Use async/await for I/O operations
- Optimize database queries
- Minimize API calls to Telegram

## Troubleshooting

### Common Issues

1. **Database connection errors**: Check database URL and credentials
2. **Telegram authentication failures**: Verify API credentials
3. **Dependency conflicts**: Update dependencies or use virtual environments
4. **Docker build failures**: Check Dockerfile and dependencies

### Debugging

1. Enable debug logging
2. Use debugger tools
3. Check application logs
4. Verify environment variables