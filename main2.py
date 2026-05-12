import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración Visual Pro
st.set_page_config(page_title="Control de Ofertas Viveres", page_icon="🛒", layout="wide")

# 2. Conexión con tu Google Sheet
# Reemplaza con tu URL real. Asegúrate de que "Cualquier persona con el enlace" sea Lector.
url_gsheet = "TU_URL_DE_GOOGLE_SHEETS_AQUÍ"
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🍎 Sistema de Control de Ofertas")
st.markdown("---")

# 3. Menú Lateral con las secciones lógicas
menu = ["📊 Dashboard de Ofertas", "📦 Catálogo de Productos", "🏪 Sucursales", "⚙️ Configuración"]
choice = st.sidebar.selectbox("Navegación", menu)

# --- CARGA DE DATOS (Las 6 Tablas) ---
#@st.cache_data(ttl=600) # Se actualiza cada 10 min
#def cargar_todas_las_tablas():
#    tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
#    data = {}
#    for t in tabs:
#        data[t] = conn.read(spreadsheet=url_gsheet, worksheet=t)
#   return data
#
#try:
#    db = cargar_todas_las_tablas()

# --- CARGA DE DATOS ---
@st.cache_data(ttl=600)
def cargar_todas_las_tablas():
    # Asegúrate de que estos nombres sean EXACTOS a tus pestañas de Excel
    tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
    data = {}
    try:
        for t in tabs:
            # Intentamos leer cada pestaña
            data[t] = conn.read(spreadsheet=url_gsheet, worksheet=t)
        return data
    except Exception as e:
        st.error(f"Error al leer las pestañas: {e}")
        return None

# Intentamos inicializar la variable db
db = cargar_todas_las_tablas()

# --- VERIFICACIÓN DE SEGURIDAD ---
if db is not None:
    # Solo si db existe, ejecutamos el resto del código
    if choice == "📊 Dashboard de Ofertas":
        # ... tu código del dashboard ...
        pass

    # El bloque de depuración ahora funcionará porque está dentro del 'if db'
    with st.expander("🛠️ Modo Depuración"):
        tabla_debug = st.selectbox("Elegir tabla:", list(db.keys()))
        st.dataframe(db[tabla_debug])
else:
    st.error("🚨 La base de datos no pudo cargarse. Revisa la URL en Secrets y los nombres de las pestañas.")


    if choice == "📊 Dashboard de Ofertas":
        st.subheader("🚀 Ofertas Activas en Tiempo Real")
        
        # Cruzamos: Ofertas + Productos + Sucursales + Supermercados
        # Usamos id_producto como eje central según acordamos
        m1 = pd.merge(db["Ofertas"], db["Productos"], on="id_producto")
        m2 = pd.merge(m1, db["Sucursales"], on="id_sucursal")
        df_final = pd.merge(m2, db["Supermercados"], on="id_super")
        
        # Filtro por ciudad (Opcional para ser más Pro)
        ciudades = df_final['ciudad'].unique()
        ciudad_sel = st.multiselect("Filtrar por Ciudad", ciudades, default=ciudades)
        
        df_filtrado = df_final[df_final['ciudad'].isin(ciudad_sel)]

        
        # Diseño de tarjetas o tabla
        for _, fila in df_filtrado.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.markdown(f"### {fila['nombre']}")
                    st.caption(f"{fila['tamano']} {fila['unidad']} | {fila['nombre_supermercado']}")
                with col2:
                    st.write(f"📍 **{fila['nombre_sucursal']}** ({fila['ciudad']})")
                    st.write(f"⏳ Vence: {fila['fecha_fin']}")
                with col3:
                    st.metric("Precio Oferta", f"${fila['precio_oferta']}", delta=f"OFERTA")
                st.divider()

    elif choice == "📦 Catálogo de Productos":
        st.subheader("📦 Inventario Global de Víveres")
        # Unir productos con sus categorías
        df_p = pd.merge(db["Productos"], db["Categorias"], on="id_cat")
        st.dataframe(df_p[['id_producto', 'nombre', 'tamano', 'unidad', 'nombre_y']], use_container_width=True)

    elif choice == "🏪 Sucursales":
        st.subheader("🏪 Ubicación de Establecimientos")
        df_s = pd.merge(db["Sucursales"], db["Supermercados"], on="id_super")
        st.table(df_s[['nombre_sucursal', 'nombre', 'ciudad']])

    elif choice == "⚙️ Configuración":
        st.info("Configuración de la conexión a Google Sheets activa.")
        if st.button("🔄 Forzar actualización de datos"):
            st.cache_data.clear()
            st.rerun()

except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.warning("Asegúrate de que los nombres de las pestañas en Google Sheets coincidan exactamente y la URL sea pública.")

# SECCIÓN DE DEPURACIÓN (Solo para revisar si las tablas cargan)
with st.expander("🛠️ Modo Depuración: Revisar tablas en Google Sheets"):
    st.write("Selecciona una tabla para ver si tiene datos:")
    tabla_debug = st.selectbox("Elegir tabla:", list(db.keys()))
    
    if tabla_debug:
        df_temp = db[tabla_debug]
        if df_temp.empty:
            st.warning(f"La tabla '{tabla_debug}' está VACÍA o no se pudo leer.")
        else:
            st.success(f"Tabla '{tabla_debug}' leída con éxito. Tiene {len(df_temp)} filas.")
            st.dataframe(df_temp) # Muestra el contenido crudo de la tabla
