from motor.motor_asyncio import AsyncIOMotorClient

import asyncio


mongo_client = AsyncIOMotorClient(
    "mongodb://admin:password@localhost:27017"
)


async def ping_mongo_client():
    try:
        await mongo_client.admin.command("ping")
        print("Есть подключение")
    except Exception as e:
        print(f"{e}")


async def main():
    await ping_mongo_client()


if __name__ == "__main__":
    asyncio.run(main())
