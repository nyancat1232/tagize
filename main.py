import streamlit as st
import pandas as pd
import pyplus.sql as splq

def split_hashtag(sr:pd.Series)->pd.Series:
    return sr.str.split("#").apply(lambda ss:ss[1:])

def explode_tag(df:pd.DataFrame,column_name='tag')->pd.DataFrame:
    df = df.copy()
    df['_split_hash']=split_hashtag(df_content[column_name])
    df=df.explode('_split_hash')
    df=df.drop(columns=[column_name])
    df=df.rename(columns={'_split_hash':column_name})
    return df

from pre import ex,conn
ex()


ts = splq.TableStructure(schema_name=st.secrets['address_007']['schema'],table_name=st.secrets['address_007']['table'],engine=conn.engine)
df = ts.read()

df_edit = df.copy()
df_edit['tags']=df_edit['tags'].apply(lambda li:"#".join(['']+li))
df_edit = st.data_editor(df_edit,num_rows='dynamic')

df_post = df_edit.copy()
df_post['tags'] = split_hashtag(df_edit['tags'])
df_post

st.stop()
df_content = pd.DataFrame({'content':[None],'tag':[None]})
df_content = st.data_editor(df_content,num_rows='dynamic')
df_content=explode_tag(df_content)
with st.expander('debug'):
    df_content

def find_supertag(df:pd.DataFrame)-> list:
    df_temp = df.copy()

    set_tag = {val for val in df_temp['tag'].unique()}
    set_content = {val for val in df_temp['content'].unique()}
    content_supertag=set_tag&set_content
    
    sr_content_likely_has_supertag = df_temp['content'].apply(lambda val: val in content_supertag)
    df_temp = df_temp[sr_content_likely_has_supertag]
    return df_temp['tag'].unique().tolist()

def split_supertag(df:pd.DataFrame)->tuple[pd.DataFrame,pd.DataFrame]:
    df_temp = df.copy()
    supertags = find_supertag(df_temp)
    with st.expander('debug'):
        supertags
    sr_row_has_supertag=df_temp['tag'].apply(lambda val:val in supertags)
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

for v in iter_split_supertag(df_content):
    ll = len(v)
    cols = st.columns(ll)
    for ind,col in enumerate(cols):
        with col:
            v[ind]