from menu import menu
import streamlit as st
from utils.verbose import html_header, html_footer
import anthropic
import pandas as pd
from classes.anthropic import analyze_clusters

st.set_page_config(
    page_title="Brain Food",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'pensum_anthropic_review' not in st.session_state:
    st.session_state.pensum_anthropic_review = True


@st.cache_resource
def anthropic_client():
    key_claude = st.secrets["apikey_anthropic"]
    client = anthropic.Anthropic(api_key=key_claude)
    return client


@st.cache_data(show_spinner=False)
def data_anthropic(proposal):
    if proposal is not None:    
        claude_review = analyze_clusters(proposal,anthropic_client())
        return claude_review


import pandas as pd

# Decorador de caché, supongo que se usará en una aplicación Streamlit o similar
@st.cache_data(show_spinner=False)
def load_and_process_data(data):
    data = pd.read_csv(f'./app/batch/{data}.csv')
    clusters = data['Cluster'].value_counts()

    cluster_insights = {}
    analysis = []
    for cluster in clusters.index:
        cluster_data = data[data['Cluster'] == cluster]
        channel_counts = cluster_data['Channel'].value_counts(normalize=True)
        avg_bounce = cluster_data['%Bounce'].mean()
        hour_bins = cluster_data['HourBins'].value_counts(normalize=True)
        distinctive_features = {
            'Channel': channel_counts.idxmax(),
            'AvgBounce': avg_bounce,
            'PeakHours': hour_bins.idxmax(),
            'AvgEvents': cluster_data['Events'].mean(),
            'AvgPageViews': cluster_data['PageViews'].mean(),
            'TopDevice': cluster_data['DeviceType'].mode().values[0],
            'TopOS': cluster_data['OS'].mode().values[0]
        }
        
        cluster_insights[cluster] = distinctive_features

    marketing_data = []
    for cluster, features in cluster_insights.items():
        for category, value in features.items():
            # Convertir value a float si es posible y formatear a dos cifras significativas
            try:
                value_float = float(value)
                value_formatted = f"{value_float:.2g}"
            except ValueError:
                # Si no se puede convertir a float, dejar value como está
                value_formatted = value
            
            marketing_data.append((cluster, category, value_formatted))

    analysis = [f"Cluster: {cluster}, Categoría: {category}, Valor: {value}" for cluster, category, value in marketing_data]

    return str(analysis)

def main():
    st.markdown("#### Análisis de Clusters | Marketing")

    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

    if 'button_disabled' not in st.session_state:
        st.session_state.button_disabled = False

    st.selectbox(label='Selecciona un modelo',options=['kmeans','gmm','meanshift'],index=None,key='_model')

    col1, col2 = st.columns(2)


    with col1:
        if st.button("Cargar y Analizar Datos", disabled=st.session_state.button_disabled,use_container_width=True,type='primary'):
            with st.spinner("Cargando y procesando datos..."):
                data_string = load_and_process_data(st.session_state._model)
                st.session_state.data_loaded = True
                st.session_state.button_disabled = True

            with st.spinner("Analizando con Claude..."):
                analysis = data_anthropic(data_string)
                st.session_state.analysis = analysis
                st.session_state.button_disabled = True

            st.success("Análisis completado!")

    with col2:
        if st.button("Reiniciar",use_container_width=True):
            st.session_state.data_loaded = False
            st.session_state.button_disabled = False
            if 'analysis' in st.session_state:
                del st.session_state.analysis

    if st.session_state.data_loaded and 'analysis' in st.session_state:
        st.subheader("Análisis de Claude:")
        st.write(st.session_state.analysis)


st.html(html_header)
st.divider()


st.markdown("""
#### Análisis Avanzado de Clusters de Marketing con IA

Bienvenido a nuestra herramienta de análisis de clusters potenciada por inteligencia artificial. 
En el mundo actual del marketing digital, los datos son abundantes, pero los insights verdaderamente valiosos pueden ser difíciles de descubrir. 
Es aquí donde la IA generativa, específicamente **Claude 3.5 Sonnet de Anthropic**, se convierte en un aliado poderoso.

Esta herramienta combina técnicas de clustering avanzadas con el análisis de IA para revelar patrones y oportunidades que podrían pasar desapercibidos en un análisis tradicional.

### Cómo utilizar esta herramienta:

1. Seleccione el modelo de clustering que desea utilizar:
   - K-means
   - GMM (Gaussian Mixture Models)
   - Mean Shift

2. Haga clic en **Analizar** para procesar los datos con el modelo seleccionado.
3. Nuestro sistema utilizará **Claude 3.5 Sonnet** para evaluar los resultados, proporcionando insights detallados y recomendaciones estratégicas basadas en los clusters identificados.

Esta integración de técnicas de machine learning y IA generativa le ofrece una perspectiva única y valiosa para optimizar sus estrategias de marketing.
Comience ahora y descubra insights que impulsarán el éxito de sus campañas.
""")

main()

st.divider()
st.html(html_footer)

menu()