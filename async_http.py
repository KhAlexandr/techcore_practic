import asyncio

import aiohttp


async def get_httpx():

    async with aiohttp.ClientSession() as session:
        response = await session.get("https://python.org")


async def main():
    tasks = [asyncio.ensure_future(get_httpx()) for _ in range(100)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":

    asyncio.run(main())
