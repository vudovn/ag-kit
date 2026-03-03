"""
Distributed Tracing com Jaeger
Rastreia todas as conversas através de todos os sistemas
"""

import logging
from typing import Optional

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.jaeger.thrift import JaegerExporter as JaegerMetricsExporter
from opentelemetry.sdk.resources import Resource

logger = logging.getLogger(__name__)


def setup_tracing(
    service_name: str = "luna-backend",
    jaeger_host: str = "localhost",
    jaeger_port: int = 6831,
    environment: str = "development",
):
    """Configurar tracing distribuído com Jaeger"""

    # Configurar exportador Jaeger
    jaeger_exporter = JaegerExporter(
        agent_host_name=jaeger_host,
        agent_port=jaeger_port,
    )

    # Configurar tracer provider
    resource = Resource.create(
        {"service.name": service_name, "environment": environment, "version": "3.0.0"}
    )

    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    trace.set_tracer_provider(trace_provider)

    # Instrumentar FastAPI
    # Nota: Deve ser chamado passandos os argumentos se não for via middleware
    # Mas a forma mais segura no lifespan é instrumentar o objeto app
    pass  # Removido daqui para ser chamado no main.py com o objeto app

    # Instrumentar Redis
    RedisInstrumentor().instrument()

    # Instrumentar Requests
    RequestsInstrumentor().instrument()

    # Metrics desativadas por incompatibilidade de versão do JaegerExporter no v3.0
    pass

    logger.info(
        f"Tracing configurado: {service_name} -> Jaeger {jaeger_host}:{jaeger_port}"
    )


class TracingHelper:
    """Helper para criar spans customizados"""

    @staticmethod
    def get_tracer(name: str = "luna.services"):
        """Obter tracer para criar spans"""
        return trace.get_tracer(name)

    @staticmethod
    def create_span(name: str, attributes: Optional[dict] = None):
        """Context manager para criar span"""
        from contextlib import contextmanager

        @contextmanager
        def span_context():
            tracer = trace.get_tracer("luna")
            with tracer.start_as_current_span(name) as span:
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, str(value))
                yield span

        return span_context()

    @staticmethod
    def trace_conversation(conversation_id: str, phone: str):
        """Trace de conversa completa"""
        from contextlib import contextmanager

        @contextmanager
        def conversation_span():
            tracer = trace.get_tracer("luna.conversations")
            with tracer.start_as_current_span("conversation") as span:
                span.set_attribute("conversation.id", conversation_id)
                span.set_attribute("customer.phone", phone)
                span.set_attribute("span.kind", "server")
                yield span

        return conversation_span()
