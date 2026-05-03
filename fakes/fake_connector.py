from protocols import DBConnector

class FakeConnector(DBConnector):
    def __init__(self, db_name : str = "db.sqlite3", table_infos : dict = None) -> None:
        self.db_name = db_name
        self.table_infos = table_infos
        self.data = []
        
    def setup(self) -> None:
        self.data = []
    
    def insert_rows(self, rows : list[dict]) -> None:
        self.data.extend(rows)