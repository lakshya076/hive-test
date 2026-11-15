PRICES_CENTS = {"apple": 50, "bread": 250, "milk": 120}


def unit_price(item: str) -> int:
    """Return the price of an item in cents."""
    return PRICES_CENTS[item]
