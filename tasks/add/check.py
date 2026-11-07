"""Smoke task: add() subtracts instead of adding."""
from add import add

assert add(2, 3) == 5, add(2, 3)
assert add(-1, 1) == 0, add(-1, 1)
assert add(0, 0) == 0, add(0, 0)
print("ok")
