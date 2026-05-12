import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Control de Ofertas Viveres", layout="wide")

# Conexión establecida
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🛒 Control de Víveres y Ofertas")

# Lista de pestañas corregida
tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
db = {}

# Cargador chismoso
st.sidebar.write("### 📂 Estado de Base de Datos")
for t in tabs:
    try:
        df = conn.read(spreadsheet=url, worksheet=t, ttl=0)
        db[t] = df
        st.sidebar.success(f"✅ {t}")
    except:
        st.sidebar.error(f"❌ {t}")

# Si Productos cargó (que ya vimos que sí), mostramos el buscador
if "Productos" in db:
    st.subheader("📦 Buscador de Víveres")
    # Usamos tus nombres de columna: Id_producto, nombre, marca...
    df_p = db["Productos"]
    busqueda = st.text_input("Busca por nombre o marca:")
    
    if busqueda:
        # Filtro inteligente
        resultado = df_p[df_p['nombre'].str.contains(busqueda, case=False, na=False) | 
                         df_p['marca'].str.contains(busqueda, case=False, na=False)]
        st.dataframe(resultado, use_container_width=True)
    else:
        st.dataframe(df_p, use_container_width=True)
else:
    st.warning("Asegúrate de que la pestaña se llame 'Productos' en el Excel.")
