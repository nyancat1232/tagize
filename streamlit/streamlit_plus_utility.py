import streamlit as st
import pandas as pd
import pdfplumber as pdfp

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
    

def do_behavior_of_multiple_files(behaviors):
    """
    Example:
    behaviors=[]
    behaviors.append({'file_regex':re.compile("^file.cscv$"),'var_name':'name','dataframe_pre_process':to_df,'dataframe_post_process':df_func})
    """
    input_df={}
    st.write([behavior['file_regex']for behavior in behaviors])
    multi_files=st.file_uploader('multifiles test',accept_multiple_files=True)
    for file in multi_files:
        for behavior in behaviors:
            if behavior['file_regex'].match(file.name) is not None:
                st.write(f"Assuming {file.name} is a {behavior['var_name']}")
                try:
                    _temp_df = behavior['dataframe_pre_process'](file,**behavior['dataframe_pre_process_kwarg'])
                except:
                    _temp_df = behavior['dataframe_pre_process'](file)
                input_df[behavior['var_name']] = behavior['dataframe_post_process'](_temp_df)
    return input_df