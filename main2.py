import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("🛒 Control de Ofertas - Conectado")

url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

# Lista de pestañas que DEBEN existir abajo en tu Excel
tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
db = {}

st.sidebar.write("### Estado de Tablas")

for t in tabs:
    try:
        # Intentamos leer especificando la pestaña
        df = conn.read(spreadsheet=url, worksheet=t, ttl=0)
        db[t] = df
        st.sidebar.success(f"✅ {t}")
    except:
        st.sidebar.error(f"❌ {t} (No encontrada)")

# Si Productos cargó, mostramos el catálogo
if "Productos" in db:
    st.subheader("📦 Catálogo de Productos")
    st.dataframe(db["Productos"], use_container_width=True)
else:
    st.warning("⚠️ Haz clic en las pestañas de tu Google Sheets y asegúrate de que se llamen exactamente como la lista de la izquierda.")
