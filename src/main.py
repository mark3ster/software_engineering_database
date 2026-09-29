import json

DATA_FILE = "data.log"


def set(key, value):
    """Guarda value bajo key añadiendo una línea al final del fichero."""
    line = json.dumps({"k": key, "v": value}, ensure_ascii=False)
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get(key):
    """Devuelve el último valor guardado para key, o None si no existe."""
    result = None
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                if record["k"] == key:
                    result = record["v"]
    except FileNotFoundError:
        return None
    return result
<
