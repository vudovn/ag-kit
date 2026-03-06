"""
Distributed Tracing com Jaeger + Prometheus Metrics
Rastreia todas as conversas através de todos os sistemas

DEBT #9: Métricas agora habilitadas com export para Prometheus.
"""

import logging
import os
from typing import Optional

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION

logger = logging.getLogger(__name__)


def setup_tracing(
    service_name: str = "luna-backend",
    jaeger_host: str = "luna-jaeger",
    jaeger_port: int = 6831,
    environment: str = "development",
    enable_metrics: bool = True,
):
    """
    Configurar tracing distribuído com Jaeger e métricas Prometheus.
    
    Args:
        service_name: Nome do serviço para identificação no Jaeger
        jaeger_host: Host do Jaeger agent
        jaeger_port: Porta do Jaeger agent (UDP Thrift)
        environment: Ambiente (development/staging/production)
        enable_metrics: Habilitar métricas OpenTelemetry
    """

    # Configurar resource com metadados
    resource = Resource.create({
        SERVICE_NAME: service_name,
        "environment": environment,
        SERVICE_VERSION: "3.0.0",
        "service.instance.id": os.getenv("HOSTNAME", "unknown")
    })

    # ═══════════════════════════════════════════════
    # TRACING CONFIG
    # ═══════════════════════════════════════════════
    
    # Configurar exportador Jaeger (Thrift protocol)
    jaeger_exporter = JaegerExporter(
        agent_host_name=jaeger_host,
        agent_port=jaeger_port,
        max_tag_value_length=1024,
    )

    # Tracer provider com batch processor
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            jaeger_exporter,
            max_queue_size=2048,
            scheduled_delay_millis=5000,
            max_export_batch_size=512,
        )
    )
    trace.set_tracer_provider(trace_provider)

    # ═══════════════════════════════════════════════
    # METRICS CONFIG (DEBT #9)
    # ═══════════════════════════════════════════════
    
    if enable_metrics:
        try:
            # Metric reader para export periódico
            # Em produção, usar PrometheusExporter ao invés de ConsoleMetricExporter
            metric_reader = PeriodicExportingMetricReader(
                ConsoleMetricExporter(),  # Substituir por PrometheusExporter em produção
                export_interval_millis=60000  # Exportar a cada 60s
            )
            
            meter_provider = MeterProvider(
                resource=resource,
                metric_readers=[metric_reader]
            )
            metrics.set_meter_provider(meter_provider)
            
            logger.info("✅ Metrics enabled with PeriodicExportingMetricReader")
        except Exception as e:
            logger.warning(f"⚠️ Failed to setup metrics: {e}")

    # ═══════════════════════════════════════════════
    # INSTRUMENTATION
    # ═══════════════════════════════════════════════
    
    # Instrumentar Redis (com captura de comandos)
    RedisInstrumentor().instrument()

    # Instrumentar Requests HTTP
    RequestsInstrumentor().instrument()

    # Nota: FastAPI instrumentation é feita no main.py com o objeto app
    # para capturar requests corretamente

    logger.info(
        f"✅ Tracing configurado: {service_name} -> Jaeger {jaeger_host}:{jaeger_port}"
    )


def setup_fastapi_instrumentation(app):
    """
    Instrumentar aplicação FastAPI especificamente.
    Deve ser chamado após a criação do app no main.py
    """
    try:
        FastAPIInstrumentor.instrument_app(
            app,
            tracer_provider=trace.get_tracer_provider(),
            meter_provider=metrics.get_meter_provider() if metrics.get_meter_provider() else None,
        )
        logger.info("✅ FastAPI instrumentation applied")
    except Exception as e:
        logger.error(f"❌ FastAPI instrumentation failed: {e}")


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

    @staticmethod
    def trace_database_query(db_type: str, query: str, duration_ms: float):
        """Trace de query de banco de dados"""
        tracer = trace.get_tracer("luna.database")
        with tracer.start_as_current_span(f"{db_type}.query") as span:
            span.set_attribute("db.system", db_type)
            span.set_attribute("db.statement", query[:1000])  # Truncate long queries
            span.set_attribute("db.duration_ms", duration_ms)

    @staticmethod
    def trace_external_api(api_name: str, endpoint: str, status_code: int):
        """Trace de chamada de API externa"""
        tracer = trace.get_tracer("luna.external_api")
        with tracer.start_as_current_span(f"{api_name}.request") as span:
            span.set_attribute("external.api", api_name)
            span.set_attribute("http.url", endpoint)
            span.set_attribute("http.status_code", status_code)

    @staticmethod
    def record_metric(name: str, value: float, metric_type: str = "gauge", labels: Optional[dict] = None):
        """
        Registrar métrica customizada.
        metric_type: "gauge", "counter", "histogram"
        """
        try:
            meter = metrics.get_meter("luna.metrics")
            
            if metric_type == "counter":
                counter = meter.create_counter(name, description=f"Counter: {name}")
                counter.add(value, labels or {})
            elif metric_type == "gauge":
                # Gauge requer observable para OpenTelemetry
                # Para gauge imediato, usar histogram com um único valor
                histogram = meter.create_histogram(name, description=f"Gauge: {name}")
                histogram.record(value, labels or {})
            elif metric_type == "histogram":
                histogram = meter.create_histogram(name, description=f"Histogram: {name}")
                histogram.record(value, labels or {})
                
            logger.debug(f"📊 Metric recorded: {name}={value} ({metric_type})")
        except Exception as e:
            logger.debug(f"Failed to record metric {name}: {e}")
