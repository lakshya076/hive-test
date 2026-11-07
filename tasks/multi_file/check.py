"""Multi-file task: one bug in prices.py and one in cart.py; both must be fixed."""
from cart import total
from prices import unit_price

assert unit_price("bread") == 250, unit_price("bread")
assert total({}) == 0, total({})
assert total({"milk": 1}) == 120, total({"milk": 1})
expected = 2 * 50 + 1 * 250 + 3 * 120
assert total({"apple": 2, "bread": 1, "milk": 3}) == expected, total({"apple": 2, "bread": 1, "milk": 3})
print("ok")
