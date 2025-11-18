from aiokafka import AIOKafkaConsumer

import json
from datetime import datetime

from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

from app.mongo_database import mongo_client
from app.open_telemetry import setup_tracing


setup_tracing("analytics_worker")

AIOKafkaInstrumentor().instrument()
PymongoInstrumentor().instrument()
# Я не знаю как сделать трассировку с асинхронным манго, везде написано что для него
# нет асинхронного варианта


class AnalyticsWorker:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            'book_views',  # топик сразу здесь
            bootstrap_servers='kafka:9092',
            group_id='analytics',
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )
        self.connection = mongo_client.analytics.book_views

    async def book_view(self):
        print("🔍 Consumer started listening...")
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                json_data = json.loads(msg.value.decode())
                print(f"📨 Partition {msg.partition}: {json_data}")

                data = {
                    "kafka_message": json_data,
                    "topic": msg.topic,
                    "partition": msg.partition,
                    "offset": msg.offset,
                    "timestamp": datetime.now()
                }
                await self.connection.insert_one(data)
                print("Загружен в монго")
                await self.consumer.commit()

        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
        except Exception as e:
            print(f"❌ Consumer error: {e}")
        finally:
            await self.consumer.stop()
