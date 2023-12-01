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

def from_xlsx_to_dataframe(label,**dataframe_keywords)->pd.DataFrame:
    if file := st.file_uploader(label=label):
        return pd.read_excel(file,**dataframe_keywords)
    
def from_parquet_to_dataframe(label,**dataframe_keywords)->pd.DataFrame:
    """Read a parquet file using a ßstrealit uploader

    Args:
        label (str): texts to show.

    Returns:
        DataFrame: A dataframe
    """
    if file := st.file_uploader(label=label,type="parquet"):
        return pd.read_parquet(path=file,**dataframe_keywords)