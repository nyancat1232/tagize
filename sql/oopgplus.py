import pandas as pd
from sqlalchemy.sql import text
from dataclasses import dataclass
import sqlalchemy
from typing import List

class TableStructure:
    schema_name : str
    table_name : str

class SQLALchemyPlus:
    engine : sqlalchemy.Engine

    def __init__(self,engine:sqlalchemy.Engine):
        self.engine = engine