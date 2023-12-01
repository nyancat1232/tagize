import pandas as pd

class PDLibrary:
    data = pd.DataFrame()
    def __init__(self,path_or_buffer,init_val=0,*columns_name):
        self.data = pd.read_csv(path_or_buffer)
        self.initialize_attribute(init_val,*columns_name)

    def initialize_attribute(self,init_val,*columns_name):
        for column_name in columns_name:
            if column_name not in self.data:
                self.data[column_name] = init_val

    def append_data(self,new_index='recent',init_var='',**col_val):
        self.data.loc[new_index] = init_var
        for column_name,column_val in col_val.items():
            self.data[column_name][new_index] = column_val

import streamlit as st

class PDLibrary_Streamlit(PDLibrary):
    def add_side_selects(self):
        for attr_name in self.data.columns:
            st.selectbox(label=attr_name,options=self.data[attr_name].unique())

    