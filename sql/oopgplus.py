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


class SQLALchemyPlus:
    engine : sqlalchemy.Engine

    def __init__(self,engine:sqlalchemy.Engine):
        self.engine = engine