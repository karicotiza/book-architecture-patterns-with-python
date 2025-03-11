"""Order line value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    """Order line entity."""

    order_id: str
    sku: str
    qty: int
