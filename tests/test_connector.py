from fakes.fake_requester import FakeResponse
from connector import SqliteConnector
from exceptions import ResponseNotOkException

import pytest
from sqlite3 import connect

@pytest.fixture
def fake_connector(tmp_path):
    return SqliteConnector(str(tmp_path / "test.db"))


@pytest.fixture
def faulty_infos():
    return {
        "table_name" : "123var",
        "columns" : [
            ("id_station", "INTEGER"),
            ("dh_utc", "TEXT"),
            ("faulty-column-name", "INT"),
            ("faulty_column_type", "CUSTOM"),
        ],
        "primary_keys" : [
            "id_station",
            "class"
        ]
    }

@pytest.fixture
def fake_connector_faulty(tmp_path, faulty_infos):
    return SqliteConnector(str(tmp_path / "test_2.db"), table_infos=faulty_infos)

def test_setup(fake_connector):
    fake_connector.setup()
    with connect(fake_connector.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (fake_connector.table_infos["table_name"], )
        )
        assert cursor.fetchone() is not None
        
        
def test_validate_infos(fake_connector):
    table_name, columns, keys = fake_connector.validate_infos()
    assert table_name.isidentifier()

    for column in columns:
        name, _type = column.split()
        assert name.isidentifier()
        assert _type in SqliteConnector.TYPE_MAPPING.keys()

    for pkey in keys:
        assert pkey.isidentifier()
        assert pkey in [column_name for column_name, _ in fake_connector.table_infos['columns']]


@pytest.fixture
def connector_invalid_column(tmp_path):
    infos = {
        "table_name": "records",
        "columns": [("faulty-column-name", "INTEGER")],
        "primary_keys": []
    }
    return SqliteConnector(str(tmp_path / "test_col.db"), table_infos=infos)


@pytest.fixture
def connector_invalid_pk_name(tmp_path):
    infos = {
        "table_name": "records",
        "columns": [("id_station", "INTEGER")],
        "primary_keys": ["bad-pk-name"]
    }
    return SqliteConnector(str(tmp_path / "test_pk.db"), table_infos=infos)


@pytest.fixture
def connector_pk_not_in_columns(tmp_path):
    infos = {
        "table_name": "records",
        "columns": [("id_station", "INTEGER")],
        "primary_keys": ["nonexistent"]
    }
    return SqliteConnector(str(tmp_path / "test_pk2.db"), table_infos=infos)


@pytest.fixture
def simple_connector(tmp_path):
    infos = {
        "table_name": "records",
        "columns": [
            ("id_station", "INTEGER"),
            ("dh_utc", "TEXT"),
            ("temperature", "REAL"),
        ],
        "primary_keys": ["id_station", "dh_utc"]
    }
    connector = SqliteConnector(str(tmp_path / "simple.db"), table_infos=infos)
    connector.setup()
    return connector


def test_validate_infos_invalid_table_name(fake_connector_faulty):
    with pytest.raises(ValueError):
        fake_connector_faulty.validate_infos()


def test_validate_infos_invalid_column_name(connector_invalid_column):
    with pytest.raises(ValueError):
        connector_invalid_column.validate_infos()


def test_validate_infos_invalid_pk_name(connector_invalid_pk_name):
    with pytest.raises(ValueError):
        connector_invalid_pk_name.validate_infos()


def test_validate_infos_pk_not_in_columns(connector_pk_not_in_columns):
    with pytest.raises(ValueError):
        connector_pk_not_in_columns.validate_infos()


def test_insert_rows(simple_connector):
    rows = [{"id_station": 42, "dh_utc": "2026-04-18 00:00:00", "temperature": 11.5}]
    simple_connector.insert_rows(rows)
    with connect(simple_connector.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM records")
        result = cursor.fetchall()
    assert len(result) == 1


def test_insert_rows_null_value(simple_connector):
    rows = [{"id_station": 42, "dh_utc": "2026-04-18 00:00:00", "temperature": None}]
    simple_connector.insert_rows(rows)
    with connect(simple_connector.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM records")
        result = cursor.fetchone()
    assert result[0] is None


def test_insert_rows_empty_string_value(simple_connector):
    rows = [{"id_station": 42, "dh_utc": "2026-04-18 00:00:00", "temperature": ""}]
    simple_connector.insert_rows(rows)
    with connect(simple_connector.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT temperature FROM records")
        result = cursor.fetchone()
    assert result[0] is None


def test_insert_rows_unknown_column(simple_connector):
    rows = [{"nonexistent": "value"}]
    with pytest.raises(ValueError):
        simple_connector.insert_rows(rows)


def test_insert_rows_bad_type(simple_connector):
    rows = [{"id_station": "not_an_int"}]
    with pytest.raises(TypeError):
        simple_connector.insert_rows(rows)


def test_fake_response_json_not_ok():
    response = FakeResponse({"error": "bad"}, 400)
    with pytest.raises(ResponseNotOkException):
        response.json()

