import pandas as pd
from sqlalchemy.sql import text
from dataclasses import dataclass
import sqlalchemy
from typing import List

class TableStructure:
    schema_name : str
    table_name : str
    engine : sqlalchemy.Engine

    def __init__(self,schema_name:str,table_name:str,engine:sqlalchemy.Engine):
        self.schema_name = schema_name
        self.table_name = table_name
        self.engine = engine

    def execute_sql(self,sql,index_column=None,drop_duplicates=False)->pd.DataFrame:
        with self.engine.connect() as conn:
            ret = pd.read_sql_query(sql=sql,con=conn)

            if drop_duplicates:
                ret = ret.drop_duplicates()

            if index_column:
                return ret.set_index(index_column)
            else:
                return ret

class SQLALchemyPlus:
    engine : sqlalchemy.Engine

    def __init__(self,engine:sqlalchemy.Engine):
        self.engine = engine