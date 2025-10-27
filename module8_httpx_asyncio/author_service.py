import httpx

import asyncio

import backoff

from pybreaker import CircuitBreaker


circuit_breaker = CircuitBreaker(fail_max=5)


class AuthorService:
    def __init__(self):
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
    @circuit_breaker
    async def get_url(self, url):
        response = await self.client.get(url)
        return response


async def main():
    async with AuthorService() as author_repo:
        response = await author_repo.get_url("https://httpbin.org/status/200")
        print(response.status_code)


if __name__ == "__main__":
    asyncio.run(main())
