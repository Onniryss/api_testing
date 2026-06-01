from connector import SqliteConnector
from client import APIClient


connector = SqliteConnector()
connector.setup()
client = APIClient(connector)
data_json = client.request("STATIC0319", "2026-04-18", "2026-04-20")
print(data_json)
client.save_to_db(data_json)