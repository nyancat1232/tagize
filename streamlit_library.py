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

def write_col_table(*positional_data,**keyword_data):
    column_table = st.columns(len(positional_data)+len(keyword_data))

    total_data = dict(enumerate(positional_data))
    total_data.update(keyword_data)

    for index,key in enumerate(total_data):
        with column_table[index]:
            st.write(key)
            st.write(total_data[key])

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
    '''
    from amesho import streamlit_library as stl

    func_list=[]
    @stl.add_func(func_list):
    def func_name():
        pass
    stl.write_tabs(*func_list)

    '''
    if names is None:
        names = [f'{num} : {funcs[num].__name__}' for num in range(len(funcs))]

    tabs = st.tabs(names)
    tabs_func = funcs
    for tab,tab_func in zip(tabs,tabs_func):
        with tab:
            tab_func()

def add_func(func_list):
    '''Decoration for write_tabs
    func_list => which collects a function.
    '''
    def ret_func(func):
        func_list.append(func)
    return ret_func