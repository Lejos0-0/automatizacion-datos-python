# Automatización de Datos con Python

Scripts desarrollados con **Pandas** y **SQLite** para procesamiento masivo de CSV, limpieza de registros y generación automática de reportes.

## ¿Qué hace?

1. **Carga masiva** — Lee un archivo CSV o todos los CSV de una carpeta y los une en un solo conjunto de datos.
2. **Limpieza de registros** — Recorta espacios, descarta filas y columnas completamente vacías y elimina duplicados.
3. **Carga en SQLite** — Guarda el resultado limpio en una base de datos `datos.db`, tabla `registros`, lista para consultas SQL.
4. **Reporte automático** — Genera `reportes/reporte.txt` con el resumen: archivos procesados, filas guardadas, columnas y valores nulos por columna.

## Tecnologías

- Python
- Pandas
- SQLite

## Instalación

```bash
git clone https://github.com/Lejos0-0/automatizacion-datos-python.git
cd automatizacion-datos-python
pip install -r requirements.txt
```

## Uso

Procesar un solo archivo:

```bash
python automatizacion.py data/ejemplo.csv
```

Procesar todos los CSV de una carpeta:

```bash
python automatizacion.py data/
```

Salidas:

- `datos.db` — base de datos SQLite con los registros limpios
- `reportes/reporte.txt` — resumen del procesamiento

## Ejemplo incluido

`data/ejemplo.csv` trae registros de prueba con casos típicos de limpieza: un duplicado exacto, espacios extra en los campos y valores vacíos. Al procesarlo, el script elimina el duplicado y reporta los nulos por columna.

## Estructura

```
automatizacion-datos-python/
├── automatizacion.py   # Script principal (carga, limpieza, SQLite, reporte)
├── data/
│   └── ejemplo.csv     # Datos de ejemplo
├── requirements.txt
└── README.md
```

## Autor

Ereddy Marmolejos — [GitHub @Lejos0-0](https://github.com/Lejos0-0)
