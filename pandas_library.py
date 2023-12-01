import pandas as pd
from datetime import datetime

def column_to_int_type(df_column):
    df_column=df_column.str.split(' |-|:')

    def _apply_func(element):
        if type(element) == list:
            temp = [int(si) for si in element]
            return datetime(*temp)
        else:
            return None
    
    df_column=df_column.apply(lambda s:_apply_func(s))
    return df_column