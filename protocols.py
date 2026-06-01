from typing import Protocol, runtime_checkable

@runtime_checkable
class APIResponse(Protocol):
    @property
    def ok(self):  # pragma: no cover
        pass

    def json(self) -> dict:  # pragma: no cover
        pass

@runtime_checkable
class APIRequester(Protocol):
    def get(self, url : str) -> APIResponse:  # pragma: no cover
        pass

@runtime_checkable
class DBConnector(Protocol):
    def setup(self) -> None:  # pragma: no cover
        pass

    def insert_rows(self, rows : list[dict]) -> None:  # pragma: no cover
        pass