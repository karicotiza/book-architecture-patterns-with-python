"""To date utility module."""

from datetime import UTC, datetime


def string_to_date(date: str) -> datetime:
    """Date as string to datetime.

    Args:
        date (str): date as string.

    Returns:
        datetime: datetime instance.

    """
    year, month, day = date.split("-")
    return datetime(
        year=int(year),
        month=int(month),
        day=int(day),
        tzinfo=UTC,
    )
