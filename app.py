from menu import menu
import streamlit as st
from utils.verbose import html_header, html_footer

st.set_page_config(
    page_title="Brain Food",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'categories' not in st.session_state:
    st.session_state.categories = ['Channel','Browser','DeviceType','OS','HourBins']



st.html(html_header)

st.divider()

st.subheader("Introducción")
st.write("""
En el entorno altamente competitivo del comercio electrónico, la personalización de las estrategias de marketing es fundamental para el éxito empresarial. Una comprensión profunda de los clientes, sus necesidades y comportamientos, permite adaptar las estrategias de marketing y optimizar la experiencia del usuario, lo que a su vez impulsa la retención de clientes y el crecimiento sostenible.
""")

st.subheader('Objetivo')

st.write("""
El objetivo principal de este proyecto es realizar un análisis exhaustivo de segmentación de clientes utilizando datos de Google Analytics. Este análisis permitirá identificar segmentos de clientes distintos en función de sus características demográficas, comportamientos de navegación, patrones de compra y otras variables relevantes. A partir de esta segmentación, se desarrollarán recomendaciones accionables para mejorar las estrategias de marketing, personalizar la experiencia del usuario y, en última instancia, aumentar la retención de clientes y el rendimiento general del negocio.
""")

with st.expander("Resultados Clave Esperados"):
    st.write("""
    1.  **Identificación de segmentos de clientes:** Se espera identificar segmentos de clientes distintos con características y comportamientos diferenciados.
    2.  **Análisis de características de los segmentos:** Se analizarán las características demográficas, comportamientos de navegación, patrones de compra y otras variables relevantes de cada segmento.
    3.  **Desarrollo de perfiles de clientes (Buyer Personas):** Se crearán perfiles detallados de los segmentos de clientes (Buyer Personas) para comprender sus necesidades, motivaciones y preferencias.
    4.  **Recomendaciones de estrategias de marketing personalizadas:** Se formularán recomendaciones específicas para adaptar las estrategias de marketing a cada segmento, incluyendo mensajes, canales y tácticas.
    5.  **Mejora de la experiencia del usuario:** Se identificarán oportunidades para optimizar la experiencia del usuario en el sitio web en función de las necesidades de cada segmento.
    6.  **Aumento de la retención de clientes:** Se espera que la implementación de estrategias de marketing personalizadas y la mejora de la experiencia del usuario contribuyan a aumentar la retención de clientes a largo plazo.
    """)

with st.expander("Preguntas Clave para Entender el Problema en Profundidad"):
    st.write("""
    Para garantizar que nuestro análisis genere el máximo valor para el cliente y aborde sus necesidades específicas, es crucial establecer una comunicación fluida y continua desde el inicio del proyecto. Esto nos permitirá comprender en profundidad sus objetivos de negocio y refinar nuestras hipótesis y enfoques a medida que avanzamos. Algunas preguntas clave que guiarán nuestras conversaciones con el cliente incluyen:
    """)

with st.expander("Objetivos de negocio"):
    st.write("""
    Estas preguntas nos permitirán conocer mejor el problema del cliente, sus expectativas y cómo medir el éxito del proyecto.

    *   **Métricas de éxito:** ¿Qué comportamiento de los usuarios en Google Analytics indicaría el éxito de una campaña de marketing? (Ej.: aumento de Page Views, disminución de la tasa de rebote, aumento en la cantidad de eventos).
    *   **ROI de campañas:** ¿Qué métricas de Google Analytics son más relevantes para evaluar el retorno de la inversión (ROI) de las campañas de marketing? (Ej.: ingresos por canal, costo por adquisición, valor de vida del cliente).
    *   **Datos adicionales:** ¿Tenemos acceso a datos demográficos, datos de CRM, encuestas a clientes? Esta información sería valiosa para enriquecer la segmentación y personalizar aún más las campañas de marketing.
    *   **Conocimiento actual de los clientes:** ¿Qué sabe la empresa sobre sus clientes actuales? ¿Cuáles son sus segmentos principales, si los hay?
    """)


with st.expander("Hipótesis (Ejemplos):"):
    st.write("""
    Plantear y validar hipótesis nos permite establecer un marco de trabajo para el análisis y guiar nuestras conclusiones. Algunos ejemplos de hipótesis que podríamos considerar son:

    *   **H0 (Nula):** No existen diferencias o patrones significativos en el comportamiento de la muestra de Google Analytics, por lo que se debe tratar los datos en conjunto como un solo segmento.
    *   **H1 (Alternativa):** Existen diferencias o patrones significativos en el comportamiento de la muestra de Google Analytics, lo que sugiere la presencia de segmentos de clientes distintos.
    """)


st.divider()
st.html(html_footer)

menu()