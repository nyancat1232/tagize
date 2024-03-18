import pandas as pd
from typing import Callable

def create_new_dataframe_keep_columns(df:pd.DataFrame,index:pd.Series|None = None)->pd.DataFrame:
    return pd.DataFrame(columns=df.columns,index=index).astype(dtype=df.dtypes).copy()

def to_date(sr:pd.Series)->pd.Series:
    return sr.dt.date

def horizontal_applier(df:pd.DataFrame,func:Callable[[tuple[pd.Series]],pd.Series],*cols:tuple[str]):
    l_cols = list(cols)
    return df[l_cols].apply(lambda c : func(*c),axis=1)