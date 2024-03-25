import streamlit as st
import pyplus.streamlit as stp


def ex():
    if not stp.check_password():
        st.stop()

if 'conn' not in st.session_state:
    st.session_state['conn'] = st.connection('myaddress',type='sql')

conn = st.session_state['conn']

import pyplus.sql as sqlp

if 'ts' not in st.session_state:
    st.session_state['ts'] = sqlp.TableStructure(schema_name=st.secrets['address_007']['schema'],table_name=st.secrets['address_007']['table'],engine=conn.engine)

ts:sqlp.TableStructure = st.session_state['ts']