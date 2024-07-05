import streamlit as st

def menu():
    st.sidebar.page_link("app.py", label=f"Challenge")
    st.sidebar.page_link("pages/eda.py", label=f"EDA & Processing")
    st.sidebar.page_link("pages/mlmodel.py", label=f"Clustering")
    st.sidebar.page_link("pages/code.py", label=f"Code Review")
    st.sidebar.page_link("pages/final.py", label=f"Summary")
