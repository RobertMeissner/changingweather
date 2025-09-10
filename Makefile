all: black isort lint mypy

# docker
up:
	@echo "bringing up project...."
	docker compose up

up-dev:
	@echo "bringing up dev project...."
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

down:
	@echo "bringing down project...."
	docker compose down

down:
	@echo "bringing down dev project...."
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

build:
	@echo "building without cache"
	docker compose build --no-cache backend


build-dev:
	@echo "building dev without cache"
	docker compose -f docker-compose.yml -f docker-compose.dev.yml build --no-cache

bash:
	@echo "connecting to container...."
	docker compose exec backend bash

# alembic
alembic-scaffold:
	@echo "scaffolding migrations folder..."
	docker compose exec backend alembic init migrations

alembic-init:
	@echo "initializing first migration...."
	docker compose exec backend alembic revision --autogenerate -m "init"

alembic-make-migrations:
	@echo "creating migration file...."
	docker compose exec backend alembic revision --autogenerate -m "add year"

alembic-migrate:
	@echo "applying migration...."
	docker compose exec backend alembic upgrade head

# lint
test:
	@echo "running pytest...."
	docker compose exec backend pytest --cov-report xml --cov=src tests/

lint:
	@echo "running ruff...."
	docker compose exec backend ruff check src

black:
	@echo "running black...."
	docker compose exec backend black .

isort:
	@echo "running isort...."
	docker compose exec backend isort .

mypy:
	@echo "running mypy...."
	docker compose exec backend mypy src/

# database
init-db: alembic-init alembic-migrate
	@echo "initializing database...."
	docker compose exec backend python3 src/db/init_db.py

# misc
check: BREW-exists
BREW-exists: ; @which brew > /dev/null

hooks: check
	@echo "installing pre-commit hooks...."
	pre-commit install

# Streamlit dev frontend
streamlit:
	@echo "starting streamlit dev frontend...."
	cd apps/frontend_streamlit && uv run streamlit run main.py

streamlit-build:
	@echo "installing streamlit dependencies...."
	cd apps/frontend_streamlit && uv sync
