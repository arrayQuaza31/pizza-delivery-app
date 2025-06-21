from redis import asyncio as aioredis
from datetime import datetime, timezone
from config_loader import Config


redis_client = aioredis.from_url(
    url=f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}",
    decode_responses=True,
)


async def test_redis_connection() -> None:
    try:
        pong = await redis_client.ping()
        print(f"Redis client is running - response received: {pong}")
    except Exception as e:
        print(f"Encountered an error with Redis: {str(e)}")


async def close_redis_connection() -> None:
    try:
        await redis_client.aclose(close_connection_pool=True)
        print(f"Redis client closed successfully.")
    except Exception as e:
        print(f"Encountered an error while closing Redis: {str(e)}")


async def blacklist_token(jti: str, auto_expiry_timestamp: int) -> None:
    ttl = max(1, (auto_expiry_timestamp - int(datetime.now(timezone.utc).timestamp())))
    await redis_client.setex(
        name=f"revoked:{jti}",
        time=ttl,  # removed from redis after token auto-expires
        value="true",
    )


async def is_blacklisted(jti: str) -> bool:
    return await redis_client.get(name=f"revoked:{jti}") == "true"
