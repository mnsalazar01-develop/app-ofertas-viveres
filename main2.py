import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Control de Víveres Pro", layout="wide")
st.title("🛒 Control de Víveres y Ofertas")

# 1. Conexión
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Función "Cazadora de Datos" (Busca por columnas, no por nombres)
@st.cache_data(ttl=10)
def cargar_datos_automaticos():
    try:
        # Leemos la primera pestaña que encuentre Google (sea cual sea su nombre)
        df_principal = conn.read(spreadsheet=url, ttl=0)
        # Normalizamos encabezados
        df_principal.columns = [str(c).lower().strip() for c in df_principal.columns]
        return df_principal
    except Exception as e:
        return f"Error de conexión: {e}"

df_datos = cargar_datos_automaticos()

# 3. INTERFAZ
if isinstance(df_datos, pd.DataFrame):
    st.success("✅ ¡Base de datos conectada!")
    
    # Imprimimos visualmente para que veas qué está leyendo el programa
    st.write(f"📊 **Pestaña detectada con las columnas:** `{list(df_datos.columns)}` seed")
    
    # Buscador Inteligente
    st.subheader("🔍 Buscador de Productos")
    busqueda = st.text_input("Escribe nombre, marca o categoría:")
    
    if busqueda:
        # Filtro que busca en todas las columnas al mismo tiempo
        mask = df_datos.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        st.dataframe(df_datos[mask], use_container_width=True)
    else:
        st.dataframe(df_datos, use_container_width=True)

    st.divider()
    st.info("💡 **TIP PRO:** Como Google está bloqueando el acceso por nombres individuales (Productos, Ofertas, etc.), la mejor opción para que tu App sea 100% funcional es poner toda la información importante en esta primera pestaña o usar una base de datos privada.")
else:
    st.error(df_datos)
