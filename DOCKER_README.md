# Docker Setup for SemantifyHTML Backend

This Docker setup includes everything except the frontend, using the official Playwright Python image for the backend.

## Services

- **Redis**: Caching service for AI explanations
- **Backend**: Flask application with Playwright for web scraping

## Prerequisites

- Docker and Docker Compose installed
- Environment variables set up (see `env.example`)

## Quick Start

1. **Set up environment variables**:

   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key and other settings
   ```

2. **Build and start services**:

   ```bash
   docker-compose up --build
   ```

3. **Access the backend**:
   - API: http://localhost:8080
   - Health check: http://localhost:8080/health

## Development

For development with hot reloading:

```bash
docker-compose up --build
```

The backend code is mounted as a volume, so changes will be reflected immediately.

## Production

For production deployment:

```bash
docker-compose -f docker-compose.yml up -d --build
```

## Docker Configuration

The backend uses the official Playwright Python image (`mcr.microsoft.com/playwright/python:v1.54.0-noble`) which includes:

- Python 3.12
- Playwright browsers (Chromium, Firefox, WebKit)
- All necessary system dependencies
- Non-root user for security

### Security Features

- Non-root user (`appuser`) for running the application
- Seccomp profile support (can be enabled if needed)
- IPC host mode for Chromium memory management
- Init process to avoid zombie processes

## Troubleshooting

### Playwright Issues

If you encounter issues with Playwright:

1. **Browser launch errors**: Try adding `--cap-add=SYS_ADMIN` to the backend service in docker-compose.yml
2. **Memory issues**: The `ipc: host` configuration should prevent Chromium memory problems
3. **Sandbox issues**: The non-root user configuration handles sandbox limitations

### Redis Connection

If Redis connection fails:

- Check that Redis is healthy: `docker-compose ps`
- Verify environment variables are set correctly
- Check logs: `docker-compose logs redis`

## Stopping Services

```bash
docker-compose down
```

To remove volumes as well:

```bash
docker-compose down -v
```
