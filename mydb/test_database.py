from mydb.database import set_preferencia, PREFERENCIAS_PATH


def test_set(tmp_path, monkeypatch):
    file_path = tmp_path / "preferencias.txt"
    monkeypatch.setattr("mydb.database.PREFERENCIAS_PATH", str(file_path))

    usuario_id = 1
    key = "language"
    value = "spanish"
#
    set_preferencia(usuario_id, key, value)

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1
    assert lines[0].strip() == "1|language|spanish"
