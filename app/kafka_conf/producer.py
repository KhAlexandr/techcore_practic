import json
from datetime import datetime

from aiokafka import AIOKafkaProducer

_producer = None


async def get_producer():
    global _producer
    if _producer is None:
        _producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    return _producer


async def view_book(book_id: int):
    p = await get_producer()
    data = {
        "book_id": book_id,
        "action": "view",
        "timestamp": datetime.now().isoformat(),
        "user_agent": "web",
    }
    await p.send_and_wait(
        "book_views", key=str(book_id).encode(), value=json.dumps(data).encode()
    )
