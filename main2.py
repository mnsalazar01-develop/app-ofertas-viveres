import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de la App
st.set_page_config(page_title="Control de Ofertas Pro", layout="wide", page_icon="🛒")

# 2. Conexión a Google Sheets
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🛒 Dashboard de Control de Víveres")

# 3. Función de Carga de las 6 Tablas (Todo en minúsculas)
@st.cache_data(ttl=60)
def cargar_base_datos():
    tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
    data = {}
    for t in tabs:
        try:
            df = conn.read(spreadsheet=url, worksheet=t, ttl=0)
            # Limpieza: Aseguramos que los nombres de columnas estén en minúsculas y sin espacios
            df.columns = [c.lower().strip() for c in df.columns]
            data[t] = df
        except:
            continue
    return data

db = cargar_base_datos()

# 4. Interfaz Principal
if "productos" in db and not db["productos"].empty:
    menu = ["📊 Ofertas del Día", "📦 Catálogo", "🏪 Sucursales"]
    choice = st.sidebar.selectbox("Menú de Navegación", menu)

    if choice == "📊 Ofertas del Día":
        st.subheader("🚀 Mejores Descuentos Encontrados")
        
        if "ofertas" in db and not db["ofertas"].empty:
            try:
                # Cruce maestro de tablas usando id_producto e id_sucursal
                resumen = pd.merge(db["ofertas"], db["productos"], on="id_producto")
                resumen = pd.merge(resumen, db["sucursales"], on="id_sucursal")
                resumen = pd.merge(resumen, db["supermercados"], on="id_super")
                
                # Cálculo de ahorro (si existe precio_base en la tabla de ofertas o precios_sucursal)
                # Mostramos la información de forma estética
                for _, fila in resumen.iterrows():
                    with st.expander(f"📌 {fila['nombre']} - {fila['marca']}"):
                        col1, col2 = st.columns(2)
                        col1.metric("Precio Oferta", f"${fila['precio_oferta']}")
                        col2.write(f"🏢 **Tienda:** {fila['nombre_supermercado']} ({fila['nombre_sucursal']})")
                        st.caption(f"Válido hasta: {fila['fecha_fin']}")
            except Exception as e:
                st.warning("Aún faltan datos o relaciones en las tablas para mostrar el Dashboard completo.")
        else:
            st.info("No hay ofertas registradas en la pestaña 'ofertas'.")

    elif choice == "📦 Catálogo":
        st.subheader("📦 Inventario Completo")
        st.dataframe(db["productos"], use_container_width=True)

    elif choice == "🏪 Sucursales":
        st.subheader("📍 Ubicación de Tiendas")
        if "sucursales" in db:
            st.table(db["sucursales"])

else:
    st.error("No se pudo cargar la tabla 'productos'. Verifica que el nombre de la pestaña en el Excel sea exacto.")
