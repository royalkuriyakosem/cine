# filmhub

A film-production platform built with Django (Python 3.11) and React (Vite).

## Features
- Django backend with apps: accounts, productions, scheduling, vfx, media, finance
- REST API with JWT authentication
- React frontend (Vite)
- Dockerized development environment

## Quick Start

### Prerequisites
- Docker & Docker Compose

### Development Setup

1. Build and start all services:
   ```powershell
   docker-compose up --build
   ```
2. Access frontend: http://localhost:3000
3. Access backend API: http://localhost:8000

## Project Structure
- `backend/` - Django project & apps
- `frontend/` - React app (Vite)
- `docker-compose.yml` - Multi-service orchestration
- `Dockerfile` - Backend Dockerfile

---
Replace placeholder code with your implementation as needed.
