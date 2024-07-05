from menu import menu
import streamlit as st
import pandas as pd
import missingno as msno
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from classes.pandas_api import APIPandas
import io
from utils.verbose import html_header, html_footer
import json



st.set_page_config(
    page_title="Brain Food",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'categories' not in st.session_state:
    st.session_state.categories = ['Channel','Browser','DeviceType','OS','HourBins']


@st.cache_data(show_spinner=False)
def loaded_data():
    rename = {
            'fullVisitorId':'UserId',
            'device.operatingSystem':'OS',
            'device.browser':'Browser',
            'device.deviceCategory':'DeviceType',
            'channelGrouping':'Channel',
            'weekend_prop':'%Weekend',
            'device.isMobile':'isMobile',
            'totals.hits':'Events',
            'totals.pageviews':'PageViews',
            'bounce_prop':'%Bounce',
            'trafficSource.medium':'Source'
            }

    dataset = pd.read_csv('./data_customers.csv')
    dataset = dataset.rename(columns=rename)
    dataflow = APIPandas(dataset)

    return dataflow

dataflow = loaded_data()


st.html(html_header)
st.divider()


import streamlit as st

st.subheader("Análisis Exploratorio de Datos (EDA) General")
st.write("Realizamos un análisis exploratorio para comprender la naturaleza de los datos, identificar patrones relevantes y detectar posibles problemas de calidad que podrían afectar el análisis posterior y la construcción de modelos.")

with st.expander("Tipos de Datos y Optimización (Haz clic)"):
    st.write("""
    - Las variables categóricas fueron convertidas a tipo `category` para optimizar el rendimiento y reducir el consumo de memoria.
    - El tamaño del dataset (685.2 KB) es adecuado para el procesamiento y análisis eficiente.
    - Se observa un equilibrio entre variables categóricas y numéricas, lo que sugiere un conjunto de datos diverso y potencialmente informativo para la segmentación.
    """)

    def df_info_to_json(df):
        dtypes_dict = df.dtypes.astype(str).to_dict()
        dtypes_json = json.dumps(dtypes_dict, indent=2)

        # Memory Usage
        memory_dict = df.memory_usage(deep=True).to_dict()
        memory_json = json.dumps({k: f"{v/1024:.2f} KB" for k, v in memory_dict.items()}, indent=2)

        return dtypes_json, memory_json


    dtypes_json, memory_json = df_info_to_json(dataflow.data)
    col1, col2 = st.columns(2)

    with col1:
        st.success("Column Types")
        st.json(dtypes_json)

    with col2:
        st.success("Memory Usage")
        st.json(memory_json)
            

with st.expander("Distribuciones y Tendencias (Haz clic)"):
    st.write("""
    - Las variables `%Weekend` y `%Bounce` presentan distribuciones sesgadas a la izquierda, con una mayor concentración de valores bajos. Esto indica que la mayoría de las sesiones ocurren durante los días de semana y tienen una baja tasa de rebote.
    """)

    st.dataframe(dataflow.data.describe(include=float).map('{:.2f}'.format),use_container_width=True)

with st.expander("Consideraciones (Haz clic)"):
    st.write("""
    Basándonos en los hallazgos del EDA, se proponen las siguientes consideraciones y pasos a seguir:
    *   **Exclusión de la variable `User Id`:** Dada su alta cardinalidad, esta variable no será incluida en el modelo de segmentación.
    *   **Optimización del tipo de datos:** Se evaluará la viabilidad de convertir las variables numéricas de tipo `float64` a `float16` para reducir el consumo de memoria sin afectar significativamente la precisión del modelo.
    *   **Implementación de un batch endpoint:** Se explorará la posibilidad de implementar un batch endpoint para proporcionar al cliente actualizaciones periódicas de las predicciones del modelo de segmentación.
    """)


st.divider()

st.subheader("Categorización de la Hora para Análisis Probabilístico")
st.write("La hora del día es un parámetro de segmentación crucial para comprender el comportamiento de los usuarios. Para aprovechar al máximo esta información, realizaremos un análisis exhaustivo de la hora, tanto desde una perspectiva categórica como probabilística.")

with st.expander("Categorización y Codificación (Haz clic)"):
    st.write("""
    *   La hora será categorizada en intervalos (bins) para facilitar su análisis y uso en modelos de segmentación.
    *   Se aplicará un One-Hot Encoder para transformar las categorías de hora en variables binarias, adecuadas para su inclusión en modelos de aprendizaje automático.
    """)

with st.expander("Análisis Probabilístico (Haz clic)"):
    st.write("""
    *   Utilizaremos Kernel Density Estimation (KDE) para estimar la distribución de probabilidad de la hora en diferentes categorías (canal, navegador, intervalo de hora, etc.).
    *   Esto nos permitirá identificar patrones y tendencias más sutiles que un simple análisis de frecuencias.
    """)
    
    def oveall_kdehour():
        fig = dataflow.hourkde_overall(st.session_state.overall_kdehour_value)
        oveall_kdehour_container.pyplot(fig)

    st.selectbox(
        label='Categorías Dinamicas | Seleccionalas',
        index=0,
        options=st.session_state.categories,
        on_change=oveall_kdehour,
        key='overall_kdehour_value'
    )

    oveall_kdehour_container = st.empty()
    oveall_kdehour()

with st.expander("Visualización Interactiva (Haz clic)"):
    st.write("""
    *   Se proporcionará una visualización interactiva en Streamlit que permita al usuario seleccionar la categoría de interés y observar la distribución de probabilidad de la hora correspondiente.
    *   Esto facilitará la exploración de los datos y la identificación de insights relevantes para cada categoría.
    """)

    def single_kdehour():
        fig = dataflow.single_hourkde(st.session_state.single_kdehour_value)
        single_kdehour_container.pyplot(fig)

    st.selectbox(
        label='Categorías Dinamicas | Seleccionalas',
        index=0,
        options=st.session_state.categories,
        on_change=single_kdehour,
        key='single_kdehour_value'
    )

    single_kdehour_container = st.empty()
    single_kdehour()


with st.expander("Consideraciones (Haz clic)"):
    st.write("""
    *   La hora, categorizada y analizada probabilísticamente, ofrece una visión más profunda del comportamiento de los usuarios que puede ser utilizada para personalizar estrategias de marketing y optimizar la experiencia del usuario.
    *   Los insights obtenidos del análisis probabilístico de la hora pueden guiar la creación de campañas de marketing dirigidas y la implementación de acciones específicas en momentos clave del día.
    *   La visualización interactiva permite explorar los datos de manera flexible y descubrir patrones relevantes para diferentes categorías de usuarios.
    """)

st.divider()

st.subheader("Manejo de Valores Nulos")
st.write("La presencia de valores nulos en los datos puede afectar significativamente la calidad del análisis y la precisión de los modelos. En este caso, la variable `trafficSource.medium` presenta valores ausentes que requieren una atención especial.")

with st.expander("Detalles del Manejo de Valores Nulos (Haz clic)"):
    st.write("""
    1. Identificación de Valores Nulos: La columna trafficSource.medium contiene el valor "(none)", el cual ha sido mapeado como valor nulo para su correcto tratamiento.
    2. **Patrón de Ausencia No Aleatoria (MNAR):** El análisis visual con `missingno.matrix` revela un patrón de ausencia no aleatoria (MNAR) en los valores nulos de `trafficSource.medium`. Estos valores se concentran principalmente en el canal "Direct".
    3. **Tratamiento del Canal "Direct":** El canal "Direct" cuenta con 1850 muestras y representa una fuente de tráfico significativa. Los valores nulos en este canal podrían deberse a campañas offline exitosas o a referidos no mapeados en Google Analytics. Dada su relevancia, se ha decidido conservar el canal "Direct" como una categoría válida y no imputar los valores faltantes.
    **Justificación:** La imputación de valores en este caso podría introducir sesgos y distorsionar el análisis. Al mantener el canal "Direct" como una categoría independiente, se preserva la información original y se evita la pérdida de datos potencialmente valiosos.
    """)

    def chart_null():
        fig = dataflow.null_chart()
        chart_null_container.pyplot(fig)

    chart_null_container = st.empty()
    chart_null()


with st.expander("Consideraciones (Haz clic)"):
    st.write("""
    - El manejo cuidadoso de los valores nulos en la variable trafficSource.medium, en particular la decisión de conservar el canal "Direct" como una categoría válida, garantiza la integridad de los datos y permite un análisis más preciso y confiable del comportamiento de los usuarios.
    - He mantenido el contenido que proporcionaste, pero he mejorado la redacción para que sea más clara, concisa y profesional. Además, he utilizado st.expander para crear una sección plegable que permita al lector acceder a los detalles del manejo de valores nulos si así lo desea.
    """)


st.divider()

st.subheader("Entendimiento de la Proporción de Tráfico en Fines de Semana (Weekend Proportion)")
st.write("Las transacciones durante los fines de semana pueden ser generadas por usuarios con mayor tiempo libre. Identificar cómo mejorar el tráfico en estos periodos es fundamental para optimizar las estrategias de marketing y aumentar las conversiones. A continuación, evaluamos la distribución del tráfico entre días de semana y fines de semana para responder a la pregunta clave: ¿Existen diferencias notables en el tráfico y el comportamiento de los usuarios durante los fines de semana?")

with st.expander("Consideraciones (Haz clic)"):

    def weekend_rate():
        fig = dataflow.weekend_weekday_rate(cat_col=st.session_state.weekend_rate_value,num_col='%Weekend')
        weekend_rate_container.pyplot(fig)

    st.selectbox(
        label='Categorías Dinamicas | Seleccionalas',
        index=0,
        options=st.session_state.categories,
        on_change=weekend_rate,
        key='weekend_rate_value'
    )

    weekend_rate_container = st.empty()
    weekend_rate()

    st.write("""
    1. Oportunidad en usuarios de iOS: Los usuarios de iOS, que representan el 5.19% de la muestra, generan aproximadamente el 27% del tráfico durante los fines de semana. Esto sugiere una oportunidad para incrementar el tráfico en dispositivos Apple, posiblemente a través de campañas dirigidas a este segmento específico.
    2. **Relevancia de Safari:** Safari y Safari In-App son los navegadores preferidos por los usuarios durante los fines de semana, representando el 7.30% de la muestra. Analizar la experiencia de usuario (UX) ofrecida por Safari podría proporcionar insights para mejorar el tráfico en fines de semana en general.
    3. **Potencial en dispositivos móviles:** Aunque el tráfico de escritorio es mayor, se recomienda intensificar las campañas en dispositivos móviles (tablets y smartphones) durante los fines de semana, utilizando notificaciones push o SMS, para aprovechar el mayor tiempo libre de los usuarios.
    4. **Optimización para dispositivos móviles:** El bajo tráfico en dispositivos móviles sugiere la necesidad de mejorar el diseño responsive del sitio web para garantizar una experiencia óptima en pantallas más pequeñas.
    5. **Oportunidad en canales de pago:** Aunque los canales CPC y CPM generan solo el 7.5% del tráfico, se sugiere aumentar los esfuerzos en estos canales durante los fines de semana, donde podría haber un mercado potencialmente más amplio. Esto se puede hacer sin descuidar los canales orgánicos y de referidos, que cubren más del 85% de los usuarios.
    6. **Importancia de la hora:** La hora del día también influye en el comportamiento de los usuarios durante los fines de semana. Las horas de la mañana parecen ser momentos de mayor tiempo libre, lo que podría ser aprovechado para campañas específicas.
    """)



st.divider()

st.subheader("Análisis de Contribución al Porcentaje de Rebote (%Bounce Rate)")
st.write("El análisis de contribución al porcentaje de rebote (%Bounce Rate) nos permite descomponer esta métrica clave en función de diferentes variables categóricas. Esto nos ayuda a entender qué factores contribuyen más al rebote de los usuarios y a identificar áreas de mejora en la experiencia del sitio web.")

with st.expander("Consideraciones y Conclusiones (Haz clic)"):
    st.write("""
    1. Alto rebote en usuarios de escritorio referidos: El 99% del 4% aproximado de usuarios de escritorio que llegaron por canales de referencia rebotaron. Es crucial analizar en detalle cuáles fueron estos referidos y evaluar su calidad para tomar medidas correctivas.
    2. **Oportunidad de mejora en todos los canales:** Se recomienda establecer un Objetivo Clave y Resultados Clave (OKR) para reducir la tasa de rebote del 4% al 2% en cada canal. Esto podría aumentar significativamente la retención de usuarios y mejorar la experiencia general del sitio web.
    """)

with st.expander("Visualizaciones (Haz clic)"):
    st.write("Aquí se incluirán los gráficos interactivos que muestran la descomposición del porcentaje de rebote por diferentes variables categóricas, como canal, dispositivo, navegador, etc. Esto permitirá al usuario explorar los datos y comprender mejor las contribuciones de cada factor al rebote.")

    def barplot_chart():
        fig = dataflow.barplot(yaxis=st.session_state.barplot_value,xaxis='DeviceType',metric='%Bounce',aggr='sum')
        barplot_container.plotly_chart(fig)

    st.selectbox(
        label='Categorías Dinamicas | Seleccionalas',
        index=0,
        options=['Channel','Browser','OS','HourBins'],
        on_change=barplot_chart,
        key='barplot_value'
    )

    barplot_container = st.empty()
    barplot_chart()    

with st.expander("Consideraciones (Haz clic)"):
    st.write("""
    El análisis de contribución al porcentaje de rebote revela insights valiosos sobre los factores que afectan la retención de usuarios en el sitio web. Al identificar las áreas problemáticas y establecer objetivos claros de mejora, la empresa puede tomar medidas específicas para optimizar la experiencia del usuario y reducir el rebote en todos los canales.
    """)

st.divider()
st.html(html_footer)

menu()