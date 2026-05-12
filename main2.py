import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🛰️ Escaneando Pestañas Disponibles")

url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Leemos SIN especificar nombre de pestaña. 
    # Esto trae por defecto la primera que encuentre.
    df = conn.read(spreadsheet=url, ttl=0)
    
    st.success("✅ ¡CONEXIÓN ESTABLECIDA!")
    st.write("La App está leyendo la primera pestaña con estas columnas:")
    st.write(df.columns.tolist())
    st.dataframe(df.head())

except Exception as e:
    st.error(f"Error técnico: {e}")
