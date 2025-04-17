"""Random data utility module."""

from uuid import uuid4


def _random_suffix() -> str:
    return uuid4().hex[:6]


def random_stock_keeping_unit(name: str = "") -> str:
    """Create random stock keeping unit.

    Args:
        name (str, optional): name. Defaults to "".

    Returns:
        str: random stock keeping unit.

    """
    return f"sku-{name}-{_random_suffix()}"


def random_batch_reference(name: str = "") -> str:
    """Create random batch reference.

    Args:
        name (str, optional): name. Defaults to "".

    Returns:
        str: random batch reference.

    """
    return f"batch-{name}-{_random_suffix()}"


def random_order_id(name: str = "") -> str:
    """Create random order id.

    Args:
        name (str, optional): name. Defaults to "".

    Returns:
        str: random order id.

    """
    return f"orderid-{name}-{_random_suffix()}"
