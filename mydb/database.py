import os


class BaseDatos:
    """Base de datos clave-valor de solo texto (append-only + índice en memoria).

    Formato de cada línea del fichero:  clave,valor
    - La clave no puede estar vacía ni contener ',' ni saltos de línea.
    - El valor no puede contener saltos de línea (sí puede contener comas).
    - El fichero solo se añade (append): nunca se edita ni se borra una línea.
    - Si una clave aparece varias veces, vale la última línea.

    El índice (self.index) es un dict:  clave -> byte offset de su última línea.
    """

    def __init__(self, ruta="datos.db"):
        self.ruta = ruta
        self.index = {}
        self.rebuild_index()

    # ---------- escritura ----------
    def set(self, key, value):
        """Añade una línea 'clave,valor' al final del fichero y actualiza el índice."""
        self._validar(key, value)
        linea = f"{key},{value}\n".encode("utf-8")
        with open(self.ruta, "ab") as f:
            f.seek(0, os.SEEK_END)
            offset = f.tell()  # posición donde empieza la línea que vamos a escribir
            f.write(linea)
        self.index[key] = offset

    # ---------- lectura ----------
    def get(self, key):
        """Devuelve el valor de la clave (o None). Usa el índice para saltar directo."""
        offset = self.index.get(key)
        if offset is None:
            return None
        with open(self.ruta, "rb") as f:
            f.seek(offset)
            linea = f.readline().decode("utf-8").rstrip("\n")
        return linea.split(",", 1)[1]

    def get_lineal(self, key):
        """Igual que get, pero escaneando todo el fichero (sin índice).

        Sirve para comparar rendimiento y para verificar que el índice es correcto.
        """
        resultado = None
        if not os.path.exists(self.ruta):
            return None
        with open(self.ruta, "r", encoding="utf-8") as f:
            for linea in f:
                k, v = linea.rstrip("\n").split(",", 1)
                if k == key:
                    resultado = v  # seguimos leyendo: la última ocurrencia gana
        return resultado

    # ---------- índice ----------
    def rebuild_index(self):
        """Reconstruye el índice leyendo el fichero (se llama al arrancar)."""
        self.index = {}
        if not os.path.exists(self.ruta):
            return
        offset = 0
        with open(self.ruta, "rb") as f:
            for linea in f:
                clave = linea.decode("utf-8").split(",", 1)[0]
                self.index[clave] = offset
                offset += len(linea)  # en bytes, no en caracteres

    # ---------- utilidades ----------
    @staticmethod
    def _validar(key, value):
        if not key or "," in key or "\n" in key:
            raise ValueError("Clave inválida: vacía, con ',' o con salto de línea")
        if "\n" in value:
            raise ValueError("El valor no puede contener saltos de línea")
