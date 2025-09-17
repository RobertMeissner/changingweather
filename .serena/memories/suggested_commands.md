# Suggested Commands for Changing Weather Project

## Development Environment
- `make up-dev` - Start development environment with docker-compose
- `make down-dev` - Stop development environment
- `make build-dev` - Rebuild containers without cache
- `make bash` - Connect to backend container

## Code Quality & Testing
- `make test` - Run pytest with coverage report
- `make lint` - Run ruff linting
- `make black` - Format code with black
- `make isort` - Sort imports with isort
- `make mypy` - Run type checking with mypy
- `make all` - Run all code quality checks (black, isort, lint, mypy)

## Database Management
- `make alembic-init` - Initialize first migration
- `make alembic-make-migrations "message"` - Create new migration
- `make alembic-migrate` - Apply migrations
- `make init-db` - Initialize database with migrations

## Frontend Development
- `make streamlit` - Start Streamlit development server
- `make streamlit-build` - Install Streamlit dependencies

## Pre-commit Hooks
- `make hooks` - Install pre-commit hooks
- `pre-commit run --all-files` - Run all pre-commit hooks manually

## System Commands (Linux)
- Standard Linux commands: `ls`, `cd`, `grep`, `find`, `git`
- Docker commands: `docker compose logs`, `docker compose ps`
