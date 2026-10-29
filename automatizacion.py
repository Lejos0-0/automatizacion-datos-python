"""
Automatización de Datos con Python
-----------------------------------
Procesa archivos CSV de forma masiva con Pandas, limpia los registros,
los guarda en una base de datos SQLite y genera un reporte automático.

Uso:
    python automatizacion.py data/ejemplo.csv
    python automatizacion.py data/            # procesa todos los CSV de la carpeta

Salidas:
    - datos.db           Base de datos SQLite con la tabla `registros`
    - reportes/reporte.txt  Resumen del procesamiento
"""

import sqlite3
import sys
from pathlib import Path

import pandas as pd

DB_PATH = Path("datos.db")
REPORT_DIR = Path("reportes")
TABLE = "registros"


def cargar_csv(rutas):
    """Lee uno o varios CSV y los une en un solo DataFrame."""
    frames = []
    for ruta in rutas:
        df = pd.read_csv(ruta, dtype=str, keep_default_na=False)
        df["archivo_origen"] = Path(ruta).name
        frames.append(df)
        print(f"Cargado {ruta}: {len(df)} filas")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def limpiar(df):
    """Limpieza básica: espacios, vacíos, duplicados y columnas vacías."""
    if df.empty:
        return df
    df = df.apply(lambda col: col.str.strip() if col.dtype == object else col)
    df = df.replace("", pd.NA)
    df = df.dropna(axis=1, how="all")      # columnas completamente vacías
    df = df.dropna(how="all")              # filas completamente vacías
    antes = len(df)
    df = df.drop_duplicates()
    print(f"Duplicados eliminados: {antes - len(df)}")
    return df


def guardar_sqlite(df):
    """Guarda el DataFrame en SQLite (reemplaza la tabla en cada corrida)."""
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(TABLE, conn, if_exists="replace", index=False)
    print(f"Guardadas {len(df)} filas en {DB_PATH} (tabla '{TABLE}')")


def generar_reporte(df, rutas):
    """Escribe un resumen del procesamiento en reportes/reporte.txt."""
    REPORT_DIR.mkdir(exist_ok=True)
    lineas = [
        "REPORTE DE AUTOMATIZACIÓN DE DATOS",
        "=" * 40,
        f"Archivos procesados: {len(rutas)}",
        *[f"  - {Path(r).name}" for r in rutas],
        f"Filas limpias guardadas: {len(df)}",
        f"Columnas: {', '.join(df.columns) if not df.empty else 'ninguna'}",
        f"Valores nulos por columna:",
    ]
    if not df.empty:
        for col, n in df.isna().sum().items():
            lineas.append(f"  - {col}: {int(n)}")
    texto = "\n".join(lineas) + "\n"
    (REPORT_DIR / "reporte.txt").write_text(texto, encoding="utf-8")
    print(texto)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    entrada = Path(sys.argv[1])
    rutas = sorted(entrada.glob("*.csv")) if entrada.is_dir() else [entrada]
    if not rutas:
        print(f"No se encontraron CSV en {entrada}")
        sys.exit(1)
    df = limpiar(cargar_csv(rutas))
    guardar_sqlite(df)
    generar_reporte(df, rutas)


if __name__ == "__main__":
    main()
