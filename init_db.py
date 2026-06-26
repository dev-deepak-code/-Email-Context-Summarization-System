import asyncio
from app.db.database import engine
from app.db.base import Base
# Make sure models are loaded so Base.metadata knows about them
import app.models

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
    print("Database tables created successfully!")
