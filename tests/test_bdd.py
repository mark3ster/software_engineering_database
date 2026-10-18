import pytest
from mydb.database import BaseDatos


@pytest.fixture
def db(tmp_path):
    """Base de datos temporal: cada test usa un fichero nuevo y limpio."""
    return BaseDatos(str(tmp_path / "test.db"))


def test_set_y_get(db):
    # Arrange
    db.set("tema", "oscuro")

    # Act
    resultado = db.get("tema")

    # Assert
    assert resultado == "oscuro"


def test_get_clave_inexistente(db):
    # Act
    resultado = db.get("nada")

    # Assert
    assert resultado is None


def test_sobrescribir_devuelve_el_ultimo(db):
    # Arrange
    db.set("idioma", "español")
    db.set("idioma", "inglés")

    # Act
    resultado = db.get("idioma")

    # Assert
    assert resultado == "inglés"


def test_valor_con_comas(db):
    # Arrange
    db.set("lista", "a,b,c")

    # Act
    resultado = db.get("lista")

    # Assert
    assert resultado == "a,b,c"


def test_persistencia_con_rebuild_index(tmp_path):
    # Arrange: escribimos con una instancia
    ruta = str(tmp_path / "p.db")
    BaseDatos(ruta).set("a", "1")

    # Act: una instancia nueva simula reiniciar el programa
    nueva = BaseDatos(ruta)

    # Assert
    assert nueva.get("a") == "1"


def test_rebuild_index_con_acentos_y_sobrescritura(tmp_path):
    # Arrange
    ruta = str(tmp_path / "r.db")
    d = BaseDatos(ruta)
    d.set("x", "ñandú")
    d.set("y", "2")
    d.set("x", "3")

    # Act
    nueva = BaseDatos(ruta)

    # Assert
    assert nueva.get("x") == "3"
    assert nueva.get("y") == "2"


def test_get_con_indice_igual_a_lineal(db):
    # Arrange
    db.set("x", "ñandú")
    db.set("y", "2")
    db.set("x", "3")

    # Act / Assert
    assert db.get("x") == db.get_lineal("x") == "3"


@pytest.mark.parametrize("clave", ["a,b", "", "a\nb"])
def test_clave_invalida(db, clave):
    with pytest.raises(ValueError):
        db.set(clave, "valor")


def test_valor_con_salto_de_linea_invalido(db):
    with pytest.raises(ValueError):
        db.set("clave", "linea1\nlinea2")