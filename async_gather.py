import asyncio
import time


async def task_1():
    await asyncio.sleep(1)
    return "Результат 1"


async def task_2():
    await asyncio.sleep(2)
    return "Результат 2"


async def task_3():
    await asyncio.sleep(3)
    return "Результат 3"


async def main():
    results = await asyncio.gather(task_1(), task_2(), task_3())
    print(*results)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)
