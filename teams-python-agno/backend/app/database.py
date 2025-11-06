"""
Database connection and configuration
Supports SQLite (default), PostgreSQL, and MongoDB
Easy migration path: SQLite -> PostgreSQL -> MongoDB
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
import os
from pathlib import Path

# Database Configuration
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")  # sqlite, postgresql, mongodb
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/teams_bots.db")

# SQLAlchemy Base
Base = declarative_base()

# Global database session
async_session_maker: async_sessionmaker = None
engine = None


async def connect_db():
    """Initialize database connection"""
    global engine, async_session_maker
    
    if DATABASE_TYPE == "sqlite":
        # Criar diretório data se não existir
        Path("./data").mkdir(exist_ok=True)
        
        # SQLite configuration (async)
        engine = create_async_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=False  # Set to True for debugging
        )
        print(f"✅ Using SQLite database: {DATABASE_URL}")
        
    elif DATABASE_TYPE == "postgresql":
        # PostgreSQL configuration (async)
        engine = create_async_engine(
            DATABASE_URL,
            echo=False,
            pool_size=20,
            max_overflow=0
        )
        print(f"✅ Using PostgreSQL database")
        
    elif DATABASE_TYPE == "mongodb":
        # MongoDB configuration (for future migration)
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient(DATABASE_URL)
        engine = client.get_database("teams_bots")
        print(f"✅ Using MongoDB database")
        return
    
    # Create session maker (SQLite/PostgreSQL)
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Create tables (SQLite/PostgreSQL only)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created")


async def close_db():
    """Close database connection"""
    global engine
    
    if engine and DATABASE_TYPE in ["sqlite", "postgresql"]:
        await engine.dispose()
        print("✅ Database connection closed")
    elif DATABASE_TYPE == "mongodb" and engine:
        engine.client.close()
        print("✅ MongoDB connection closed")


async def get_session() -> AsyncSession:
    """Get database session (SQLite/PostgreSQL)"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


def get_database():
    """Get database instance (MongoDB compatibility)"""
    return engine


# Helper for easy migration
def get_database_info():
    """Get current database configuration"""
    return {
        "type": DATABASE_TYPE,
        "url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL,
        "supports_migration": True,
        "migration_path": "SQLite -> PostgreSQL -> MongoDB"
    }
