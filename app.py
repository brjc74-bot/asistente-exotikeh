import streamlit as st
import google.generativeai as genai
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

# 1. Configuración de la página y Estética "Premium"
st.set_page_config(page_title="Asistente Exotikeh", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Asistente de Gestión Exotikeh")
st.subheader("Consultoría de Inventario y Operaciones")

# 2. Configuración de Seguridad (Secrets)
try:
    GEN_AI_KEY = st.secrets["GEMINI_KEY"]
    PINECONE_KEY = st.secrets["PINECONE_API_KEY"]
    
    # Configurar Google AI
    genai.configure(api_key=GEN_AI_KEY)
    
    # Configurar Pinecone
    pc = Pinecone(api_key=PINECONE_KEY)
    index_name = "exotibot-index" # Tu nombre de índice
    
except KeyError as e:
    st.error(f"Falta configurar el secreto: {e}")
    st.stop()

# 3. Inicializar Modelos de Inteligencia
@st.cache_resource
def load_models():
    # Embeddings para buscar en tus documentos de Exotikeh
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Conexión al índice de Pinecone
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    
    # Selección de cerebro (Gemini) con respaldo para evitar el error "NotFound"
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Prueba rápida para ver si el modelo responde
        model.generate_content("test") 
    except Exception:
        try:
            model = genai.GenerativeModel('gemini-pro')
        except Exception:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            
    return vectorstore, model

vectorstore, model = load_models()

# 4. Interfaz de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte con Exotikeh?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # A. Buscar información relevante en tus documentos (RAG)
            docs = vectorstore.similarity_search(prompt, k=3)
            contexto = "\n".join([doc.page_content for doc in docs])
            
            # B. Construir el Prompt para el Asistente
            full_prompt = f"""
            Eres el Asistente de Gestión de EXOTIKEH. Tu tono es profesional, premium y eficiente.
            Usa el siguiente contexto de nuestros manuales para responder:
            ---
            CONTEXTO: {contexto}
            ---
            PREGUNTA: {prompt}
            
            Si la información no está en el contexto, usa tu conocimiento general para ayudar 
            mencionando que es una sugerencia externa.
            """
            
            # C. Generar respuesta
            response = model.generate_content(full_prompt)
            respuesta_texto = response.text
            
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
        except Exception as e:
            st.error(f"Hubo un detalle técnico: {str(e)}")
            st.info("Tip: Verifica que tu API Key de Gemini tenga permisos en AI Studio.")

# Pie de página aesthetic
st.divider()
st.caption("Exotikeh Premium Glassware - Gestión Inteligente 2026")
