"""Order line value object."""

from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class OrderLine:
    """Order line entity."""

    order_id: str
    stock_keeping_unit: str
    quantity: int
