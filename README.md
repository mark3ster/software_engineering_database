# Database

Small key-value database in Python that stores everything in a plain text file. Project for the Software Engineering course.

## How it works

The file is an append-only log: every write adds a line at the end and old lines are never edited. If a key appears more than once, the last line wins.

To avoid reading the whole file on every `get`, we keep an index in memory (a dict that maps each key to the byte position of its last line). When the program starts, `rebuild_index()` reads the file and builds the index again.

## File format

One line per write:

```
key,value
```

- The key cannot be empty or contain commas or line breaks.
- The value cannot contain line breaks (commas are fine).
- Deleting a key adds a tombstone line: `key,__DELETED__`. That value is reserved.

## Usage

```python
from mydb.database import Database

db = Database("data.db")
db.set("theme", "dark")
print(db.get("theme"))   # dark
db.delete("theme")
print(db.get("theme"))   # None
```

Other methods: `get_linear(key)` (same as `get` but scanning the file, without index) and `rebuild_index()`. `set` and `delete` raise `ValueError` if the key or value is not valid.

## Tests

```
pip install -r requirements.txt
pytest
```

No commit should be pushed if a test fails. GitHub Actions runs the tests on every push and pull request to `main`.

## Limitations

- The file keeps growing because old lines are never removed (no compaction yet).
- All keys must fit in memory.
- Not safe with several processes writing at the same time.

## Requirements

Requirements from customer feedback are in the [Product Backlog](backlog.md).

## Authors

- Daniel Cals
- Lucas Carvalho
- Andrea Ávila
- Marcos Jiménez