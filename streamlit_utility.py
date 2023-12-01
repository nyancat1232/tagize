import streamlit as st
import pandas as pd

def url_analyzer(url):
    temp = "?"
    result = url[url.find(temp)+len(temp):].split("&")
    result = [r.split("=") for r in result]
    result_column = ['attribute','value']
    result = pd.DataFrame(result,columns=result_column)
    return result

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
    write_col_table(first_time_local,duration_now,first_time_local+goal_duration)