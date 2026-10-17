import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, Response, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from leadqual.config import settings
from leadqual.db import engine, get_session

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

class HealthCheckResponse(BaseModel):
    status: Literal["healthy", "unhealthy"]
    database: Literal["connected", "disconnected"]

@app.get("/health", responses={503: {"model": HealthCheckResponse}})
async def health_check(
    response: Response,
    session: AsyncSession = Depends(get_session)
) -> HealthCheckResponse:
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        # An unreachable database is a health result, not an error, so it is
        # returned rather than raised. That is why ERR-2's handler isn't used here.
        logger.exception("Health check failed")

        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return HealthCheckResponse(
            status="unhealthy",
            database="disconnected"
        )
    
    return HealthCheckResponse(
        status="healthy",
        database="connected"
    )