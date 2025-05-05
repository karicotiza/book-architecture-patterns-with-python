"""Flask add batch view."""

from typing import TYPE_CHECKING

from flask import Blueprint, Response, request

from src.application.services.add import AddAppService
from src.infrastructure.uow.allocation.postgresql_allocation import (
    PostgresqlAllocationUOW,
)
from src.presentation.dtos.flask.add_batch import (
    AddBatchRequestBody,
    AddBatchResponseBody,
)
from src.presentation.utils.status_codes import StatusCode

if TYPE_CHECKING:
    from src.domain.entities.batch import Batch


add_batch_blueprint: Blueprint = Blueprint("add_batch", __name__)

add_app_service: AddAppService = AddAppService()


@add_batch_blueprint.route("/add_batch", methods=["POST"])
def add_batch_endpoint() -> tuple[Response, int]:
    """Add batch endpoint.

    Returns:
        tuple[Response, int]: Response body and status code.

    """
    body: Batch = AddBatchRequestBody.from_flask_request(
        request=request,
    ).as_batch()

    add_app_service.add_batch(
        batch=(
            body.reference,
            body.stock_keeping_unit,
            body.available_quantity,
            body.estimated_arrival_time,
        ),
        unit_of_work=PostgresqlAllocationUOW(),
    )

    return AddBatchResponseBody(
        body={
            "status": "ok",
        },
        status_code=StatusCode.created,
    ).as_flask_response()
