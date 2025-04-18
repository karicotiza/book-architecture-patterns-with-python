"""Flask allocate view."""

from typing import TYPE_CHECKING

from flask import Blueprint, Response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.application.services.allocation import (
    AllocationAppService,
    InvalidSKUError,
)
from src.domain.exceptions.out_of_stock import OutOfStockError
from src.infrastructure.repositories.sql_repository.postgresql import (
    PostgreSQLRepository,
)
from src.infrastructure.settings import settings
from src.presentation.dtos.flask.allocate import (
    AllocateRequestBody,
    AllocateResponseBody,
)
from src.presentation.utils.status_codes import StatusCode

if TYPE_CHECKING:
    from src.domain.value_objects.order_line import OrderLine


allocate_blueprint: Blueprint = Blueprint("allocate", __name__)

session: Session = sessionmaker(create_engine(settings.postgres_uri))()
repository: PostgreSQLRepository = PostgreSQLRepository(session)
allocation_app_service: AllocationAppService = AllocationAppService()


@allocate_blueprint.route("/allocate", methods=["POST"])
def allocate_endpoint() -> tuple[Response, int]:
    """Process allocate_endpoint.

    Returns:
        tuple[Response, int]: Response body and status code.

    """
    body: OrderLine = AllocateRequestBody.from_flask_request(
        request=request,
    ).as_order_line()

    try:
        batch_reference: str = allocation_app_service.allocate(
            order_id=body.order_id,
            stock_keeping_unit=body.stock_keeping_unit,
            quantity=body.quantity,
            repository=repository,
            session=session,
        )

    except (OutOfStockError, InvalidSKUError) as error:
        return AllocateResponseBody(
            body={
                "message": str(error),
            },
            status_code=StatusCode.bad_request,
        ).as_flask_response()

    return AllocateResponseBody(
        body={
            "batch_reference": batch_reference,
        },
        status_code=StatusCode.created,
    ).as_flask_response()
