import streamlit as st
import google.generativeai as genai
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

# ==========================================
# 1. DISEÑO UI: TROPICAL / TIKI AESTHETIC
# ==========================================
st.set_page_config(
    page_title="Asistente Exotikeh Tiki-Bot", 
    page_icon="🌴", 
    layout="centered"
)

# CSS Personalizado: Fondo Amarillo Tropical y Estilo Tiki Premium
st.markdown("""
    <style>
    /* Fondo principal: Amarillo suave y cálido (Arena del Caribe) */
    .stApp { 
        background-color: #FFF9C4; 
        background-image: linear-gradient(180deg, #FFF9C4 0%, #FFF59D 100%);
    }
    
    /* Fuente y Contenedor */
    .main { 
        background: transparent;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Título Tiki en Naranja Quemado Intenso */
    h1 { 
        color: #E65100; 
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 4px;
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0px !important;
    }
    
    h3 { 
        color: #2E7D32; /* Verde Selva */
        text-align: center;
        font-weight: 500 !important;
        font-size: 1.2rem !important;
        margin-top: 0px !important;
        margin-bottom: 30px !important;
    }

    /* Input de Chat Estilo Premium */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 2px solid #FBC02D !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Mensajes de Usuario (Coco 🥥) */
    .stChatMessage.user {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 20px 20px 0px 20px !important;
        border: 1px solid #FFD54F !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* Mensajes del Asistente (Tiki 🗿) */
    .stChatMessage.assistant {
        background-color: #E8F5E9 !important;
        border-radius: 20px 20px 20px 0px !important;
        border: 1px solid #C8E6C9 !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

    /* Divider Tropical */
    hr { border-top: 2px dashed #E65100; opacity: 0.2; }
    
    /* Pie de página */
    .footer-text {
        color: #E65100;
        text-align: center;
        font-size: 0.9rem;
        font-style: italic;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Encabezado Visual
st.markdown("<h1>🌺 EXOTIKEH 🗿</h1>", unsafe_allow_html=True)
st.markdown("<h3>Gestión Operativa en el Paraíso</h3>", unsafe_allow_html=True)

# ==========================================
# 2. SEGURIDAD Y CONEXIÓN (Secrets)
# ==========================================
try:
    # Usando tus nombres exactos de Secrets
    GEN_AI_KEY = st.secrets["GEMINI_KEY"]
    PINECONE_KEY = st.secrets["PINECONE_API_KEY"]
    
    genai.configure(api_key=GEN_AI_KEY)
    pc = Pinecone(api_key=PINECONE_KEY)
    index_name = "exotibot-index" 
    
except Exception as e:
    st.error("¡Aloha! Parece que faltan las llaves de acceso en los Secrets de Streamlit.")
    st.stop()

# ==========================================
# 3. CARGA DE MODELOS (Basado en Diagnóstico)
# ==========================================
@st.cache_resource
def load_system():
    # Embeddings para tus documentos
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Conexión al índice de Pinecone
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    
    # El modelo más estable y funcional para tu cuenta (según tu lista)
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    return vectorstore, model

vectorstore, model = load_system()

# ==========================================
# 4. LÓGICA DEL CHAT (Ohana Spirit)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con avatares Tiki
for message in st.session_state.messages:
    avatar = "🥥" if message["role"] == "user" else "🗿"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Entrada de chat
if prompt := st.chat_input("¿Qué duda operativa tienes hoy, Ohana?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🥥"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🗿"):
        try:
            # RAG: Buscar contexto en tus manuales de cristalería
            docs = vectorstore.similarity_search(prompt, k=3)
            contexto = "\n".join([doc.page_content for doc in docs])
            
            # Prompt Personalizado (Tono Exotikeh)
            full_prompt = f"""
            Eres el experto en gestión y logística de EXOTIKEH. 
            Tu tono es profesional, premium y muy eficiente, pero con la amabilidad 
            de un resort de lujo. Trata al usuario como 'Ohana' cuando sea natural.
            
            Información de nuestros manuales:
            {contexto}
            
            Pregunta: {prompt}
            
            Respuesta ejecutiva y tropical:
            """
            
            response = model.generate_content(full_prompt)
            respuesta_texto = response.text
            
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
        except Exception as e:
            st.error(f"¡Rayos! Una ola bloqueó la señal. Intenta de nuevo en un momento. (Error: {str(e)})")

# ==========================================
# 5. PIE DE PÁGINA
# ==========================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='footer-text'>🌴 © 2026 EXOTIKEH Premium Glassware - Ohana Management System 🥥</div>", unsafe_allow_html=True)
