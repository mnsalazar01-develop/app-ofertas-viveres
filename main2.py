import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de la App
st.set_page_config(page_title="Control de Víveres Pro", layout="wide", page_icon="🛒")

# 2. Conexión Segura
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🛒 Dashboard de Control de Víveres")

# 3. Función de Carga (Pestañas en Mayúscula)
@st.cache_data(ttl=60)
def cargar_base_datos():
    # Nombres de pestañas con mayúscula inicial
    tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_sucursal", "Ofertas"]
    data = {}
    for t in tabs:
        try:
            df = conn.read(spreadsheet=url, worksheet=t, ttl=0)
            # TRUCO: Forzamos que los CAMPOS internos siempre sean minúsculas
            df.columns = [str(c).lower().strip() for c in df.columns]
            data[t] = df
        except:
            continue
    return data

db = cargar_base_datos()

# 4. Interfaz Principal
if "productos" in db and not db["productos"].empty:
    menu = ["📊 Ofertas del Día", "📦 Catálogo Completo", "🏪 Directorio de Tiendas"]
    choice = st.sidebar.selectbox("Navegación Principal", menu)

    if choice == "📊 Ofertas del Día":
        st.subheader("🚀 Análisis de Descuentos Activos")
        
        # Verificamos si tenemos lo necesario para el cruce
        if all(x in db for x in ["ofertas", "productos", "sucursales", "supermercados"]):
            try:
                # Cruce maestro usando id_producto e id_sucursal (en minúsculas)
                resumen = pd.merge(db["ofertas"], db["productos"], on="id_producto")
                resumen = pd.merge(resumen, db["sucursales"], on="id_sucursal")
                resumen = pd.merge(resumen, db["supermercados"], on="id_super")
                
                # Visualización Estética
                for _, fila in resumen.iterrows():
                    with st.container():
                        col1, col2, col3 = st.columns([2, 2, 1])
                        with col1:
                            st.markdown(f"### {fila['nombre']} ({fila['marca']})")
                            st.write(f"📏 Tamaño: {fila['tamano']} {fila['unidad']}")
                        with col2:
                            st.write(f"🏪 **{fila['nombre_supermercado']}**")
                            st.caption(f"Sucursal: {fila['nombre_sucursal']}")
                        with col3:
                            st.metric("OFERTA", f"${fila['precio_oferta']}")
                        st.divider()
            except Exception as e:
                st.warning("⚠️ Hay una inconsistencia en los IDs de las tablas. Revisa que coincidan.")
        else:
            st.info("💡 Completa las 6 pestañas en tu Excel para activar el Dashboard inteligente.")

    elif choice == "📦 Catálogo Completo":
        st.subheader("📦 Lista Maestra de Productos")
        st.dataframe(db["productos"], use_container_width=True)

    elif choice == "🏪 Directorio de Tiendas":
        st.subheader("📍 Sucursales Registradas")
        if "sucursales" in db:
            df_s = pd.merge(db["sucursales"], db["supermercados"], on="id_super")
            st.table(df_s[['nombre_supermercado', 'nombre_sucursal', 'ciudad']])

else:
    st.error("🚨 La pestaña 'Productos' no se reconoce. Revisa que el nombre empiece con Mayúscula.")
