
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