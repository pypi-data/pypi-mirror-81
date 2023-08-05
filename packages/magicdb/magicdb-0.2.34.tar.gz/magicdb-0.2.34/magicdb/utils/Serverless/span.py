import os
from contextlib import contextmanager

SHOULD_USE_SPAN = False
try:
    if os.getenv("USE_SPAN", True):
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
