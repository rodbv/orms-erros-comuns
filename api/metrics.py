import time
import tracemalloc
from functools import wraps


def measure_time_and_memory(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        inicio = time.monotonic()

        response = view_func(*args, **kwargs)

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tempo = f"{time.monotonic() - inicio:.2f}".replace(".", ",")
        memory_str = f"{peak / (1024 * 1024):.1f}"

        data = getattr(response, "data", None)
        if isinstance(data, list):
            payload = {"results": data}
        elif isinstance(data, dict):
            payload = data
            payload.setdefault("results", [])
        else:
            payload = {"results": []}

        payload["elapsed"] = tempo
        payload["memory_mb"] = memory_str

        response.data = payload
        return response

    return wrapper
