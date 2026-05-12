import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="App Ofertas Víveres", layout="wide")

# Conexión Segura
try:
    url_gsheet = st.secrets["connections"]["gsheets"]["spreadsheet"]
except:
    st.error("❌ No se encontró la URL en Secrets.")
    st.stop()

conn = st.connection("gsheets", type=GSheetsConnection)

# Carga de datos con detección de errores por pestaña
@st.cache_data(ttl=60) 
def cargar_datos():
    tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
    data = {}
    for t in tabs:
        try:
            data[t] = conn.read(spreadsheet=url_gsheet, worksheet=t)
        except Exception:
            # Si una falla, nos avisa cuál es
            st.error(f"❌ Error al leer la pestaña: '{t}'. Revisa el nombre en tu Excel.")
            return None
    return data

db = cargar_datos()

st.title("🛒 Control de Ofertas de Víveres")

if db is not None:
    st.success("✅ ¡Todas las tablas cargadas con éxito!")
    
    # Menú para revisar las tablas
    menu = ["Dashboard", "Explorador de Datos"]
    choice = st.sidebar.selectbox("Menú", menu)
    
    if choice == "Explorador de Datos":
        tabla_sel = st.selectbox("Ver tabla:", list(db.keys()))
        st.dataframe(db[tabla_sel])
