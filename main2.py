import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="App Ofertas Víveres", layout="wide")

# 2. Conexión segura con Secrets
try:
    url_gsheet = st.secrets["connections"]["gsheets"]["spreadsheet"]
except:
    st.error("❌ No se encontró la URL en los Secrets de Streamlit.")
    st.stop()

conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Función de carga protegida
@st.cache_data(ttl=600)
def cargar_datos():
    tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
    data = {}
    for t in tabs:
        try:
            data[t] = conn.read(spreadsheet=url_gsheet, worksheet=t)
        except Exception:
            st.error(f"❌ Error específico en la pestaña: '{t}'. Revisa que el nombre sea igual en Excel.")
            return None
    return data

# Intentar cargar la base de datos
db = cargar_datos()

st.title("🛒 Control de Ofertas")

# 4. Verificación de la variable db antes de usarla
if db is not None:
    menu = ["Dashboard", "Explorador de Tablas"]
    choice = st.sidebar.selectbox("Menú", menu)

    if choice == "Dashboard":
        st.subheader("🚀 Ofertas Activas")
        # Aquí va tu lógica de merges...
        st.info("Tablas cargadas correctamente. Configure aquí sus cruces de datos.")

    elif choice == "Explorador de Tablas":
        st.subheader("🛠️ Verificador de Datos")
        # Aquí ya no dará NameError porque está dentro del 'if db is not None'
        tabla_sel = st.selectbox("Selecciona una tabla para revisar:", list(db.keys()))
        st.write(f"Datos actuales en: {tabla_sel}")
        st.dataframe(db[tabla_sel])
else:
    st.warning("⚠️ La aplicación está esperando que la base de datos esté disponible.")
    st.info("Revisa que los nombres de las pestañas en Excel sean: Categorias, Productos, Supermercados, Sucursales, Precios_Sucursal, Ofertas.")
