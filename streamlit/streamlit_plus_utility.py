import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import Callable,Self
import re
from unicodedata import normalize

@dataclass
class FileDescription:
    '''
    methods how to read a file
    ## See Also:
    execute_file_descriptions
    ## Examples:
    >>> import pandas as pd
    >>> from pyplus.streamlit.streamlit_plus_utility import FileDescription,execute_file_descriptions
    >>> 
    >>> fds : list[FileDescription]=[]
    >>> fds.append(FileDescription('^train.csv$',pd.read_csv))
    >>> fds.append(FileDescription('^codebook.csv$',pd.read_csv))
    >>> dfs = execute_file_descriptions(fds)
    '''
    file_regex_str : str
    read_method : Callable
    var_name : str|None = None
    dataframe_post_process : Callable|None = None
    read_method_kwarg : dict|None = None
    dataframe_post_process_kwarg : dict|None  = None

class FileExecutor:
    behaviors : list[FileDescription] = []

    def append_behavior(self,file_regex_str:str,read_method:Callable,post_method:Callable=None):
        if post_method is None:
            self.behaviors.append(FileDescription(file_regex_str,read_method))
        else:
            self.behaviors.append(FileDescription(file_regex_str,read_method,dataframe_post_process=post_method))
        return self.behaviors

    def execute_file_descriptions(self,show:bool=False,label:str='multifiles test')->dict[str,pd.DataFrame]:
        '''
        Accept multiple files and reads some files you want.
        ## Parameters:
        behaviors : ...
            Case that accept files.
        show : bool
            Verbose. Show if accept files.
        ## Examples:
        >>> import streamlit as st
        >>> import pandas as pd
        >>> from pyplus.streamlit.streamlit_plus_utility import FileExecutor,FileDescription
        >>> 
        >>> with st.sidebar:
        >>>     fe = FileExecutor()
        >>>     fe.behaviors.append( FileDescription('ratings.txt',pd.read_table) )
        >>>     dfs = fe.execute_file_descriptions()
        >>> 
        >>> dfs
        '''
        
        input_df={}
        multi_files=st.file_uploader(label,accept_multiple_files=True)
        for file in multi_files:
            for behavior in self.behaviors:
                if show:
                    st.write(re.compile(behavior.file_regex_str))
                    st.write(file.name)

                if re.compile(normalize("NFC",behavior.file_regex_str)).match(normalize("NFC",file.name)) is not None:
                    if behavior.var_name:
                        input_key = behavior.var_name
                    else:
                        input_key = "_".join(file.name.split(".")[:-1])

                    if show:
                        st.write(f"Assuming {file.name} is a {input_key}")
                    
                    try:
                        _temp_df = behavior.read_method(file,**behavior.read_method_kwarg)
                    except Exception as e1:
                        st.error(e1)
                        try:
                            _temp_df = behavior.read_method(file)
                        except Exception as e:
                            st.error(e)
                    
                    try:
                        input_df[input_key] = behavior.dataframe_post_process(_temp_df,**behavior.dataframe_post_process_kwarg)
                    except:
                        try:
                            input_df[input_key] = behavior.dataframe_post_process(_temp_df)
                        except Exception as e:
                            input_df[input_key] = _temp_df
                            st.error(e)

        return input_df