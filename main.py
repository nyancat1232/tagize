import streamlit as st
import pandas as pd

df_content = pd.read_csv(st.file_uploader("Load contents"))
df_meta = pd.read_csv(st.file_uploader("Load metas"))

def split_hashtag(sr:pd.Series)->pd.Series:
    return sr.str.split("#").apply(lambda ss:ss[1:])

df_content

df_meta = df_meta.set_index('tag_group')
df_meta

cols = st.multiselect('select columns',df_meta.index)

def tableize(df_content:pd.DataFrame,df_meta:pd.DataFrame,selected_cols:list[str],tag_column_name:str='tag',drop_if:str|None=None)->pd.DataFrame:
    df_content = df_content.copy()
    df_meta = df_meta.copy()

    content_hashtag_split=split_hashtag(df_content[tag_column_name])
    meta_hashtag_split=split_hashtag(df_meta[tag_column_name])

    for col in selected_cols:
        def pr(strs:list[str]):
            rrr = [s for s in strs if s in meta_hashtag_split[col]]
            if len(rrr)>0:
                return [s for s in strs if s in meta_hashtag_split[col]]
            else:
                return None
        df_content[col]=content_hashtag_split.apply(pr)

    if drop_if:
        df_content = df_content.dropna(axis=0,subset=selected_cols,how=drop_if)

    return df_content

df_res = tableize(df_content=df_content,df_meta=df_meta,selected_cols=cols,drop_if='any')
df_res