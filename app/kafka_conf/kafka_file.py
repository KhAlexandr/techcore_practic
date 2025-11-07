from aiokafka import AIOKafkaProducer


async def producer():
    return AIOKafkaProducer(bootstrap_servers="kafka:9092")

