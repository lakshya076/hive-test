from prices import unit_price


def total(cart: dict) -> int:
    """Calculate total price of items in cart."""
    result = 0
    for name, quantity in cart.items():
        result += unit_price(name) * quantity
    return result
