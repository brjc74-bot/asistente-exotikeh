import streamlit as st
import google.generativeai as genai
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

# 1. Configuración de la interfaz "Premium"
st.set_page_config(page_title="Asistente Exotikeh", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #1A1A1A; color: white; border: none; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Asistente de Gestión Exotikeh")
st.caption("Inteligencia Operativa para Cristalería de Lujo")

# 2. Configuración de Seguridad y Conexión
try:
    # Usamos los nombres exactos de tus Secrets
    GEN_AI_KEY = st.secrets["GEMINI_KEY"]
    PINECONE_KEY = st.secrets["PINECONE_API_KEY"]
    
    genai.configure(api_key=GEN_AI_KEY)
    pc = Pinecone(api_key=PINECONE_KEY)
    index_name = "exotibot-index" 
    
except Exception as e:
    st.error("Error en la configuración de las llaves de seguridad.")
    st.stop()

# 3. Carga de Modelos (Optimizados)
@st.cache_resource
def load_system():
    # Modelo de embeddings para tus documentos
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Conexión a tu base de datos de manuales en Pinecone
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    
    # El modelo más óptimo según tu lista de diagnóstico
    # Usamos el 2.0 Flash por su balance perfecto
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    
    return vectorstore, model

vectorstore, model = load_system()

# 4. Lógica del Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con estilo
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Consulta sobre inventario o logística..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Búsqueda de contexto en tus archivos (RAG)
            docs = vectorstore.similarity_search(prompt, k=3)
            contexto = "\n".join([doc.page_content for doc in docs])
            
            # Instrucciones precisas para el asistente
            full_prompt = f"""
            Actúa como el experto en gestión de EXOTIKEH. 
            Tu objetivo es dar respuestas precisas basándote en la información técnica de la marca.
            
            CONTEXTO DE MANUALES:
            {contexto}
            
            PREGUNTA DEL USUARIO:
            {prompt}
            
            Respuesta (en español, profesional y ejecutiva):
            """
            
            response = model.generate_content(full_prompt)
            respuesta_final = response.text
            
            st.markdown(respuesta_final)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
            
        except Exception as e:
            st.error(f"Nota: El asistente está procesando la información. Detalle: {str(e)}")

# Pie de página
st.divider()
st.caption("© 2026 EXOTIKEH - Gestión de Procesos y Diseño Premium")
