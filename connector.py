from sqlite3 import connect
from protocols import DBConnector

class SqliteConnector(DBConnector):
    TYPE_MAPPING = {
        "INTEGER": int,
        "REAL": float,
        "TEXT": str
    }
    
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
    
    
    def __init__(self, db_name : str = "db.sqlite3", table_infos : dict = None) -> None:
        self.db_name = db_name
        self.table_infos = table_infos or SqliteConnector.default_table_infos
        self.column_types = {name: self.TYPE_MAPPING.get(dtype, str) 
                             for name, dtype in self.table_infos["columns"]}

    def setup(self) -> None:
        creation_query = self.create_query()
        with connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute(creation_query)


    def validate_infos(self) -> tuple[str, list[str], list[str]]:
        # name validation
        allowed_table = self.table_infos['table_name']
        if not allowed_table.isidentifier():
            raise ValueError(f"Invalid table name: {allowed_table}")

        # columns validation
        columns = []
        for name, _type in self.table_infos['columns']:
            if not name.isidentifier():
                raise ValueError(f"Invalid column name: {name}")
            columns.append(f"{name} {_type}")

        # primary keys validation
        keys = []
        for key in self.table_infos['primary_keys']:
            if not key.isidentifier():
                raise ValueError(f"Invalid primary key name: {key}")
            keys.append(key)
        
        return allowed_table, columns, keys
    
    
    def create_query(self) -> str:
        table_name, columns, keys = self.validate_infos()
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name}(
            {', '.join(columns)},
            PRIMARY KEY ({', '.join(keys)})
        )
        """
        return query


    def insert_rows(self, rows : list[dict]) -> None:
        table_name = self.table_infos['table_name']
        
        with connect(self.db_name) as conn:
            for row in rows:
                validated_values = []
                
                for col_name, value in row.items():
                    if col_name not in self.column_types:
                        raise ValueError(f"La colonne '{col_name}' n'existe pas dans la config.")
                    
                    if value is None or value == '':
                        validated_values.append(None)
                        continue
                    
                    target_type = self.column_types[col_name]
                    try:
                        clean_value = target_type(value)
                        validated_values.append(clean_value)
                    except (ValueError, TypeError):
                        raise TypeError(f"Type incorrect pour '{col_name}': reçu '{value}', attendu {target_type.__name__}")

                placeholders = ", ".join(["?"] * len(row))
                columns = ", ".join(row.keys())
                query = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                cursor = conn.cursor()
                cursor.execute(query, validated_values)
                conn.commit()
