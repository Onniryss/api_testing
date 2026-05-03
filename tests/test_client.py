from fakes.fake_connector import FakeConnector
from fakes.fake_requester import FakeRequester, FakeResponse
from client import APIClient
from connector import SqliteConnector
from exceptions import ResponseNotOkException

import pytest


@pytest.fixture
def fake_data():
    return {
        "hourly": {
            "42": [
                {
                    "id_station": "42",
                    "dh_utc": "2026-04-18 00:00:00",
                    "temperature": "11.5",
                    "pression": "1020.5",
                    "pression_variation_3h": "-0.2",
                    "humidite": "81",
                    "point_de_rosee": "8.4",
                    "visibilite": "60000",
                    "vent_moyen": "7.2",
                    "vent_rafales": "10.8",
                    "vent_rafales_10min": "7.2",
                    "vent_direction": "100",
                    "temperature_min": None,
                    "temperature_max": None,
                    "pluie_1h": "0",
                    "pluie_3h": "0",
                    "pluie_6h": None,
                    "pluie_12h": None,
                    "pluie_24h": None,
                    "ensoleillement": None,
                    "temperature_sol": None,
                    "temps_omm": None,
                    "source": "ogimet",
                    "radiations": None,
                    "neige_au_sol": None,
                    "nebulosite": "8",
                    "raw_msg": "You may not rest now, there are monsters nearby",
                },
                {
                    "id_station": "42",
                    "dh_utc": "2026-04-18 01:00:00",
                    "temperature": "11.9",
                    "pression": "1020.4",
                    "pression_variation_3h": "-0.3",
                    "humidite": "79",
                    "point_de_rosee": "8.4",
                    "visibilite": "60000",
                    "vent_moyen": "3.6",
                    "vent_rafales": "7.2",
                    "vent_rafales_10min": "7.2",
                    "vent_direction": "90",
                    "temperature_min": None,
                    "temperature_max": None,
                    "pluie_1h": "0",
                    "pluie_3h": None,
                    "pluie_6h": None,
                    "pluie_12h": None,
                    "pluie_24h": None,
                    "ensoleillement": None,
                    "temperature_sol": None,
                    "temps_omm": None,
                    "source": "ogimet",
                    "radiations": None,
                    "neige_au_sol": None,
                    "nebulosite": "8",
                    "raw_msg": "You may not rest now, there are monsters nearby",
                },
            ],
            "_params": [
                "temperature",
                "pression",
                "pression_variation_3h",
                "humidite",
                "point_de_rosee",
                "visibilite",
                "vent_moyen",
                "vent_rafales",
                "vent_rafales_10min",
                "vent_direction",
                "temperature_min",
                "temperature_max",
                "pluie_1h",
                "pluie_3h",
                "pluie_6h",
                "pluie_12h",
                "pluie_24h",
                "ensoleillement",
                "temperature_sol",
                "temps_omm",
                "source",
                "radiations",
                "neige_au_sol",
                "nebulosite",
                "raw_msg",
            ],
        }
    }


@pytest.fixture
def fake_url():
    return "http://fake-api.fr/"


@pytest.fixture
def fake_token():
    return "very_secure_token"


@pytest.fixture
def fake_client(fake_data, fake_url, fake_token):
    fake_connector = FakeConnector()
    fake_requester = FakeRequester(fake_data, ok=True)
    
    return APIClient(fake_connector, fake_requester, fake_url, fake_token)


def test_construct_url(fake_client, fake_url, fake_token):
    request_url = fake_client.construct_url("42", "2026-04-18", "2026-04-20")
    assert request_url == f"{fake_url}&token={fake_token}&stations[]=42&start=2026-04-18&end=2026-04-20"


def test_parse_response(fake_client, fake_data):
    parsed_list = fake_client.parse_response(fake_data)
    assert parsed_list == [fake_data.get("hourly").get("42")]

    
def test_save_to_db(fake_client, fake_data):
    fake_client.db_connector.setup()
    fake_client.save_to_db(fake_data)
    assert len(fake_client.db_connector.data) == 2
    

def test_request_ok(fake_client, fake_data):
    data_json = fake_client.request("42", "2026-04-18", "2026-04-20")
    assert data_json == fake_data
    

def test_request_not_ok(fake_client):
    fake_client._api_requester.ok = False
    with pytest.raises(ResponseNotOkException):
        _ = fake_client.request("42", "2026-04-18", "2026-04-20")