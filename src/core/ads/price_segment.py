"""
Price segment calculation: maps a USD price into one of 5 fixed bands.

"""


def calculate_price_segment(price_usd) -> int | None:
    if price_usd is None:
        return None
    try:
        price = float(price_usd)
    except (TypeError, ValueError):
        return None
    if price < 0:
        return None

    if price < 200:
        return 1
    if price < 500:
        return 2
    if price < 1000:
        return 3
    if price < 5000:
        return 4
    return 5
