"""Flask controller."""

from flask import Flask

from src.infrastructure.repositories.sql_repository.postgresql import (
    create_mappers,
)
from src.presentation.views.flask.add_batch import add_batch_blueprint
from src.presentation.views.flask.allocate import allocate_blueprint

app: Flask = Flask(__name__)

create_mappers()

app.register_blueprint(add_batch_blueprint)
app.register_blueprint(allocate_blueprint)
