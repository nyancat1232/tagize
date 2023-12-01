import pandas as pd

def read_from_server(schema_name:str,table_name:str,st_conn):
    with st_conn.connect() as conn_conn:
        return pd.read_sql_table(table_name=table_name,con=conn_conn,schema=schema_name)

def get_foreign_keys(schema,table,conn):
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