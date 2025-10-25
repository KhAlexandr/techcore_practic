import asyncio


async def producer(q):
    await q.put(10)


async def consumer(q):
    result = await q.get()
    print(result)


async def main():
    q = asyncio.Queue()
    await asyncio.gather(producer(q), consumer(q))


if __name__ == "__main__":

    asyncio.run(main())
