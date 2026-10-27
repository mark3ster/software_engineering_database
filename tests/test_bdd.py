import pytest
from mydb.database import Database


@pytest.fixture
def db(tmp_path):
    """Temporary database: each test gets a fresh, empty file."""
    return Database(str(tmp_path / "test.db"))


def test_set_and_get(db):
    # Arrange
    db.set("theme", "dark")

    # Act
    result = db.get("theme")

    # Assert
    assert result == "dark"


def test_get_missing_key(db):
    # Act
    result = db.get("missing")

    # Assert
    assert result is None


def test_overwrite_returns_last_value(db):
    # Arrange
    db.set("language", "spanish")
    db.set("language", "english")

    # Act
    result = db.get("language")

    # Assert
    assert result == "english"


def test_value_with_commas(db):
    # Arrange
    db.set("list", "a,b,c")

    # Act
    result = db.get("list")

    # Assert
    assert result == "a,b,c"


def test_persistence_with_rebuild_index(tmp_path):
    # Arrange: write with one instance
    path = str(tmp_path / "p.db")
    Database(path).set("a", "1")

    # Act: a new instance simulates restarting the program
    reopened = Database(path)

    # Assert
    assert reopened.get("a") == "1"


def test_rebuild_index_with_accents_and_overwrite(tmp_path):
    # Arrange
    path = str(tmp_path / "r.db")
    db = Database(path)
    db.set("x", "ñandú")
    db.set("y", "2")
    db.set("x", "3")

    # Act
    reopened = Database(path)

    # Assert
    assert reopened.get("x") == "3"
    assert reopened.get("y") == "2"


def test_indexed_get_matches_linear_get(db):
    # Arrange
    db.set("x", "ñandú")
    db.set("y", "2")
    db.set("x", "3")

    # Act / Assert
    assert db.get("x") == db.get_linear("x") == "3"


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
    assert db.get_linear("a") is None


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
    # Act
    db.delete("missing")

    # Assert
    assert db.get("missing") is None