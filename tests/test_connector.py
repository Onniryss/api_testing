from fakes.fake_connector import FakeConnector
from fakes.fake_requester import FakeRequester, FakeResponse
from client import APIClient
from connector import SqliteConnector
from exceptions import ResponseNotOkException
import copy

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


