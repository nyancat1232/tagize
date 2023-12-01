import streamlit as st
import pandas as pd
import tabula as tb

def from_csv_to_dataframe(label,**dataframe_keywords)->pd.DataFrame:
    """Read a csv file using a ßstrealit uploader

    Args:
        label (str): texts to show.

    Returns:
        DataFrame: A dataframe
    """
    if file := st.file_uploader(label=label,type="csv"):
        return pd.read_csv(filepath_or_buffer=file,**dataframe_keywords)


def from_pdf_to_dataframe(label,number=0)->pd.DataFrame:
    if file := st.file_uploader(label=label,type="pdf"):
        return tb.read_pdf(file)[number]

def from_txt_to_dataframe(label,preprocess_function)->pd.DataFrame:
    if text := st.text_area(label=label):
        return preprocess_function(text)

def from_xlsx_to_dataframe(label)->pd.DataFrame:
    if file := st.file_uploader(label=label):
        return pd.read_excel(file)