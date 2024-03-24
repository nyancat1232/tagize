import streamlit as st
import pandas as pd
import pyplus.sql as sqlp
import pyplus.streamlit as stp

from pre import conn


from hashprocessor.process import split_hashtag

ts = sqlp.TableStructure(schema_name=st.secrets['address_007']['schema'],table_name=st.secrets['address_007']['table'],engine=conn.engine)
df = ts.read()


df_edit = df.copy()
df_edit['tags']=df_edit['tags'].apply(lambda li:"#".join(['']+li))
df_edit = st.data_editor(df_edit,disabled=ts.refresh_identity())

df_post = df.copy()

df_post_edit = df_edit.copy()
df_post_edit['tags'] = split_hashtag(df_edit['tags'])

stp.write_columns(original=df_post,edit=df_post_edit)

indexes_changed = df_post.compare(df_post_edit).index.tolist()
indexes_changed

if st.button('edit'):
    for ind in indexes_changed:
        st.toast(ind)
        content = df_post_edit.loc[ind].to_dict()
        ts.upload(id_row=ind,**content)