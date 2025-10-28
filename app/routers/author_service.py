import httpx

import asyncio

import backoff

from pybreaker import CircuitBreaker, CircuitBreakerError

from circuitbreaker import circuit


circuit_breaker = CircuitBreaker(fail_max=5, reset_timeout=5)
semaphore = asyncio.Semaphore(5)


class AuthorService:
    def __init__(self):
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    @circuit(failure_threshold=5)
    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
    async def get_author(self, author_id):
        async with semaphore:
            task1 = asyncio.create_task(
                self.client.get(f"http/api/author/{author_id}")
            )
            task2 = asyncio.create_task(self.client.get("http://review-service/"))
            response = await asyncio.gather(task1, task2, return_exceptions=True)
            response_1 = response[0]
            response_1.raise_for_status()
            return response_1.json()

    async def get_author_name(self, author_id):
        try:
            author = await self.get_author(author_id)
            return author["name"]
        except CircuitBreakerError:
            return "Default Author"
        except Exception as e:
            return "Default Author"


async def main():
    async with AuthorService() as author_repo:
        for i in range(6):
            try:
                await author_repo.get_author(1)
            except CircuitBreakerError as e:
                print(f"Ошибка: {type(e).__name__}")
            except Exception as e:
                print(f"Другая ошибка: {type(e).__name__}")


if __name__ == "__main__":
    asyncio.run(main())
