"""
api.py
------
Módulo encargado de la conexión y obtención de datos
desde la API CKAN del Ministerio de Salud (datos.gob.cl).
"""

import requests
import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
API_URL = "https://datos.gob.cl/api/3/action/datastore_search"
RESOURCE_ID = "2c44d782-3365-44e3-aefb-2c8b8363a1bc"
LIMITE_POR_PAGINA = 10000  # máximo permitido por CKAN


# ─────────────────────────────────────────────
# FUNCIONES
# ─────────────────────────────────────────────

def obtener_pagina(offset: int) -> dict: #offset es la posición de inicio para la paginación 
    """
    Realiza una solicitud GET a la API CKAN y retorna el JSON de respuesta.

    Parámetros:
        offset (int): Posición de inicio para la paginación.

    Retorna:
        dict: Respuesta JSON de la API.

    Lanza:
        requests.exceptions.RequestException: Si la solicitud falla.
    """
    params = {
        "resource_id": RESOURCE_ID,
        "limit": LIMITE_POR_PAGINA,
        "offset": offset,
    }
    respuesta = requests.get(API_URL, params=params, timeout=60)
    respuesta.raise_for_status()
    return respuesta.json()


@st.cache_data(show_spinner="Cargando datos desde la API del MINSAL...")
def obtener_todos_los_datos() -> pd.DataFrame:
    """
    Recorre todas las páginas de la API CKAN y consolida los registros
    en un único DataFrame.

    Retorna:
        pd.DataFrame: Todos los establecimientos de salud disponibles.
    """
    registros = []
    offset = 0

    while True: 
        datos = obtener_pagina(offset)

        if not datos.get("success"):
            st.error("La API retornó un error inesperado.")
            break

        resultado = datos["result"]
        filas = resultado.get("records", [])
        registros.extend(filas)

        total = resultado.get("total", 0)
        offset += LIMITE_POR_PAGINA

        if offset >= total:
            break

    return pd.DataFrame(registros)
