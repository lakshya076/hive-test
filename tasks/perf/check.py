"""Performance task: fib() is correct but exponential. fib(90) must finish within 5 seconds."""
import subprocess
import sys
from pathlib import Path

from fib import fib

for n, expected in ((0, 0), (1, 1), (2, 1), (10, 55), (20, 6765)):
    assert fib(n) == expected, (n, fib(n))

# Run the slow case in a child process so a still-exponential fib() fails fast
# instead of hanging until the worker's test_timeout.
try:
    result = subprocess.run(
        [sys.executable, "-c", "from fib import fib; print(fib(90))"],
        cwd=Path(__file__).parent,
        capture_output=True,
        text=True,
        timeout=5,
    )
except subprocess.TimeoutExpired:
    raise SystemExit("fib(90) took longer than 5 seconds: make fib() fast")
assert result.stdout.strip() == "2880067194370816120", (result.stdout, result.stderr)
print("ok")
