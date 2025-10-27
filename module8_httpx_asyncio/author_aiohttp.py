import asyncio

import aiohttp


class AuthorService:
    async def get_url(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://httpbin.org/status/200")
            return response


author_repo = AuthorService()


async def main():
    result = await author_repo.get_url()
    print(result.status)


if __name__ == "__main__":
    asyncio.run(main())
