import httpx

import asyncio

import backoff


class AuthorService:
    def __init__(self):
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
    async def get_url(self, url):
        response = await asyncio.wait_for(self.client.get(url), timeout=2.0)
        return response


async def main():
    async with AuthorService() as author_repo:
        response = await author_repo.get_url("https://httpbin.org/get")
        print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
