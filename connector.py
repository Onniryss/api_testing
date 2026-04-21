from sqlite3 import connect, OperationalError

class Connector:
    default_table_infos = {
        "table_name" : "records",
        "columns" : [
            ("id_station", "INTEGER"),
            ("dh_utc", "TEXT"),
            ("temperature", "REAL"),
            ("pression", "REAL"), 
            ("pression_variation_3h", "REAL"), 
            ("humidite", "REAL"), 
            ("point_de_rosee", "REAL"), 
            ("visibilite", "REAL"), 
            ("vent_moyen", "REAL"), 
            ("vent_rafales", "REAL"), 
            ("vent_rafales_10min", "REAL"), 
            ("vent_direction", "REAL"), 
            ("temperature_min", "REAL"), 
            ("temperature_max", "REAL"), 
            ("pluie_1h", "REAL"), 
            ("pluie_3h", "REAL"), 
            ("pluie_6h", "REAL"), 
            ("pluie_12h", "REAL"), 
            ("pluie_24h", "REAL"), 
            ("ensoleillement", "REAL"), 
            ("temperature_sol", "REAL"), 
            ("temps_omm", "REAL"), 
            ("source", "TEXT"), 
            ("radiations", "REAL"), 
            ("neige_au_sol", "REAL"), 
            ("nebulosite", "REAL"), 
            ("raw_msg", "TEXT"),
        ],
        "primary_keys" : [
            "id_station",
            "dh_utc"
        ]
    }
    
    def __init__(self, db_name = "db.sqlite3", table_infos : dict = None):
        self.db_name = db_name
        self.table_infos = table_infos or Connector.default_table_infos
        creation_query = self.create_query()
        
        try:
            with connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                cursor.execute(creation_query)
        except OperationalError as e:
            print(e)
    
    def create_query(self):
        columns = [f'{name} {_type}' for name, _type in self.table_infos['columns']]
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_infos['table_name']}(
            {', '.join(columns)},
            PRIMARY KEY ({', '.join(self.table_infos['primary_keys'])})
        )
        """
        return query
    
    
if __name__=="__main__":
    connector = Connector()