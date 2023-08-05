import os
from contextlib import contextmanager

SHOULD_USE_SPAN = False
use_span_env = os.getenv("USE_SPAN", "true").lower()
use_span = "true" in use_span_env or "1" in use_span_env

try:
    if use_span:
        from serverless_sdk import span

        SHOULD_USE_SPAN = True
except ModuleNotFoundError as e:
    SHOULD_USE_SPAN = False


@contextmanager
def safe_span(label, use=True):
    if not SHOULD_USE_SPAN or not use:
        print("should not use span...")
        yield
    else:
        with span(label):
            print("there is span!")
            yield
