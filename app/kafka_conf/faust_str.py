import faust


app = faust.App(
    "my-streaming-up",
    broker="kafka://kafka:9092",
    opic_allow_declare=True,
)


input_topic = app.topic("book_views", value_serializer="json")

output_topic = app.topic("book_views_stream", value_serializer="json")


@app.agent(input_topic)
async def process(messages):
    async for message in messages:
        await output_topic.send(value=message)
