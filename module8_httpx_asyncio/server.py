import asyncio

import greeter_pb2
import greeter_pb2_grpc
import grpc


class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    async def SayHello(self, request, context):
        return greeter_pb2.HelloReply(message=f"Привет, {request.name}!")


async def serve():
    server = grpc.aio.server()
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Сервер запущен на порту 50051")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
