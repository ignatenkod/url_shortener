#!/usr/bin/env python
import asyncio
from sqlalchemy import text
from url_shortener.database.session import async_engine
from url_shortener.config import settings

async def create_database():
    async with async_engine.connect() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
        await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {settings.postgres_db}"))
        await conn.commit()

if __name__ == "__main__":
    asyncio.run(create_database())
