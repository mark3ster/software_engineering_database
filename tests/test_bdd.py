import os
import pytest
from mydb.database import Database

# every test gets its own empty file (tmp_path is a new folder each time)
@pytest.fixture
def path(tmp_path):
    return str(tmp_path / "test.db")

def test_set_y_get(path):
    db = Database(path)
    db.set("theme", "dark")
    assert db.get("theme") == "dark"


def test_write_in_file(path):
    db = Database(path)
    db.set("theme", "dark")
    f = open(path, "r", encoding="utf-8")
    contenido = f.read()
    f.close()
    assert contenido == "theme,dark\n"

def test_get_no_existent_key(path):
    db = Database(path)
    assert db.get("nada") is None


def test_overwrite_returns_last_value(path):
    db = Database(path)
    db.set("language", "spanish")
    db.set("language", "english")
    assert db.get("language") == "english"

def test_list_values_with_commas(path):
    db = Database(path)
    db.set("list", "a,b,c")
    assert db.get("list") == "a,b,c"


def test_save_and_open_again(path):
    db = Database(path)
    db.set("a", "1")
    db2 = Database(path)
    assert db2.get("a") == "1"


def test_invalid_key_with_comma(path):
    db = Database(path)
    with pytest.raises(ValueError):
        db.set("a,b", "valor")
    assert db.get("a,b") is None

def test_invalid_key_with_empty_string(path):
    db = Database(path)
    with pytest.raises(ValueError):
        db.set("", "valor")
    assert db.get("") is None


def test_invalid_value_with_line_break(path):
    db = Database(path)
    with pytest.raises(ValueError):
        db.set("clave", "linea1\nlinea2")
    assert db.get("clave") is None


def test_invalid_delete_key_with_comma(path):
    db = Database(path)
    with pytest.raises(ValueError):
        db.delete("a,b")


def test_delete_deletes_key(path):
    db = Database(path)
    db.set("a", "1")
    db.delete("a")
    assert db.get("a") is None

def test_delete_does_not_delete_other_keys(path):
    db = Database(path)
    db.set("a", "1")
    db.set("b", "2")
    db.delete("a")
    assert db.get("b") == "2"


def test_set_after_delete(path):
    db = Database(path)
    db.set("a", "1")
    db.delete("a")
    db.set("a", "2")
    assert db.get("a") == "2"


def test_delete_no_existent_key(path):
    db = Database(path)
    db.set("a", "1")
    db.delete("otra")
    assert db.get("a") == "1"

def test_key_with_leading_spaces(path):
    db = Database(path)
    db.set("  a", "1")
    assert db.get("  a") == "1"
    assert db.get("a") is None


def test_value_with_spaces_at_the_ends(path):
    db = Database(path)
    db.set("a", "  hello  ")
    assert db.get("a") == "  hello  "


def test_key_with_colon(path):
    db = Database(path)
    db.set("Meeting: Monday", "room 4")
    assert db.get("Meeting: Monday") == "room 4"


def test_other_alphabets(path):
    db = Database(path)
    for text in ["ñ", "Привет", "🎉"]:
        db.set(text, text)
        assert db.get(text) == text

def test_invalid_key_with_line_break(path):
    db = Database(path)
    with pytest.raises(ValueError):
        db.set("a\nb", "value")
    assert db.list() == {}


def test_delete_adds_deleted_line(path):
    db = Database(path)
    db.set("a", "1")
    db.delete("a")
    f = open(path, "r", encoding="utf-8")
    contenido = f.read()
    f.close()
    # the old line is still there
    assert contenido == "a,1\na,__DELETED__\n"


def test_delete_no_existent_key_writes_nothing(path):
    db = Database(path)
    db.delete("nada")
    assert not os.path.exists(path)


def test_invalid_value_deleted_marker(path):
    db = Database(path)
    with pytest.raises(ValueError):
        db.set("a", "__DELETED__")
    assert db.get("a") is None

# tests for rebuild_index
def test_value_with_comma_survives_restart(path):
    db = Database(path)

    # Arrange: store a value that contains a comma
    db.set("city", "Madrid, Spain")

    # Act: rebuild the index, as if the program restarted
    db.rebuild_index()

    # Assert: the whole value comes back
    assert db.get("city") == "Madrid, Spain"


def test_rebuild_index_keeps_last_value(path):
    db = Database(path)
    db.set("a", "1")
    db.set("a", "2")
    db.rebuild_index()
    assert db.get("a") == "2"


def test_rebuild_index_skips_deleted_keys(path):
    db = Database(path)
    db.set("a", "1")
    db.set("b", "2")
    db.delete("a")
    db.rebuild_index()
    assert db.get("a") is None
    assert db.get("b") == "2"

def test_rebuild_index_empty_file(path):
    db = Database(path)
    db.rebuild_index()
    assert db.list() == {}


def test_rebuild_index_ignores_empty_lines(path):
    f = open(path, "w", encoding="utf-8")
    f.write("a,1\n\nb,2\nbroken line\nc,3\n")
    f.close()
    db = Database(path)
    assert db.list() == {"a": "1", "b": "2", "c": "3"}


def test_rebuild_index_with_non_ascii_lines(path):
    # ñ and emojis are more than 1 byte
    db = Database(path)
    db.set("ñ", "Привет 🎉")
    db.set("b", "2")
    db.rebuild_index()
    assert db.get("b") == "2"
    assert db.get("ñ") == "Привет 🎉"


# tests for list method
def test_list_all_keys(path):
    db = Database(path)
    db.set("a", "1")
    db.set("b", "2")
    assert db.list() == {"a": "1", "b": "2"}


def test_list_last_value_wins(path):
    db = Database(path)
    db.set("a", "1")
    db.set("a", "2")
    assert db.list() == {"a": "2"}

def test_list_after_delete(path):
    db = Database(path)
    db.set("a", "1")
    db.set("b", "2")
    db.delete("a")
    assert db.list() == {"b": "2"}

def test_list_empty_database(path):
    db = Database(path)
    assert db.list() == {}