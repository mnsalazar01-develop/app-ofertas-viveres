import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🛰️ Buscando Señal de Google Sheets")

# Conectamos
try:
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Este comando le pide a Google que nos diga qué hojas existen
    # SIN intentar leer los datos todavía
    df_prueba = conn.read(spreadsheet=url, ttl=0)
    
    st.success("✅ ¡CONECTADO AL ARCHIVO!")
    st.write("Esto es lo que la app ve dentro de tu archivo:")
    st.write(df_prueba.columns.tolist()) # Aquí deberían salir tus 6 tablas

except Exception as e:
    st.error("❌ FALLA TOTAL DE CONEXIÓN")
    st.write("Detalle del error:", e)
    st.info("Revisa que la URL en Secrets sea la correcta y que el archivo sea público.")
