"""Reader domain service."""


class Reader:
    """Reader domain service."""

    def __init__(
        self,
        source: dict[str, str],
        destination: dict[str, str],
    ) -> None:
        """Create new instance.

        Args:
            source (dict[str, str]): source content.
            destination (dict[str, str]): destination content.

        """
        self._memory: dict[str, dict[str, str]] = {
            "/source": source,
            "/destination": destination,
        }

    def get_hashes(self, key: str) -> dict[str, str]:
        """Get hashes.

        Args:
            key (str): key.

        Returns:
            dict[str, str]]: hashes.

        """
        return self._memory[key]
