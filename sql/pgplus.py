import pandas as pd



def read_from_server(schema_name:str,table_name:str,st_conn):
    with st_conn.connect() as conn_conn:
        return pd.read_sql_table(table_name=table_name,con=conn_conn,schema=schema_name)
    
def write_to_server(df:pd.DataFrame,schema_name:str,table_name:str,st_conn):
    with st_conn.connect() as conn_conn:
        return df.to_sql(name=table_name,con=conn_conn,schema=schema_name)
    
def write_to_server_replace(df:pd.DataFrame,schema_name:str,table_name:str,st_conn):
    with st_conn.session as session:
        delete_sql = f'''
            DELETE FROM {schema_name}.{table_name};
        '''
        try:
          session.execute(delete_sql)
          session.commit()
        except:
          pass #Nothing to delete

    with st_conn.connect() as conn_conn:
        return df.to_sql(name=table_name,con=conn_conn,schema=schema_name,if_exists='append')

def get_foreign_keys(schema:str,table:str,conn):
    foreign_key_sql = f'''
    SELECT KCU.column_name AS current_column_name,
        CCU.table_schema AS upper_schema, 
        CCU.table_name AS upper_table,
        CCU.column_name AS  upper_column_name
    FROM information_schema.key_column_usage AS KCU
    JOIN information_schema.constraint_column_usage AS CCU ON KCU.constraint_name = CCU.constraint_name
    JOIN information_schema.table_constraints AS TC ON KCU.constraint_name = TC.constraint_name
    WHERE TC.constraint_type = 'FOREIGN KEY'
    AND KCU.table_schema='{schema}'
    AND KCU.table_name='{table}';
    '''

    with conn.connect() as con_con:
        ret = pd.read_sql_query(foreign_key_sql,con=con_con).drop_duplicates()
    
        return ret.set_index('current_column_name')
    
def get_identity(schema:str,table:str,conn):
    sql = f'''SELECT attname as identity_column
  FROM pg_attribute 
  JOIN pg_class 
    ON pg_attribute.attrelid = pg_class.oid
  JOIN pg_namespace
    ON pg_class.relnamespace = pg_namespace.oid
 WHERE nspname = '{schema}'
   AND relname = '{table}'
   AND attidentity = 'a';
'''
    
    with conn.connect() as con_con:
        ret = pd.read_sql_query(sql,con=con_con)
    
        return ret['identity_column']
    
def get_default_value(schema:str,table:str,conn):
    sql = f'''SELECT column_name, column_default
  FROM information_schema.columns
 WHERE table_schema = '{schema}'
   AND table_name = '{table}'
   AND column_default IS NOT NULL ;
'''
        
    with conn.connect() as con_con:
        ret = pd.read_sql_query(sql,con=con_con)
    
        return ret.set_index('column_name')