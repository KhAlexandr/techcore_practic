import asyncio


async def fetch_data():
    await asyncio.sleep(1)
    print("Я выполнился")


async def main():
    await fetch_data()


if __name__ == "__main__":
    asyncio.run(main())
