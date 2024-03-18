import streamlit as st
import pandas as pd
import pyplus.sql as sqlp

from pre import conn


from hashprocessor.process import split_hashtag

ts = sqlp.TableStructure(schema_name=st.secrets['address_007']['schema'],table_name=st.secrets['address_007']['table'],engine=conn.engine)
df = ts.read()

df_edit = df.copy()
df_edit['tags']=df_edit['tags'].apply(lambda li:"#".join(['']+li))
df_edit = st.data_editor(df_edit,num_rows='dynamic')

df_post = df_edit.copy()
df_post['tags'] = split_hashtag(df_edit['tags'])
df_post

st.stop()