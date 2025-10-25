import asyncio


async def stream_data():
    for x in range(10):
        await asyncio.sleep(1)
        yield x


async def main():
    async for data in stream_data():
        print(data)


if __name__ == "__main__":
    asyncio.run(main())
