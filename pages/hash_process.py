import pandas as pd
import streamlit as st

from pre import ex,conn
ex()

from hashprocessor.process import tag_explode,iter_split_supertag

df_content = pd.DataFrame({'content':[None],'tag':[None]})
df_content = st.data_editor(df_content,num_rows='dynamic')
df_content=tag_explode(df_content)
with st.expander('debug'):
    df_content


for v in iter_split_supertag(df_content):
    ll = len(v)
    cols = st.columns(ll)
    for ind,col in enumerate(cols):
        with col:
            v[ind]