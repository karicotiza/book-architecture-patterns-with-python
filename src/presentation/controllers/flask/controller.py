"""Flask controller."""

from flask import Flask, Response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.application.services.allocation import (
    AllocationAppService,
    InvalidSKUError,
)
from src.domain.exceptions.out_of_stock import OutOfStockError
from src.infrastructure.repositories.sql_repository.postgresql import (
    PostgreSQLRepository,
    create_mappers,
)
from src.infrastructure.settings import settings
from src.presentation.dtos.flask.allocate import RequestBody, ResponseBody
from src.presentation.utils.status_codes import StatusCode

app: Flask = Flask(__name__)

create_mappers()

session: Session = sessionmaker(create_engine(settings.postgres_uri))()
repository: PostgreSQLRepository = PostgreSQLRepository(session)
allocation_app_service: AllocationAppService = AllocationAppService()


@app.route("/allocate", methods=["POST"])
def allocate_endpoint() -> tuple[Response, int]:
    """Process allocate_endpoint.

    Returns:
        tuple[Response, int]: Response body and status code.

    """
    try:
        batch_reference: str = allocation_app_service.allocate(
            order_line=RequestBody.from_flask_request(request).as_order_line(),
            repository=repository,
            session=session,
        )

    except (OutOfStockError, InvalidSKUError) as error:
        return ResponseBody(
            body={
                "message": str(error),
            },
            status_code=StatusCode.bad_request,
        ).as_flask_response()

    return ResponseBody(
        body={
            "batch_reference": batch_reference,
        },
        status_code=StatusCode.created,
    ).as_flask_response()
