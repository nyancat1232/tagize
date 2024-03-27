import pandas as pd
import streamlit as st

from pre import ex,ts
ex()

from hashprocessor.process import tag_explode,iter_split_supertag

df_content = ts.read()
st.dataframe(df_content)
df_content=tag_explode(df_content)
with st.expander('debug'):
    df_content

final_res = None
for v in iter_split_supertag(df_content):
    final_res = v
    ll = len(v)
    cols = st.columns(ll)
    for ind,col in enumerate(cols):
        with col:
            v[ind]

df = pd.concat(final_res)
df