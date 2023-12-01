import streamlit as st

def divide(old_func):
    def new_func(*parg,**kwarg):
        st.divider()
        old_func(*parg,**kwarg)
        st.divider()
    return new_func

def write_columns(*positional_data,**keyword_data):
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