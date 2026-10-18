from mydb.database import BaseDatos

db = BaseDatos("datos.db")

db.set("tema", "oscuro")
db.set("idioma", "español")
db.set("notificaciones", "activadas")

print("Tema:", db.get("tema"))
print("Idioma:", db.get("idioma"))

db.set("idioma", "inglés")  # sobrescribir: se añade una línea nueva
print("Idioma actualizado:", db.get("idioma"))