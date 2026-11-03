TOMBSTONE = "__DELETED__"


class DatabaseError(Exception):
    """Raised when the database file cannot be read or written."""


class Database:
    def __init__(self, path: str = "data.db") -> None:
        self.path = path

    def set(self, key: str, value: str) -> None:
        self._validate_key(key)
        self._validate_value(value)
        self._append(key, value)

    def get(self, key: str) -> str | None:
        result = None
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                for line in file:
                    stored_key, value = line.rstrip("\n").split(",", 1)
                    if stored_key == key:
                        result = None if value == TOMBSTONE else value
        except FileNotFoundError:
            return None
        except OSError as error:
            raise DatabaseError(f"Could not read database file: {self.path}") from error
        return result

    def delete(self, key: str) -> None:
        self._validate_key(key)
        if self.get(key) is not None:
            self._append(key, TOMBSTONE)

    def _append(self, key: str, value: str) -> None:
        try:
            with open(self.path, "a", encoding="utf-8") as file:
                file.write(f"{key},{value}\n")
        except OSError as error:
            raise DatabaseError(f"Could not write database file: {self.path}") from error

    @staticmethod
    def _validate_key(key: str) -> None:
        if not key or "," in key or "\n" in key:
            raise ValueError("Invalid key")

    @staticmethod
    def _validate_value(value: str) -> None:
        if "\n" in value or value == TOMBSTONE:
            raise ValueError("Invalid value")
