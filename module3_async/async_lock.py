import asyncio


lock = asyncio.Lock()


async def get_lock(i):

    async with lock:
        print(f"Корутина {i}")
        await asyncio.sleep(0.1)
    print(f"завершилась {i}")


async def main():
    results = [asyncio.ensure_future(get_lock(i)) for i in range(1, 11)]
    await asyncio.gather(*results)


if __name__ == "__main__":
    asyncio.run(main())
