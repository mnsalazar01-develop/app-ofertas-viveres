import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Control de Ofertas", layout="wide")
st.title("🛒 Control de Víveres y Ofertas")

# 1. Conexión
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. ESCÁNER AUTOMÁTICO (Para no fallar con los nombres)
try:
    # Leemos la primera hoja para activar la conexión
    df_inicial = conn.read(spreadsheet=url, ttl=0)
    
    st.sidebar.write("### 📂 Pestañas Detectadas")
    
    # Intentamos cargar las 6 tablas una por una
    # IMPORTANTE: Revisa que en el Excel las pestañas se llamen así
    tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
    db = {}

    for t in tabs:
        try:
            # El truco: Limpiamos el nombre de cualquier espacio
            df = conn.read(spreadsheet=url, worksheet=t.strip(), ttl=0)
            if not df.empty:
                db[t] = df
                st.sidebar.success(f"✅ {t}")
        except:
            st.sidebar.error(f"❌ {t}")

    # 3. MOSTRAR DATOS (Si Productos funciona)
    if "Productos" in db:
        st.subheader("📦 Catálogo de Productos")
        st.dataframe(db["Productos"], use_container_width=True)
    else:
        st.warning("⚠️ La pestaña 'Productos' no se reconoce.")
        st.info("Asegúrate de que en el Excel la pestaña de abajo se llame exactamente 'Productos'")

except Exception as e:
    st.error(f"Error de conexión: {e}")
