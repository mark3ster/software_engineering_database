from mydb.database import set_preferencia, PREFERENCIAS_PATH


def test_set(tmp_path, monkeypatch):
    archivo = tmp_path / "preferencias.txt"
    monkeypatch.setattr("mydb.database.PREFERENCIAS_PATH", str(archivo))

    usuario_id = 1
    clave = "idioma"
    valor = "español"

    set_preferencia(usuario_id, clave, valor)

    with open(archivo, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1
    assert lines[0].strip() == "1|idioma|español"
