"""Flask controller."""

from flask import Flask
from sqlalchemy import Engine, create_engine

from src.infrastructure.repositories.sql_repository.postgresql import (
    create_mappers,
    metadata,
)
from src.infrastructure.settings import settings
from src.presentation.views.flask.add_batch import add_batch_blueprint
from src.presentation.views.flask.allocate import allocate_blueprint

app: Flask = Flask(__name__)

engine: Engine = create_engine(settings.postgres_uri)
metadata.create_all(engine)
create_mappers()

app.register_blueprint(add_batch_blueprint)
app.register_blueprint(allocate_blueprint)
