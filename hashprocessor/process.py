import pandas as pd
import streamlit as st

def tag_split(sr:pd.Series)->pd.Series:
    return sr.str.split("#").apply(lambda ss:ss[1:])

def tag_explode(df:pd.DataFrame,column_name:str='tags')->pd.DataFrame:
    df = df.copy()
    df=df.explode(column_name)
    df=df.rename(columns={'_split_hash':column_name})
    return df

def find_supertag(df:pd.DataFrame,column_name:str='tags')-> list:
    df_temp = df.copy()

    set_tag = {val for val in df_temp[column_name].unique()}
    set_content = {val for val in df_temp['content'].unique()}
    content_supertag=set_tag&set_content
    
    sr_content_likely_has_supertag = df_temp['content'].apply(lambda val: val in content_supertag)
    df_temp = df_temp[sr_content_likely_has_supertag]
    return df_temp[column_name].unique().tolist()

def split_supertag(df:pd.DataFrame,column_name:str='tags')->tuple[pd.DataFrame,pd.DataFrame]:
    df_temp = df.copy()
    supertags = find_supertag(df_temp)
    with st.expander('debug'):
        supertags
    sr_row_has_supertag=df_temp[column_name].apply(lambda val:val in supertags)
    df_group=df_temp[sr_row_has_supertag]
    df_new_content=df_temp[~sr_row_has_supertag]

    sr_group_duplicate = df_group['content'].apply(lambda val: val in df_new_content['content'].unique())
    df_group=df_group[~sr_group_duplicate]

    return df_new_content, df_group

from typing import Generator
def iter_split_supertag(df:pd.DataFrame)-> Generator[list[pd.DataFrame],None,None]:
    dfs:list[pd.DataFrame] = [df.copy()]
    while not dfs[-1].empty:
        dfs.extend(split_supertag(dfs.pop(-1)))
        yield dfs