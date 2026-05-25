# Dashboard de Establecimientos de Salud en Chile

Aplicacion web interactiva desarrollada con Streamlit para visualizar y analizar establecimientos de salud vigentes en Chile, consumiendo datos en tiempo real desde la API publica del Ministerio de Salud.

Aplicacion en linea: [solemneii-jznyvpmdoh8vkupksc3a47.streamlit.app](https://solemneii-jznyvpmdoh8vkupksc3a47.streamlit.app/)

## Descripcion

Este proyecto corresponde a la evaluacion Solemne II del curso FITO9017 (Universidad San Sebastian).

Objetivo principal:
- Integrar consumo de API REST publica.
- Realizar limpieza y analisis de datos con pandas.
- Presentar resultados de forma interactiva con Streamlit.

Fuente de datos:
- Dataset: [Establecimientos de Salud Vigentes](https://datos.gob.cl/dataset/establecimientos-de-salud-vigentes)
- Publicador: Ministerio de Salud de Chile (MINSAL)
- Licencia: Creative Commons Zero (CC0)
- API: CKAN Datastore (`resource_id=2c44d782-3365-44e3-aefb-2c8b8363a1bc`)

## Funcionalidades

- Consulta en tiempo real a API CKAN con paginacion automatica.
- Filtros por region, sistema de salud, estado de funcionamiento y nivel de atencion.
- Indicadores KPI en tiempo real:
  - Total de establecimientos.
  - Cantidad de establecimientos publicos.
  - Cantidad de establecimientos privados.
  - Cantidad con servicio de urgencia.
- Visualizaciones con matplotlib:
  - Distribucion por region.
  - Publico vs. privado.
  - Nivel de atencion.
  - Top 10 tipos de establecimiento.
  - Dependencia administrativa.
- Tabla de datos filtrada para inspeccion de registros.
- Cache de datos con `st.cache_data` para mejorar rendimiento.

## Estructura del proyecto

```text
.
|- app.py
|- api.py
|- procesamiento.py
|- graficos.py
|- requirements.txt
|- README.md
`- .streamlit/
   `- config.toml
```

### Responsabilidad por modulo

| Archivo | Responsabilidad |
| --- | --- |
| `app.py` | Punto de entrada; interfaz, layout y orquestacion general. |
| `api.py` | Conexion a API CKAN, solicitudes GET y paginacion de datos. |
| `procesamiento.py` | Limpieza, transformacion, filtros y calculo de KPIs. |
| `graficos.py` | Funciones reutilizables para generacion de graficos en matplotlib. |

## Requisitos

- Python 3.10 o superior
- pip

## Instalacion y ejecucion local

1. Clonar repositorio:

```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
```

En Windows:

```bash
venv\Scripts\activate
```

En macOS/Linux:

```bash
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar aplicacion:

```bash
streamlit run app.py
```

La app quedara disponible en `http://localhost:8501`.

## Dependencias principales

- `requests>=2.31.0`
- `pandas>=2.0.0`
- `matplotlib>=3.7.0`
- `streamlit>=1.35.0`

## API utilizada

Endpoint base:

```http
GET https://datos.gob.cl/api/3/action/datastore_search
```

Ejemplo de consulta:

```text
resource_id=2c44d782-3365-44e3-aefb-2c8b8363a1bc
limit=10000
offset=0
```

El modulo `api.py` implementa paginacion automatica hasta recuperar todos los registros disponibles.

## Equipo

Proyecto desarrollado en Solemne II, Unidad 3, Semana 13.

Curso: FITO9017 - Universidad San Sebastian

Integrantes:
- Carlos Hormazabal Andreades
- Juan Carlos Rifo
- Ignacio Guzman
- Michael Figueroa

## Referencias

- [Documentacion de Streamlit](https://docs.streamlit.io/)
- [Documentacion de pandas](https://pandas.pydata.org/docs/)
- [Documentacion de matplotlib](https://matplotlib.org/stable/index.html)
- [API CKAN de datos.gob.cl](https://datos.gob.cl/api/3/action/)
- [Dataset MINSAL: Establecimientos de Salud Vigentes](https://datos.gob.cl/dataset/establecimientos-de-salud-vigentes)

