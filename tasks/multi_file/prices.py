PRICES_CENTS = {"apple": 50, "bread": 250, "milk": 120}


def unit_price(item: str) -> int:
    """Price of one item, in cents."""
    return PRICES_CENTS[item] // 100
