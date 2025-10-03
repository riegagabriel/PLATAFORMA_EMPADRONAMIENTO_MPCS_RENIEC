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
        resultados = data[data["ID del empadronado"].astype(str).str.contains(dni_input)]
        
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
    mcps_opcion = st.selectbox("Seleccione MCPS", sorted(data["MCP"].dropna().unique()))
    
    # 2. Filtrar empadronadores según MCPS elegido
    empadronadores_filtrados = data[data["MCP"] == mcps_opcion]["Empadronador"].dropna().unique()
    empadronador_opcion = st.selectbox("Seleccione Empadronador", sorted(empadronadores_filtrados))
    
    # 3. Filtrar fechas según MCPS + empadronador
    fechas_filtradas = data[
        (data["MCP"] == mcps_opcion) &
        (data["Empadronador"] == empadronador_opcion)
    ]["Jornada de trabajo"].dropna().unique()
    fecha_opcion = st.selectbox("Seleccione Fecha de Registro", sorted(fechas_filtradas))
    
    # --- CALCULAR KPIs ---
    
    # KPI 1: Total empadronados en la fecha seleccionada
    total_fecha_seleccionada = len(data[
        (data["MCP"] == mcps_opcion) &
        (data["Empadronador"] == empadronador_opcion) &
        (data["Jornada de trabajo"] == fecha_opcion)
    ])
    
    # KPI 2: Total empadronados en TODAS las fechas para este empadronador
    total_todas_fechas = len(data[
        (data["MCP"] == mcps_opcion) &
        (data["Empadronador"] == empadronador_opcion)
    ])
    
    # --- MOSTRAR KPIs EN CAJAS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label=f"📅 Empadronados en {fecha_opcion}",
            value=total_fecha_seleccionada,
            help=f"Total de personas empadronadas por {empadronador_opcion} en la fecha seleccionada"
        )
    
    with col2:
        st.metric(
            label="🏆 Cantidad total de empadronados según Empadronador",
            value=total_todas_fechas,
            help=f"Total acumulado de todas las jornadas de trabajo de {empadronador_opcion}"
        )
    
    # 4. Mostrar resultados finales
    resultados_finales = data[
        (data["MCP"] == mcps_opcion) &
        (data["Empadronador"] == empadronador_opcion) &
        (data["Jornada de trabajo"] == fecha_opcion)
    ]
    
    st.write(f"📌 Resultados para MCPS: **{mcps_opcion}**, Empadronador: **{empadronador_opcion}**, Fecha: **{fecha_opcion}**")
    st.dataframe(resultados_finales[["ID del empadronado", "Nombre del empadronado", "Departamento"]])
