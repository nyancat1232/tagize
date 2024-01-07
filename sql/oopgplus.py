import pandas as pd
from sqlalchemy.sql import text
from dataclasses import dataclass
import sqlalchemy
from typing import List,Self,Dict

class TableStructure:
    schema_name : str
    table_name : str
    engine : sqlalchemy.Engine
    parent_table : Self
    parent_foreign_id : str
    generation : int

    _identity_column : str

    def get_foreign_table(self):
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
        return self.execute_sql_read(sql,index_column='current_column_name',drop_duplicates=True)
    
    def get_types(self):
        sql = f'''
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = '{self.schema_name}' AND 
        table_name = '{self.table_name}';
        '''
        return self.execute_sql_read(sql,index_column='column_name')
    
    def refresh_identity(self):
        sql = f'''SELECT attname as identity_column
        FROM pg_attribute 
        JOIN pg_class 
            ON pg_attribute.attrelid = pg_class.oid
        JOIN pg_namespace
            ON pg_class.relnamespace = pg_namespace.oid
        WHERE nspname = '{self.schema_name}'
        AND relname = '{self.table_name}'
        AND attidentity = 'a';
        '''
        self._identity_column = self.execute_sql_read(sql)['identity_column'].to_list()
        return self._identity_column

    def get_default_value(self):
        sql = f'''SELECT column_name, column_default
        FROM information_schema.columns
        WHERE table_schema = '{self.schema_name}'
        AND table_name = '{self.table_name}'
        AND column_default IS NOT NULL ;
        '''
        return self.execute_sql_read(sql).set_index('column_name')
    
    def detect_child_tables(self):
        child_tables=[]
        
        df_foreign_keys = self.get_foreign_table()
        
        for foreign_key_index,foreign_key_series in df_foreign_keys.iterrows():
            current_foreign_schema =  foreign_key_series['upper_schema']
            current_foreign_table =  foreign_key_series['upper_table']
            column_name_before_foreign = foreign_key_index
            child_tables.append(TableStructure(schema_name=current_foreign_schema,
                                                    table_name=current_foreign_table,
                                                    engine=self.engine,
                                                    parent_table=self,
                                                    parent_foreign_id=column_name_before_foreign,
                                                    generation=self.generation+1))
        return child_tables


    def __init__(self,schema_name:str,table_name:str,
                 engine:sqlalchemy.Engine,
                 parent_table:Self=None,parent_foreign_id:str=None,
                 generation:int=0):
        self.schema_name = schema_name
        self.table_name = table_name
        self.engine = engine
        if parent_table:
            self.parent_table = parent_table
            self.parent_foreign_id = parent_foreign_id
        self.generation = generation
        self._identity_column = self.refresh_identity()


    def execute_sql_read(self,sql,index_column=None,drop_duplicates=False)->pd.DataFrame:
        with self.engine.connect() as conn:
            ret = pd.read_sql_query(sql=sql,con=conn)

            if drop_duplicates:
                ret = ret.drop_duplicates()

            if index_column:
                return ret.set_index(index_column)
            else:
                try:
                    return ret.set_index(self._identity_column)
                except:
                    return ret
                
    def execute_sql_write(self,sql):
        with self.engine.connect() as conn:
            conn.execute(sql)
            conn.commit()
            
        
        return self.read()
            
    def get_all_children(self):
        children = self.detect_child_tables()
        if len(children)>0:
            rr = [self]
            for ts_child in children:
                rr.extend(ts_child.get_all_children())
            rr.sort(key=lambda l:l.generation,reverse=False)

            return rr
        else:
            return [self]
            

    def read(self):
        sql = f'''SELECT * FROM {self.schema_name}.{self.table_name}
        '''
        return self.execute_sql_read(sql)
    
    def expand_read(self):
        df = self.read().reset_index()
        
        all_children = self.get_all_children()[1:]

        for child in all_children:
            try:
                df_child = child.expand_read()
                df_child_columns = df_child.columns
                df_child_indicate = {col : f'{child.parent_foreign_id}.{col}' for col in df_child_columns}
                df_child = df_child.rename(columns=df_child_indicate)

                df = pd.merge(left=df,right=df_child,
                        left_on=child.parent_foreign_id,right_index=True,
                        how='left')
                del df[child.parent_foreign_id]
            except:
                pass

        df=df.set_index(self._identity_column)
        
        return df
    
    def upload(self,id_row:int,**kwarg):

        original=",".join(["=".join([key,f"'{str(kwarg[key])}'"]) for key in kwarg if kwarg[key]])
        
        sql = text(f"""
        UPDATE {self.schema_name}.{self.table_name}
        SET {original}
        WHERE {self._identity_column[0]} = {id_row};
        """)
        
        return self.execute_sql_write(sql)
    
    def upload_append(self,**kwarg):
        ke = ','.join([key for key in kwarg])
        vvv = ','.join(["'"+str(kwarg[key])+"'" for key in kwarg])
        sql = text(f"""
        INSERT INTO {self.schema_name}.{self.table_name} ({ke})
        VALUES ({vvv})
        """)
        return self.execute_sql_write(sql)


    
def get_table_list(engine:sqlalchemy.Engine):
    '''
    Get table list in a database.
    ## Parameters:
    engine : sqlalchemy.Engine
    a engine.
    ## See Also:
    
    ## Examples:
    import streamlit as st
    eng = st.connection(name='postgresql',type='sql').engine

    df_list=get_table_list(eng)
    '''


    sql = f'''SELECT DISTINCT table_schema,table_name
    FROM information_schema.table_constraints;
    '''
    with engine.connect() as con_con:
        ret = pd.read_sql_query(sql,con=con_con)
    
        return ret

class SQLALchemyPlus:
    engine : sqlalchemy.Engine
    tables : List[TableStructure]

    def __init__(self,engine:sqlalchemy.Engine):
        self.engine = engine
    
    def add_tables(self,schema_name:str,table_name:str):
        self.tables.append(TableStructure(schema_name,table_name))