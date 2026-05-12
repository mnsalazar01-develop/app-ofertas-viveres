import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Control de Ofertas Pro", layout="wide")
st.title("🛒 Control de Víveres y Ofertas")

# 1. Conexión
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. CARGA INTELIGENTE
# Vamos a intentar leer las tablas. Si falla por nombre, usaremos la primera por defecto.
@st.cache_data(ttl=60)
def cargar_datos_seguros():
    try:
        # Cargamos Productos (que ya sabemos que es la primera y sí funciona)
        df_productos = conn.read(spreadsheet=url, ttl=0)
        
        # Intentamos cargar Ofertas (asumiendo que es la pestaña llamada 'Ofertas')
        # Si da error, al menos tendremos los productos
        try:
            df_ofertas = conn.read(spreadsheet=url, worksheet="Ofertas", ttl=0)
        except:
            df_ofertas = pd.DataFrame() # Vacío si falla
            
        return df_productos, df_ofertas
    except:
        return None, None

df_p, df_o = cargar_datos_seguros()

# 3. INTERFAZ
if df_p is not None:
    st.sidebar.success("✅ Conectado al Catálogo")
    
    # Buscador usando tus nombres de columna exactos (Id_producto, nombre, marca)
    st.subheader("📦 Buscador de Productos")
    busqueda = st.text_input("Busca por nombre, marca o categoría:")
    
    if busqueda:
        # Filtrado en todas las columnas de texto
        filtro = df_p.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        df_filtrado = df_p[filtro]
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.dataframe(df_p, use_container_width=True)
        
    if df_o.empty:
        st.info("💡 Para ver las ofertas, asegúrate de crear la pestaña 'Ofertas' en tu Google Sheets.")
else:
    st.error("No se pudieron cargar los datos. Revisa la conexión.")
