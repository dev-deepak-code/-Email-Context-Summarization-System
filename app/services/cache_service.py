from typing import Optional
from redis import asyncio as aioredis
from app.config import settings

class CacheService:
    def __init__(self):
        # We initialize decode_responses=True so that we get strings back instead of bytes
        self.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get_summary(self, client_id: str) -> Optional[str]:
        """Retrieves the encrypted summary string from the cache."""
        return await self.redis.get(f"summary:{client_id}")

    async def set_summary(self, client_id: str, encrypted_summary: str, ttl_seconds: int = 3600):
        """Caches the encrypted summary string."""
        await self.redis.set(f"summary:{client_id}", encrypted_summary, ex=ttl_seconds)

    async def invalidate_summary(self, client_id: str):
        """Removes the cached summary for a given client."""
        await self.redis.delete(f"summary:{client_id}")

cache_service = CacheService()
