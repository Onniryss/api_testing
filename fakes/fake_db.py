class FakeDB:
    def __init__(self):
        self.fake_cursor = None
    
    def cursor(self):
        return self.fake_cursor or FakeCursor()
    
    def __enter__(self):
        self.fake_cursor = FakeCursor()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def commit(self):
        pass
        
class FakeCursor:
    def __init__(self):
        pass
    
    def execute(self, query):
        pass
    
    def execute(self, query, values):
        pass