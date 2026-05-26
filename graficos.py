"""
graficos.py
-----------
Módulo encargado de la generación de todos los gráficos
de la aplicación usando matplotlib.
Contiene funciones reutilizables para barras horizontales,
barras verticales, torta y preparación de datos para mapa.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# Paleta de colores consistente para todos los gráficos
COLOR_PRINCIPAL = "#1a7abf"
COLOR_SECUNDARIO = "#3d8b6e"
PALETA = ["#1a7abf", "#f4a522", "#e84c4c", "#4caf50", "#9c27b0", "#ff7043"]


def grafico_barras_horizontales(
    serie: pd.Series,
    titulo: str,
    xlabel: str,
    color: str = COLOR_PRINCIPAL,
    figsize: tuple = (10, 7),
) -> plt.Figure:
    """
    Genera un gráfico de barras horizontales ordenado de menor a mayor.

    Parámetros:
        serie   (pd.Series): Datos a graficar (índice = categorías, valores = conteos).
        titulo  (str): Título del gráfico.
        xlabel  (str): Etiqueta del eje X.
        color   (str): Color de las barras. Por defecto COLOR_PRINCIPAL.
        figsize (tuple): Tamaño de la figura en pulgadas (ancho, alto).

    Retorna:
        plt.Figure: Objeto figura de matplotlib listo para renderizar.
    """
    serie_ordenada = serie.sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.barh(serie_ordenada.index, serie_ordenada.values,
                   color=color, edgecolor="white")
    ax.bar_label(bars, padding=4, fontsize=9, color="#333")
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_title(titulo, fontsize=13, fontweight="bold")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout()
    return fig


def grafico_barras_verticales(
    serie: pd.Series,
    titulo: str,
    ylabel: str,
    colores: list = None,
    figsize: tuple = (10, 4),
    rotar_etiquetas: bool = False,
) -> plt.Figure:
    """
    Genera un gráfico de barras verticales con etiquetas de valor sobre cada barra.

    Parámetros:
        serie           (pd.Series): Datos a graficar.
        titulo          (str): Título del gráfico.
        ylabel          (str): Etiqueta del eje Y.
        colores         (list): Lista de colores para las barras. Si es None, usa COLOR_PRINCIPAL.
        figsize         (tuple): Tamaño de la figura en pulgadas (ancho, alto).
        rotar_etiquetas (bool): Si True, rota 20° las etiquetas del eje X para mejor legibilidad.

    Retorna:
        plt.Figure: Objeto figura de matplotlib listo para renderizar.
    """
    if colores is None:
        colores = [COLOR_PRINCIPAL] * len(serie)

    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(serie.index, serie.values,
                  color=colores[:len(serie)], edgecolor="white", width=0.5)
    ax.bar_label(bars, padding=4, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(titulo, fontsize=13, fontweight="bold")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    if rotar_etiquetas:
        plt.xticks(rotation=20, ha="right", fontsize=9)

    plt.tight_layout()
    return fig


def grafico_torta(
    serie: pd.Series,
    titulo: str,
    figsize: tuple = (8, 5),
) -> plt.Figure:
    """
    Genera un gráfico de torta con leyenda lateral ordenada.
    Los porcentajes se muestran dentro de cada sector y las etiquetas
    en la leyenda lateral para evitar superposiciones en categorías pequeñas.

    Parámetros:
        serie   (pd.Series): Datos a graficar (índice = categorías, valores = conteos).
        titulo  (str): Título del gráfico.
        figsize (tuple): Tamaño de la figura en pulgadas (ancho, alto).

    Retorna:
        plt.Figure: Objeto figura de matplotlib listo para renderizar.
    """
    colores = PALETA[:len(serie)]
    total = serie.sum()

    fig, ax = plt.subplots(figsize=figsize)

    wedges, _, autotexts = ax.pie(
        serie.values,
        labels=None,               # etiquetas solo en leyenda, no sobre el gráfico
        autopct="%1.1f%%",
        colors=colores,
        startangle=140,
        pctdistance=0.78,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )

    # Ajustar estilo de los porcentajes dentro de cada sector
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_color("white")
        at.set_fontweight("bold")

    # Leyenda lateral: nombre + cantidad absoluta + porcentaje
    leyenda_labels = [
        f"{cat}  ({val:,} — {val / total * 100:.1f}%)"
        for cat, val in zip(serie.index, serie.values)
    ]
    ax.legend(
        wedges,
        leyenda_labels,
        title="Sistema de Salud",
        title_fontsize=8,
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        fontsize=8,
        frameon=True,
        framealpha=0.9,
        edgecolor="#ccc",
    )

    ax.set_title(titulo, fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    return fig


def datos_para_mapa(
    df: pd.DataFrame,
    lat_col: str = "Latitud",
    lon_col: str = "Longitud",
    max_puntos: int = 5000,
) -> pd.DataFrame:
    """
    Prepara un DataFrame con columnas 'lat' y 'lon' para usar en st.map().
    Filtra coordenadas inválidas, nulas y fuera de rango geográfico válido.

    Parámetros:
        df         (pd.DataFrame): DataFrame de entrada con columnas de coordenadas.
        lat_col    (str): Nombre de la columna de latitud. Por defecto 'Latitud'.
        lon_col    (str): Nombre de la columna de longitud. Por defecto 'Longitud'.
        max_puntos (int): Máximo de puntos a mostrar para optimizar el rendimiento del mapa.

    Retorna:
        pd.DataFrame: DataFrame con columnas 'lat' y 'lon' limpias y válidas.
                      Retorna DataFrame vacío si las columnas no existen.
    """
    if lat_col not in df.columns or lon_col not in df.columns:
        return pd.DataFrame(columns=["lat", "lon"])

    # Renombrar y convertir a numérico
    mapa = df[[lat_col, lon_col]].rename(
        columns={lat_col: "lat", lon_col: "lon"}
    ).copy()
    mapa["lat"] = pd.to_numeric(mapa["lat"], errors="coerce")
    mapa["lon"] = pd.to_numeric(mapa["lon"], errors="coerce")

    # Eliminar filas con coordenadas nulas
    mapa = mapa.dropna(subset=["lat", "lon"])

    # Filtrar coordenadas fuera del rango geográfico válido
    mapa = mapa[mapa["lat"].between(-90, 90) & mapa["lon"].between(-180, 180)]

    # Limitar cantidad de puntos para mejorar rendimiento
    if max_puntos and len(mapa) > max_puntos:
        mapa = mapa.sample(n=max_puntos, random_state=42)

    return mapa
