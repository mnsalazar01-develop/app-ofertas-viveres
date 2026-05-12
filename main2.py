import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Control Víveres Pro", layout="wide")

# 1. Conexión
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🛒 Dashboard de Control de Víveres")

# 2. Función de Carga Ultra-Flexible
@st.cache_data(ttl=10)
def cargar_db_flexible():
    # Buscamos primero qué pestañas EXISTEN realmente en tu Excel
    try:
        # Leemos el archivo completo para extraer nombres de hojas
        query = f'SELECT * FROM "Productos"' # Intento inicial
        # Para ser más seguros, leemos la lista de todas las pestañas
        # mediante un pequeño truco: leer sin worksheet trae la primera
        df_test = conn.read(spreadsheet=url, ttl=0)
        
        # Lista de lo que queremos buscar
        buscar = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_sucursal", "Ofertas"]
        data = {}
        
        for t in buscar:
            try:
                # Intentamos leer la pestaña tal cual
                df = conn.read(spreadsheet=url, worksheet=t, ttl=0)
                # Convertimos encabezados a minúsculas inmediatamente
                df.columns = [str(c).lower().strip() for c in df.columns]
                data[t.lower()] = df
                st.sidebar.success(f"✅ {t}")
            except:
                st.sidebar.error(f"❌ {t}")
                continue
        return data
    except:
        return None

db = cargar_db_flexible()

# 3. Verificación y Lógica
if db and "productos" in db:
    st.sidebar.divider()
    menu = ["📊 Ofertas", "📦 Catálogo"]
    choice = st.sidebar.radio("Navegación", menu)
    
    if choice == "📦 Catálogo":
        st.subheader("Catálogo Maestro")
        st.dataframe(db["productos"], use_container_width=True)
        
    if choice == "📊 Ofertas":
        if "ofertas" in db:
            st.subheader("Ofertas Activas")
            st.dataframe(db["ofertas"], use_container_width=True)
        else:
            st.info("Crea la pestaña 'Ofertas' para ver los descuentos.")
else:
    st.error("🚨 Sistema en espera: No se detecta la pestaña 'Productos'.")
    st.info("Acción requerida: Asegúrate de que en Google Sheets la pestaña se llame exactamente Productos y que tenga datos.")
    # Botón para forzar recarga
    if st.button("🔄 Reintentar Conexión"):
        st.cache_data.clear()
        st.rerun()
