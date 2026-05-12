import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Detector de Pestañas", layout="wide")
st.title("🔍 Escáner de Nombres Reales")

# 1. Conexión
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. El Chismoso: Intentamos listar las pestañas
st.write("### 📜 Pestañas encontradas en tu Google Sheets:")

try:
    # Este es el comando técnico para pedir los nombres a Google
    # Si la conexión es pública, intentaremos este método alternativo
    from gspread_dataframe import get_as_dataframe
    
    # Intentamos obtener los nombres de las pestañas
    # (Nota: Algunos conectores públicos solo muestran la primera, 
    # pero este código intentará 'forzar' la visibilidad)
    
    # Listado visual para el usuario
    tabs_esperadas = ["Productos", "Categorias", "Supermercados", "Sucursales", "Precios_sucursal", "Ofertas"]
    
    for t in tabs_esperadas:
        try:
            # Si logra leer aunque sea una celda, la pestaña existe
            df = conn.read(spreadsheet=url, worksheet=t, ttl=0)
            st.success(f"✅ La App encontró la pestaña: **'{t}'**")
        except:
            st.error(f"❌ La App NO reconoce el nombre: **'{t}'**")
            st.write(f"  ↳ *Verifica en tu Excel si tiene espacios o tildes.*")

except Exception as e:
    st.warning("No se pudo obtener la lista automática. Revisa los mensajes de arriba.")

# 3. TRUCO FINAL: Imprimir lo que ve la primera pestaña
st.divider()
st.subheader("👀 Contenido de la Primera Pestaña Detectada:")
try:
    df_first = conn.read(spreadsheet=url, ttl=0)
    st.write(f"Columnas detectadas: `{list(df_first.columns)}`")
    st.dataframe(df_first.head(2))
except:
    st.error("Ni siquiera la primera pestaña es accesible. Revisa el link de Compartir.")
