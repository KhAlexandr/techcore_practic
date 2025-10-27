import httpx

import asyncio


class AuthorService:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get_url(self, url):
        response = await asyncio.wait_for(self.client.get(url), timeout=2.0)
        return response


author_repo = AuthorService()


async def get_response(url):
    response = await author_repo.get_url(url)
    print(response.json())


async def main():
    await get_response("https://httpbin.org/get")


if __name__ == "__main__":
    asyncio.run(main())
