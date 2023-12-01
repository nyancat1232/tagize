import pandas as pd
import numpy as np
from datetime import datetime
from . import streamlit_library as stlt
import pytz

class PDLibrary:
    _data = pd.DataFrame()
    _path = ''

    def __init__(self,path,*columns_name,index_name='',init_val=np.nan):
        self._path = path
        try:
            self._data = pd.read_csv(self._path,index_col=index_name)
        except FileNotFoundError:
            self._data = pd.DataFrame(columns=columns_name)
            self._data.index.name = index_name
            self.save_data()
        finally:
            self._data.index = pd.DatetimeIndex(self._data.index)
            
    def append_data_nowtime(self,init_var=np.nan,**col_val):
        new_index = datetime.utcnow()
        
        self._data.loc[new_index] = np.nan
        for column_name,column_val in col_val.items():
            self._data[column_name][new_index] = column_val

    def save_data(self):
        self._data.to_csv(path_or_buf=self._path)

    def get_recent_data(self,column_name):
        filtered_data = self._data[column_name]
        filtered_data =  filtered_data[filtered_data.notna()]
        try:
            return filtered_data.loc[max(filtered_data.index)]
        except ValueError:
            return 0
    

import streamlit as st

class PDLibrary_Streamlit(PDLibrary):
    def add_side_selects(self):
        for attr_name in self._data.columns:
            st.selectbox(label=attr_name,options=self._data[attr_name].unique())

    def add_save_download_button(self,label="Download it"):
        st.download_button(label=label,data=self._data.to_csv().encode('UTF-8'),file_name='result.csv',)
    
    def show_data(self):
        st.dataframe(self._data)