class Database:
    def __init__(self, path="data.db"):
        self.path = path

    def set(self, key, value):
        # no se permiten comas en la clave ni saltos de linea
        if key == "" or "," in key or "\n" in key:
            print("Clave no valida")
            return
        if "\n" in value:
            print("Valor no valido")
            return

        # guardamos al final del archivo
        f = open(self.path, "a")
        f.write(key + "," + value + "\n")
        f.close()

    def get(self, key):
        result = None
        try:
            f = open(self.path, "r")
        except FileNotFoundError:
            return None

        # recorremos todo el archivo, nos quedamos con el ultimo valor
        for line in f:
            line = line.strip()
            parts = line.split(",", 1)
            if parts[0] == key:
                result = parts[1]
        f.close()
        return result

    def delete(self, key):
        try:
            f = open(self.path, "r")
        except FileNotFoundError:
            return
        lines = f.readlines()
        f.close()

        # reescribimos el archivo sin las lineas de esa clave
        f = open(self.path, "w")
        for line in lines:
            if line.split(",", 1)[0] != key:
                f.write(line)
        f.close()