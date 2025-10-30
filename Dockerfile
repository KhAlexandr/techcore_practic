FROM python:3.12-slim
WORKDIR /code
RUN apt-get update && apt-get install -y gcc libpq-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
