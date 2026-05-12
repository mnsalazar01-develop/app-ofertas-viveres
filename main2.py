import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Escáner de Pestañas Pro", layout="wide")
st.title("🔍 Comparador Visual de Pestañas")

# 1. Conexión
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. El Programa Comparador
try:
    # Obtenemos los nombres REALES de las pestañas directamente de la API de Google
    # Usamos el motor de gspread que viene dentro de la conexión
    sheet_metadata = conn._instance.spreadsheet(url).worksheets()
    nombres_reales = [sheet.title for sheet in sheet_metadata]
    
    st.write("### 📜 Resultado del Escaneo")
    
    # Lista de lo que nosotros queremos (Lo que busca el código)
    nombres_esperados = ["Categorias", "Productos", "Supermercados", "Sucursales", "Precios_sucursal", "Ofertas"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Lo que el programa busca:**")
        for esp in nombres_esperados:
            if esp in nombres_reales:
                st.success(f"✅ {esp}")
            else:
                st.error(f"❌ {esp}")

    with col2:
        st.write("**Lo que Google Sheets tiene realmente:**")
        for real in nombres_reales:
            if real in nombres_esperados:
                st.info(f"💎 {real} (¡Coincidencia perfecta!)")
            else:
                st.warning(f"⚠️ '{real}' (No coincide con lo que busca el código)")
                st.write(f"  ↳ *Tip: Revisa si tiene espacios invisibles: '{real}'*")

    st.divider()

    # 3. Comparación Visual Detallada
    st.subheader("📊 Comparación Visual Lado a Lado")
    
    # Creamos una tabla para verlo más claro
    comparativa = []
    for i in range(max(len(nombres_esperados), len(nombres_reales))):
        esp = nombres_esperados[i] if i < len(nombres_esperados) else "---"
        real = nombres_reales[i] if i < len(nombres_reales) else "---"
        comparativa.append({"Buscado por Código": esp, "Escrito en Excel": real, "Estado": "✅ OK" if esp == real else "❌ ERROR"})
    
    st.table(pd.DataFrame(comparativa))

except Exception as e:
    st.error("No se pudo leer la lista de pestañas.")
    st.info(f"Detalle: {e}")

if st.button("🔄 Volver a Escanear"):
    st.cache_data.clear()
    st.rerun()
