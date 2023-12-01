import pandas as pd
import numpy as np
from datetime import dateime
from . import streamlit_library as stlt
import pytz

class PDLibrary:
    _data = pd.DataFrame()
    _path = ''

    def __init__(self,path,*columns_name,index_col='',init_val=np.nan):
        self._path = path
        try:
            self._data = pd.read_csv(self._path,index_col=index_col,usecols=columns_name)
        except FileNotFoundError:
            self._data = pd.DataFrame(columns=columns_name)
            self._data.set_index(index_col)
            self._data.to_csv(path_or_buf = self._path)

    def append_data(self,new_index=None,init_var=np.nan,**col_val):
        if new_index is None:
            new_index = datetime.utcnow().strftime("%F %T")
        
        self._data.loc[new_index] = np.nan
        for column_name,column_val in col_val.items():
            self._data[column_name][new_index] = column_val

    def save_data(self):
        self._data.to_csv(path_or_buf=self._path)
    

import streamlit as st

class PDLibrary_Streamlit(PDLibrary):
    def add_side_selects(self):
        for attr_name in self._data.columns:
            st.selectbox(label=attr_name,options=self._data[attr_name].unique())

    def add_save_download_button(self,label):
        st.download_button(label=label,data=self._data.to_csv().encode('UTF-8'),file_name='result.csv',)
    
    def append_and_save_data(self,label,**column_data):
        if st.button(label=label):
            self.append_data(**column_data)
            self.save_data()
    
    def show_data(self):
        st.dataframe(self._data)