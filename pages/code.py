from menu import menu
import streamlit as st
from utils.verbose import html_header, html_footer,code_review

st.set_page_config(
    page_title="Brain Food",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.html(html_header)
st.divider()

st.subheader('Estructura del Proyecto')

st.markdown(code_review)

st.subheader('Estructura del Código')

st.code("""
├── app.py                   # Aplicación principal de Streamlit
├── Dockerfile               # Configuración para despliegue en Docker
├── main.ipynb               # Notebook principal con análisis exploratorio y modelado
├── menu.py                  # Configuración del menú de la aplicación Streamlit
├── models_notebook.ipynb    # Notebook auxiliar para experimentación con modelos
├── README.md                # Descripción del proyecto y cómo ejecutarloen FastAPI
├── requirements.txt         # Dependencias del proyecto

├── .streamlit/             # Configuración de Streamlit
│   └── config.toml         # Archivo de configuración

├── app/                    # Módulo de la aplicación Streamlit
│   ├── server.py           # Lógica del servidor
│   └── batch/               # Resultados de clustering por lotes
│       ├── gmm.csv
│       ├── kmeans.csv
│       ├── meanshift.csv

├── classes/                # Clases auxiliares
│   ├── pandas_api.py

├── models/                 # Modelos entrenados
│   ├── gmm_model.joblib
│   ├── kmeans_model.joblib
│   ├── meanshift_model.joblib
│   ├── preprocessor.joblib
│   ├── selector.joblib

├── pages/                  
│   ├── codigo.py           # Página para mostrar el código
│   ├── eda.py              # Página de análisis exploratorio de datos
│   ├── final.py            # Página con las conclusiones finales
│   ├── mlmodel.py          # Página de selección y entrenamiento de modelos

└── utils/                   # Funciones de utilidad
    ├── transform_data.py
    ├── verbose.py
""")

st.divider()
st.html(html_footer)

menu()