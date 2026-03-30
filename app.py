import streamlit as st
import os
import time
from datetime import datetime
import google.generativeai as genai
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

# --- CONFIGURACIÓN ESTÉTICA ---
st.set_page_config(page_title="Asistente Exotikeh", layout="wide")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 12px; margin-bottom: 15px; border: 1px solid #e0e6ed; }
    .time-stamp { font-size: 0.7rem; color: #95a5a6; display: block; text-align: right; }
    h1 { color: #2c3e50; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>✨ Asistente de Gestión Exotikeh</h1>", unsafe_allow_html=True)

# --- CARGA DE LLAVES SEGURAS (STREAMLIT SECRETS) ---
try:
    GENAI_KEY = st.secrets["GEMINI_KEY"]
    PINECONE_KEY = st.secrets["PINECONE_API_KEY"]
    genai.configure(api_key=GENAI_KEY)
except:
    st.error("Error: Configura las llaves en el panel de Streamlit.")
    st.stop()

# --- MEMORIA ANALÍTICA (PINECONE) ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = PineconeVectorStore(index_name="exotibot-index", embedding=embeddings, pinecone_api_key=PINECONE_KEY)

# --- HISTORIAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"<span class='time-stamp'>🕒 {message['time']}</span>", unsafe_allow_html=True)
        st.markdown(message["content"])

# --- INTERACCIÓN ---
if prompt := st.chat_input("Consulta técnica sobre Exotikeh..."):
    hora = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": hora})
    
    with st.chat_message("user"):
        st.markdown(f"<span class='time-stamp'>🕒 {hora}</span>", unsafe_allow_html=True)
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Búsqueda profunda (Analiza los 5 mejores fragmentos)
        docs = vector_store.similarity_search(prompt, k=5)
        contexto = "\n".join([f"[{d.metadata.get('source','Doc')}, p.{d.metadata.get('page','?')}] {d.page_content}" for d in docs])
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_prompt = f"Eres el analista senior de Exotikeh. Responde de forma técnica y profesional usando este contexto:\n{contexto}\n\nPregunta: {prompt}"
        
        response = model.generate_content(full_prompt)
        res_text = response.text
        hora_res = datetime.now().strftime("%H:%M:%S")
        
        st.markdown(f"<span class='time-stamp'>🕒 {hora_res}</span>", unsafe_allow_html=True)
        st.markdown(res_text)
        st.session_state.messages.append({"role": "assistant", "content": res_text, "time": hora_res})
