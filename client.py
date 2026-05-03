import requests
from dotenv import load_dotenv
import os
from connector import SqliteConnector
from exceptions import ResponseNotOkException
from protocols import APIRequester, DBConnector

load_dotenv()

class APIClient:
    def __init__(
        self, 
        db_connector : DBConnector,
        api_requester : APIRequester = requests, 
        api_url : str = None, 
        api_token : str = None,
    ) -> None:
        self.db_connector = db_connector
        self._api_requester = api_requester
        self._api_url = api_url or os.environ.get("API_URL")
        self._api_token = api_token or os.environ.get("API_KEY")

    def construct_url(self, station_id : int | str, date_start : str, date_end : str) -> str:
        return f"{self._api_url}&token={self._api_token}&stations[]={station_id}&start={date_start}&end={date_end}"


    def parse_response(self, data : dict) -> list[dict]:
        station_list = []
        if stations := data.get("hourly"):
            for key in stations.keys():
                if key != "_params":
                    station_list.append(stations[key])
        
        return station_list

    def save_to_db(self, data : dict) -> None:
        station_list = self.parse_response(data)
        for station_data in station_list:
            self.db_connector.insert_rows(station_data)

    def request(self, station_id : int | str, date_start : str, date_end : str) -> dict:
        request_url = self.construct_url(station_id, date_start, date_end)
        response = self._api_requester.get(request_url)
        if response.ok:
            return response.json()
        
        raise ResponseNotOkException(str(response))

if __name__=="__main__":
    connector = SqliteConnector()
    connector.setup()
    client = APIClient(connector)
    data_json = client.request("07240", "2026-04-18", "2026-04-20")
    client.save_to_db(data_json)
