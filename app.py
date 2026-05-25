"""
app.py
------
Punto de entrada de la aplicación Streamlit.
Coordina la interfaz de usuario, los filtros y la presentación
de datos importando los módulos: api, procesamiento y graficos.

Uso:
    streamlit run app.py
"""

import streamlit as st
import requests

from api import obtener_todos_los_datos
from procesamiento import (
    limpiar_datos,
    aplicar_filtros,
    calcular_kpis,
    conteo_por_columna,
    columnas_disponibles,
    COLUMNAS_TABLA,
)
from graficos import (
    grafico_barras_horizontales,
    grafico_barras_verticales,
    grafico_torta,
    PALETA,
)

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Establecimientos de Salud - Chile",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────
# CARGA Y LIMPIEZA DE DATOS
# ─────────────────────────────────────────────
try:
    df_raw = obtener_todos_los_datos()
    df = limpiar_datos(df_raw)
except requests.exceptions.RequestException as e:
    st.error(f"Error al conectar con la API del MINSAL: {e}")
    st.stop()


# ─────────────────────────────────────────────
# SIDEBAR — FILTROS
# ─────────────────────────────────────────────
_ = st.sidebar.image(
    "https://www.minsal.cl/wp-content/uploads/2015/08/logo.png",
    width=160,
)
st.sidebar.title("Filtros")
st.sidebar.markdown("Ajusta los filtros para explorar los datos.")

regiones = ["Todas"] + sorted(df["RegionGlosa"].dropna().unique().tolist())
region_sel = st.sidebar.selectbox("Región", regiones)

sistemas = ["Todos"] + sorted(df["TipoSistemaSaludGlosa"].dropna().unique().tolist())
sistema_sel = st.sidebar.selectbox("Sistema de Salud", sistemas)

estados = ["Todos"] + sorted(df["EstadoFuncionamiento"].dropna().unique().tolist())
estado_sel = st.sidebar.selectbox("Estado de Funcionamiento", estados)

niveles = (
    ["Todos"] + sorted(df["NivelAtencionEstabglosa"].dropna().unique().tolist())
    if "NivelAtencionEstabglosa" in df.columns
    else ["Todos"]
)
nivel_sel = st.sidebar.selectbox("Nivel de Atención", niveles)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Fuente:** [datos.gob.cl](https://datos.gob.cl/dataset/establecimientos-de-salud-vigentes)  \n"
    "**Publicado por:** Ministerio de Salud  \n"
    "**Licencia:** CC Zero"
)


# ─────────────────────────────────────────────
# APLICAR FILTROS
# ─────────────────────────────────────────────
df_filtrado = aplicar_filtros(df, region_sel, sistema_sel, estado_sel, nivel_sel)


# ─────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────
st.title("Establecimientos de Salud en Chile")
st.markdown(
    "Análisis y visualización de los establecimientos de salud vigentes en Chile, "
    "obtenidos en tiempo real desde la API del Ministerio de Salud."
)
st.markdown("---")


# ─────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────
kpis = calcular_kpis(df_filtrado)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total establecimientos", f"{kpis['total']:,}")
col2.metric("Públicos",               f"{kpis['publicos']:,}")
col3.metric("Privados",               f"{kpis['privados']:,}")
col4.metric("Con urgencia",           f"{kpis['con_urgencia']:,}")
st.markdown("---")


# ─────────────────────────────────────────────
# GRÁFICO 1 — Por Región
# ─────────────────────────────────────────────
st.subheader("Distribución de establecimientos por región")
fig1 = grafico_barras_horizontales(
    serie=conteo_por_columna(df_filtrado, "RegionGlosa"),
    titulo="Establecimientos de salud por región",
    xlabel="Cantidad de establecimientos",
)
st.pyplot(fig1)


# ─────────────────────────────────────────────
# GRÁFICO 2 — Sistema Público vs Privado
# ─────────────────────────────────────────────
st.subheader("Distribución por sistema de salud")
fig2 = grafico_torta(
    serie=conteo_por_columna(df_filtrado, "TipoSistemaSaludGlosa"),
    titulo="Establecimientos según sistema de salud",
)
st.pyplot(fig2)


# ─────────────────────────────────────────────
# GRÁFICO 3 — Nivel de Atención
# ─────────────────────────────────────────────
st.subheader("Establecimientos por nivel de atención")
fig3 = grafico_barras_verticales(
    serie=conteo_por_columna(df_filtrado, "NivelAtencionEstabglosa"),
    titulo="Establecimientos por nivel de atención",
    ylabel="Cantidad",
    colores=PALETA,
)
st.pyplot(fig3)


# ─────────────────────────────────────────────
# GRÁFICO 4 — Top 10 Tipos de Establecimiento
# ─────────────────────────────────────────────
st.subheader("Tipos de establecimiento más frecuentes")
fig4 = grafico_barras_horizontales(
    serie=conteo_por_columna(df_filtrado, "TipoEstablecimientoGlosa", top=10),
    titulo="Top 10 tipos de establecimientos de salud",
    xlabel="Cantidad",
)
st.pyplot(fig4)


# ─────────────────────────────────────────────
# GRÁFICO 5 — Dependencia Administrativa
# ─────────────────────────────────────────────
st.subheader("Dependencia administrativa")
fig5 = grafico_barras_verticales(
    serie=conteo_por_columna(df_filtrado, "DependenciaAdministrativa", top=8),
    titulo="Establecimientos por dependencia administrativa",
    ylabel="Cantidad",
    colores=["#3d8b6e"] * 8,
    rotar_etiquetas=True,
)
st.pyplot(fig5)


# ─────────────────────────────────────────────
# TABLA DE DATOS
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("Tabla de establecimientos")

cols_mostrar = columnas_disponibles(df_filtrado, COLUMNAS_TABLA)
st.dataframe(
    df_filtrado[cols_mostrar].reset_index(drop=True),
    use_container_width=True,
    height=400,
)
st.caption(
    f"Mostrando {kpis['total']:,} establecimientos. "
    "Datos obtenidos desde la API CKAN del Ministerio de Salud de Chile."
)
