# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Telegram MTProto integration with PyroFork
- TMA Web UI with React + Next.js
- Group management system
- Message management system
- Automated blacklist management
- Docker support for easy deployment
- Comprehensive documentation
- API with FastAPI
- Database models with SQLAlchemy
- Telegram Mini App implementation with React + Vite
- Migration from Next.js web app to Telegram Mini App
- Repository pattern with base repository class for reduced code duplication
- API error handling decorator for consistent error responses
- Modular frontend components for better maintainability

### Changed
- Improved .gitignore file for better security
- Enhanced README with detailed setup instructions
- Updated environment variable handling
- Updated Pydantic validators to use newer syntax
- Updated FastAPI lifespan handlers to use context managers
- Fixed database model imports
- Fixed type annotations in repository classes
- Replaced Next.js frontend with Telegram Mini App
- Updated development documentation to reflect Telegram Mini App architecture
- Updated production deployment documentation for Telegram Mini App
- Refactored repository classes to use base repository pattern
- Simplified frontend structure with modular components
- Improved API error handling with consistent decorator pattern

### Fixed
- Session management issues
- Database connection stability
- Error handling for Telegram API errors
- Removed deprecated FastAPI event handlers
- Fixed Pydantic deprecation warnings
- Fixed SQLAlchemy declarative_base warnings
- Removed unused Next.js frontend components
- Simplified project structure to focus on Telegram Mini App
- Removed unused dependencies and code examples
- Resolved code duplication in repository pattern
- Standardized error handling across API endpoints

### Removed
- Next.js frontend implementation
- Tailwind CSS dependencies
- Unused frontend components and pages
- Unused backend dependencies (python-jose, passlib, httpx)
- Empty directories (schemas, services, utils)
- Example code blocks from production files
- axios dependency from frontend

## [1.0.0] - 2025-09-12

### Added
- Initial release of the Telegram Userbot system
- Backend API with FastAPI
- Frontend TMA Web UI with React + Next.js
- Docker Compose setup for easy deployment
- Comprehensive documentation
- Automated posting to Telegram groups
- Real-time blacklist management
- JWT authentication for TMA Web UI