# Changing Weather Project Overview

## Purpose
A weather data application that allows users to see how weather has changed at their location over time. Built with FastAPI backend and Streamlit frontend.

## Tech Stack
- **Backend**: FastAPI, Python 3.11+, SQLAlchemy, PostgreSQL, Redis, Alembic
- **Frontend**: Streamlit (development dashboard)
- **External APIs**: OpenMeteo weather API
- **Development**: Docker Compose, uv (dependency management)
- **Testing**: pytest, pytest-cov, pytest-mock
- **Code Quality**: black, isort, ruff, mypy, pre-commit hooks

## Architecture
Follows Clean/Hexagonal Architecture with clear separation of layers:
- **Domain Layer**: Business entities and ports (weather domain)
- **Application Layer**: Weather service orchestration
- **Infrastructure Layer**: External adapters (Redis, OpenMeteo, PostgreSQL)
- **Presentation Layer**: FastAPI controllers and Streamlit UI

## Key Features
- Weather data fetching with caching (Redis)
- Historical weather analysis
- Coordinate-based queries
- Database persistence with migrations
- CORS-enabled API
- Health check endpoints
