from protocols import APIRequester, APIResponse
from exceptions import ResponseNotOkException

class FakeResponse(APIResponse):
    def __init__(self, json_data : dict, status : int) -> None:
        self.json_data = json_data
        self.status = status
    
    @property
    def ok(self) -> bool:
        if self.status // 100 == 2:
            return True

        return False
    
    def json(self) -> dict:
        if self.ok:
            return self.json_data
        
        raise ResponseNotOkException()

class FakeRequester(APIRequester):
    def __init__(self, data : dict, ok : bool = True):
        self.data = data
        self.ok = ok
    
    def get(self, url : str) -> APIResponse:
        if self.ok:
            return FakeResponse(self.data, 200)

        return FakeResponse({"error" : "There was an error"}, 400)
