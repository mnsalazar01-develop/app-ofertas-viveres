import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Prueba de Conexión", layout="wide")

st.title("🛰️ Verificando Hoja: DB_Productos_Final")

# 1. Intentar obtener la URL de los Secrets
try:
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.success("✅ URL detectada en Secrets")
except Exception as e:
    st.error(f"❌ Error al leer Secrets: {e}")
    st.stop()

# 2. Intentar leer la pestaña 'Productos'
st.write("---")
st.write("### Intentando leer pestaña 'Productos'...")

try:
    # Leemos sin usar memoria vieja (ttl=0)
    df = conn.read(spreadsheet=url, worksheet="Productos", ttl=0)
    
    if not df.empty:
        st.balloons()
        st.success("🎉 ¡CONEXIÓN EXITOSA!")
        st.write("Aquí están los datos que la app ve en tu Excel:")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ El archivo se conectó, pero la pestaña 'Productos' parece estar vacía.")

except Exception as e:
    st.error("❌ Falló la lectura de la pestaña.")
    st.info(f"Detalle técnico: {e}")
    st.write("Consejo: Revisa que el nombre de la pestaña abajo en Excel sea exactamente 'Productos' (con P mayúscula y terminado en s).")
