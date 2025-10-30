from fastapi import FastAPI, HTTPException
import httpx


app = FastAPI()


# @app.get("/getaway/api/books/{book_id}")
# async def get_book(book_id: int):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"http://api:80/api/books/{book_id}")
#         print(f"Gateway: получил ответ {response.status_code}")
#         return response.json()


@app.get("/getaway/api/books/{book_id}")
async def get_book(book_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://api:80/api/books/{book_id}", timeout=10.0
            )
            return response.json()
        except Exception as e:
            return {"error": f"Ошибка Gateway: {str(e)}"}
