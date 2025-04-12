import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from src.conf.config import config


# class DatabaseSessionManager:
#     def __init__(self, url: str):
#         self._engine: AsyncEngine | None = create_async_engine(url)
#         self._session_maker: async_sessionmaker = async_sessionmaker(
#             autoflush=False, autocommit=False, bind=self._engine
#         )

#     @contextlib.asynccontextmanager
#     async def session(self):
#         if self._session_maker is None:
#             raise Exception("Database session is not initialized")
#         session = self._session_maker()
#         try:
#             yield session
#         except SQLAlchemyError as e:
#             await session.rollback()
#             raise  # Re-raise the original error
#         finally:
#             await session.close()


# sessionmanager = DatabaseSessionManager(config.DB_URL)


# async def get_db():
#     async with sessionmanager.session() as session:
#         yield session


class DatabaseSessionManager:
    """
    Manages asynchronous database sessions using SQLAlchemy.

    This class creates an async engine and session factory, and provides an
    asynchronous context manager to handle sessions with proper commit/rollback/close logic.

    Attributes:
        _engine (AsyncEngine | None): SQLAlchemy asynchronous engine instance.
        _session_maker (async_sessionmaker): Factory for creating async database sessions.
    """

    def __init__(self, url: str):
        """
        Initializes the database session manager.

        Args:
            url (str): The database connection URL.
        """
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        """
        Provides an asynchronous context-managed session.

        Ensures that the session is properly committed or rolled back depending
        on whether an exception is raised during use.

        Yields:
            AsyncSession: A SQLAlchemy asynchronous session.

        Raises:
            SQLAlchemyError: If a database error occurs during operations.
        """
        if self._session_maker is None:
            raise Exception("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    """
    Dependency function that provides an asynchronous database session.

    Yields:
        AsyncSession: A SQLAlchemy asynchronous session for use in route handlers.
    """
    async with sessionmanager.session() as session:
        yield session
