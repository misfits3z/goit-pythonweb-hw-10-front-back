import os
import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)
"""
This module sets up the connection to a Redis instance using the `redis.asyncio` client.

1. It first attempts to read the Redis URL from the environment variable `REDIS_URL`.
2. If the environment variable is not set, it defaults to `redis://localhost:6379`.

The `redis_client` object is created using the `from_url` method, which establishes a connection to Redis and configures it to decode responses as strings (using `decode_responses=True`).

Usage:
- You can interact with Redis asynchronously using the `redis_client` object, which provides methods to interact with the Redis server.

Example:
    await redis_client.set("key", "value")
    value = await redis_client.get("key")

Environment Variables:
- `REDIS_URL`: The URL of the Redis instance (optional, defaults to `redis://localhost:6379`).
"""
