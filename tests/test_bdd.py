import pytest
from mydb.database import Database, DatabaseError


@pytest.fixture
def db(tmp_path):
    """Temporary database: each test gets a fresh, empty file."""
    return Database(str(tmp_path / "test.db"))


def test_set_writes_to_file(db):
    db.set("theme", "dark")
    with open(db.path, encoding="utf-8") as file:
        assert file.read() == "theme,dark\n"


def test_get_missing_key(db):
    # Act
    result = db.get("missing")

    # Assert
    assert result is None


def test_overwrite_returns_last_value(db):
    with open(db.path, "w", encoding="utf-8") as file:
        file.write("language,spanish\nlanguage,english\n")
    assert db.get("language") == "english"


def test_value_with_commas(db):
    with open(db.path, "w", encoding="utf-8") as file:
        file.write("list,a,b,c\n")
    assert db.get("list") == "a,b,c"


def test_persistence_with_rebuild_index(tmp_path):
    path = str(tmp_path / "p.db")
    Database(path).set("a", "1")
    reopened = Database(path)
    assert reopened.get("a") == "1"


def test_rebuild_index_with_accents_and_overwrite(tmp_path):
    path = str(tmp_path / "r.db")
    with open(path, "w", encoding="utf-8") as file:
        file.write("x,ñandú\ny,2\nx,3\n")
    reopened = Database(path)
    assert reopened.get("x") == "3"
    assert reopened.get("y") == "2"


@pytest.mark.parametrize("key", ["a,b", "", "a\nb"])
def test_invalid_key(db, key):
    with pytest.raises(ValueError):
        db.set(key, "value")


def test_value_with_newline_is_invalid(db):
    with pytest.raises(ValueError):
        db.set("key", "line1\nline2")


def test_reserved_value_is_invalid(db):
    with pytest.raises(ValueError):
        db.set("key", "__DELETED__")


def test_delete_removes_key(db):
    # Arrange
    db.set("a", "1")

    # Act
    db.delete("a")

    # Assert
    assert db.get("a") is None


def test_delete_persists_after_restart(tmp_path):
    # Arrange
    path = str(tmp_path / "d.db")
    first = Database(path)
    first.set("a", "1")
    first.delete("a")

    # Act
    reopened = Database(path)

    # Assert
    assert reopened.get("a") is None


def test_set_after_delete_restores_key(db):
    # Arrange
    db.set("a", "1")
    db.delete("a")

    # Act
    db.set("a", "2")

    # Assert
    assert db.get("a") == "2"


def test_delete_missing_key_does_nothing(db):
    db.delete("missing")
    assert db.get("missing") is None


def test_read_error_is_reported(tmp_path):
    db = Database(str(tmp_path))
    with pytest.raises(DatabaseError):
        db.get("key")


def test_write_error_is_reported(tmp_path):
    db = Database(str(tmp_path))
    with pytest.raises(DatabaseError):
        db.set("key", "value")