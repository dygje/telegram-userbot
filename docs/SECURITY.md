# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please send an email to [security@example.com](mailto:security@example.com). All security vulnerabilities will be promptly addressed.

Please do not publicly disclose the vulnerability until it has been addressed by the team.

## Security Considerations

This project handles sensitive information including:

1. Telegram API credentials
2. User session data
3. Database credentials

We implement the following security measures:

- All sensitive data is stored encrypted
- Communication should use HTTPS in production
- JWT tokens for API authentication
- Proper input validation and sanitization
- Regular dependency updates

## Best Practices for Users

To ensure the security of your deployment:

1. Use strong, unique passwords
2. Keep all dependencies up to date
3. Use HTTPS for all communications
4. Regularly backup your database
5. Monitor logs for suspicious activity
6. Restrict access to the administration interface
7. Use environment variables for sensitive configuration