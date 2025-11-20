import asyncio

import redis.asyncio as redis

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


async def ping_client():
    result = await redis_client.ping()
    return result


async def main():
    result = await ping_client()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
