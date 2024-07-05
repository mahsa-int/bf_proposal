
html_header = """
<div style="position: relative; width: 100%; padding: 10px;">
    <div style="border-radius: 15px; overflow: hidden;">
        <img src="https://i.ibb.co/GVMsMcg/20.png" alt="Imagen de fondo" style="width: 100%; height: auto;">
    </div>
</div>
"""

html_footer = """
<div style="position: relative; width: 100%; padding: 10px;">
    <div style="border-radius: 15px; overflow: hidden;">
        <img src="https://i.ibb.co/x1HPNwG/21.png" alt="Imagen de fondo" style="width: 100%; height: auto;">
    </div>
</div>
"""

mldescription_kmeans = """
#### Metodología
:blue[_Selección de Algoritmos de Clustering_]

En la búsqueda de la segmentación óptima de clientes, se evaluaron tres algoritmos de clustering ampliamente utilizados, cada uno con ventajas específicas para el análisis de datos de marketing:

#### K-Means

- :blue[**Ventajas:**]
    - Escalabilidad para manejar grandes volúmenes de datos de Google Analytics.
- :blue[**Limitaciones:**]
    - Asume clusters esféricos, lo que puede no ser adecuado para formas complejas.
    - Sensible a la inicialización, los resultados pueden variar según la elección inicial de centroides.
"""

kmeans_output = """
#### Conclusiones | K-Means
Se determinó que 6 clusters es el número óptimo para la segmentación de clientes utilizando K-Means.
Esta elección se basa en el Silhouette Score (0.214), que indica una separación moderada entre los clusters y una cohesión interna razonable, 
y en el Índice de Calinski-Harabasz (1731), que confirma una estructura de clustering sólida. Aunque el gráfico del codo sugiere 14 clusters, 
se considera que 6 segmentos ofrecen un equilibrio entre granularidad e interpretabilidad.
"""


mldescription_meanshift = """
#### Mean Shift

- :blue[**Ventajas:**]
    - No requiere especificar el número de clusters, el algoritmo los encuentra automáticamente.
    - Flexible en cuanto a la forma de los clusters, puede identificar formas arbitrarias.
- :blue[**Limitaciones:**]
    - Computacionalmente más costoso, puede ser más lento con grandes conjuntos de datos.
"""

meanshift_output = """
#### Conclusiones | Mean Shift
El algoritmo Mean Shift identificó 6 clusters de clientes. La elección del parámetro quantile es crucial 
para determinar el ancho de banda óptimo, que controla la escala de agrupamiento. Un valor de quantile más bajo 
favorece la detección de clusters pequeños y densos, mientras que un valor más alto resulta en clusters más grandes y 
menos sensibles al ruido.
"""

mldescription_gmm = """
#### Gaussian Mixture Models (GMM)

- :blue[**Ventajas:**]
    - Modela clusters de diferentes formas y tamaños, capturando la variabilidad dentro de los segmentos de clientes.
- :blue[**Limitaciones:**]
    - Complejidad, requiere comprensión de modelos probabilísticos.
    - Sensible a la inicialización, similar a K-Means.
"""

gmm_output = """
#### Conclusiones | Gaussian Mixture Models (GMM)
El criterio de (BIC) determinó que 9 es el número óptimo de clusters 
para segmentar a los clientes, lo que indica la existencia de 9 grupos distintos con características similares. GMM asume que los clusters 
son gaussianos, lo que le permite encontrar clusters de diferentes formas y tamaños. Esta elección evita el sobreajuste, 
permitiendo un análisis detallado de cada grupo y la personalización de estrategias de marketing.
"""

metricas = """
    
#### Metricas

- **Índice de Calinski-Harabasz (CH):** Mide la relación entre la dispersión dentro de los clusters y la dispersión entre clusters. Un valor más alto indica una mejor estructura de clustering.
- **Silhouette Score (SS):** Evalúa qué tan similares son los puntos dentro de un cluster en comparación con otros clusters. Un valor más alto indica una mejor separación entre clusters.
- **Gráfico del Codo (Elbow Method):** Visualiza la inercia (suma de distancias cuadradas) en función del número de clusters. El "codo" en el gráfico sugiere un número adecuado de clusters.
"""




code_review = """
Desde la concepción del proyecto, se priorizó la creación de un modelo de segmentación de clientes que pudiera ser fácilmente desplegado en un entorno productivo. Para lograr esto, se adoptó una estructura modular y se utilizaron tecnologías clave como Scikit-learn, FastAPI, Uvicorn, Docker y Railway.

#### Estructura Modular

El código se dividió en módulos bien definidos para facilitar el mantenimiento y la escalabilidad

- `app/:` Contiene la aplicación principal de Streamlit, que proporciona una interfaz visual para interactuar con el modelo.
- `classes/:` Incluye clases auxiliares para el manejo de datos y la visualización de resultados.
- `models/:` Almacena los modelos de clustering entrenados (K-Means, Mean Shift, GMM) y otros componentes necesarios para la predicción.
- `pages/:` Define las diferentes páginas de la aplicación Streamlit, como el análisis exploratorio de datos (EDA), la selección de modelos y la visualización de resultados.
- `utils/:` Contiene funciones de utilidad para la transformación de datos y otras tareas comunes.


#### Tecnologías Clave

- **Scikit-learn**: Se utilizó para implementar los algoritmos de clustering (K-Means, Mean Shift, GMM), así como para el preprocesamiento de datos (escalado, selección de características).
- **FastAPI**: Se empleó para crear una API RESTful que expone los modelos de clustering entrenados. Esto permite que la aplicación Streamlit interactúe con los modelos de manera eficiente y que otros sistemas puedan consumir las predicciones.
- **Uvicorn**: Sirve como servidor ASGI para ejecutar la API de FastAPI.
- **Docker**: Se utilizó para empaquetar la aplicación y sus dependencias en un contenedor, lo que facilita el despliegue en diferentes entornos.
- **Railway**: Se eligió como plataforma de despliegue debido a su facilidad de uso y su capacidad para escalar automáticamente la aplicación según la demanda.

#### Metodología

- **Análisis Exploratorio de Datos (EDA):** Se realizó un análisis exhaustivo de los datos de Google Analytics para comprender su estructura, distribución y relaciones entre variables.
- **Preprocesamiento de Datos:** Se limpiaron y transformaron los datos para prepararlos para el modelado.
- **Entrenamiento de Modelos:** Se entrenaron los modelos de clustering (K-Means, Mean Shift, GMM) utilizando Scikit-learn.
- **Evaluación de Modelos:** Se evaluaron los modelos utilizando métricas como el índice de Calinski-Harabasz, el Silhouette Score y el gráfico del codo.
Selección del Modelo Óptimo: Se seleccionó el modelo y el número de clusters que mejor se ajustaron a los datos y al objetivo de negocio.
- **Creación de la API:** Se desarrolló una API RESTful con FastAPI para exponer el modelo seleccionado.
Desarrollo de la Aplicación Streamlit: Se creó la interfaz de usuario en Streamlit para interactuar con la API y visualizar los resultados.
- **Empaquetado con Docker:** Se empaquetó la aplicación y sus dependencias en un contenedor Docker.
- **Despliegue en Railway:** Se desplegó el contenedor Docker en la plataforma Railway.

"""