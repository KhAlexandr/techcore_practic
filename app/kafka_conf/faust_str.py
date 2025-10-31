import faust


app = faust.App("stream_apps", broker="kafka://kafka:9092")


topic = app.topic("book_views", value_serializer="raw")


@app.agent(topic)
async def process_message(messages):
    async for message in messages:
        print(f"Получено сообщение: {message.decode('utf-8')}")


if __name__ == "__main__":
    app.main()
