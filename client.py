import requests
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

class APIClient:
    def __init__(
        self, 
        api_client = requests, 
        api_url : str = None, 
        api_token : str = None,
        db_name : str = "sqlite3.db"
    ):
        self._api_client = api_client
        self._api_url = api_url or os.environ.get("API_URL")
        self._api_token = api_token or os.environ.get("API_KEY")
        self.db_name = db_name

    def construct_url(self, station_id, date_start, date_end):
        return f"{self._api_url}&token={self._api_token}&stations[]={station_id}&start={date_start}&end={date_end}"

    def save_to_db(self, data):
        pass

    def request(self, station_id, date_start, date_end):
        request_url = self.construct_url(station_id, date_start, date_end)
        response = self._api_client.get(request_url)
        data_json = response.json()
        
        self.save_to_db(data_json)
        
        return data_json

if __name__=="__main__":
    
    client = APIClient()
    print(client.request("07240", "2026-04-18", "2026-04-20"))
