import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
from . import streamlit_library as stl

def url_analyzer(url):
    temp = "?"
    result = url[url.find(temp)+len(temp):].split("&")
    result = [r.split("=") for r in result]
    result_column = ['attribute','value']
    result_pd_in = pd.DataFrame(result,columns=result_column)
    result = list_input(result_pd_in['attribute'])
    result_pd_out = pd.Series(result)
    result_url = url[:url.find(temp)+len(temp)]
    result_url += "&".join(["=".join([key,val]) for key,val in result.items()])
    return result_pd_out, result_url

def list_input(attribute_list):
    return {attr : st.text_input(label=f'{attr}') for attr in attribute_list}

def time_show(first_time,max_hour_duration,current_time,timezone="UTC",text="blank"):

    my_timezone = pytz.timezone(timezone)

    duration_now = current_time-first_time
    goal_duration = timedelta(hours=max_hour_duration)
    first_time_local = first_time.astimezone(my_timezone)
    current_time_local = current_time.astimezone(my_timezone)


    st.divider()
    
    st.progress(min(duration_now/goal_duration,1.),text=text)
    stl.write_col_table(first_time_local,duration_now,first_time_local+goal_duration)


import pandas as pd
import tabula as tb

def from_csv_to_dataframe(label)->'DataFrame':
    """Convert csv file which is from streamlit to DataFrame.

    Args:
        label (str): texts to show.

    Returns:
        DataFrame: A dataframe
    """
    if file := st.file_uploader(label=label,type="csv"):
        return pd.read_csv(filepath_or_buffer=file)


def from_pdf_to_dataframe(label,number=0)->'DataFrame':
    if file := st.file_uploader(label=label,type="pdf"):
        return tb.read_pdf(file)[number]

def from_txt_to_dataframe(label,preprocess_function):
    if text := st.text_area(label=label):
        return preprocess_function(text)