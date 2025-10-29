from confluent_kafka import Consumer, KafkaError

from app.mongo_database import mongo_client

import asyncio

conf = {"bootstrap.servers": "kafka:9092", "group.id": "analytics", "enable.auto.commit": False}

consumer = Consumer(conf)

consumer.subscribe(["book_views"])


async def consume_message():
    db = mongo_client.analytics
    collection = db.book_views
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"Конец раздела {msg.topic()} [{msg.partition()}]")
                elif msg.error():
                    print(f"Ошибка Kafka: {msg.error()}")
            else:
                value = msg.value().decode("utf-8")
                print(f"Получено сообщение: {value}")
                doc = {"topic": msg.topic(), "value": value}
                await collection.insert_one(doc)
                consumer.commit(message=msg, asynchronous=True)
    finally:
        consumer.close()


async def main():
    await consume_message()


if __name__ == "__main__":
    asyncio.run(main())
