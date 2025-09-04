import os


# Set test environment variables before any imports happen
os.environ.setdefault("POSTGRES_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "test")
