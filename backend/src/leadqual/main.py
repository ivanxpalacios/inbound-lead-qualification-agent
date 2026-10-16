from fastapi import FastAPI, Depends, HTTPException, status
from leadqual.config import settings
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from leadqual.db import engine, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError as e:
        logger.exception("Health check failed")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected"
            }
        ) from e
    
    return {
        "status": "healthy",
        "database": "connected"
    }