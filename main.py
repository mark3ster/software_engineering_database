from mydb.database import Database

db = Database("datos.db")
print(db.get("theme"))
print(db.get("language"))