import os


class Database:
    """Plain-text key-value database (append-only log + in-memory index).

    File format, one line per write:  key,value
    - The key cannot be empty or contain ',' or newlines.
    - The value cannot contain newlines (commas are allowed).
    - The file is only ever appended to: lines are never edited or removed.
    - If a key appears several times, the last line wins.

    The index (self.index) is a dict:  key -> byte offset of its last line.
    """

    def __init__(self, path="data.db"):
        self.path = path
        self.index = {}
        self.rebuild_index()

    # ---------- writing ----------
    def set(self, key, value):
        """Append a 'key,value' line to the file and update the index."""
        self._validate(key, value)
        line = f"{key},{value}\n".encode("utf-8")
        with open(self.path, "ab") as f:
            f.seek(0, os.SEEK_END)
            offset = f.tell()  # where the line we are about to write starts
            f.write(line)
        self.index[key] = offset

    def delete(self, key):
        if key not in self.index:
            return
        line = f"{key}\n".encode("utf-8")
        with open(self.path, "ab") as f:
            f.write(line)
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
        result = None
        if not os.path.exists(self.path):
            return None
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                text = line.rstrip("\n")
                if "," in text:
                    k, v = text.split(",", 1)
                    if k == key:
                        result = v
                elif text == key:   # tombstone
                    result = None
        return result

       # ---------- index ----------
    def rebuild_index(self):
        """Rebuild the index by reading the file (called on startup)."""
        self.index = {}
        if not os.path.exists(self.path):
            return
        offset = 0
        with open(self.path, "rb") as f:
            for line in f:
                text = line.decode("utf-8").rstrip("\n")
                if "," in text:
                    key = text.split(",", 1)[0]
                    self.index[key] = offset
                else:
                    # tombstone: la clave fue borrada
                    self.index.pop(text, None)
                offset += len(line)  # bytes, not characters

    # ---------- helpers ----------
    @staticmethod
    def _validate(key, value):
        if not key or "," in key or "\n" in key:
            raise ValueError("Invalid key: empty, or contains ',' or a newline")
        if "\n" in value:
            raise ValueError("The value cannot contain newlines")