from confluent_kafka import Consumer, KafkaError

import asyncio


conf = {"bootstrap.servers": "localhost:9092", "group.id": "analytics"}

consumer = Consumer(conf)

consumer.subscribe(["book_views"])


async def consume_message():
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
                print(f'Получено сообщение: {msg.value().decode("utf-8")}')
    finally:
        consumer.close()


async def main():
    await consume_message()


if __name__ == "__main__":
    asyncio.run(main())
