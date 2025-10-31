import os

from dotenv import load_dotenv

from opentelemetry import trace, metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.resources import Resource


load_dotenv()


def setup_tracing(service_name: str):
    resource = Resource.create({"service.name": service_name})

    tracer_provider = TracerProvider(resource=resource)

    trace.set_tracer_provider(tracer_provider)

    zipkin_exporter = ZipkinExporter(
        endpoint=os.getenv("ZIPKIN_ENDPOINT", "http://localhost:9411/api/v2/spans"),
    )

    span_processor = BatchSpanProcessor(zipkin_exporter)

    tracer_provider.add_span_processor(span_processor)

    return tracer_provider


def setup_metrics(service_name: str):
    resource = Resource.create({"service.name": service_name})
    reader = PrometheusMetricReader()

    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[reader]
    )
    metrics.set_meter_provider(meter_provider)

    return meter_provider
