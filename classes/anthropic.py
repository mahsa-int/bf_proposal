from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

MAX_TOKENS = 300

def analyze_clusters(cluster_data, client):
    chat = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1, anthropic_api_key=client.api_key,max_tokens=MAX_TOKENS)

    prompt = ChatPromptTemplate.from_template("""
    Analiza los siguientes datos del modelo de clustering y proporciona recomendaciones de estrategia de marketing para los 3 clusters mas relevantes. 
    Identifica la característica más distintiva. Prioriza insights accionables y específico y justificables, Limita tu respuesta a 300 tokens y 
    Usa un parrafo por cluster.

    Datos de clustering:
    {cluster_data}
    """)

    chain = prompt | chat

    result = chain.invoke({"cluster_data": cluster_data})

    return result.content
