# Solemne II - Dashboard Streamlit

Aplicacion en Streamlit para visualizar establecimientos de salud vigentes en Chile usando la API CKAN de datos.gob.cl.

## Ejecucion local

1. Crear y activar entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar:

```bash
streamlit run app.py
```

## Deploy en Streamlit Community Cloud

1. Verifica que el repositorio en GitHub este actualizado.
2. Entra a https://share.streamlit.io
3. Click en **New app**.
4. Selecciona:
   - Repository: `maikel3333/Solemne_II`
   - Branch: `main`
   - Main file path: `app.py`
5. Click en **Deploy**.

## Dependencias

El proyecto usa:
- streamlit
- pandas
- matplotlib
- requests

Si el deploy falla por compilacion de paquetes, vuelve a desplegar despues de confirmar `requirements.txt`.
