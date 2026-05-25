"""
procesamiento.py
----------------
Módulo encargado de la limpieza, normalización y análisis
del DataFrame obtenido desde la API del MINSAL.
"""

import pandas as pd


# ─────────────────────────────────────────────
# COLUMNAS CLAVE DEL DATASET
# ─────────────────────────────────────────────
COLUMNAS_TEXTO = [
    "RegionGlosa",
    "TipoSistemaSaludGlosa",
    "NivelAtencionEstabglosa",
    "DependenciaAdministrativa",
    "TipoEstablecimientoGlosa",
    "EstadoFuncionamiento",
]

COLUMNAS_TABLA = [
    "EstablecimientoGlosa",
    "RegionGlosa",
    "ComunaGlosa",
    "TipoSistemaSaludGlosa",
    "TipoEstablecimientoGlosa",
    "NivelAtencionEstabglosa",
    "DependenciaAdministrativa",
    "TieneServicioUrgencia",
    "EstadoFuncionamiento",
]


# ─────────────────────────────────────────────
# LIMPIEZA
# ─────────────────────────────────────────────

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y normaliza el DataFrame obtenido desde la API.

    Pasos:
        1. Elimina la columna interna '_id' de CKAN.
        2. Convierte coordenadas a tipo numérico.
        3. Elimina espacios en columnas de texto.
        4. Rellena nulos en columnas clave con 'Sin información'.

    Parámetros:
        df (pd.DataFrame): DataFrame crudo desde la API.

    Retorna:
        pd.DataFrame: DataFrame limpio y listo para análisis.
    """
    if "_id" in df.columns:
        df = df.drop(columns=["_id"])

    for col in ["Latitud", "Longitud"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    cols_obj = df.select_dtypes(include="object").columns
    df[cols_obj] = df[cols_obj].apply(lambda c: c.str.strip())

    for col in COLUMNAS_TEXTO:
        if col in df.columns:
            df[col] = df[col].fillna("Sin información")

    return df


# ─────────────────────────────────────────────
# FILTRADO
# ─────────────────────────────────────────────

def aplicar_filtros(
    df: pd.DataFrame,
    region: str,
    sistema: str,
    estado: str,
    nivel: str,
) -> pd.DataFrame:
    """
    Filtra el DataFrame según los parámetros seleccionados por el usuario.

    Parámetros:
        df      (pd.DataFrame): Dataset limpio.
        region  (str): Región seleccionada o 'Todas'.
        sistema (str): Sistema de salud o 'Todos'.
        estado  (str): Estado de funcionamiento o 'Todos'.
        nivel   (str): Nivel de atención o 'Todos'.

    Retorna:
        pd.DataFrame: DataFrame filtrado.
    """
    resultado = df.copy()

    if region != "Todas":
        resultado = resultado[resultado["RegionGlosa"] == region]

    if sistema != "Todos":
        resultado = resultado[resultado["TipoSistemaSaludGlosa"] == sistema]

    if estado != "Todos":
        resultado = resultado[resultado["EstadoFuncionamiento"] == estado]

    if nivel != "Todos" and "NivelAtencionEstabglosa" in resultado.columns:
        resultado = resultado[resultado["NivelAtencionEstabglosa"] == nivel]

    return resultado


# ─────────────────────────────────────────────
# ANÁLISIS / MÉTRICAS
# ─────────────────────────────────────────────

def calcular_kpis(df: pd.DataFrame) -> dict:
    """
    Calcula los indicadores clave (KPIs) del DataFrame filtrado.

    Parámetros:
        df (pd.DataFrame): DataFrame filtrado.

    Retorna:
        dict: Diccionario con métricas: total, públicos, privados, con_urgencia.
    """
    total = len(df)

    publicos = len(df[df["TipoSistemaSaludGlosa"] == "Público"]) \
        if "TipoSistemaSaludGlosa" in df.columns else 0

    privados = len(df[df["TipoSistemaSaludGlosa"] == "Privado"]) \
        if "TipoSistemaSaludGlosa" in df.columns else 0

    con_urgencia = len(df[df["TieneServicioUrgencia"] == "SI"]) \
        if "TieneServicioUrgencia" in df.columns else 0

    return {
        "total": total,
        "publicos": publicos,
        "privados": privados,
        "con_urgencia": con_urgencia,
    }


def conteo_por_columna(df: pd.DataFrame, columna: str, top: int = None) -> pd.Series:
    """
    Cuenta la frecuencia de valores en una columna del DataFrame.

    Parámetros:
        df      (pd.DataFrame): DataFrame a analizar.
        columna (str): Nombre de la columna.
        top     (int, optional): Si se indica, retorna solo los N más frecuentes.

    Retorna:
        pd.Series: Serie con conteos ordenados de mayor a menor.
    """
    if columna not in df.columns:
        return pd.Series(dtype=int)

    conteo = df[columna].value_counts()
    return conteo.head(top) if top else conteo


def columnas_disponibles(df: pd.DataFrame, columnas: list) -> list:
    """
    Retorna solo las columnas de la lista que existen en el DataFrame.

    Parámetros:
        df       (pd.DataFrame): DataFrame a verificar.
        columnas (list): Lista de nombres de columnas deseadas.

    Retorna:
        list: Columnas existentes en el DataFrame.
    """
    return [c for c in columnas if c in df.columns]
