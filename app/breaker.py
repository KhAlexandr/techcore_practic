import pybreaker
from opentelemetry import metrics

detail_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=10,
)

meter = metrics.get_meter(__name__)
breaker_state = meter.create_observable_gauge(
    name="circuit_breaker_state",
    description="Circuit Breaker state",
    unit="1",
    callbacks=[
        lambda options: [
            metrics.Observation(
                {"closed": 0, "open": 1, "half_open": 2}[detail_breaker.current_state],
                attributes={"breaker": "book_service"},
            )
        ]
    ],
)
