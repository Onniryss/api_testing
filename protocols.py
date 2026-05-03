from typing import Protocol, runtime_checkable
from requests import Response

@runtime_checkable
class APIRequester(Protocol):
    def get(self, url : str) -> Response:
        pass

@runtime_checkable
class DBConnector(Protocol):
    def setup(self) -> None:
        pass
    
    def insert_rows(self, rows : list[dict]) -> None:
        pass