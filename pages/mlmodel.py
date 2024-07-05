from menu import menu
import streamlit as st
from utils.verbose import (html_header, html_footer, mldescription_kmeans,
                        mldescription_gmm,mldescription_meanshift,
                        kmeans_output,meanshift_output,gmm_output,metricas)

st.set_page_config(
    page_title="Brain Food",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.html(html_header)
st.divider()


st.markdown(mldescription_kmeans)
st.image('gallery/output_means.png',use_column_width=True)
st.markdown(kmeans_output)

st.markdown(mldescription_meanshift)
st.markdown(meanshift_output)

st.markdown(mldescription_gmm)
st.image('gallery/output_gmm.png',use_column_width=True)
st.markdown(gmm_output)

st.markdown(metricas)

st.divider()
st.html(html_footer)

menu()