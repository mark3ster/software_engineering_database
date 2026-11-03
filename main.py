from mydb.database import Database

db = Database("datos.db")
print(db.get("theme"))
print(db.get("language"))

db.set("temporary", "example")
print(db.get("temporary"))
db.delete("temporary")