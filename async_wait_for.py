import asyncio


async def wait_for():
    await asyncio.sleep(5)


async def main():
    await asyncio.wait_for(wait_for(), timeout=2)


if __name__ == "__main__":

    asyncio.run(main())
