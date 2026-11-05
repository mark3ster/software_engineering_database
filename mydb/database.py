class Database:
    def __init__(self, path="data.db"):
        self.path = path
        self.index = {}  # key -> position of its line
        self.rebuild_index()


    def rebuild_index(self):
        self.index = {}
        try:
            f = open(self.path, "r", encoding="utf-8")
        except FileNotFoundError:
            return

        # tell() does not work with "for line in f", so we use readline()
        position = 0
        line = f.readline()
        while line != "":
            line = line.rstrip("\n")
            if "," in line:
                key, value = line.split(",", 1)
                if value == "__DELETED__":
                    if key in self.index:
                        del self.index[key]
                else:
                    self.index[key] = position
            position = f.tell()
            line = f.readline()
        f.close()

    def set(self, key, value):
        if key == "" or "," in key or "\n" in key:
            raise ValueError("Invalid key")
        if "\n" in value or value == "__DELETED__":
            raise ValueError("Invalid value")

        f = open(self.path, "a", encoding="utf-8")
        position = f.tell()
        f.write(key + "," + value + "\n")
        f.close()
        self.index[key] = position

    def get(self, key):
        result = None
        if key in self.index:
            f = open(self.path, "r", encoding="utf-8")
            f.seek(self.index[key])
            line = f.readline()
            f.close()
            line = line.rstrip("\n")
            result = line.split(",", 1)[1]
        return result

    def delete(self, key):
        if key == "" or "," in key or "\n" in key:
            raise ValueError("Invalid key")

        # the file is append-only, so we add a line that says it is deleted
        if key in self.index:
            f = open(self.path, "a", encoding="utf-8")
            f.write(key + ",__DELETED__\n")
            f.close()
            del self.index[key]


    def list(self):
        result = {}
        for key in self.index:
            result[key] = self.get(key)
        return result