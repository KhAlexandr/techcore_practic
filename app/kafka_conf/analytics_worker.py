from confluent_kafka import Consumer


conf = {"bootstrap.servers": "localhost:9092", "group.id": "analytics"}

consumer = Consumer(conf)
