import asyncio

import greeter_pb2
import greeter_pb2_grpc
import grpc


async def run():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = greeter_pb2_grpc.GreeterStub(channel)
        response = await stub.SayHello(greeter_pb2.HelloRequest(name="Александр"))
        print("Ответ:", response.message)


if __name__ == "__main__":
    asyncio.run(run())
