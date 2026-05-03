from typing import Protocol, runtime_checkable

@runtime_checkable
class APIResponse(Protocol):
    @property
    def ok(self):
        pass
    
    def json(self) -> dict:
        pass

@runtime_checkable
class APIRequester(Protocol):
    def get(self, url : str) -> APIResponse:
        pass

@runtime_checkable
class DBConnector(Protocol):
    def setup(self) -> None:
        pass
    
    def insert_rows(self, rows : list[dict]) -> None:
        pass