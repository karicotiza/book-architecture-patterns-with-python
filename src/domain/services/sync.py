"""Sync domain service."""

from pathlib import Path

from src.domain.repositories.file_system import IFileSystem
from src.domain.services.reader import Reader


class SyncService:
    """Sync domain service."""

    def sync(
        self,
        reader: Reader,
        file_system: IFileSystem,
        source: str,
        destination: str,
    ) -> None:
        """Sync two folders.

        Args:
            reader (Reader): reader service.
            file_system (IFileSystem): file system repository.
            source (Path): source folder.
            destination (Path): destination folder.

        """
        source_hashes: dict[str, str] = reader.get_hashes(source)
        destination_hashes: dict[str, str] = reader.get_hashes(destination)

        for hash_value, file_name in source_hashes.items():
            if hash_value not in destination_hashes:
                self._copy(file_name, source, destination, file_system)

            elif destination_hashes[hash_value] != file_name:
                self._move(
                    file_name=file_name,
                    hash_value=hash_value,
                    hashes=destination_hashes,
                    destination=destination,
                    file_system=file_system,
                )

        for hash_value, file_name in destination_hashes.items():
            if hash_value not in source_hashes:
                self._delete(file_name, destination, file_system)

    def _copy(
        self,
        file_name: str,
        source: str,
        destination: str,
        file_system: IFileSystem,
    ) -> None:
        source_path: Path = Path(source) / file_name
        destination_path: Path = Path(destination) / file_name
        file_system.copy(source_path, destination_path)

    def _move(
        self,
        file_name: str,
        hash_value: str,
        hashes: dict[str, str],
        destination: str,
        file_system: IFileSystem,
    ) -> None:
        old_destination_path: Path = Path(destination) / hashes[hash_value]
        new_destination_path: Path = Path(destination) / file_name
        file_system.move(old_destination_path, new_destination_path)

    def _delete(
        self,
        file_name: str,
        destination: str,
        file_system: IFileSystem,
    ) -> None:
        delete_path: Path = Path(destination) / file_name
        file_system.delete(delete_path)
