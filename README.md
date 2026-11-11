# Database

Small key-value database in Python that stores everything in a plain text file. Project for the Software Engineering course.

## How it works

The file is append-only: every write adds a line at the end and old lines are never edited or removed. If a key appears more than once, the last line is the one that counts.

To avoid reading the whole file on every `get`, we keep an index in memory (a dict called `index`). It maps each key to the position of its last line in the file.

- `set` adds a line at the end of the file and saves its position in the index.
- `get` looks for the key in the index and goes directly to that line.
- `delete` adds a line `key,__DELETED__` and removes the key from the index.
- `list` returns all the keys with their value.
- `rebuild_index` reads the whole file once and builds the index again. It runs when we create a `Database`, as if the program was restarting. The last line of each key wins, and keys that end as deleted are skipped.

## File format

One line per write:

```
key,value
```

Example (the `theme` key was written twice and `language` was deleted):

```
theme,dark
language,English
theme,light
language,__DELETED__
Meeting: Monday,room 4
```

- The key cannot be empty or have commas or line breaks (the comma is the separator).
- The value cannot have line breaks, but commas are fine.
- The value `__DELETED__` is reserved, because it marks a deleted key.
- Colons are allowed in the key, for example `Meeting: Monday`.
- Spaces are kept, so `"  a"` and `"a"` are different keys.
- The file uses UTF-8, so `ñ`, `Привет` and 🎉 work.

## Usage

The database is a class (`Database`) and everything is done with its methods.

```python
from mydb.database import Database

db = Database("data.db")
db.set("theme", "dark")
print(db.get("theme"))   # dark
print(db.list())         # {'theme': 'dark'}
db.delete("theme")
print(db.get("theme"))   # None
```

`get` returns `None` if the key does not exist. `delete` does nothing in that case. `list` returns `{}` if the file does not exist or is empty. `set` and `delete` raise `ValueError` if the key or the value is not valid:

```python
db.set("Milk, bread", "buy today")   # ValueError, comma in the key
db.set("note", "line1\nline2")       # ValueError, line break in the value
db.set("a", "__DELETED__")           # ValueError, reserved value
```

There is a longer example in `main.py`.

## Tests

```
pip install -r requirements.txt
pytest
```

Every test uses its own temporary file, so they do not depend on each other. There are tests for `set`, `get`, `delete`, `list` and `rebuild_index`.

No commit should be pushed if a test fails. GitHub Actions runs the tests on every push.

## Limitations

- The file keeps growing because old lines are never removed (no compaction yet). Overwriting or deleting a key adds a new line.
- All keys must fit in memory because of the index.
- When the program starts, `rebuild_index` reads the whole file, so it can be slow with a big file.
- If two `Database` objects use the same file, one does not see the changes of the other until we call `rebuild_index()`.
- Keys with commas and values with line breaks are not allowed.
- Not safe with several processes writing at the same time.
- There is no command line, it only works from Python.

## Requirements

Requirements from customer feedback are in the [Product Backlog](backlog.md).

## Authors

- Daniel Cals
- Lucas Carvalho
- Andrea Ávila
- Marcos Jiménez