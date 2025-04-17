"""Settings."""


class Settings:
    """Settings."""

    postgres_uri: str = (
        "postgresql+psycopg2://admin:admin@localhost:5432/"
        "book-architecture-patterns-with-python"
    )

    api_url: str = "http://localhost:5000"


settings: Settings = Settings()
