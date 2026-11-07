"""New-file task: create tasks/new_file/slugify.py with a slugify(text) function.

slugify lowercases the text, turns every run of characters other than letters
and digits into a single "-", and strips "-" from both ends.
"""
from slugify import slugify

cases = {
    "Hello World": "hello-world",
    "  Quick Sort/SIMD  ": "quick-sort-simd",
    "C++ & Rust!": "c-rust",
    "already-a-slug": "already-a-slug",
    "Version 2.0": "version-2-0",
    "": "",
}
for text, expected in cases.items():
    assert slugify(text) == expected, (text, slugify(text), expected)
print("ok")
