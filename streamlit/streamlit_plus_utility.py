import streamlit as st
import pandas as pd
import pdfplumber as pdfp
from dataclasses import dataclass
from typing import Callable,Dict,Any,List,Optional
import re
from unicodedata import normalize

def from_csv_to_dataframe(label,**dataframe_keywords)->pd.DataFrame:
    """Read a csv file using a ßstrealit uploader

    Args:
        label (str): texts to show.

    Returns:
        DataFrame: A dataframe
    """
    if file := st.file_uploader(label=label,type="csv"):
        return pd.read_csv(filepath_or_buffer=file,**dataframe_keywords)


def from_pdf_to_dataframe(label,number=0,**dataframe_keywords)->pd.DataFrame:
    if file := st.file_uploader(label=label,type="pdf"):
        #df = tb.read_pdf(file)[number]
        with pdfp.open(file) as pdf:
            lis_ = pdf.pages[0].extract_table()
        return pd.DataFrame(lis_,**dataframe_keywords)

def from_txt_to_dataframe(label,preprocess_function,**dataframe_keywords)->pd.DataFrame:
    if text := st.text_area(label=label):
        txt_pre = preprocess_function(text)
        df = pd.DataFrame(txt_pre,**dataframe_keywords)
        return df.set_axis(df.loc[0],axis=1).drop(labels=[0],axis=0)

def from_xls_to_dataframe(label,**dataframe_keywords)->pd.DataFrame:
    if file := st.file_uploader(label=label,type='xls'):
        return pd.read_excel(file,engine="xlrd",**dataframe_keywords)
    
def from_parquet_to_dataframe(label,**dataframe_keywords)->pd.DataFrame:
    """Read a parquet file using a ßstrealit uploader

    Args:
        label (str): texts to show.

    Returns:
        DataFrame: A dataframe
    """
    if file := st.file_uploader(label=label,type="parquet"):
        return pd.read_parquet(path=file,**dataframe_keywords)

@dataclass
class FileDescription:
    file_regex_str : str
    dataframe_read_method : Callable
    var_name : Optional[str] = None
    dataframe_post_process : Optional[Callable] = None
    dataframe_read_method_kwarg : Optional[Dict[Any,Any]] = None
    dataframe_post_process_kwarg : Optional[Dict[Any,Any]]  = None


def execute_file_descriptions(behaviors : List[FileDescription],show:bool=False)->Dict[str,pd.DataFrame]:
    '''
    Accept multiple files and reads some files you want.
    ## Parameters:
    behaviors : Case that accept files.
    show : Verbose. Show if accept files.
    ## Examples:
    ??
    '''
    input_df={}
    multi_files=st.file_uploader('multifiles test',accept_multiple_files=True)
    for file in multi_files:
        for behavior in behaviors:
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
                    _temp_df = behavior.dataframe_read_method(file,**behavior.dataframe_read_method_kwarg)
                except:
                    _temp_df = behavior.dataframe_read_method(file)
                
                try:
                    input_df[input_key] = behavior.dataframe_post_process(_temp_df,**behavior.dataframe_post_process_kwarg)
                except:
                    try:
                        input_df[input_key] = behavior.dataframe_post_process(_temp_df)
                    except:
                        input_df[input_key] = _temp_df

    return input_df