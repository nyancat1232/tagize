import pandas as pd
from sqlalchemy.sql import text
from dataclasses import dataclass
import sqlalchemy
from typing import Self
from datetime import datetime

def _apply_escaping(sentence:str):
    return sentence.replace("'","''")

def _conversion_Sql_value(val:None|int|float|str|pd.Timestamp|list):
    match val:
        case None:
            return 'NULL'
        case int():
            return f"'{str(val)}'"
        case float():
            return f"'{str(val)}'"
        case str():
            return f"'{_apply_escaping(val)}'"
        case pd.Timestamp():
            return f"'{str(val)}'"
        case list():
            val_after = [f'"{str(v)}"' for v in val]
            return "'{"+f"{','.join(val_after)}"+"}'"
        case _:
            raise NotImplementedError(type(val))

def _convert_pgsql_type_to_pandas_type(pgtype:str):
    #https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#basics-dtypes
    match pgtype:
        case 'bigint':
            return 'Int64' #Int vs int
        case 'integer':
            return 'Int32' #Int vs int
        case 'boolean':
            return 'boolean'
        case 'text':
            return 'string'
        case 'double precision':
            return 'Float64'
        case 'date':
            return 'object'
        case 'timestamp without time zone':
            return 'datetime64[ns]'
        case 'timestamp with time zone':
            return 'datetime64[ns, UTC]'
        case 'ARRAY':
            return 'object'
        case _:
            raise NotImplementedError(pgtype)

def _ret_a_line(key:str,dtype:str):
    def _default_value_of_type(type:str):
        match type:
            case 'date':
                return ['DEFAULT','now()']
            case 'timestamp without time zone':
                return ['DEFAULT','now()']
            case 'timestamp with time zone':
                return ['DEFAULT','now()']
            case _:
                return None
            
    ret= [f'"{key}"',dtype]
    if (retplus := _default_value_of_type(dtype)) is not None:
        ret.extend(retplus)
    return ret

_reserved_columns = ['id']

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
        SELECT column_name, data_type, udt_name
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
                 parent_table:Self|None=None,parent_foreign_id:str|None=None,
                 generation:int=0):
        self.schema_name = schema_name
        self.table_name = table_name
        self.engine = engine
        if parent_table:
            self.parent_table = parent_table
            self.parent_foreign_id = parent_foreign_id
        self.generation = generation
        self._identity_column = self.refresh_identity()


    def execute_sql_read(self,sql,index_column:str|None=None,drop_duplicates:bool=False)->pd.DataFrame:
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
            
    def create_table(self,**type_dict):
        '''
        create a table
        
        Parameters
        ----------
        type_dict : dict
            {column_name : column_type}.
        
        
        Examples
        --------  
        >>> ts = sqlp.TableStructure(schema_name=schema_name,table_name=table_name,engine=conn.engine)
        >>> res = ts.create_table(name='text',location='text',grade='bigint',x='double precision',y='double precision')
            text   location    grade    x    y
        ...
        '''
        for rc in _reserved_columns:
            if rc in type_dict:
                raise ValueError(f'{rc} is reserved.')
        


        qlines = [" ".join(_ret_a_line(key,type_dict[key])) for key in type_dict]
        qlines.insert(0,"id bigint NOT NULL GENERATED ALWAYS AS IDENTITY")
        qlines.append("PRIMARY KEY (id)")
        query=text(f'''CREATE TABLE {self.schema_name}.{self.table_name} (
            {','.join(qlines)}
        );''')
        
        return self.execute_sql_write(query)

    def append_column(self,**type_dict):
        for rc in _reserved_columns:
            if rc in type_dict:
                raise ValueError(f'{rc} is reserved.')
        
        qlines = [" ".join(['ADD COLUMN']+_ret_a_line(key,type_dict[key])) for key in type_dict]
        query = text(f'''ALTER TABLE {self.schema_name}.{self.table_name} {','.join(qlines)};''')
        return self.execute_sql_write(query)

    def read(self,ascending=False,columns:list[str]|None=None):
        sql = f'''SELECT * FROM {self.schema_name}.{self.table_name}
        '''
        df_exec_res = self.execute_sql_read(sql)
        df_col_types = self.get_types()
        column_identity = df_exec_res.index.name

        conv_type = {column_name:_convert_pgsql_type_to_pandas_type(df_col_types['data_type'][column_name]) for column_name 
                     in df_col_types.index if column_name != column_identity}
        df_exec_res = df_exec_res.astype(conv_type)
        df_exec_res = df_exec_res.sort_index(ascending=ascending)

        if columns is not None:
            df_exec_res = df_exec_res[columns]

        return df_exec_res
    
    def read_expand(self,ascending=False):
        df = self.read().reset_index()
        
        all_children = self.get_all_children()[1:]

        for child in all_children:
            try:
                df_child = child.read_expand()
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
        
        return df.sort_index(ascending=ascending)
    
    def upload(self,id_row:int,**kwarg):

        original=",".join(["=".join([key,f"{_conversion_Sql_value(kwarg[key])}"]) for key in kwarg])
        
        sql = text(f"""
        UPDATE {self.schema_name}.{self.table_name}
        SET {original}
        WHERE {self._identity_column[0]} = {id_row};
        """)
        
        return self.execute_sql_write(sql)
    
    def upload_append(self,**kwarg):
        columns = ','.join([f'"{key}"' for key in kwarg])
        values = ','.join([_conversion_Sql_value(kwarg[key]) for key in kwarg])
        sql = text(f"""
        INSERT INTO {self.schema_name}.{self.table_name} ({columns})
        VALUES ({values})
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
    tables : list[TableStructure]

    def __init__(self,engine:sqlalchemy.Engine):
        self.engine = engine
    
    def add_tables(self,schema_name:str,table_name:str):
        self.tables.append(TableStructure(schema_name,table_name))