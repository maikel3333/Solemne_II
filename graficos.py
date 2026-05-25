import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
 
 
# Colores peronalizadops para los gráficos
COLOR_PRINCIPAL = "#1a7abf"
COLOR_SECUNDARIO = "#3d8b6e"
PALETA = ["#1a7abf", "#f4a522", "#e84c4c", "#4caf50", "#9c27b0", "#ff7043"]
 
 
# Funciones graficos
# Se define función para grafico de barras horizontales.
def grafico_barras_horizontales(
    serie: pd.Series, #
    titulo: str,
    xlabel: str, # 
    color: str = COLOR_PRINCIPAL,
    figsize: tuple = (10, 7), # f
) -> plt.Figure:
    """
    Genera un gráfico de barras horizontales.
 
    Parámetros:
        serie   (pd.Series): Datos a graficar (índice = categorías, valores = conteos).
        titulo  (str): Título del gráfico.
        xlabel  (str): Etiqueta del eje X.
        color   (str): Color de las barras.
        figsize (tuple): Tamaño de la figura.
 
    Retorna:
        plt.Figure: Objeto figura de matplotlib.
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
    Genera un gráfico de barras verticales.
 
    Parámetros:
        serie           (pd.Series): Datos a graficar.
        titulo          (str): Título del gráfico.
        ylabel          (str): Etiqueta del eje Y.
        colores         (list): Lista de colores para las barras.
        figsize         (tuple): Tamaño de la figura.
        rotar_etiquetas (bool): Si True, rota las etiquetas del eje X.
 
    Retorna:
        plt.Figure: Objeto figura de matplotlib.
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
    Genera un gráfico de torta (pie chart) con leyenda lateral ordenada.
    Las etiquetas se muestran solo en la leyenda para evitar superposiciones.
 
    Parámetros:
        serie   (pd.Series): Datos a graficar.
        titulo  (str): Título del gráfico.
        figsize (tuple): Tamaño de la figura.
 
    Retorna:
        plt.Figure: Objeto figura de matplotlib.
    """
    colores = PALETA[:len(serie)]
    total = serie.sum()
 
    fig, ax = plt.subplots(figsize=figsize)
 
    wedges, _, autotexts = ax.pie(
        serie.values,
        labels=None,                  # sin etiquetas sobre el gráfico
        autopct="%1.1f%%",
        colors=colores,
        startangle=140,
        pctdistance=0.78,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
 
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_color("white")
        at.set_fontweight("bold")
 
    # Leyenda lateral con etiqueta + valor + porcentaje
    leyenda_labels = [
        f"{cat}  ({val:,} — {val/total*100:.1f}%)"
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