from functools import lru_cache

@lru_cache(maxsize=None)
def _fib(n: int) -> int:
    if n < 2:
        return n
    return _fib(n - 1) + _fib(n - 2)

def fib(n: int) -> int:
    """Return the n-th Fibonacci number (fib(0) == 0, fib(1) == 1)."""
    return _fib(n)
