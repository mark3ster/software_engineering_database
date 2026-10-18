from mydb.database import Database

db = Database("data.db")
db.set("theme", "dark")
print(db.get("theme"))