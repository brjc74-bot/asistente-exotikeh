import streamlit as st
import google.generativeai as genai

st.title("Diagnóstico de Modelos Exotikeh")

try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    st.write("### Lista de modelos disponibles para tu cuenta:")
    
    # Esta es la función que te pide el error (ListModels)
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.code(f"Nombre: {m.name}")
            
except Exception as e:
    st.error(f"Error al listar modelos: {e}")
