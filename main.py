from mydb.database import Database
 
db = Database("datos.db")
 
# read the values that are already saved
print("theme:", db.get("theme"))
print("language:", db.get("language"))
 
# a key that does not exist should give None
print("missing:", db.get("something"))
# set and delete a temporary key
db.set("temporary", "example")
print("temporary:", db.get("temporary"))
db.delete("temporary")
print("temporary after delete:", db.get("temporary"))
 
# if we set the same key twice, the last value is the one we get
db.set("counter", "1")
db.set("counter", "2")
print("counter:", db.get("counter"))
db.delete("counter")
 
# values can have commas
db.set("colors", "red,green,blue")
print("colors:", db.get("colors"))
db.delete("colors")
 
# a key with a comma is not valid, so we catch the error
try:
    db.set("bad,key", "value")
except ValueError:
    print("error: the key can not have commas")
 
# same with an empty key
try:
    db.set("", "value")
except ValueError:
    print("error: the key can not be empty")