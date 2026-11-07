"""Conflict task: every fix rewrites the same lines of greet.py.

Run it with two strategies, merge one, then merge the other: the second merge
conflicts, which exercises hive merge's conflict handling.
"""
from greet import greet

assert greet("ari") == "Hello, ari!", greet("ari")
assert greet("") == "Hello, world!", greet("")
assert greet("  Hermes ") == "Hello, Hermes!", greet("  Hermes ")
print("ok")
