import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Diagnóstico de Tablas", layout="wide")

# Conexión Segura
try:
    url_gsheet = st.secrets["connections"]["gsheets"]["spreadsheet"]
except:
    st.error("❌ No se encontró la URL en Secrets.")
    st.stop()

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔍 Diagnóstico Ultra-Chismoso de Base de Datos")

# Intentamos leer todas las tablas sin detenernos si una falla
tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
db = {}
reporte = []

st.write("### Reporte de Conexión:")

for t in tabs:
    try:
        # Intentamos leer la pestaña
        df = conn.read(spreadsheet=url_gsheet, worksheet=t)
        db[t] = df
        st.success(f"✅ Pestaña **'{t}'**: Leída correctamente ({len(df)} filas encontradas).")
    except Exception as e:
        # Si falla, nos cuenta el chisme completo del porqué
        st.error(f"❌ Pestaña **'{t}'**: FALLÓ. Revisa que se llame exactamente así en el Excel.")
        with st.expander(f"Ver detalle técnico del error en '{t}'"):
            st.code(e)

st.divider()

# Solo mostramos el menú si al menos hay datos
if len(db) > 0:
    st.info(f"Se cargaron {len(db)} de {len(tabs)} tablas.")
    tabla_sel = st.selectbox("Revisar contenido de tabla exitosa:", list(db.keys()))
    st.dataframe(db[tabla_sel])
else:
    st.warning("No se pudo cargar ninguna tabla. Revisa que el archivo de Google Sheets tenga los permisos de 'Lector' para 'Cualquier persona con el enlace'.")
