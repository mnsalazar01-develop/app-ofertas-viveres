import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Escáner Pro", layout="wide")
st.title("🔍 Escáner de Pestañas y Campos")

# 1. Conexión
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Lista de lo que queremos encontrar
esperados = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_sucursal", "Ofertas"]

st.write("### 📜 Resultado del Análisis Lado a Lado")

# 3. Intentamos leer las pestañas una por una
resultados = []

for nombre in esperados:
    try:
        # Intentamos leer la pestaña
        df = conn.read(spreadsheet=url, worksheet=nombre, ttl=0)
        
        # Si llega aquí, es que la encontró
        columnas = ", ".join(df.columns.tolist()[:3]) # Vemos las primeras 3 columnas
        resultados.append({
            "Pestaña Buscada": nombre,
            "Estado": "✅ ENCONTRADA",
            "Columnas que ve la App": columnas
        })
    except Exception as e:
        # Si falla, tratamos de adivinar por qué
        error_msg = str(e)
        estado = "❌ NO ENCONTRADA"
        if "400" in error_msg:
            sugerencia = "Nombre mal escrito o pestaña vacía"
        else:
            sugerencia = "Error de conexión"
            
        resultados.append({
            "Pestaña Buscada": nombre,
            "Estado": estado,
            "Columnas que ve la App": sugerencia
        })

# Mostrar tabla visual
st.table(pd.DataFrame(resultados))

# 4. TRUCO FINAL: ¿Qué hay en la PRIMERA pestaña que aparezca?
st.divider()
st.subheader("👀 Contenido de la primera pestaña que detecta Google:")
try:
    df_first = conn.read(spreadsheet=url, ttl=0)
    st.write(f"La App está leyendo una pestaña con estas columnas: `{list(df_first.columns)}`")
    st.dataframe(df_first.head(3))
except:
    st.error("Ni siquiera se pudo leer la primera pestaña.")

if st.button("🔄 Reintentar Escaneo"):
    st.cache_data.clear()
    st.rerun()
