import pandas as pd
from typing import Optional

def create_new_dataframe_keep_columns(df:pd.DataFrame,index:Optional[pd.Series] = None)->pd.DataFrame:
    return pd.DataFrame(columns=df.columns,index=index).astype(dtype=df.dtypes).copy()

def to_date(sr:pd.Series)->pd.Series:
    return sr.dt.date

