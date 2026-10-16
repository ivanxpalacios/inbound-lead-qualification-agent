from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from leadqual.config import settings

# Creates the connection pool
engine = create_async_engine(settings.database_url.get_secret_value())

# Template that knows how to create a session on one of the connections from the engine
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Function that FastAPI will call on every request, provides a session to the database
# so FastAPI can give it to a specific endpoint to interact with it.
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session