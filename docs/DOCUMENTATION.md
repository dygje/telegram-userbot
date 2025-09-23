# Telegram Userbot - Detailed Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [TMA Web UI Guide](#tma-web-ui-guide)
6. [API Reference](#api-reference)
7. [Database Schema](#database-schema)
8. [Error Handling](#error-handling)
9. [Security Considerations](#security-considerations)
10. [Troubleshooting](#troubleshooting)

## System Overview

The Telegram Userbot is a sophisticated system designed for automated posting to Telegram groups using the MTProto API. It consists of two main components:

1. **Backend (TMA API)**: A FastAPI application that handles Telegram interactions, database operations, and provides a RESTful API.
2. **Frontend (TMA Web UI)**: A React-based web interface for managing the userbot through a user-friendly dashboard.

### Key Features

- **Telegram MTProto Integration**: Uses PyroFork library for authenticating and interacting with Telegram.
- **Group Management**: Add, edit, and remove Telegram groups for posting.
- **Message Management**: Create and manage messages to be sent.
- **Automated Blacklist**: Automatically manages blacklisted chats based on Telegram errors.
- **Real-time Monitoring**: View status and activity in real-time through the web interface.
- **Role-based Access Control**: Secure access to the management interface.
- **Dark Mode Support**: Modern UI with dark mode option.

## Installation

### Prerequisites

- Docker & Docker Compose (recommended)
- Or Python 3.11+ and Node.js 18+ for local development
- Telegram API credentials (API ID and Hash)

### Getting Telegram API Credentials

1. Visit https://my.telegram.org/
2. Log in with your Telegram account
3. Click on "API development tools"
4. Fill in the form to create a new application
5. Note down the `api_id` and `api_hash` values

### Docker Installation (Recommended)

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

### Local Development Installation

#### Backend Setup

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

#### Frontend Setup

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

## Configuration

### Environment Variables

Create a `.env` file in the backend directory based on `.env.example`:

```env
# Telegram API Credentials
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
PHONE_NUMBER=your_phone_number_here
SESSION_STRING=your_session_string_here

# Application Settings
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite+aiosqlite:///./telegram_bot.db

# TMA Web UI Settings
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Configuration Details

#### Telegram API Credentials

- `TELEGRAM_API_ID` (required): Your Telegram API ID from https://my.telegram.org/
- `TELEGRAM_API_HASH` (required): Your Telegram API Hash from https://my.telegram.org/
- `PHONE_NUMBER` (optional): Your phone number for initial authentication
- `SESSION_STRING` (optional): Persistent session string after initial authentication

#### Application Settings

- `SECRET_KEY` (required): Secret key for JWT token generation
- `DATABASE_URL` (required): Database connection string (SQLite or PostgreSQL)

#### TMA Web UI Settings

- `NEXT_PUBLIC_API_URL` (optional): API URL for frontend (default: http://localhost:8000)

## Usage

### Initial Setup

1. Start the application using Docker or locally
2. Access the TMA Web UI at http://localhost:3000
3. If this is your first time, you'll need to authenticate with your phone number:
   - Enter your phone number in the authentication page
   - Check your Telegram app for the verification code
   - Enter the code in the TMA Web UI
   - If 2FA is enabled, enter your password when prompted

### Adding Groups

1. Navigate to the "Groups" section in the TMA Web UI
2. Click "Add Group"
3. Enter the group identifier (link, username, or ID)
4. The system will validate the group and add it to the list
5. Toggle the "Active" switch to enable/disable posting to the group

### Managing Messages

1. Navigate to the "Messages" section in the TMA Web UI
2. Click "Add Message"
3. Enter the message text
4. Toggle the "Active" switch to enable/disable the message

### Configuration Settings

1. Navigate to the "Config" section in the TMA Web UI
2. Adjust settings like:
   - Message delay (5-10 seconds between messages)
   - Cycle delay (1.1-1.3 hours between cycles)
3. Changes are applied in real-time without restarting the system

### Monitoring

1. Navigate to the "Dashboard" or "Status" section
2. View real-time information about:
   - Current posting status
   - Last posted message
   - Next scheduled post time
   - Active groups and messages
   - Blacklisted chats

## TMA Web UI Guide

### Dashboard

The dashboard provides an overview of the system status, including:
- Current posting cycle status
- Number of active groups
- Number of active messages
- Recent activity log

### Groups Management

The groups management page allows you to:
- View all configured groups
- Add new groups
- Edit existing groups
- Enable/disable groups
- Remove groups

Group identifiers can be in any of these formats:
- Link: `t.me/groupname`
- Username: `@groupname`
- ID: `-100xxxxxxxxxx`

### Messages Management

The messages management page allows you to:
- View all configured messages
- Add new messages
- Edit existing messages
- Enable/disable messages
- Remove messages

### Blacklist Management

The blacklist management page shows:
- Permanently blacklisted chats
- Temporarily blacklisted chats
- Reason for blacklisting
- Expiry time for temporary blacklists

### Configuration

The configuration page allows you to adjust:
- Message delay settings
- Cycle delay settings
- Other system parameters

### Authentication

The authentication page is where you:
- Log in to the TMA Web UI
- Authenticate with Telegram (first time setup)
- Handle 2FA if enabled

## API Reference

The backend provides a RESTful API for programmatic access to all features.

### Authentication

Most API endpoints require authentication with a JWT token.

#### POST /api/v1/auth/login

Authenticate with username/password to obtain a JWT token.

**Request Body:**
```json
{
  "username": "admin",
  "password": "password"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

#### POST /api/v1/auth/telegram

Authenticate with Telegram (first time setup).

**Request Body:**
```json
{
  "phone_number": "+1234567890"
}
```

**Response:**
```json
{
  "phone_code_hash": "code_hash_here"
}
```

#### POST /api/v1/auth/telegram/verify

Verify Telegram authentication code.

**Request Body:**
```json
{
  "phone_number": "+1234567890",
  "phone_code": "12345",
  "phone_code_hash": "code_hash_here"
}
```

**Response:**
```json
{
  "session_string": "session_string_here"
}
```

### Groups

#### GET /api/v1/groups

Get all groups.

**Response:**
```json
[
  {
    "id": 1,
    "identifier": "t.me/groupname",
    "name": "Group Name",
    "is_active": true,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

#### POST /api/v1/groups

Create a new group.

**Request Body:**
```json
{
  "identifier": "t.me/groupname",
  "name": "Group Name",
  "is_active": true
}
```

#### PUT /api/v1/groups/{id}

Update a group.

#### DELETE /api/v1/groups/{id}

Delete a group.

### Messages

#### GET /api/v1/messages

Get all messages.

#### POST /api/v1/messages

Create a new message.

#### PUT /api/v1/messages/{id}

Update a message.

#### DELETE /api/v1/messages/{id}

Delete a message.

### Blacklist

#### GET /api/v1/blacklist

Get all blacklisted chats.

#### DELETE /api/v1/blacklist/{id}

Remove a chat from blacklist.

### Configuration

#### GET /api/v1/config

Get all configuration settings.

#### PUT /api/v1/config

Update configuration settings.

### Status

#### GET /api/v1/status

Get system status.

## Error Handling

The API implements consistent error handling using a decorator pattern. All endpoints return appropriate HTTP status codes:

- 200: Success
- 400: Bad Request (invalid input or client error)
- 401: Unauthorized (missing or invalid authentication)
- 404: Not Found (resource not found)
- 500: Internal Server Error (unexpected server error)

Error responses follow a consistent format:
```json
{
  "detail": "Error message describing the problem"
}
```

The `@handle_api_errors` decorator is used to wrap endpoint functions and provide consistent error handling across the API.

## Database Schema

The application uses SQLAlchemy ORM with the following models:

### Group

```python
class Group(Base):
    """Model for managed Telegram groups"""
    
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True)  # Link, username, or ID
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Group(id={self.id}, identifier='{self.identifier}', name='{self.name}')>"
```

### Message

```python
class Message(Base):
    """Model for messages to be sent"""
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Message(id={self.id}, text='{self.text[:50]}...')>"
```

### BlacklistedChat

```python
class BlacklistedChat(Base):
    """Model for blacklisted chats"""
    
    __tablename__ = "blacklisted_chats"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True)
    reason = Column(String)
    is_permanent = Column(Boolean, default=False)
    expiry_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<BlacklistedChat(chat_id='{self.chat_id}', reason='{self.reason}')>"
```

### Config

```python
class Config(Base):
    """Model for configuration settings"""
    
    __tablename__ = "config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Config(key='{self.key}', value='{self.value}')>"
```

## Repository Pattern

The application implements a repository pattern for data access with a base repository class that provides common CRUD operations. Each model has its own repository class that extends the base repository:

### BaseRepository

```python
class BaseRepository(Generic[T]):
    """Base repository class with common CRUD operations"""
    
    def __init__(self, model_class: T, db: Session = None):
        self.model_class = model_class
        self.db = db or get_db_session()
    
    def get_all(self, filter_active: bool = True) -> List[T]:
        """Get all records"""
        # Implementation
    
    def get_by_id(self, id: int, filter_active: bool = True) -> Optional[T]:
        """Get record by ID"""
        # Implementation
    
    def create(self, **kwargs) -> T:
        """Create a new record"""
        # Implementation
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update a record"""
        # Implementation
    
    def delete(self, id: int, soft_delete: bool = True) -> bool:
        """Delete a record"""
        # Implementation
```

### Model-Specific Repositories

Each model has its own repository that extends `BaseRepository`:

1. `GroupRepository` - For managing Telegram groups
2. `MessageRepository` - For managing messages
3. `BlacklistRepository` - For managing blacklisted chats
4. `ConfigRepository` - For managing configuration settings

## Error Handling

The system implements comprehensive error handling for various scenarios:

### Telegram API Errors

The system automatically handles and responds to various Telegram API errors:

- **ChatForbidden**: Adds chat to permanent blacklist
- **ChatIdInvalid**: Adds chat to permanent blacklist
- **UserBlocked**: Adds chat to permanent blacklist
- **PeerIdInvalid**: Adds chat to permanent blacklist
- **ChannelInvalid**: Adds chat to permanent blacklist
- **UserBannedInChannel**: Adds chat to permanent blacklist
- **ChatWriteForbidden**: Adds chat to permanent blacklist
- **ChatRestricted**: Adds chat to permanent blacklist
- **SlowModeWait**: Adds chat to temporary blacklist with expiry time
- **FloodWait**: Adds chat to temporary blacklist with expiry time

### Application Errors

All API endpoints return appropriate HTTP status codes and error messages:

- 400: Bad Request (invalid input)
- 401: Unauthorized (missing or invalid authentication)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource not found)
- 500: Internal Server Error (unexpected server error)

## Security Considerations

### Credential Storage

- Telegram API credentials are stored as environment variables
- Session strings are stored encrypted in the database
- Secrets like JWT secret key are stored as environment variables

### Authentication

- JWT tokens are used for API authentication
- Tokens have a configurable expiration time
- Passwords are hashed using bcrypt

### Communication

- All communication should use HTTPS in production
- CORS is configured to restrict origins in production

### Session Management

- User sessions are managed securely
- Session strings are encrypted before storage
- Automatic session renewal and validation

## Troubleshooting

### Common Issues

#### Telegram Authentication Fails

1. Verify your API ID and API Hash are correct
2. Ensure your phone number is in international format
3. Check that you can receive SMS or Telegram messages on the number
4. If using 2FA, ensure you have your password ready

#### Messages Not Sending

1. Check that groups are active
2. Verify messages are active
3. Check the blacklist for any blocked groups
4. Review logs for error messages

#### Database Connection Issues

1. Verify database URL in environment variables
2. Ensure database service is running (for Docker setup)
3. Check database credentials

#### Docker Issues

1. Ensure Docker and Docker Compose are installed
2. Check that ports 3000 and 8000 are not in use
3. Verify environment variables in .env file

### Logging

The application provides detailed logging for troubleshooting:

- Backend logs can be viewed with `docker-compose logs backend`
- Frontend logs can be viewed with `docker-compose logs frontend`
- For local development, logs are printed to the console

### Getting Help

If you encounter issues not covered in this documentation:

1. Check the GitHub issues for similar problems
2. Create a new issue with detailed information about the problem
3. Include relevant logs and error messages
4. Specify your environment (Docker/local, OS, etc.)