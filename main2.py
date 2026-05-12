import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="App Ofertas Pro", layout="wide", page_icon="🛒")

# 1. Conexión con Secrets
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🛒 Control Maestro de Víveres")

# 2. Función para cargar las 6 pestañas
@st.cache_data(ttl=60)
def cargar_todo():
    # Nombres de tus pestañas en Google Sheets (Mayúsculas)
    nombres_pestañas = ["Productos", "Categorias", "Supermercados", "Sucursales", "Precios_sucursal", "Ofertas"]
    tablas = {}
    
    for p in nombres_pestañas:
        try:
            # Leemos la pestaña
            df = conn.read(spreadsheet=url, worksheet=p, ttl=0)
            # Convertimos TODOS los campos a minúsculas automáticamente
            df.columns = [str(c).lower().strip() for c in df.columns]
            tablas[p.lower()] = df
        except:
            # Si una pestaña no existe o falla, la dejamos vacía para no romper la app
            tablas[p.lower()] = pd.DataFrame()
            
    return tablas

db = cargar_todo()

# 3. Interfaz de Usuario
if not db["productos"].empty:
    menu = ["📊 Dashboard de Ofertas", "📦 Catálogo Completo", "🏪 Tiendas y Sucursales"]
    choice = st.sidebar.selectbox("Menú Principal", menu)

    if choice == "📊 Dashboard de Ofertas":
        st.subheader("🚀 Ofertas Detectadas")
        
        # Verificamos que tengamos ofertas cargadas
        if not db["ofertas"].empty:
            try:
                # Cruce de datos inteligente
                res = pd.merge(db["ofertas"], db["productos"], on="id_producto")
                res = pd.merge(res, db["sucursales"], on="id_sucursal")
                res = pd.merge(res, db["supermercados"], on="id_super")
                
                # Mostrar en formato estético
                for _, fila in res.iterrows():
                    with st.expander(f"📍 {fila['nombre']} - {fila['marca']} (${fila['precio_oferta']})"):
                        st.write(f"🏢 **Supermercado:** {fila['nombre_supermercado']}")
                        st.write(f"🏬 **Sucursal:** {fila['nombre_sucursal']} ({fila['ciudad']})")
                        st.write(f"📅 **Vence:** {fila['fecha_fin']}")
            except:
                st.info("💡 Para ver el cruce de ofertas, asegúrate de llenar los IDs correctamente en el Excel.")
        else:
            st.info("No hay ofertas registradas en la pestaña 'Ofertas'.")

    elif choice == "📦 Catálogo Completo":
        st.subheader("📦 Lista de Productos")
        st.dataframe(db["productos"], use_container_width=True)

    elif choice == "🏪 Tiendas y Sucursales":
        st.subheader("🏪 Información de Establecimientos")
        if not db["sucursales"].empty:
            st.dataframe(db["sucursales"], use_container_width=True)

# 4. Reporte de estado en el lateral
st.sidebar.divider()
st.sidebar.write("### 📂 Estado de Tablas")
for t in ["Productos", "Categorias", "Supermercados", "Sucursales", "Precios_sucursal", "Ofertas"]:
    if not db[t.lower()].empty:
        st.sidebar.success(f"✅ {t}")
    else:
        st.sidebar.error(f"❌ {t}")
