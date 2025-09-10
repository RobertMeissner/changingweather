
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.7.18 /uv /uvx /bin/

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --no-install-project

# Copy application code
COPY . .

# Sync project
RUN --mount=type=cache,target=/root/.cache/uv \
      uv sync

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "main.py", "--server.address", "0.0.0.0"]
