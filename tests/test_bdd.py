import os
from mydb.database import Database


def test_set_y_get():
    db = Database("test.db")
    db.set("theme", "dark")
    assert db.get("theme") == "dark"
    os.remove("test.db")


def test_set_escribe_en_archivo():
    db = Database("test.db")
    db.set("theme", "dark")
    f = open("test.db", "r")
    contenido = f.read()
    f.close()
    assert contenido == "theme,dark\n"
    os.remove("test.db")


def test_get_clave_que_no_existe():
    db = Database("test.db")
    assert db.get("nada") is None


def test_sobrescribir_devuelve_el_ultimo():
    db = Database("test.db")
    db.set("language", "spanish")
    db.set("language", "english")
    assert db.get("language") == "english"
    os.remove("test.db")


def test_valor_con_comas():
    db = Database("test.db")
    db.set("list", "a,b,c")
    assert db.get("list") == "a,b,c"
    os.remove("test.db")


def test_guardar_y_abrir_otra_vez():
    db = Database("test.db")
    db.set("a", "1")
    db2 = Database("test.db")
    assert db2.get("a") == "1"
    os.remove("test.db")


def test_clave_con_coma_no_valida():
    db = Database("test.db")
    db.set("a,b", "valor")
    assert db.get("a,b") is None


def test_clave_vacia_no_valida():
    db = Database("test.db")
    db.set("", "valor")
    assert db.get("") is None


def test_valor_con_salto_de_linea_no_valido():
    db = Database("test.db")
    db.set("clave", "linea1\nlinea2")
    assert db.get("clave") is None


def test_mensaje_de_clave_no_valida(capsys):
    db = Database("test.db")
    db.set("a,b", "valor")
    salida = capsys.readouterr().out
    assert "Clave no valida" in salida


def test_delete_borra_la_clave():
    db = Database("test.db")
    db.set("a", "1")
    db.delete("a")
    assert db.get("a") is None
    os.remove("test.db")


def test_delete_no_borra_otras_claves():
    db = Database("test.db")
    db.set("a", "1")
    db.set("b", "2")
    db.delete("a")
    assert db.get("b") == "2"
    os.remove("test.db")


def test_set_despues_de_delete():
    db = Database("test.db")
    db.set("a", "1")
    db.delete("a")
    db.set("a", "2")
    assert db.get("a") == "2"
    os.remove("test.db")


def test_delete_clave_que_no_existe():
    db = Database("test.db")
    db.set("a", "1")
    db.delete("otra")
    assert db.get("a") == "1"
    os.remove("test.db")

#new test issue 25
def test_clave_con_espacios_al_inicio(tmp_path):
    db = Database(str(tmp_path / "t.db"))
    db.set("  a", "1")
    assert db.get("  a") == "1"
    assert db.get("a") is None