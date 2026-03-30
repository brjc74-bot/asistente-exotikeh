# ==========================================
# 1. Configuración de la página y UX TROPICAL CÁLIDO
# ==========================================
st.set_page_config(
    page_title="Asistente Exotikeh Tiki-Bot", 
    page_icon="🌴", 
    layout="centered"
)

# Estilos CSS con Fondo Amarillo Tropical Cálido
st.markdown("""
    <style>
    /* Fondo principal: Amarillo suave pero cálido */
    .stApp { 
        background-color: #FFF9C4; 
        background-image: linear-gradient(180deg, #FFF9C4 0%, #FFF59D 100%);
    }
    
    /* Contenedor principal de la app */
    .main { 
        background: transparent;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Título Tiki en Naranja Quemado */
    h1 { 
        color: #E65100; 
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h3 { 
        color: #2E7D32; /* Verde Selva profundo */
        text-align: center;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-bottom: 20px !important;
    }

    /* Input de Chat con estilo Premium */
    .stChatInputContainer {
        border-radius: 25px !important;
        border: 2px solid #FBC02D !important; /* Borde amarillo intenso */
        background-color: #ffffff !important;
    }

    /* Estilo de Mensajes: Usuario (Coco) */
    .stChatMessage.user {
        background-color: rgba(255, 255, 255, 0.7); /* Blanco traslúcido */
        border-radius: 20px;
        border: 1px solid #FFD54F;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Estilo de Mensajes: Asistente (Tiki) */
    .stChatMessage.assistant {
        background-color: #E8F5E9; /* Verde pálido refrescante */
        border-radius: 20px;
        border: 1px solid #C8E6C9;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }

    /* Divider Tiki */
    hr { border-top: 2px solid #E65100; opacity: 0.3; }
    
    </style>
    """, unsafe_allow_html=True)

# Encabezado Tropical
st.markdown("<h1>🌺 EXOTIKEH 🗿</h1>", unsafe_allow_html=True)
st.markdown("<h3>Gestión Inteligente en el Paraíso</h3>", unsafe_allow_html=True)
