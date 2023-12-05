import streamlit as st
import numpy as np


def divide(old_func):
    def new_func(*parg,**kwarg):
        st.divider()
        old_func(*parg,**kwarg)
        st.divider()
    return new_func

def write_columns(*positional_data,**keyword_data):
    '''
    write by columns
    ## Parameters:
    positional_data : Any
    .
    keyword_data : Any
    .
    ## See Also:
    st.write
    st.columns
    ## Examples:
    from pyplus.streamlit.streamlit_plus import write_columns
    import streamlit as st

    xx=np.array([['x1','x2'],['x3','x4']])
    ww=np.array([['w1','w2'],['w3','w4']])

    write_columns(X1=xx,W1=ww)

    >> X1           W1
    >> 0    1       0       1
    >> x1   x2      w1      w2
    >> x3   x4      w3      w4

    '''
    if len(positional_data)+len(keyword_data)<1:
        st.write('No arguments')
        return

    column_table = st.columns(len(positional_data)+len(keyword_data))

    total_data = dict(enumerate(positional_data))
    total_data.update(keyword_data)

    for index,key in enumerate(total_data):
        with column_table[index]:
            st.write(key)
            st.write(total_data[key])

def write_tabs(*funcs,names=None):
    '''
    from amesho import streamlit_library as stl

    func_list=[]
    @stl.add_tab_func(func_list):
    def func_name():
        pass
    stl.write_tabs(*func_list)

    '''
    if names is None:
        names = [f'{funcs[num].__name__}' for num in range(len(funcs))]

    tabs = st.tabs(names)
    tabs_func = funcs
    for tab,tab_func in zip(tabs,tabs_func):
        with tab:
            tab_func()

def add_tab_func(func_list):
    def ret_func(func):
        func_list.append(func)
    return ret_func


def list_text_input_by_vals(*attribute_list,**kwarg_text_input):
    return {attr : st.text_input(label=f'{attr}',**kwarg_text_input) for attr in attribute_list}

def list_checkbox(*names):
    return {name : st.checkbox(label=name,value=False) for name in names}

def list_text_inputs(label):
    row_amount = st.slider(label=f'{label}\'s row',min_value=1,max_value=100,value=1)
    col_amount = st.slider(label=f'{label}\'s column',min_value=1,max_value=100,value=1)
    def gen_names(current_label,max_num):
        cur_name=0
        ret = f'{current_label}_{cur_name}'
        yield ret
        while (cur_name:=cur_name+1)<max_num:
            ret = f'{current_label}_{cur_name}'
            yield ret

    input_data=[]
    columns=st.columns(col_amount)
    for col_ind, column in enumerate(columns):
        with column:
            row_data=[]
            for row_ind in range(row_amount):
                row_data.append(st.text_input(label=f'{label}\'s c{col_ind} r{row_ind}'))
            input_data.append(row_data)
    

    return input_data


def list_slider_inputs(label,row_nums=2,col_nums=2):
    res = np.zeros(shape=(row_nums,col_nums))

    cols = st.columns(col_nums)
    for row_ind in range(row_nums):
        for col_ind,_ in enumerate(cols):
            with cols[col_ind]:
                res[row_ind,col_ind]=st.slider(f'{label},row_{row_ind},column_{col_ind}',-1.,1.,0.)
    return res