# Quick Start Guide

This guide will help you get started with the Telegram Userbot quickly and easily.

## Prerequisites

Before you begin, you'll need:

1. Telegram API credentials (API ID and Hash)
2. Docker & Docker Compose installed on your system
3. A phone number that can receive SMS or Telegram messages

## Step 1: Get Telegram API Credentials

1. Visit https://my.telegram.org/
2. Log in with your Telegram account
3. Click on "API development tools"
4. Fill in the form to create a new application:
   - App title: `Telegram Userbot`
   - Short name: `telegram-userbot`
   - URL: `http://localhost` (or any valid URL)
   - Platform: Leave empty
5. Click "Create application"
6. Note down the `api_id` and `api_hash` values

## Step 2: Configure the Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd telegram-userbot
   ```

2. Create the environment configuration file:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your credentials:
   ```env
   # Telegram API Credentials (from Step 1)
   TELEGRAM_API_ID=12345678
   TELEGRAM_API_HASH=your_api_hash_here
   
   # Your phone number for initial authentication
   PHONE_NUMBER=+1234567890
   
   # Secret key for JWT authentication (generate a random string)
   SECRET_KEY=your_secret_key_here_32_characters_min
   
   # Database URL (SQLite for development)
   DATABASE_URL=sqlite+aiosqlite:///./telegram_bot.db
   ```

## Step 3: Start the Application

Start all services with Docker Compose:
```bash
docker-compose up -d
```

This will start:
- Backend API on port 8000
- Telegram Mini App on port 3001
- Database (PostgreSQL in docker-compose, SQLite for development)

## Step 4: Initial Authentication

1. Open your browser and go to http://localhost:3001
2. The Telegram Mini App interface will load
3. Navigate to the "Auth" section using the bottom navigation
4. Enter your phone number in international format (e.g., +1234567890)
5. Click "Send Code"
6. Check your Telegram app for the verification code
7. Enter the code in the Mini App
8. If you have two-factor authentication enabled, you'll be prompted for your password

## Step 5: Configure Groups and Messages

After successful authentication:

1. Go to the "Groups" section
2. Add the groups you want to send messages to:
   - Group link: `t.me/groupname`
   - Username: `@groupname`
   - ID: `-100xxxxxxxxxx`
3. Go to the "Messages" section
4. Add your message templates (plain text only)
5. Go to the "Config" section to adjust posting intervals if needed

## Step 6: Start the Userbot

1. Go to the Dashboard
2. In the "Userbot Control" section, click "Start"
3. The userbot will begin sending messages to your configured groups according to the schedule

## Monitoring and Management

- Check the "Dashboard" for system status
- View blacklisted chats in the "Blacklist" section
- Stop the userbot at any time using the "Stop" button

## Troubleshooting

### Common Issues

1. **Authentication fails**: 
   - Double-check your API ID and Hash
   - Ensure your phone number is in international format
   - Verify you can receive messages on that number

2. **Messages not sending**:
   - Check that groups are added and active
   - Verify messages are added and active
   - Check the blacklist for blocked groups

3. **Database connection issues**:
   - Verify the DATABASE_URL in your .env file
   - For Docker, ensure the database service is running

### Getting Help

If you encounter issues not covered in this guide:

1. Check the logs: `docker-compose logs`
2. Review the detailed documentation in `docs/DOCUMENTATION.md`
3. Create an issue on GitHub with detailed information about the problem