## TechCore Practice Project

## Запуск

```bach
docker build -t techcore_practic-app:latest .
```

```bash
docker-compose up -d
```

## Сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| API | 8000 | Основное FastAPI приложение |
| Gateway | 8080 | API Gateway |
| PostgreSQL | 5432 | База данных |
| Redis | 6379 | Кэш и брокер для Celery |
| RabbitMQ | 5672, 15672 | Брокер сообщений (UI: 15672) |
| MongoDB | 27017 | NoSQL база данных |
| Kafka | 9092 | Стриминговая платформа |
| Zipkin | 9411 | Distributed tracing |
| Jaeger | 16686 | Tracing система |
| Grafana | 3000 | Мониторинг и дашборды |
| Prometheus | 9090 | Сбор метрик |
| Loki | 3100 | Логи |
| Flower | 5555 | Мониторинг Celery |

## Компоненты

- **FastAPI** - основной фреймворк
- **Celery** - асинхронные задачи (worker + beat)
- **Kafka/Faust** - стриминг данных
- **PostgreSQL** - основная БД
- **MongoDB** - документная БД
- **Redis** - кэш и брокер
- **OpenTelemetry** - трассировка
- **Prometheus/Grafana/Loki** - мониторинг и логи

## Переменные окружения

Основные настройки в `docker-compose.yml`:

- `DATABASE_URL` - PostgreSQL подключение
- `REDIS_HOST` - Redis хост
- `KAFKA_BOOTSTRAP_SERVERS` - Kafka брокеры
- `MONGODB_URL` - MongoDB подключение
- `CELERY_BROKER_URL` - брокер для Celery

## Доступ

- API: http://localhost:8000
- Gateway: http://localhost:8080
- RabbitMQ UI: http://localhost:15672 (guest/guest)
- Grafana: http://localhost:3000 (admin/admin)
- Jaeger UI: http://localhost:16686
- Flower: http://localhost:5555
