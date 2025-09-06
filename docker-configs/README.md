# 🐳 Docker Configuration Files

This directory contains Docker-related files that are **not used by Railway**.

Railway uses **Nixpacks** for deployment (see `../RAILWAY_DEPLOY.md`).

## Files:

- `Dockerfile.backup` - Original Dockerfile for local development
- `Dockerfile.railway` - Alternative Railway Dockerfile (unused)
- `docker-compose.yml` - For local Docker Compose setup
- `.dockerignore` - Docker ignore rules

## Local Docker Usage:

```bash
# Copy Dockerfile to root for local development
cp docker-configs/Dockerfile.backup Dockerfile

# Build and run locally
docker build -t eri-bot .
docker run --env-file .env eri-bot

# Or use docker-compose
cp docker-configs/docker-compose.yml .
docker-compose up --build

# Clean up when done
rm Dockerfile docker-compose.yml
```

## Why moved here?

Railway was detecting these Docker files and trying to use Docker instead of Nixpacks,
causing build failures. Moving them here forces Railway to use Nixpacks.
