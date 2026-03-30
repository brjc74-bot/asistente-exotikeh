import streamlit as st
import google.generativeai as genai
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

# ==========================================
# 1. Configuración de la página y UX TIKI/TROPICAL
# ==========================================
st.set_page_config(
    page_title="Asistente Exotikeh Tiki-Bot", 
    page_icon="🌴", 
    layout="centered"
)

# Estilos CSS Personalizados para el ambiente Tiki Aesthetic
st.markdown("""
    <style>
    /* Fondo principal y tipografía */
    .main { 
        background-color: #fdf6e3; /* Crema suave tropical */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Personalización del Título y Subtítulo */
    h1 { 
        color: #d35400; /* Naranja quemado Tiki */
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0px !important;
    }
    
    h3 { 
        color: #27ae60; /* Verde esmeralda selva */
        text-align: center;
        font-weight: 400 !important;
        margin-top: 0px !important;
        font-size: 1.2rem !important;
    }

    /* Estilo para el Divider y Captions */
    hr { border-top: 2px dashed #d35400; }
    .stCaption { color: #e67e22; text-align: center; font-style: italic; }

    /* Estilo Aesthetic para el Input de Chat */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 2px solid #27ae60 !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Botón de enviar (Input) */
    .stChatInput button {
        background-color: #d35400 !important;
        color: white !important;
        border-radius: 50% !important;
    }

    /* Personalización de los Mensajes de Chat */
    .stChatMessage.user {
        background-color: #ffe0b2; /* Naranja muy suave para el usuario */
        border-radius: 20px 20px 0px 20px;
        margin-bottom: 15px;
        border: 1px solid #ffcc80;
    }
    
    .stChatMessage.assistant {
        background-color: #e8f5e9; /* Verde muy suave para el asistente */
        border-radius: 20px 20px 20px 0px;
        margin-bottom: 15px;
        border: 1px solid #c8e6c9;
    }

    /* Iconos y textos de los mensajes */
    .stChatMessage strong { color: #333; }
    .stChatMessage.assistant p { color: #1a1a1a; font-size: 1rem; }

    </style>
    """, unsafe_allow_html=True)

# Encabezado Aesthetic con Iconos
st.markdown("<h1>🌺 EXOTIKEH 🗿</h1>", unsafe_allow_html=True)
st.markdown("<h3>Tiki-Bot de Gestión Operativa</h3>", unsafe_allow_html=True)

# ==========================================
# 2. Configuración de Seguridad y Conexión
# ==========================================
try:
    GEN_AI_KEY = st.secrets["GEMINI_KEY"]
    PINECONE_KEY = st.secrets["PINECONE_API_KEY"]
    
    genai.configure(api_key=GEN_AI_KEY)
    pc = Pinecone(api_key=PINECONE_KEY)
    index_name = "exotibot-index" 
    
except KeyError as e:
    st.error(f"Falta configurar el secreto: {e}")
    st.stop()

# ==========================================
# 3. Carga de Modelos (Optimizados)
# ==========================================
@st.cache_resource
def load_system():
    # Modelo de embeddings para tus documentos
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Conexión a tu base de datos de manuales en Pinecone
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    
    # El modelo más funcional según tu diagnóstico
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    return vectorstore, model

vectorstore, model = load_system()

# ==========================================
# 4. Lógica del Chat con Personalidad Tiki
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con iconos tropicales
for message in st.session_state.messages:
    # Asignar icono tropical según el rol
    if message["role"] == "user":
        avatar_icon = "🥥"
    else:
        avatar_icon = "🗿"
        
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿Qué dudita tienes hoy, Ohana?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🥥"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🗿"):
        try:
            # Búsqueda de contexto en tus archivos (RAG)
            docs = vectorstore.similarity_search(prompt, k=3)
            contexto = "\n".join([doc.page_content for doc in docs])
            
            # Prompt para guiar el tono del asistente
            full_prompt = f"""
            Eres el experto en gestión de EXOTIKEH. Tu tono es profesional, premium, 
            eficiente pero amable y relajado (como un resort de lujo en el Caribe).
            Trata a los usuarios como 'Ohana' (familia) cuando sea apropiado.
            
            CONTEXTO DE MANUALES DE EXOTIKEH:
            {contexto}
            
            PREGUNTA DEL USUARIO:
            {prompt}
            
            Respuesta (en español y con un toque tropical elegante):
            """
            
            response = model.generate_content(full_prompt)
            respuesta_final = response.text
            
            st.markdown(respuesta_final)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
            
        except Exception as e:
            # Error amigable
            st.error(f"¡Aloha! El asistente está tomando un breve descanso tropical. Vuelve a intentarlo en unos segundos. Detalle: {str(e)}")

# ==========================================
# 5. Pie de página Tiki Aesthetic
# ==========================================
st.divider()
st.caption("🌴 © 2026 EXOTIKEH - Botcito de Procesos & Diseño Premium 🥥")
