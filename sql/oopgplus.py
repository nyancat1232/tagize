import pandas as pd
from sqlalchemy.sql import text
from dataclasses import dataclass
import sqlalchemy
from typing import List,Self,Dict

class TableStructure:
    schema_name : str
    table_name : str
    engine : sqlalchemy.Engine
    child_tables : List[Self] = None

    def detect_child_tables(self):
        sql = f'''
        SELECT KCU.column_name AS current_column_name,
            CCU.table_schema AS upper_schema, 
            CCU.table_name AS upper_table,
            CCU.column_name AS  upper_column_name
        FROM information_schema.key_column_usage AS KCU
        JOIN information_schema.constraint_column_usage AS CCU ON KCU.constraint_name = CCU.constraint_name
        JOIN information_schema.table_constraints AS TC ON KCU.constraint_name = TC.constraint_name
        WHERE TC.constraint_type = 'FOREIGN KEY'
        AND KCU.table_schema='{self.schema_name}'
        AND KCU.table_name='{self.table_name}';
        '''

        
        self.child_tables=[]
        
        df_foreign_keys = self.execute_sql(sql,index_column='current_column_name',drop_duplicates=True)
        
        for foreign_key_index,foreign_key_series in df_foreign_keys.iterrows():
            current_foreign_schema =  foreign_key_series['upper_schema']
            current_foreign_table =  foreign_key_series['upper_table']
            self.child_tables.append(TableStructure(schema_name=current_foreign_schema,
                                                    table_name=current_foreign_table,
                                                    engine=self.engine))
        return self.child_tables
    
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