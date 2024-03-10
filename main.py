import streamlit as st
import pandas as pd

files = {label:st.file_uploader(f"Load {label}") for label in ["content"]}

if all(files.values()):
    dfs = {key:pd.read_csv(files[key]) for key in files}
    df_content = dfs['content']
else:
    st.stop()

def split_hashtag(sr:pd.Series)->pd.Series:
    return sr.str.split("#").apply(lambda ss:ss[1:])


def explode_tag(df:pd.DataFrame,column_name='tag')->pd.DataFrame:
    df = df.copy()
    df['_split_hash']=split_hashtag(df_content[column_name])
    df=df.explode('_split_hash')
    df=df.drop(columns=[column_name])
    df=df.rename(columns={'_split_hash':column_name})
    return df

df_content
df_content=explode_tag(df_content)
df_content

def find_supertag(df:pd.DataFrame)-> list:
    df_temp = df.copy()

    set_tag = {val for val in df_temp['tag'].unique()}
    set_content = {val for val in df_temp['content'].unique()}
    content_supertag=set_tag&set_content
    
    df_temp = df_temp.drop_duplicates(subset=['content'])
    df_temp['content_likely_has_supertag'] = df_temp['content'].apply(lambda val: val in content_supertag)
    df_temp = df_temp[df_temp['content_likely_has_supertag']]
    return df_temp['tag'].unique().tolist()

def split_supertag(df:pd.DataFrame)->tuple[pd.DataFrame,pd.DataFrame]:
    df_temp = df.copy()
    supertags = find_supertag(df_temp)
    with st.expander('debug'):
        supertags
    row_has_supertag=df_temp['tag'].apply(lambda val:val in supertags)
    df_group=df_temp[row_has_supertag]
    df_new_content=df_temp[~row_has_supertag]
    
    return df_new_content, df_group

from typing import Generator
def iter_split_supertag(df:pd.DataFrame)-> Generator[list[pd.DataFrame],None,None]:
    dfs:list[pd.DataFrame] = [df.copy()]
    while not dfs[-1].empty:
        dfs.extend(split_supertag(dfs.pop(-1)))
        yield dfs

for v in iter_split_supertag(df_content):
    ll = len(v)
    cols = st.columns(ll)
    for ind,col in enumerate(cols):
        with col:
            v[ind]
st.stop()

cols = st.multiselect('select columns',df_group.index)

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

df_res = tableize(df_content=df_content,df_meta=df_group,selected_cols=cols,drop_if='any')
df_res