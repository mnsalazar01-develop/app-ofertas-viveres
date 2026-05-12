import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Diagnóstico de Pestañas", layout="wide")
st.title("🔍 Diagnóstico de nombres de Excel")

# Conexión
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. TRUCO PARA VER LOS NOMBRES REALES
try:
    # Leemos la primera hoja sin especificar nombre para abrir la conexión
    df_inicial = conn.read(spreadsheet=url, ttl=0)
    
    # Intentamos obtener los nombres de todas las pestañas disponibles
    # Nota: st_gsheets a veces no da los nombres de hojas directamente, 
    # así que vamos a intentar leerlas por fuerza bruta.
    
    tabs_a_probar = ["Productos", "Categorias", "Supermercados", "Sucursales", "Precios_sucursal", "Ofertas"]
    
    st.write("### 📂 Reporte de lectura:")
    
    for t in tabs_a_probar:
        try:
            # Intentamos leer con .strip() por si hay espacios
            df = conn.read(spreadsheet=url, worksheet=t.strip(), ttl=0)
            st.success(f"✅ La pestaña **'{t}'** se leyó correctamente.")
            st.dataframe(df.head(2)) # Mostramos un poquito de datos
        except Exception as e:
            st.error(f"❌ La pestaña **'{t}'** NO se encuentra o está mal escrita.")
            st.info(f"Sugerencia: Verifica que en Excel no diga '{t} ' (con espacio) o '{t.lower()}'.")

except Exception as e:
    st.error(f"Error de conexión general: {e}")

if st.button("🔄 Limpiar memoria y reintentar"):
    st.cache_data.clear()
    st.rerun()
