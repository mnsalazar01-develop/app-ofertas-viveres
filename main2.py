iimport streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🛰️ Escáner de Pestañas Real")

url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Este comando es diferente: intenta leer los metadatos del archivo
    # Para obtener los nombres reales de las hojas
    from gspread_pandas import Spread
    # Si no tienes esa librería, usamos este truco de pandas:
    full_df = conn.read(spreadsheet=url)
    
    st.write("### 📋 Lo que Google le está enviando a la App:")
    st.info("Si aquí no aparecen tus 6 nombres, el archivo no está guardado como 'Google Sheets'.")
    
    # Intento de lectura por nombre forzado
    tabs = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_Sucursal", "Ofertas"]
    for t in tabs:
        try:
            df = conn.read(spreadsheet=url, worksheet=t, ttl=0)
            st.success(f"✅ ¡Conexión establecida con **{t}**!")
        except:
            st.error(f"❌ La pestaña **{t}** no responde. Revisa el formato del archivo.")

except Exception as e:
    st.error(f"Error técnico: {e}")
