"""Benchmark for the perf task. Prints one JSON object, which hive shows in its Benchmark column."""
import json
import sys
import timeit
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fib import fib  # noqa: E402

runs = 2000
seconds = timeit.timeit(lambda: fib(90), number=runs)
print(json.dumps({"fib90_us": round(seconds / runs * 1e6, 2)}))
