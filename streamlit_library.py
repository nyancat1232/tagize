import streamlit as st
from datetime import datetime, timedelta
import pytz
from . import dataio as dio

def dec_func(old_func):
    def new_func(*parg,**kwarg):
        st.divider()
        old_func(*parg,**kwarg)
        st.divider()
    return new_func

def write_col_table(*column_data):
    column_length = len(column_data)
    column_table = st.columns(column_length)

    for column in range(column_length):
        with column_table[column]:
            st.write(column_data[column])

    return column_data

def write_col_eval(sstr_eval,globs=None):
    globs = globs.copy()
    daa = sstr_eval.split('\n')
    filtered_globals = {key:value for key,value in zip(globs.keys(),globs.values() ) if key.find("__") == -1 }

    daa_eval = [eval(l,filtered_globals) for l in daa]

    st.divider()
    write_col_table(*daa)
    write_col_table(*daa_eval)
    st.divider()

def time_show(first_time,max_hour_duration,current_time,timezone="UTC",text="blank"):

    my_timezone = pytz.timezone(timezone)

    duration_now = current_time-first_time
    goal_duration = timedelta(hours=max_hour_duration)
    first_time_local = first_time.astimezone(my_timezone)
    current_time_local = current_time.astimezone(my_timezone)


    st.divider()
    
    st.progress(min(duration_now/goal_duration,1.),text=text)
    write_col_table(first_time_local,duration_now,first_time_local+goal_duration)

def write_tabs(*funcs,names=None):
    if names is None:
        names = [f'col {num}' for num in range(len(funcs))]

    tabs = st.tabs(names)
    tabs_func = funcs
    for tab,tab_func in zip(tabs,tabs_func):
        with tab:
            tab_func()