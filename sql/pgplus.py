import pandas as pd
from sqlalchemy.sql import text
'''
DO NOT USE AS PUBLIC. 
'''

def read_from_server(schema_name:str,table_name:str,st_conn):
    with st_conn.connect() as conn_conn:
        return pd.read_sql_table(table_name=table_name,con=conn_conn,schema=schema_name)

def get_foreign_keys(schema_name:str,table_name:str,st_conn):
    foreign_key_sql = f'''
    SELECT KCU.column_name AS current_column_name,
        CCU.table_schema AS upper_schema, 
        CCU.table_name AS upper_table,
        CCU.column_name AS  upper_column_name
    FROM information_schema.key_column_usage AS KCU
    JOIN information_schema.constraint_column_usage AS CCU ON KCU.constraint_name = CCU.constraint_name
    JOIN information_schema.table_constraints AS TC ON KCU.constraint_name = TC.constraint_name
    WHERE TC.constraint_type = 'FOREIGN KEY'
    AND KCU.table_schema='{schema_name}'
    AND KCU.table_name='{table_name}';
    '''

    with st_conn.connect() as con_con:
        ret = pd.read_sql_query(foreign_key_sql,con=con_con).drop_duplicates()
    
        return ret.set_index('current_column_name')
    
def get_identity(schema_name:str,table_name:str,st_conn):
    sql = f'''SELECT attname as identity_column
  FROM pg_attribute 
  JOIN pg_class 
    ON pg_attribute.attrelid = pg_class.oid
  JOIN pg_namespace
    ON pg_class.relnamespace = pg_namespace.oid
 WHERE nspname = '{schema_name}'
   AND relname = '{table_name}'
   AND attidentity = 'a';
'''
    
    with st_conn.connect() as con_con:
        ret = pd.read_sql_query(sql,con=con_con)
    
        return ret['identity_column']
    
def get_default_value(schema_name:str,table_name:str,st_conn):
    sql = f'''SELECT column_name, column_default
  FROM information_schema.columns
 WHERE table_schema = '{schema_name}'
   AND table_name = '{table_name}'
   AND column_default IS NOT NULL ;
'''
        
    with st_conn.connect() as con_con:
        ret = pd.read_sql_query(sql,con=con_con)
    
        return ret.set_index('column_name')
    

      
def write_to_server(df:pd.DataFrame,schema_name:str,table_name:str,st_conn):
    with st_conn.connect() as conn_conn:
        return df.to_sql(name=table_name,con=conn_conn,schema=schema_name,if_exists='append',index=False)

def upload_to_sql_by_value(schema_name,table_name,select_row_by_column,select_row_by_column_val,column_name,value_name,st_conn):
    update_query = text(f"""
    UPDATE {schema_name}.{table_name}
    SET {column_name} = {value_name}
    WHERE {select_row_by_column} = '{select_row_by_column_val}';
    """)
    update_query
    with st_conn.session as session:
        session.execute(update_query)
        session.commit()
