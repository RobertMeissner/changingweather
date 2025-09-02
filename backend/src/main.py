import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import routes
from src.core.config import settings
from src.db.session import add_postgresql_extension


logger = logging.getLogger(__name__)


tags_metadata = [
    {
        "name": "health",
        "description": "Health check for api",
    }
]

app = FastAPI(
    title="changingweather",
    description="base project for fastapi backend",
    version=settings.VERSION,
    openapi_url=f"/{settings.VERSION}/openapi.json",
    openapi_tags=tags_metadata,
)


def on_startup() -> None:
    add_postgresql_extension()
    logger.info("FastAPI app running...")


app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.add_event_handler("startup", on_startup)

app.include_router(routes.home_router)
app.include_router(routes.api_router, prefix=f"/{settings.VERSION}")
