# This module sets up the SQLAlchemy database connection for the application.
# It configures the engine using settings from the config module, defines a session factory,
# and provides a dependency (`get_db`) for managing database sessions in FastAPI routes.
# The `Base` object is used for model class definitions.

"""from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load from .env if it exists (for local dev only)
load_dotenv()

DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Priority: environment variable → fallback to local .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate connection string
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Set it in Railway or .env for local dev.")

# Async DB engine setup
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session