import asyncio
import time


def block_async(seconds):
    start = time.time()
    time.sleep(seconds)
    return time.time() - start


async def main():
    tasks = [
        asyncio.to_thread(block_async, 5),
        asyncio.to_thread(block_async, 5),
        asyncio.to_thread(block_async, 5),
        asyncio.to_thread(block_async, 5),
        asyncio.to_thread(block_async, 5),
    ]
    results = await asyncio.gather(*tasks)
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
