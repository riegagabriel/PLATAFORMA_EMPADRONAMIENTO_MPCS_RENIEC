# app.py
import streamlit as st
import pandas as pd

# Cargar Excel directamente desde el repo (ruta relativa)
data = pd.read_excel("clean_empa.xlsx")

st.write(data.head())


st.set_page_config(page_title="Búsqueda de Empadronados", layout="wide")

st.title("📊 Buscador de Empadronados")

# --- CREAR TABS ---
tab1, tab2 = st.tabs(["🔍 Buscar por DNI", "📅 Filtros por MCPS/Empadronador/Fecha"])

# ======================
# TAB 1: Buscar por DNI
# ======================
with tab1:
    st.subheader("Buscar empadronado por DNI")
    
    dni_input = st.text_input("Ingrese el DNI:", "")
    
    if dni_input:
        resultados = data[data["dni_empadronado"].astype(str).str.contains(dni_input)]
        
        if not resultados.empty:
            st.success(f"🔎 Se encontraron {len(resultados)} resultados")
            st.dataframe(resultados)
        else:
            st.warning("⚠️ No se encontró ningún DNI con ese valor")

# ======================
# TAB 2: Filtros jerárquicos
# ======================
with tab2:
    st.subheader("Buscar DNIs por MCPS → Empadronador → Fecha")
    
    # 1. Seleccionar MCPS
    mcps_opcion = st.selectbox("Seleccione MCPS", sorted(data["MCPS"].dropna().unique()))
    
    # 2. Filtrar empadronadores según MCPS elegido
    empadronadores_filtrados = data[data["MCPS"] == mcps_opcion]["EMPADRONADORES_ORIGINAL"].dropna().unique()
    empadronador_opcion = st.selectbox("Seleccione Empadronador", sorted(empadronadores_filtrados))
    
    # 3. Filtrar fechas según MCPS + empadronador
    fechas_filtradas = data[
        (data["MCPS"] == mcps_opcion) &
        (data["EMPADRONADORES_ORIGINAL"] == empadronador_opcion)
    ]["fecha_registro"].dropna().unique()
    fecha_opcion = st.selectbox("Seleccione Fecha de Registro", sorted(fechas_filtradas))
    
    # 4. Mostrar resultados finales
    resultados_finales = data[
        (data["MCPS"] == mcps_opcion) &
        (data["EMPADRONADORES_ORIGINAL"] == empadronador_opcion) &
        (data["fecha_registro"] == fecha_opcion)
    ]
    
    st.write(f"📌 Resultados para MCPS: **{mcps_opcion}**, Empadronador: **{empadronador_opcion}**, Fecha: **{fecha_opcion}**")
    st.dataframe(resultados_finales[["dni_empadronado", "nombres_empadronado", "departamento"]])
