# Production Deployment Guide

This guide explains how to deploy the Telegram Userbot in a production environment.

## Prerequisites

- Docker & Docker Compose
- Domain name (optional but recommended)
- SSL certificate (optional but recommended)

## Production Configuration

### Environment Variables

Create a `.env` file with production values:

```env
# Telegram API Credentials
TELEGRAM_API_ID=your_production_api_id
TELEGRAM_API_HASH=your_production_api_hash
PHONE_NUMBER=your_production_phone_number
SESSION_STRING=your_production_session_string

# Application Settings
SECRET_KEY=your_production_secret_key
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/telegram_bot

# TMA Web UI Settings
NEXT_PUBLIC_API_URL=https://yourdomain.com
```

### Docker Compose Override

Create a `docker-compose.prod.yml` file for production overrides:

```yaml
version: '3.8'

services:
  backend:
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:password@db:5432/telegram_bot
    restart: unless-stopped
    networks:
      - app-network

  frontend:
    restart: unless-stopped
    networks:
      - app-network

  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - db-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
  db-network:
    driver: bridge
```

## Deployment Steps

### 1. Prepare the Server

1. Install Docker and Docker Compose on your server
2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd telegram-userbot
   ```

3. Create the `.env` file with production values

### 2. Configure SSL (Recommended)

If you have an SSL certificate, place it in `nginx/ssl/` directory:
- `nginx/ssl/cert.pem`: SSL certificate
- `nginx/ssl/key.pem`: SSL private key

### 3. Configure Nginx

Create `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com;
        
        # Redirect all HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        location /api/ {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        location /docs {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        location /redoc {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

### 4. Start Services

Start all services:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 5. Initialize Database

If this is a fresh installation, you may need to run database migrations:
```bash
docker-compose exec backend alembic upgrade head
```

## Monitoring

### Logs

View logs for all services:
```bash
docker-compose logs -f
```

View logs for specific service:
```bash
docker-compose logs -f backend
```

### Health Checks

Check if services are running:
```bash
docker-compose ps
```

## Maintenance

### Updates

To update to the latest version:

1. Pull the latest code:
   ```bash
   git pull
   ```

2. Rebuild and restart services:
   ```bash
   docker-compose down
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
   ```

### Backups

#### Database Backup

Create a database backup:
```bash
docker-compose exec db pg_dump -U user telegram_bot > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Restore Database

Restore from a backup:
```bash
docker-compose exec -T db psql -U user telegram_bot < backup_file.sql
```

## Scaling

### Horizontal Scaling

To scale the backend service:
```bash
docker-compose up -d --scale backend=3
```

Note: You may need to configure a load balancer for horizontal scaling.

## Troubleshooting

### Common Issues

1. **Services not starting**: Check logs with `docker-compose logs`
2. **Database connection errors**: Verify database credentials and network connectivity
3. **SSL issues**: Check certificate files and Nginx configuration
4. **Performance issues**: Monitor resource usage and scale accordingly

### Useful Commands

Check resource usage:
```bash
docker stats
```

Execute commands in containers:
```bash
docker-compose exec backend bash
```

View running processes:
```bash
docker-compose top
```

## Security Best Practices

1. Use strong, unique passwords
2. Keep all software up to date
3. Restrict access to the server
4. Use firewalls to limit open ports
5. Regularly backup data
6. Monitor logs for suspicious activity
7. Use HTTPS for all communications
8. Limit database permissions
9. Regularly rotate API keys and secrets