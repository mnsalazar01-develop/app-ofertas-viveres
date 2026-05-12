import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🔍 Diagnóstico de Nombres de Pestañas")

url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Intentamos leer la primera pestaña disponible SIN nombre
    df_primera = conn.read(spreadsheet=url, ttl=0)
    st.success("✅ Conexión establecida con el archivo.")
    
    # 2. TRUCO MAESTRO: Vamos a imprimir los nombres de las columnas que ve
    # Si la pestaña se llama 'Productos', aquí deberían salir tus columnas
    st.write("### Columnas detectadas en la primera pestaña:")
    st.write(df_primera.columns.tolist())

    # 3. PRUEBA DE FUEGO: Vamos a intentar cargar 'Productos' forzando el formato
    st.write("---")
    st.write("### Intento de acceso directo:")
    
    try:
        # Probamos con el nombre tal cual
        test_df = conn.read(spreadsheet=url, worksheet="Productos", ttl=0)
        st.success("🎉 ¡LOGRADO! La pestaña 'Productos' fue reconocida.")
        st.dataframe(test_df.head())
    except Exception as e:
        st.error("❌ Falló el acceso por nombre 'Productos'.")
        st.info("Esto sucede si el nombre en el Excel tiene un espacio invisible o es diferente.")
        
except Exception as e:
    st.error(f"Error crítico: {e}")
