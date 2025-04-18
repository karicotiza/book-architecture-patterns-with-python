"""API Flask view end-to-end test."""

from typing import Any

import pytest
from requests import Response, post

from src.infrastructure.settings import settings
from tests.utils.generate_random import (
    random_batch_reference,
    random_order_id,
    random_stock_keeping_unit,
)


def post_to_add_batch(
    reference: str,
    stock_keeping_unit: str,
    quantity: int,
    estimated_arrival_time: str | None,
) -> None:
    """Make post request ot add batch.

    Args:
        reference (str): reference.
        stock_keeping_unit (str): stock keeping unit.
        quantity (int): quantity.
        estimated_arrival_time (date): estimated arrival time.

    """
    post(
        url=f"{settings.api_url}/add_batch",
        json={
            "reference": reference,
            "stock_keeping_unit": stock_keeping_unit,
            "quantity": quantity,
            "estimated_arrival_time": estimated_arrival_time,
        },
        timeout=5,
    )


@pytest.mark.parametrize(
    argnames=(
        "early_batch",
        "later_batch",
        "other_batch",
        "expected_status_code",
    ),
    argvalues=[
        (
            random_batch_reference("1"),
            random_batch_reference("2"),
            random_batch_reference("3"),
            201,
        )
    ],
)
def test_api_created(
    early_batch: str,
    later_batch: str,
    other_batch: str,
    expected_status_code: int,
) -> None:
    """Test API returns 201 on known SKU and choose earliest batch."""
    first_stock_keeping_unit: str = random_stock_keeping_unit("first")
    second_stock_keeping_unit: str = random_stock_keeping_unit("second")

    post_to_add_batch(
        reference=later_batch,
        stock_keeping_unit=first_stock_keeping_unit,
        quantity=100,
        estimated_arrival_time="2011-01-02",
    )

    post_to_add_batch(
        reference=early_batch,
        stock_keeping_unit=first_stock_keeping_unit,
        quantity=100,
        estimated_arrival_time="2011-01-01",
    )

    post_to_add_batch(
        reference=other_batch,
        stock_keeping_unit=second_stock_keeping_unit,
        quantity=100,
        estimated_arrival_time=None,
    )

    payload: dict[str, Any] = {
        "order_id": random_order_id(),
        "stock_keeping_unit": first_stock_keeping_unit,
        "quantity": 3,
    }

    response: Response = post(
        url=f"{settings.api_url}/allocate",
        json=payload,
        timeout=5,
    )

    assert response.status_code == expected_status_code
    assert response.json()["batch_reference"] == early_batch


@pytest.mark.parametrize(
    argnames=(
        "expected_status_code",
        "expected_message",
    ),
    argvalues=[
        (400, "Invalid SKU: "),
    ],
)
def test_api_invalid_sku(
    expected_status_code: int,
    expected_message: str,
) -> None:
    """Test API returns 400 on unknown SKU."""
    order_id: str = random_order_id()
    stock_keeping_unit: str = random_stock_keeping_unit()

    payload: dict[str, Any] = {
        "order_id": order_id,
        "stock_keeping_unit": stock_keeping_unit,
        "quantity": 20,
    }

    response: Response = post(
        url=f"{settings.api_url}/allocate",
        json=payload,
        timeout=5,
    )

    assert response.status_code == expected_status_code
    assert response.json()["message"].startswith(expected_message)
