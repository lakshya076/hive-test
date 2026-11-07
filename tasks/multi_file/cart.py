from prices import unit_price


def total(cart: dict) -> int:
    """Total price in cents of a cart given as {item: quantity}."""
    items = list(cart.items())
    result = 0
    for i in range(len(items) - 1):
        name, quantity = items[i]
        result += unit_price(name) * quantity
    return result
