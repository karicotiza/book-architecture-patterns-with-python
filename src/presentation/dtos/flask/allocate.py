"""Allocation data transfer objects."""

from dataclasses import dataclass
from typing import Any, Self

from flask import Request, Response, jsonify

from src.domain.value_objects.order_line import OrderLine
from src.presentation.utils.status_codes import StatusCode


@dataclass(frozen=True, slots=True)
class RequestBody:
    """Allocation request body."""

    order_id: str
    stock_keeping_unit: str
    quantity: int

    @classmethod
    def from_flask_request(cls, request: Request) -> Self:
        """Make new instance from a Flask request.

        Args:
            request (Request): Flask request

        Returns:
            Self: allocation request body

        """
        if not isinstance(request.json, dict):
            msg: str = "Can't parse request body since it's not a dict."
            raise TypeError(msg)

        for variable_name, expected_type in cls.__annotations__.items():
            try:
                variable_value: Any = request.json[variable_name]
            except KeyError:
                msg = f"Request must have {variable_name} field."
                raise ValueError(msg) from KeyError

            if not isinstance(variable_value, expected_type):
                msg = f"{variable_name} must have {expected_type} type."

        return cls(**request.json)

    def as_order_line(self) -> OrderLine:
        """Get as order line.

        Returns:
            OrderLine: _description_order line value object.

        """
        return OrderLine(
            order_id=self.order_id,
            stock_keeping_unit=self.stock_keeping_unit,
            quantity=self.quantity,
        )


@dataclass(frozen=True, slots=True)
class ResponseBody:
    """Allocation response body."""

    body: dict[str, Any]
    status_code: StatusCode

    def as_flask_response(self) -> tuple[Response, int]:
        """Get as flask response.

        Returns:
            tuple[Response, int]: flask response and status code.

        """
        return (jsonify(self.body), self.status_code.value)
