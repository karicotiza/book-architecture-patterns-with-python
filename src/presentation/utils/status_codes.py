"""Status code util."""

from enum import IntEnum


class StatusCode(IntEnum):
    """Status code choices."""

    created = 201
    bad_request = 400
