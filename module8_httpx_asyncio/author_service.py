import httpx

import asyncio

import backoff

from pybreaker import CircuitBreaker, CircuitBreakerError

from unittest.mock import AsyncMock

from circuitbreaker import circuit


circuit_breaker = CircuitBreaker(fail_max=5, reset_timeout=5)


class AuthorService:
    def __init__(self):
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient()
        return self
        # self.client = AsyncMock()
        # self.client.get.side_effect = Exception("Mocked error")
        # return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        # pass

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
    @circuit(failure_threshold=5)
    async def get_url(self, url):
        response = await self.client.get(url)
        response.raise_for_status()
        return response


async def main():
    async with AuthorService() as author_repo:
        for i in range(6):
            try:
                response = await author_repo.get_url(
                    "https://example.com/api")
            except CircuitBreakerError as e:
                print(f"Ошибка: {type(e).__name__}")
            except Exception as e:
                print(f"Другая ошибка: {type(e).__name__}")


if __name__ == "__main__":
    asyncio.run(main())
