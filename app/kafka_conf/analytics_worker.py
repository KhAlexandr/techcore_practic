from aiokafka import AIOKafkaConsumer

from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

from app.mongo_database import mongo_client
from app.open_telemetry import setup_tracing

import asyncio


setup_tracing("analytics_worker")

AIOKafkaInstrumentor().instrument()
PymongoInstrumentor().instrument()
# Я не знаю как сделать трассировку с асинхронным манго, везде написано что для него
# нет асинхронного варианта


async def consume_message():
    consumer = AIOKafkaConsumer(
        "book_views",
        bootstrap_servers="kafka:9092",
        group_id="analytics",
        enable_auto_commit=False,
    )
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
