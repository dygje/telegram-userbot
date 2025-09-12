# Telegram Userbot TMA - Qwen Code Context

## PROJECT OVERVIEW

This project is a Telegram Userbot with automatic posting capabilities built with Python and PyroFork. The system enables automated messaging to Telegram groups with intelligent blacklist management and a modern Telegram Mini App interface for configuration.

## CORE REQUIREMENTS

### 1. Authentication (REQUIRED)
- Must use real user account (non-bot)
- Must connect to Telegram server via MTProto API
- Login process must use phone number and OTP
- If 2FA is enabled, system must support password input
- TMA must provide initial setup form for:
  • Telegram API ID
  • Telegram API Hash
  • Phone number
- Data must be stored encrypted, only accessible by Admin/Superuser

### 2. Group Management (REQUIRED)
- Must be managed through TMA (Telegram Management Application)
- Must support adding, editing, and deleting group list
- Required group formats:
  • Group link: t.me/groupname
  • Username: @groupname
  • ID: -100xxxxxxxxxx
- Must allow bulk addition (one group per line)

### 3. Message Management (REQUIRED)
- Must be managed through TMA
- Users must be able to create, edit, and delete message list
- Messages must be plain text only

### 4. Configuration (REQUIRED)
- All settings must be configurable real-time through TMA
- Changes must apply without stopping system
- API ID, API Hash, or phone number changes must trigger login reload

### 5. Automatic Message Sending (REQUIRED)
- System must only send to non-blacklisted groups
- Must clean temporary blacklist at start of each cycle
- Must send text messages according to prepared list
- Must apply random 5-10 second delay between messages
- Must apply random 1.1-1.3 hour delay between cycles

### 6. Automatic Blacklist Management (REQUIRED)
- Must permanently blacklist for errors:
  ChatForbidden, ChatIdInvalid, UserBlocked, PeerIdInvalid,
  ChannelInvalid, UserBannedInChannel, ChatWriteForbidden, ChatRestricted
- Must temporarily blacklist for:
  • SlowModeWait: record duration and skip group
  • FloodWait: record wait time and continue after completion
- Temporary blacklist must auto-clean after duration expires

### 7. Modern Practices & Maintenance (REQUIRED)
- Code must follow Clean Architecture and modern Python (async, typing)
- Must implement linting, formatting, modular design, and thorough testing
- Must encrypt credentials, isolate sessions, and store audit logs
- Must have retry mechanisms, graceful shutdown, monitoring, and fallback
- Must support Docker, 12-Factor App principles, and CI/CD pipeline
- TMA interface must be responsive, support real-time status, RBAC, and dark mode

## TECHNICAL STACK

- **Backend**: Python 3.11+ using PyroFork (MTProto client) and FastAPI
- **Frontend (Telegram Mini App)**: React + TypeScript + Vite with Telegram Web App SDK
- **Database**: SQLite (local) or PostgreSQL (production)
- **Authentication**: JWT for TMA, MTProto session management
- **Deployment**: Docker & Docker Compose
- **Architecture**: Clean Architecture principles

## CURRENT IMPLEMENTATION

The project now uses a Telegram Mini App as the primary interface instead of a traditional web application. This provides better integration with Telegram's ecosystem and a more native user experience.

### Telegram Mini App Features
- Built with React + Vite for better performance
- Integrated with Telegram Web App SDK (@twa-dev/sdk)
- Responsive design that adapts to Telegram's light/dark themes
- Native Telegram UI components (MainButton, BackButton, etc.)
- Bottom navigation for easy access to all features

### Available Sections
1. **Dashboard**: System status and quick actions
2. **Authentication**: Phone number setup and OTP verification
3. **Group Management**: Add/remove Telegram groups
4. **Message Management**: Create/manage message templates
5. **Configuration**: Adjust posting settings and intervals
6. **Userbot Control**: Start/stop the userbot service
7. **Blacklist Management**: View and manage blacklisted chats

## DEVELOPMENT GUIDELINES

### Code Generation Preferences
- Generate idiomatic Python code following PyroFork and FastAPI patterns
- Generate React components with TypeScript and Telegram Web App SDK
- Include comprehensive error handling and logging
- Provide clear comments for complex logic
- Use type hints consistently
- Follow Clean Architecture principles

### Explanation Style
- Provide detailed explanations with code examples
- Link to relevant PyroFork, FastAPI, React, and Telegram Web App SDK documentation
- Explain both the "how" and "why" of implementations
- Include best practices and security considerations
- Reference Clean Architecture patterns

### Focus Areas
1. Telegram MTProto API integration with PyroFork
2. FastAPI backend development for TMA
3. React frontend development with Telegram Web App SDK
4. Clean Architecture implementation
5. Security best practices for userbots
6. Docker deployment and 12-Factor App principles
7. Automated blacklist management
8. Session management and authentication
9. Real-time status updates in Telegram Mini App

## ENVIRONMENT VARIABLES
Required environment variables:
- `TELEGRAM_API_ID`: Telegram API ID
- `TELEGRAM_API_HASH`: Telegram API Hash
- `SECRET_KEY`: Secret key for JWT authentication
- `DATABASE_URL`: Database connection string

## TOOLS AND DEPENDENCIES
- pyrofork: MTProto client library
- fastapi: Backend framework
- react: Frontend library
- vite: Build tool
- @twa-dev/sdk: Telegram Web App SDK
- python-dotenv: Environment variable management
- pytest: Testing framework
- black: Code formatting
- flake8: Linting
- mypy: Type checking