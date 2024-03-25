import streamlit as st
import pandas as pd
import pyplus.sql as sqlp
import pyplus.streamlit as stp

from pre import ex,ts
ex()


from hashprocessor.process import tag_split

df = ts.read()


df_edit = df.copy()
df_edit['tags']=df_edit['tags'].apply(lambda li:"#".join(['']+li))
df_edit = st.data_editor(df_edit,disabled=ts.refresh_identity())

df_post = df.copy()

df_post_edit = df_edit.copy()
df_post_edit['tags'] = tag_split(df_edit['tags'])

stp.write_columns(original=df_post,edit=df_post_edit)

indexes_changed = df_post.compare(df_post_edit).index.tolist()
indexes_changed

if st.button('edit'):
    for ind in indexes_changed:
        st.toast(ind)
        content = df_post_edit.loc[ind].to_dict()
        ts.upload(id_row=ind,**content)


content_input = st.text_area('input content')
tags_input = st.data_editor([None,],num_rows='dynamic')
content_input
tags_input

if st.button('append'):
    ts.upload_append(content=content_input,tags=tags_input)