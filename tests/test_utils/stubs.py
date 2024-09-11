"""Stubs for testing utils package."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Self

if TYPE_CHECKING:
    from types import TracebackType


class SpanStub:
    """A stub for simulating a tracing span."""

    def __enter__(self) -> Self:
        """Simulate entering a context."""
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        """Simulate exiting a context."""

    @property
    def name(self) -> Literal["test_span"]:
        """Simulate getting the span name."""
        return "test_span"


class TracerStub:
    """A stub for simulating an OpenTelemetry tracer."""

    def start_as_current_span(self, span_name: str) -> SpanStub:
        """Simulate starting a span as the current span."""
        assert span_name == "test_span"
        return SpanStub()


class TraceStub:
    """A stub for the opentelemetry.trace module."""

    def get_tracer(self, module_name: str) -> TracerStub:
        """Simulate getting a tracer."""
        assert module_name == "test_module"
        return TracerStub()
