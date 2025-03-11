# book-architecture-patterns-with-python

Following the book "Architecture Patterns with Python: Enabling Test-Driven
Development, Domain-Driven Design, and Event-Driven Microservices"

## Requirements

Development:

* `python==3.12.3` (with modules from `./requirements.txt`)

## Code quality

The code of this repository passes the following checks without any errors
and warnings:

* `python -m pytest ./tests/`
* `python -m ruff check ./src/ ./tests/`
* `python -m ruff format ./src/ ./tests/`
* `python -m flake8 ./src/ ./tests/`
* `python -m pyright ./src/ ./tests/`
* `python -m mypy ./src/ ./tests/`
