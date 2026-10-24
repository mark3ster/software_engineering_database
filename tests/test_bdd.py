import pytest
from mydb.database import Database
import os


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

#new tests for delete

def test_empty_value_is_not_a_tombstone(tmp_path):
    # Arrange
    path = str(tmp_path / "e.db")
    db = Database(path)
    db.set("k", "")

    # Act
    reopened = Database(path)

    # Assert
    assert reopened.get("k") == ""
    assert reopened.get_linear("k") == ""


def test_delete_missing_key_does_not_write_to_file(tmp_path):
    # Arrange
    path = str(tmp_path / "m.db")
    db = Database(path)
    db.set("a", "1")
    size_before = os.path.getsize(path)

    # Act
    db.delete("missing")

    # Assert
    assert os.path.getsize(path) == size_before

    
def test_delete_existing_key_get_returns_none(db):
    # Arrange
    db.set("a", "1")

    # Act
    db.delete("a")

    # Assert
    assert db.get("a") is None


def test_delete_existing_key_get_linear_returns_none(db):
    # Arrange
    db.set("a", "1")

    # Act
    db.delete("a")

    # Assert
    assert db.get_linear("a") is None


def test_delete_same_key_twice_does_not_fail(db):
    # Arrange
    db.set("a", "1")
    db.delete("a")

    # Act
    db.delete("a")

    # Assert
    assert db.get("a") is None
    assert db.get_linear("a") is None


def test_delete_then_set_returns_new_value(db):
    # Arrange
    db.set("a", "1")
    db.delete("a")

    # Act
    db.set("a", "2")

    # Assert
    assert db.get("a") == "2"
    assert db.get_linear("a") == "2"


def test_delete_persists_after_reopening(tmp_path):
    # Arrange
    path = str(tmp_path / "d.db")
    db = Database(path)
    db.set("a", "1")
    db.delete("a")

    # Act: a new instance simulates restarting the program
    reopened = Database(path)

    # Assert
    assert reopened.get("a") is None
    assert reopened.get_linear("a") is None


def test_delete_one_key_keeps_the_others(db):
    # Arrange
    db.set("a", "1")
    db.set("b", "ñandú")
    db.set("c", "x,y,z")

    # Act
    db.delete("b")

    # Assert
    assert db.get("a") == "1"
    assert db.get("b") is None
    assert db.get("c") == "x,y,z"
    assert db.get_linear("a") == "1"
    assert db.get_linear("c") == "x,y,z"


def test_delete_key_with_empty_value(db):
    # Arrange
    db.set("k", "")

    # Act
    db.delete("k")

    # Assert
    assert db.get("k") is None
    assert db.get_linear("k") is None


def test_rebuild_index_with_deletes_and_later_writes(tmp_path):
    # Arrange
    path = str(tmp_path / "rb.db")
    db = Database(path)
    db.set("a", "1")
    db.delete("a")
    db.set("a", "2")      # written again after being deleted
    db.set("b", "ñ")
    db.delete("b")        # deleted and never written again
    db.set("c", "3")

    # Act
    reopened = Database(path)

    # Assert
    assert reopened.get("a") == "2"
    assert reopened.get("b") is None
    assert reopened.get("c") == "3"
    assert reopened.get_linear("a") == "2"
    assert reopened.get_linear("b") is None
    