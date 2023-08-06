# opentelemetry-samplers-python

**NOTE**: This is experimental and is subject to change a _lot_ or go away entirely. Use with caution.

Honeycomb Samplers for use with the OpenTelemetry Python SDK

## Samplers

### Deterministic Sampler

This is a port of the deterministic sampler included in our [Python Beeline](https://github.com/honeycombio/beeline-python). To use it, just instantiate it with a sample rate:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from opentelemetry.ext.honeycomb import DeterministicSampler

sampler = DeterministicSampler(5)
trace.set_tracer_provider(TracerProvider(sampler=sampler))

trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(ConsoleSpanExporter())
)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("Test span"):
    with tracer.start_as_current_span("bar"):
        with tracer.start_as_current_span("baz"):
            print("Hello world from OpenTelemetry Python!")
```
