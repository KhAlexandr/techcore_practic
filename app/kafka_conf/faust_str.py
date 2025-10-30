import asyncio

import faust


app = faust.App("stream_app", broker="kafka://kafka:9092")


topic = app.topic("book_views", value_type=str)


@app.agent(topic)
async def process_message(messages):
    async for message in messages:
        print(f"Получено сообщение: {message}")


if __name__ == "__main__":
    app.main()
