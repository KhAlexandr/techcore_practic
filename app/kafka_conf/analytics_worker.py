from aiokafka import AIOKafkaConsumer

from app.mongo_database import mongo_client

import asyncio

consumer = AIOKafkaConsumer(
    "book_views",
    bootstrap_servers="kafka:9092",
    group_id="analytics",
    enable_auto_commit=False,
)


async def consume_message():
    db = mongo_client.analytics
    collection = db.book_views
    await consumer.start()
    try:
        async for msg in consumer:
            value = msg.value.decode("utf-8")

            doc = {
                "topic": msg.topic,
                "value": value,
            }
            await collection.insert_one(doc)

            await consumer.commit()

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await consumer.stop()


async def main():
    await consume_message()


if __name__ == "__main__":
    asyncio.run(main())
