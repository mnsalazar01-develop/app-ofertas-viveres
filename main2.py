import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Control Víveres Pro", layout="wide")

# Conexión
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🛒 Control de Víveres y Ofertas")

# BOTÓN DE RESETEO (Para limpiar la memoria de la app)
if st.sidebar.button("🔄 Actualizar Datos del Excel"):
    st.cache_data.clear()
    st.rerun()

# Lista de pestañas con Mayúscula Inicial
nombres_tabs = ["Productos", "Categorias", "Supermercados", "Sucursales", "Precios_sucursal", "Ofertas"]
db = {}

st.sidebar.write("### 📂 Estado de Tablas")

for t in nombres_tabs:
    try:
        # ttl=0 obliga a la app a NO usar memoria vieja y leer el Excel real
        df = conn.read(spreadsheet=url, worksheet=t, ttl=0)
        if not df.empty:
            # Convertimos campos a minúsculas
            df.columns = [str(c).lower().strip() for c in df.columns]
            db[t.lower()] = df
            st.sidebar.success(f"✅ {t}")
    except:
        db[t.lower()] = pd.DataFrame()
        st.sidebar.error(f"❌ {t}")

# Visualización del Catálogo
if "productos" in db and not db["productos"].empty:
    st.subheader("📦 Catálogo de Productos")
    st.dataframe(db["productos"], use_container_width=True)
else:
    st.info("Esperando datos de la pestaña 'Productos'...")
