import pandas as pd
from datetime import datetime

def column_to_int_type(df_column):
    df_column=df_column.str.split(' |-|:')
    df_column=df_column.apply(lambda l:[int(s) for s in l])
    df_column=df_column.apply(lambda l:datetime(*l))
    return df_column