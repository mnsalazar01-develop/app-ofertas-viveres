import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Control Víveres Pro", layout="wide")
st.title("🛒 Dashboard de Control de Víveres")

# 1. CONEXIÓN
try:
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("❌ Revisa los Secrets en Streamlit Cloud.")
    st.stop()

# 2. CARGA POR POSICIÓN (No por nombre)
@st.cache_data(ttl=10)
def cargar_datos_primera_pestaña():
    try:
        # Al NO poner 'worksheet', Google Sheets entrega la primera pestaña por defecto
        df = conn.read(spreadsheet=url, ttl=0)
        # Normalizamos encabezados a minúsculas
        df.columns = [str(c).lower().strip() for c in df.columns]
        return df
    except Exception as e:
        return str(e)

df_principal = cargar_datos_primera_pestaña()

# 3. VERIFICACIÓN VISUAL
if isinstance(df_principal, pd.DataFrame):
    st.success("✅ ¡Conexión establecida con la primera pestaña!")
    
    # Buscador Pro
    st.subheader("📦 Buscador de Productos")
    busqueda = st.text_input("Escribe nombre, marca o categoría:")
    
    if busqueda:
        # Filtro en todas las columnas
        mask = df_principal.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        st.dataframe(df_principal[mask], use_container_width=True)
    else:
        st.dataframe(df_principal, use_container_width=True)
        
    st.info("💡 Sugerencia: Para activar el resto de las 6 tablas, asegúrate de que la primera pestaña sea 'Productos'.")

else:
    st.error(f"🚨 Error crítico de lectura: {df_principal}")
    st.info("Asegúrate de que el archivo tenga permiso de 'Cualquier persona con el enlace' como 'Lector'.")
