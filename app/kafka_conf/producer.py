from aiokafka import AIOKafkaProducer
import json
from datetime import datetime


producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")


async def view_book(book_id: int):
    data = {
        "book_id": book_id,
        "action": "view",
        "timestamp": datetime.now().isoformat(),
        "user_agent": "web"
    }
    await producer.send_and_wait(
        "book_views",
        key=str(book_id).encode(),
        value=json.dumps(data).encode()
    )

