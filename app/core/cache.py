from typing import Any
from typing import Optional
from typing import Set
from typing import Union

from redis.asyncio import Redis

from app.core.settings import settings


def cache_key_builder(prefix: str, param: str):
    def builder(func, *args, **kwargs):
        if param in kwargs["kwargs"]:
            return f"{prefix}:{kwargs['kwargs'][param]}"
        raise ValueError(f"Expected '{param}' in kwargs")

    return builder


class CacheManagerError(Exception):
    """Exception raised when CacheManager is not properly initialized."""

    pass


class CacheManager:
    def __init__(self) -> None:
        self._redis_connection: Optional[Redis] = None

    def init(self, redis_url: str = settings.REDIS_URL) -> None:
        self._redis_connection = Redis.from_url(redis_url)

    def _ensure_connection(self) -> Redis:
        """Ensure Redis connection is initialized."""
        if self._redis_connection is None:
            raise CacheManagerError("CacheManager not initialized. Call init() first.")
        return self._redis_connection

    async def get(self, key: str) -> Optional[bytes]:
        """Get Value from Key"""
        return await self._ensure_connection().get(key)

    async def set(
        self,
        key: str,
        value: Union[str, bytes],
        expire: Optional[int] = None,
        pexpire: Optional[int] = None,
    ) -> Optional[bool]:
        """Set Key to Value"""
        return await self._ensure_connection().set(
            name=key,
            value=value,
            ex=expire,
            px=pexpire,
        )

    async def pttl(self, key: str) -> int:
        """Get PTTL from a Key"""
        return int(await self._ensure_connection().pttl(key))

    async def ttl(self, key: str) -> int:
        """Get TTL from a Key"""
        return int(await self._ensure_connection().ttl(key))

    async def pexpire(self, key: str, pexpire: int) -> bool:
        """Sets and PTTL for a Key"""
        return bool(await self._ensure_connection().pexpire(key, pexpire))

    async def expire(self, key: str, expire: int) -> bool:
        """Sets and TTL for a Key"""
        return bool(await self._ensure_connection().expire(key, expire))

    async def incr(self, key: str) -> int:
        """Increases an Int Key"""
        return int(await self._ensure_connection().incr(key))

    async def decr(self, key: str) -> int:
        """Decreases an Int Key"""
        return int(await self._ensure_connection().decr(key))

    async def delete(self, key: str) -> int:
        """Delete value of a Key"""
        return await self._ensure_connection().delete(key)

    async def smembers(self, key: str) -> Set[bytes]:
        """Gets Set Members"""
        return set(await self._ensure_connection().smembers(key))

    async def sadd(self, key: str, value: Any) -> int:
        """Adds a Member to a Set"""
        return await self._ensure_connection().sadd(key, value)

    async def srem(self, key: str, member: Any) -> int:
        """Removes a Member from a Set"""
        return await self._ensure_connection().srem(key, member)

    async def exists(self, key: str) -> int:
        """Checks if a Key exists"""
        return await self._ensure_connection().exists(key)


cache_manager: CacheManager = CacheManager()
