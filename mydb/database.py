import os

TOMBSTONE = "__DELETED__"


class Database:
    """Plain-text key-value database (append-only log + in-memory index).

    File format, one line per write:  key,value
    - The key cannot be empty or contain ',' or newlines.
    - The value cannot contain newlines (commas are allowed).
    - The file is only ever appended to: lines are never edited or removed.
    - If a key appears several times, the last line wins.
    - Deleting a key appends a tombstone line:  key,__DELETED__

    The index (self.index) is a dict:  key -> byte offset of its last line.
    """

    def __init__(self, path="data.db"):
        self.path = path
        self.index = {}
        self.rebuild_index()

    # ---------- writing ----------
    def set(self, key, value):
        """Append a 'key,value' line to the file and update the index."""
        self._validate_key(key)
        self._validate_value(value)
        self.index[key] = self._append(key, value)

    def delete(self, key):
        """Delete a key by appending a tombstone line (the log is never edited)."""
        self._validate_key(key)
        if key not in self.index:
            return
        self._append(key, TOMBSTONE)
        del self.index[key]

    # ---------- reading ----------
    def get(self, key):
        """Return the value for key (or None). Uses the index to jump straight to it."""
        offset = self.index.get(key)
        if offset is None:
            return None
        with open(self.path, "rb") as f:
            f.seek(offset)
            line = f.readline().decode("utf-8").rstrip("\n")
        return line.split(",", 1)[1]

    def get_linear(self, key):
        """Same as get, but scanning the whole file (no index).

        Useful to compare performance and to check that the index is correct.
        """
        result = None
        if not os.path.exists(self.path):
            return None
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                k, v = line.rstrip("\n").split(",", 1)
                if k == key:
                    result = v  # keep reading: the last occurrence wins
        return None if result == TOMBSTONE else result

    # ---------- index ----------
    def rebuild_index(self):
        """Rebuild the index by reading the file (called on startup)."""
        self.index = {}
        if not os.path.exists(self.path):
            return
        offset = 0
        with open(self.path, "rb") as f:
            for line in f:
                key, value = line.decode("utf-8").rstrip("\n").split(",", 1)
                if value == TOMBSTONE:
                    self.index.pop(key, None)
                else:
                    self.index[key] = offset
                offset += len(line)  # bytes, not characters

    # ---------- helpers ----------
    def _append(self, key, value):
        """Append one line to the file and return the offset where it starts."""
        line = f"{key},{value}\n".encode("utf-8")
        with open(self.path, "ab") as f:
            f.seek(0, os.SEEK_END)
            offset = f.tell()
            f.write(line)
        return offset

    @staticmethod
    def _validate_key(key):
        if not key or "," in key or "\n" in key:
            raise ValueError("Invalid key: empty, or contains ',' or a newline")

    @staticmethod
    def _validate_value(value):
        if "\n" in value:
            raise ValueError("The value cannot contain newlines")
        if value == TOMBSTONE:
            raise ValueError(f"'{TOMBSTONE}' is a reserved value")