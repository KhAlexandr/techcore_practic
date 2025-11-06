import os

from dotenv import load_dotenv

from opentelemetry import trace, metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource


load_dotenv()


def setup_tracing(service_name: str):
    resource = Resource.create({"service.name": service_name})

    tracer_provider = TracerProvider(resource=resource)

    trace.set_tracer_provider(tracer_provider)

    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger-agent.monitoring.svc.cluster.local",
        agent_port=6831,
    )

    span_processor = BatchSpanProcessor(jaeger_exporter)

    tracer_provider.add_span_processor(span_processor)

    return tracer_provider


def setup_metrics(service_name: str):
    resource = Resource.create({"service.name": service_name})
    reader = PrometheusMetricReader()

    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)

    return meter_provider
